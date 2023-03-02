# pyre-strict
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.urls import include, path
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from search import views as search_views

from typing import List, Union
from django.urls import URLResolver, URLPattern

from landing.views import handle_404, handle_500  # pyre-ignore[21]

handler404 = handle_404  # pyre-ignore[5]
handler500 = handle_500  # pyre-ignore[5]

urlpatterns: List[Union[URLResolver, URLPattern]] = [
    # pyre comment suppresses an error caused by pyre's limited understanding of django
    path('django-admin/', admin.site.urls),

    path('admin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),

    path('search/', search_views.search, name='search'),
    path('profile/', include('userauth.urls')),
    path('dashboard/', include('dashboard.urls'), name='dashboard'),
    path('spring/', include('spring.urls'), name='spring'),
    path('river/', include('river.urls'), name='river'),
    path('action/', include('action.urls')),
    path('poll/', include('poll.urls')),
    path('analytics/', include('analytics.urls')),

    path("__reload__/", include("django_browser_reload.urls")),

    path('resources/', include('resources.urls')),
    path('core/', include('core.urls')),
    path('', include('landing.urls')),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    import debug_toolbar

    # Serve static and media files from development server
    MIDDLEWARE_CLASSES = ['debug_toolbar.middleware.DebugToolbarMiddleware', ]
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]

urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:

    path("", include(wagtail_urls)),

    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
]
