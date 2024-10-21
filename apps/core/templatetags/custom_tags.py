import uuid

from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()

DJANGO_VITE_DEV_MODE = getattr(settings, "DJANGO_VITE_DEV_MODE", False)


@register.simple_tag
def generate_id(*args):
    return uuid.uuid4()


@register.simple_tag
def maptiler_api_key(*args):
    return settings.MAPTILER_API_KEY


@register.simple_tag(takes_context=True)
def active_link(context, text, *view_names, **view_params):
    """Use to output text when the specified view is active

    Using it for CSS classnames would be class, but not limited to that.

    Usage examples:

        When we are on the home page have pink text:
            <a class="{% active_link 'text-pink' 'homepage' %}">homepage</a>

        When we are on the homepage OR the dashboard, have pink text:
            <a class="{% active_link 'text-pink' 'homepage' 'dashboard'%}">homepage</a>

        When we are on user "nick"'s profile, have green text:
            <a class="{% active_link 'text-green' 'profile' username="nick" %}">homepage</a>
    """
    request = context.get("request")
    if request is None:
        return ""

    # Fetch our resolved route
    try:
        current_view_name = request.resolver_match.view_name
    except AttributeError:
        """
        Django's APPEND_SLASH setting can cause issues when trying to access
        request.resolver_match. This is because it tries to redirect requests
        that don't have a trailing slash, which results in the loss of the
        original request object.

        In this case, we try to get the view name from the URL instead. We do
        this by resolving the URL again with a trailing '/' appended if
        necessary.
        """
        # Try to get the view name from the URL
        from django.urls import resolve

        url = request.path_info
        if not url.endswith("/"):
            url += "/"
        match = resolve(url)
        current_view_name = match.view_name

    # Match on route name
    if current_view_name not in view_names:
        return ""

    # If provided, match on the params too
    try:
        kwargs_match = request.resolver_match.kwargs == view_params
    except AttributeError:
        """
        Same issue as above: Django's APPEND_SLASH setting can cause issues
        when trying to access request.resolver_match. In this case, we try
        to get the kwargs from the URL instead.
        """
        # Try to get the kwargs from the URL
        from django.urls import resolve

        url = request.path_info
        if not url.endswith("/"):
            url += "/"
        match = resolve(url)
        kwargs_match = match.kwargs == view_params

    if view_params and not kwargs_match:
        return ""

    # It passed! Give 'em the text
    return text


@register.simple_tag
@mark_safe
def sfs_vite_prevent_unstyled_flash(*args):
    """Prevent a flash of unstyled html for full page loads in dev mode

    Without this, as the CSS is loaded with vite via js module,
    there is a delay between when the browser has received all the
    html and when the CSS is ready.

    This hides sets visibility: hidden on the body until later on...

    The "DOMContentLoaded" event fires when all deferred scripts have
    been executed, and vite has injected the CSS by then.

    If you still see a flash of unstyled content, then make sure you place this
    right after the opening <body> tag, e.g.:

        <body>
          {% sfs_vite_prevent_unstyled_flash %}
          <!-- other stuff here -->
        </body>
    """
    if not DJANGO_VITE_DEV_MODE:
        return ""

    return """
        <script>
            if (!window.__sfs_vite_prevent_unstyled_flash) {
                document.body.style.visibility = 'hidden'
            }
            window.addEventListener('DOMContentLoaded', () => {
                window.__sfs_vite_prevent_unstyled_flash = true
                document.body.style.visibility = ''
            })
        </script>
        """
