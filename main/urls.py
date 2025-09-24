from django.contrib import admin
from django.urls import path, include
from marketing import views as landing_page_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", landing_page_views.index, name="home"),
    # path("api/", include("store.api_urls")),  # later
    # path("accounts/", include("allauth.urls")),  # if using allauth
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
