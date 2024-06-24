from django.urls import path,include
from blogs.views import home,sub_category,blog_description,logout_page,about
from django.conf.urls import handler400,handler500
from django.conf.urls.static import static
from django.views.static import serve
from django.conf import settings
from django.urls import re_path as url

urlpatterns = [
    url(r'^media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT}),# use in productinon media file
    url(r'^static/(?P<path>.*)$',serve,{'document_root':settings.STATIC_ROOT}),# use in productinon static file
    path('logout/',logout_page,name='logout'),
    path('',home,name='home'),
    path('about/',about,name='about'),
    path('subcategory/<str:url>/<int:id>/',sub_category,name="subcategory"),
    path('blog/<str:url>/<str:title>/',blog_description,name="blogdescription"),
]

handler404 = 'blogs.views.error_404'
handler500 = 'blogs.views.error_500'