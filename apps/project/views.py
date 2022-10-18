# pyre-strict

from django.views.generic.base import TemplateView, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth.decorators import login_required
from django.db.models.fields import CharField
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse
from itertools import chain

from .models import Project, ProjectMembership
from messaging.models import Chat, Message  # pyre-ignore[21]
from userauth.util import get_system_user, get_userpair  # pyre-ignore[21]
from messaging.views import ChatView  # pyre-ignore[21]
from action.util import send_offer  # pyre-ignore[21]
from action.models import Action  # pyre-ignore[21]
from area.models import Area  # pyre-ignore[21]
from messaging.util import send_system_message  # pyre-ignore[21]
from resources.views import filter_and_cluster_resources  # pyre-ignore[21]
from core.utils.tags_declusterer import tag_cluster_to_list  # pyre-ignore[21]
from typing import Dict, List, Any, Union


class ProjectView(DetailView):  # pyre-ignore[24]
    model = Project

    def post(self, request: WSGIRequest, slug: str) -> HttpResponse:
        project = Project.objects.get(slug=slug)
        if (request.POST['action'] == 'leave'):
            membership = ProjectMembership.objects.get(user=request.user, project=project)
            if not membership.owner:  # reject owners attempting to leave, this is not supported by the interface - you should rescind ownership first, because you won't be allowed to if you're the last owner left. TODO: allow owners to leave as well if they're not the last owner
                membership.delete()
                print(
                    '!!! WARNING C !!! not sending a message to the project, because projects no longer have one central chat. how to disseminate that information?')
                # send_system_message(project.chat, 'left_project', context_project = project, context_user_a = request.user)
        if (request.POST['action'] == 'join'):
            if len(ProjectMembership.objects.filter(user=request.user, project=project)) == 0:
                ProjectMembership.objects.create(user=request.user, project=project, owner=False, champion=False)
                print(
                    '!!! WARNING D !!! not sending a message to the project, because projects no longer have one central chat. how to disseminate that information?')
                # send_system_message(project.chat, 'joined_project', context_project = project, context_user_a = request.user)
        # TESTING PURPOSES ONLY!! TODO # # # # # # # # # #
        if (request.POST['action'] == 'start_envision'):  #
            project.start_envision()  #
        # # # # # # # # # # # # # # # # # # # # # # # # #
        return super().get(request, slug)

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['owners'] = ProjectMembership.objects.filter(project=context['object'].pk, owner=True)
        context['champions'] = ProjectMembership.objects.filter(project=context['object'].pk, champion=True)
        context['members'] = ProjectMembership.objects.filter(project=context['object'].pk)
        context['object'].tags = tag_cluster_to_list(context['object'].tags)
        context['resources'] = list(chain(
            *[filter_and_cluster_resources(tag, 'latest') for tag in map(lambda t: t.name, context['object'].tags)]))
        return context


class SpringView(TemplateView):
    def get(self, request: HttpRequest, *args: List[Any], **kwargs: Dict[str, str]) -> Union[
        HttpResponse, HttpResponseRedirect]:
        # RETURN URL PATH
        slug = str(kwargs['slug'])
        if '-' in slug:
            name = slug.replace('-', ' ')
        else:
            name = slug
        print(slug)

        if Area.objects.filter(name__iexact=name).exists():
            area = Area.objects.get(name__iexact=name)
            print(area)
        else:
            return HttpResponseRedirect(reverse('404'))

        projects = Project.objects.filter(area=area)
        #projects = Project.objects.all()
        for project in projects:
            project.tags = tag_cluster_to_list(project.tags)
            project.swimmers = ProjectMembership.objects.filter(project=project).values_list('user', flat=True)
        num_swimmers = ProjectMembership.objects.filter(
            project__in=Project.objects.filter(area=area)).values_list('user', flat=True).distinct().count()

        context = {
            'area': area,
            'projects': projects,
            'num_swimmers': num_swimmers
        }

        # context is:
        #   'projects' -> list of projects with .tags and .swimmers set appropriately
        #   'num_swimmers' -> number of distinct swimmers involved in all projects in this spring

        return render(request, 'project/all_projects.html', context)


class EditProjectView(UpdateView):  # pyre-ignore[24]
    model = Project
    fields = ['name', 'description']

    def get(self, *args: List[Any], **kwargs: Dict[str, Any]) -> HttpResponse:
        # login_required is idempotent so we may as well apply it here in case it's forgotten in urls.py
        return login_required(super().get)(*args, **kwargs)  # pyre-ignore[6]

    def post(self, request: WSGIRequest, slug: str, **kwargs: Dict[str, Any]) -> HttpResponse:  # pyre-ignore[14]
        project = Project.objects.get(slug=slug)
        if (ProjectMembership.objects.get(project=project, user=request.user).owner == True):
            if ('abdicate' in request.POST and request.POST['abdicate'] == 'abdicate'):
                ownerships = ProjectMembership.objects.filter(project=project, owner=True)
                if (
                        len(ownerships) >= 2):  # won't be orphaning the project (TODO: allow projects to be shut down, in which case they can be orphaned)
                    my_membership = ProjectMembership.objects.get(project=project, user=request.user, owner=True)
                    my_membership.owner = False
                    my_membership.save()
                    print(
                        '!!! WARNING E !!! not sending a message to the project, because projects no longer have one central chat. how to disseminate that information?')
                    # send_system_message(project.chat, 'lost_ownership', context_user_a = request.user)
            project.name = request.POST['name']
            project.description = request.POST['description']
            project.save()
        return redirect(reverse('view_project', args=[slug]))

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['ownerships'] = ProjectMembership.objects.filter(project=context['object'], owner=True)
        return context


class ManageProjectView(DetailView):  # pyre-ignore[24]
    model = Project

    def post(self, request: WSGIRequest, slug: str) -> HttpResponse:
        project = Project.objects.get(slug=slug)
        membership = ProjectMembership.objects.get(id=request.POST['membership'])
        # security checks
        if (ProjectMembership.objects.get(user=request.user, project=project).owner == True
                and membership.project == Project.objects.get(slug=slug)):  # since the form takes any uid
            if (request.POST['action'] == 'offer_ownership'):
                if not membership.owner:  # not an owner already
                    send_offer(request.user, membership.user, 'become_owner', param_project=project)
            elif (request.POST['action'] == 'offer_championship'):
                if not membership.champion:
                    send_offer(request.user, membership.user, 'become_champion', param_project=project)
            elif (request.POST['action'] == 'remove_championship'):
                if membership.champion:
                    membership.champion = False
                    print(
                        '!!! WARNING F !!! not sending a message to the project, because projects no longer have one central chat. how to disseminate that information?')
                    # send_system_message(project.chat, 'lost_championship', context_user_a = membership.user, context_user_b = request.user)
                    send_system_message(get_userpair(request.user, membership.user).chat,
                                        'lost_championship_notification', context_user_a=request.user,
                                        context_project=membership.project)
            membership.save()
        return self.get(request, slug)

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['ownerships'] = ProjectMembership.objects.filter(project=context['object'].pk, owner=True)
        context['memberships'] = ProjectMembership.objects.filter(project=context['object'].pk)
        return context


class ProjectChatView(ChatView):  # pyre-ignore[11]
    def get_chat(self, project: Project, stage: str, topic: str) -> Chat:  # pyre-ignore[11]
        if stage == 'envision':
            chat = project.envision_stage.chat
        elif stage == 'plan':
            if topic == 'general':
                chat = project.plan_stage.general_chat
            elif topic == 'funding':
                chat = project.plan_stage.funding_chat
            elif topic == 'location':
                chat = project.plan_stage.location_chat
            elif topic == 'dates':
                chat = project.plan_stage.dates_chat
        elif stage == 'act':
            if topic == 'general':
                chat = project.act_stage.general_chat
            elif topic == 'funding':
                chat = project.act_stage.funding_chat
            elif topic == 'location':
                chat = project.act_stage.location_chat
            elif topic == 'dates':
                chat = project.act_stage.dates_chat
        elif stage == 'reflect':
            chat = project.reflect_stage.chat
        return chat  # pyre-ignore[61]

    def post(self, request: WSGIRequest, slug: str, stage: str, topic: str = '') -> HttpResponse:
        project = Project.objects.get(slug=slug)
        chat = self.get_chat(project, stage, topic)
        return super().post(request, chat=chat, url=request.get_full_path(), members=list(
            map(lambda x: x.user, ProjectMembership.objects.filter(project=project))))  # pyre-ignore[16]

    def get_context_data(self, slug: str, stage: str, topic: str) -> Dict[str, Any]:
        project = Project.objects.get(slug=slug)
        ctx = super().get_context_data(chat=self.get_chat(project, stage, topic), url=self.request.get_full_path(),
                                       members=list(map(lambda x: x.user, ProjectMembership.objects.filter(
                                           project=project))))  # pyre-ignore[16]
        return ctx


class EnvisionView(TemplateView):
    def post(self, request: WSGIRequest, slug: str) -> HttpResponse:
        Project.objects.get(slug=slug).start_plan()  # TODO TESTING PURPOSES ONLY
        return super().get(request, slug)

    def get_context_data(self, *args: List[Any], **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        ctx = super().get_context_data(*args, **kwargs)
        ctx['project'] = Project.objects.get(slug=self.kwargs['slug'])
        return ctx


class PlanView(TemplateView):
    def post(self, request: WSGIRequest, slug: str) -> HttpResponse:
        Project.objects.get(slug=slug).start_act()  # TODO TESTING PURPOSES ONLY
        return super().get(request, slug)

    def get_context_data(self, *args: List[Any], **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        ctx = super().get_context_data(*args, **kwargs)
        ctx['project'] = Project.objects.get(slug=self.kwargs['slug'])
        return ctx


class ActView(TemplateView):
    def post(self, request: WSGIRequest, slug: str) -> HttpResponse:
        Project.objects.get(slug=slug).start_reflect()  # TODO TESTING PURPOSES ONLY
        return super().get(request, slug)

    def get_context_data(self, *args: List[Any], **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        ctx = super().get_context_data(*args, **kwargs)
        ctx['project'] = Project.objects.get(slug=self.kwargs['slug'])
        return ctx


class ReflectView(TemplateView):
    def get_context_data(self, *args: List[Any], **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        ctx = super().get_context_data(*args, **kwargs)
        ctx['project'] = Project.objects.get(slug=self.kwargs['slug'])
        return ctx
