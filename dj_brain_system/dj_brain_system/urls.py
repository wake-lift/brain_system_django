from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

urlpatterns = [
    path('', include('common_pages.urls')),
    path('brain_system/', include('brain_system.urls')),
    path('questions/', include('questions.urls')),
    path('admin-site/', admin.site.urls),
    path('api/v1/', include('api.v1.urls')),
    path('auth/', include('users.urls'))
]

urlpatterns += [
    path('captcha/', include('captcha.urls')),
]
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)

handler404 = 'common_pages.views.page_not_found'
handler403 = 'common_pages.views.forbidden'
handler400 = 'common_pages.views.bad_request'
handler500 = 'common_pages.views.internal_server_error'

schema_view = get_schema_view(
    openapi.Info(
        title="Brain API",
        default_version='v1',
        description="Brain API description",
        terms_of_service="https://db.chgk.info/copyright",
        license=openapi.License(name="CC BY-SA 4.0 Deed"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
    path(
        'api/v1/redoc/',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'
    ),
]
