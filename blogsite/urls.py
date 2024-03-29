
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

urlpatterns = [
    path('', include('pages.urls')),
    path('posts/', include('posts.urls')),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
