# pyre-strict
from django.conf import settings
from django.urls import include, path, URLResolver, URLPattern
from django.contrib.auth.decorators import login_required
from .views import CustomUserUpdateView, CustomUserDeleteView, profile_view, user_request_view, admin_request_view, CustomUserPersonalView
from typing import List, Union

# !!! when adding new urls, don't forget to make them login_required if appropriate!
urlpatterns: List[Union[URLResolver, URLPattern]] = [
    path('request/', login_required(user_request_view), name='account_request'),
    path('managerequests/', login_required(admin_request_view), name='account_request_panel'),
    path('view/', login_required(profile_view), name='account_view'),
    path('data/', login_required(CustomUserPersonalView.as_view(template_name='account/data.html')), name='account_data'),
    path('update/', login_required(CustomUserUpdateView.as_view(template_name='account/update.html')), name='account_update'),
    path('delete/', login_required(CustomUserDeleteView.as_view(template_name='account/delete.html')), name='account_delete')
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    import debug_toolbar
    # Serve static and media files from development server
    MIDDLEWARE_CLASSES: List[str] = ['debug_toolbar.middleware.DebugToolbarMiddleware',]
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
