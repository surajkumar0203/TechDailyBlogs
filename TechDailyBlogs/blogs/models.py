from django.db import models
from django.utils.html import format_html
from django_ckeditor_5.fields import CKEditor5Field


class CommonFields(models.Model):
    title=models.CharField(max_length=100)
    
    class Meta:
        abstract=True

# Category Models
class Category(CommonFields):
    cat_id=models.AutoField(primary_key=True)
    description=models.TextField()
    images=models.ImageField(upload_to='category/')
    add_date=models.DateField(auto_now_add=True,null=True)

    def __str__(self):
        return f'{self.title}-{str(self.cat_id)}'
    
    def image_tag(self):
        return format_html(f'<img src="/media/{self.images}" style="width:40px; height:40px;border-radius: 25px;"/>')
    
   

# Post Models
class Post(CommonFields):
    post_id=models.AutoField(primary_key=True)
    content=CKEditor5Field('Text', config_name='extends')
    description=models.CharField(max_length=50)
    cat=models.ForeignKey(Category,on_delete=models.CASCADE,verbose_name="category")
    images=models.ImageField(upload_to='post/')

    def __str__(self):
        return self.title
    
    def image_tag(self):
        return format_html(f'<img src="/media/{self.images}" style="width:40px; height:40px;border-radius: 25px;"/>')

  
class Comments(models.Model):
    comment_id=models.AutoField(primary_key=True)
    Name=models.CharField(max_length=50)
    user_comments=models.TextField()
    date=models.DateField(auto_now_add=True)
    time=models.TimeField(auto_now_add=True)
    refrence_post=models.ForeignKey(Post,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.Name} - {str(self.comment_id)}'
    

class reply_message(models.Model):
    reply_message_id=models.AutoField(primary_key=True)
    user_reply_message=models.TextField()
    date=models.DateField(auto_now_add=True)
    time=models.TimeField(auto_now_add=True)
    refrence_post=models.ForeignKey(Comments,on_delete=models.CASCADE)


    