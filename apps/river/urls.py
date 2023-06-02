from django.urls import path, URLResolver, URLPattern
from .views import RiverView, EditRiverView, ManageRiverView, EnvisionView, PlanView, ActView, ReflectView, RiverChatView, RiverStartView, CreateRiverPollView, RiverChatUpdateView
from django.contrib.auth.decorators import login_required
from typing import List, Union


# !!! when adding new urls, don't forget to make them login_required if appropriate!
urlpatterns: List[Union[URLResolver, URLPattern]] = [
    path('create/', login_required(RiverStartView.as_view(template_name='start_river.html')), name='start_river'),
    path('view/<str:slug>/', RiverView.as_view(template_name='river.html'), name='view_river'),
    path('view/<str:slug>/envision/', EnvisionView.as_view(template_name='envision_view.html'), name='view_envision'),
    path('view/<str:slug>/plan/',PlanView.as_view(template_name='plan_view.html'), name='view_plan'),
    path('view/<str:slug>/act/', ActView.as_view(template_name='act_view.html'), name='view_act'),
    path('view/<str:slug>/reflect/', ReflectView.as_view(template_name='reflect_view.html'), name='view_reflect'),
    path('view/<str:slug>/createpoll/<str:stage>/<str:topic>/', CreateRiverPollView.as_view(template_name = 'create_river_poll.html'), name='create_river_poll'),
    path('view/<str:slug>/chat/<str:stage>/<str:topic>/', RiverChatView.as_view(template_name ='river_chat.html'), name='river_chat'),
    path('view/<str:slug>/chat/<str:stage>/<str:topic>/<str:count>', RiverChatUpdateView.as_view(),
         name='river_chat'),

    path('edit/<str:slug>/', login_required(EditRiverView.as_view(template_name='edit_river.html')), name='edit_river'),
    path('manage/<str:slug>/', ManageRiverView.as_view(template_name='swimmers_list.html'), name='manage_river'),
    #path('change/title/<str:slug>/', ManageRiverView.as_view(template_name='swimmers_list.html'), name='manage_river'),

]
