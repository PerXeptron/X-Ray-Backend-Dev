from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chexray/', include('samplexray.urls')),

    #REST_FRAMEWORK_URLS
    path('api/chexray/', include('samplexray.api.urls', 'samplexray-api')),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
