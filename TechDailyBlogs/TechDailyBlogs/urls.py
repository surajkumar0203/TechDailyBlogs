from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path('admin/', admin.site.urls),
    path('',include('blogs.urls')),
    # path('admin1/',include('administrater.urls'))
  
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
