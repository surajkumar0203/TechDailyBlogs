from django.contrib import admin
from blogs.models import Category,Post,Comments,reply_message
from django.utils.html import format_html
# form 

@admin.register(Category)
class Category_admin(admin.ModelAdmin):
    list_display=['image_tag','cat_id','title','description','add_date']
    search_fields=['title']
    list_filter = ['add_date']
    list_per_page=10

   
    


@admin.register(Post)
class Post_admin(admin.ModelAdmin):
    list_display=['image_tag','post_id','title','cat']
    search_fields=['title']
    list_filter = ['cat','title']
    list_per_page=10

@admin.register(Comments)
class Comments_admin(admin.ModelAdmin):
    list_display=['comment_id','Name','user_comments','date','time','refrence_post']
    search_fields=['Name']
    list_filter = ['refrence_post']
    list_per_page=10

@admin.register(reply_message)
class reply_message_admin(admin.ModelAdmin):

    list_display=['reply_message_id','user_reply_message','date','time','refrence_post']
    search_fields=['refrence_post']
    list_per_page=10