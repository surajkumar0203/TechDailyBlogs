from django.shortcuts import render,redirect,HttpResponseRedirect
from blogs.models import *
from django.core.paginator import Paginator
from django.contrib.auth import logout
from django.core.cache import cache

def error_404(request, exception):
    return render(request,'404.html')

def error_500(request):
    return render(request,'500.html')


def home(request):
    cache_data=cache.get("blog_Caches",version=1)
    if not cache_data:
        category = Category.objects.filter(cat_id__in=Post.objects.values('cat')).order_by('-add_date')
        # caches
        cache.set("blog_Caches", category,300,version=1)
        cache_data=cache.get("blog_Caches",version=1)
        
    # pagination
    paginator = Paginator(cache_data, 20)
    page_number=request.GET.get('page') # get page number from client
    finalData=paginator.get_page(page_number) # show current page
    totalpage=paginator.page_range
    
    context={
        'category_banners':cache_data[:5],
        'category_all_news':finalData
    }
    
    return render(request,'blogs/Home.html',{'context':context,'totalpagelist':totalpage,'lastpage':paginator.page_range[-1]})

def about(request):
    
    return render(request,'blogs/about.html')


def sub_category(request,url,id):
    cache_data=cache.get("sub_category_caches",version=id)
    if not cache_data:
        post=Post.objects.filter(cat=id).order_by('-post_id')
      
        # caches
        cache.set("sub_category_caches", post,300,version=id)
        cache_data=cache.get("sub_category_caches",version=id)
    
    
    # pagination
    paginator = Paginator(cache_data, 20)
    page_number=request.GET.get('page') # get page number from client
    finalData=paginator.get_page(page_number) # show current page
    totalpage=paginator.page_range
   
    context={
        'post_banners':cache_data[:5],
        'post_all_news':finalData,
        
    }
    return render(request,'blogs/subcategory.html',{'context':context,'title':url,'totalpagelist':totalpage,'lastpage':paginator.page_range[-1]})


def blog_description(request,url,title):
    post_id=url.split('-')[1]
    
    blog=Post.objects.get(title__iexact=title)
    
    blog_cache_decrip_id=str(blog).replace(' ','')
   
    # comments
    if request.method=='POST':
        is_replied_msg=int(request.POST['hidden_bool'])
        # reply of comment
        if is_replied_msg:
            replied_msg=request.POST['replied_comment']
            hidden_comment_id=request.POST['hidden_comment_id']
            comment_refrence=Comments.objects.get(comment_id=hidden_comment_id)
            reply_message.objects.create(refrence_post=comment_refrence,user_reply_message=replied_msg)
            
        else:
            # comment
            name=request.POST['name']
            message=request.POST['message']
            Comments.objects.create(Name=name,user_comments=message,refrence_post=blog)
            cache.delete("uses_comment",version=blog_cache_decrip_id)
        
        cache.delete("usesreplied_message",version=blog_cache_decrip_id)
        
    
    # cache
    uses_comment_cache_data=cache.get("uses_comment",version=blog_cache_decrip_id)
    if not uses_comment_cache_data:
        # get comments
        uses_comment=Comments.objects.filter(refrence_post=blog).order_by('?')
        # caches
        cache.set("uses_comment", uses_comment,300,version=blog_cache_decrip_id)
        uses_comment_cache_data=cache.get("uses_comment",version=blog_cache_decrip_id)
    
    # cache
    uses_replied_message_cache_data=cache.get("usesreplied_message",version=blog_cache_decrip_id)
    if not uses_replied_message_cache_data:
        # get replird message
        uses_replied_message_cache_data=[reply_message.objects.filter(refrence_post=rep) for rep in uses_comment_cache_data]
        # caches
        cache.set("usesreplied_message", uses_replied_message_cache_data,300,version=blog_cache_decrip_id)
        uses_replied_message_cache_data=cache.get("usesreplied_message",version=blog_cache_decrip_id)
    
    description=blog.content
    post=Post.objects.filter(cat=post_id).order_by('?')
    
    context={
        'post_banners':post[:5],
        'uses_comment':uses_comment_cache_data,
        
    }
    return render(request,'blogs/BlogDescription.html',{'description':description,'titlebar':title,'context':context,'category':blog.cat,'user_replied_message':uses_replied_message_cache_data,'iscat':True})


# logout
def logout_page(request):
    logout(request)
    return redirect('/admin')