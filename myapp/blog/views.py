from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
import logging
from .models import Post,Aboutus
from django.http import Http404
from django.core.paginator import Paginator
from .forms import contactForm
# Create your views here.
# Hardcode data
#posts = [
#         {'id':1, 'title': 'Post 1', 'content': 'Content of Post 1'},
#         {'id':2, 'title': 'Post 2', 'content': 'Content of Post 2'},
#         {'id':3, 'title': 'Post 3', 'content': 'Content of Post 3'},
#         {'id':4, 'title': 'Post 4', 'content': 'Content of Post 4'},   
#        ]

def index(request):
    blog_title= "Latest Post"
    all_posts = Post.objects.all()

    #paginate
    paginator = Paginator(all_posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request,'blog/index.html',{'blog_title': blog_title, 'page_obj':page_obj})

def detail(request, slug):
    # code for hardcode data
    #post = next((item for item in posts if item['id'] == int(post_id)), None)
    try:
        # getting postdata from module by post id
        post=Post.objects.get(slug=slug)
        related_posts = Post.objects.filter(category = post.category).exclude(pk=post.id)
    except Post.DoesNotExist:
        raise Http404("Post Does Not Exist!")

    #logger = logging.getLogger("TESTING")
    #logger.debug(f'post variable is {post}')

    return render(request,'blog/detail.html', {'post':post, 'related_posts':related_posts})

def old_url_redirect(request):
    return redirect(reverse('blog:new_url'))

def new_url_view(request):
    return HttpResponse("this is new url")
 
def contact_view(request):
    if request.method == 'POST':
        form = contactForm(request.POST)
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
    
        form = contactForm(request.POST)
        logger = logging.getLogger("TESTING")
        if form.is_valid():        
            logger.debug(f'post data is {form.cleaned_data["name"]} {form.cleaned_data["email"]} {form.cleaned_data["message"]}')
            # succesfully email sent or save in db
            success_message= 'Your Email has been sent!'
            return render(request,'blog/contact.html', {'form':form,'success_message':success_message})
        else:
            logger.debug("FORM Validation failure!")
            return render(request,'blog/contact.html',{'form':form, 'name':name, 'email':email, 'message':message })
    return render(request,'blog/contact.html')

def about_view(request):
    about_us_content= Aboutus.objects.first().content
    return render(request,'blog/about_us.html',{'about_us_content':about_us_content})  