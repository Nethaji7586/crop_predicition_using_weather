from django.contrib import admin
from django.urls import include, path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('crops.urls')),  # Include your crops app URLs
]

urlpatterns += staticfiles_urlpatterns()