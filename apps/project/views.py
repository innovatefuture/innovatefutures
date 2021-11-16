# pyre-strict

from django.views.generic.base import TemplateView, View
from django.views.generic.detail import DetailView
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

from .models import Project, ProjectMessage, ProjectOwnership, ProjectSupport
from typing import Dict, Any

class ProjectView(DetailView):
    model = Project
    def post(self, request: WSGIRequest, pk: int) -> HttpResponse:
        if (request.POST['form'] == 'give_support'):
            if (0 == len(ProjectSupport.objects.filter(project=Project.objects.get(id=pk), # pyre-ignore[16]
                                                       user=request.user))): # pyre-ignore[16]
                support = ProjectSupport(project=Project.objects.get(id=pk),
                                         user=request.user)
                support.save()
        elif (request.POST['form'] == 'remove_support'):
            supports = ProjectSupport.objects.filter(project=Project.objects.get(id=pk),
                                                     user=request.user)
            for support in supports:
                support.delete()
        elif (request.POST['form'] == 'message'):
            msg = ProjectMessage(project=Project.objects.get(id=pk),
                                 message=request.POST['msg'],
                                 user_from=request.user)
            msg.save()
        return super().get(request, pk)
    def get_context_data(self, **kwargs: Dict[str,Any]) -> Dict[str,Any]:
        context = super().get_context_data(**kwargs)
        context['owners'] = ProjectOwnership.objects.filter(project=context['object'].pk) # pyre-ignore[16]
        context['supporters'] = ProjectSupport.objects.filter(project=context['object'].pk) # pyre-ignore[16]
        #if (self.request.user in context['owners']):
        context['messages'] = ProjectMessage.objects.filter(project=context['object'].pk) # pyre-ignore[16]
        return context

class AllProjectsView(TemplateView):
    def post(self, request: WSGIRequest) -> HttpResponse:
        return super().get(request)
    def get_context_data(self, **kwargs: Dict[str,Any]) -> Dict[str,Any]:
        context = super().get_context_data(**kwargs)
        if ('to_view' in self.request.POST and self.request.POST['to_view'] == 'mine'): # pyre-ignore[16]
            context['projects'] = [ownership.project for ownership in
                                   ProjectOwnership.objects.filter(user=self.request.user)] # pyre-ignore[16]
            context['viewing'] = 'mine'
        else:
            context['projects'] = Project.objects.all() # pyre-ignore[16]
        return context

class MakeProjectView(TemplateView):
    def post(self, request: WSGIRequest) -> HttpResponse:
        new_project = Project(name=request.POST['name'], description=request.POST['description'])
        new_project.save()
        ownership = ProjectOwnership(project=new_project, user=request.user) # pyre-ignore[16]
        ownership.save()
        return redirect(reverse('all_projects'))

class DeleteMessageView(View):
    def post(self, request: WSGIRequest) -> HttpResponse:
        msg = ProjectMessage.objects.get(pk=request.POST['target']) # pyre-ignore[16]
        if (request.user in [ownership.user for ownership in # pyre-ignore[16]
                             ProjectOwnership.objects.filter(project=msg.project)]): # pyre-ignore[16]
            msg.delete()
        return redirect(reverse('view_project', args=[msg.project.id]))
