from django.shortcuts import render,get_object_or_404

# Create your views here.
from django.http import HttpResponse
from .models import Post,Category,Tag
import markdown
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension


def index(request):
    post_list = Post.objects.all().order_by('-created_time')
    #取出全部文章 orderby排序 按创造时间逆序
    return render(request,'blog/index.html',context={'post_list':post_list})

def detail(request,pk):
    #根据URL捕获的PK在数据库取出记录，并传给模板渲染（不存在则返回404）
    post = get_object_or_404(Post, pk=pk)
    post.body = markdown.markdown(post.body,
                                    extensions=[
                                    'markdown.extensions.extra',
                                    'markdown.extensions.codehilite',
                                    'markdown.extensions.toc',   
                                    TocExtension(slugify = slugify) 
                                  ])
    #extension拓展 extra本身包含很多基础拓展 而codehilite是语法高亮拓展 这为后面的实现代码高亮功能提供基础，toc允许自动生成目录
    return render(request, 'blog/detail.html', context={'post':post})

def archives(request,year,month):
    post_list = Post.objects.filter(created_time__year = year,
                                    created_time__month = month,
                                    ).order_by('-created_time')
    return render(request,'blog/index.html',context={'post_list':post_list})

def category(request, pk):
    # 记得在开始部分导入 Category 类
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})

def tag(request, pk):
    # 记得在开始部分导入 Tag 类
    t = get_object_or_404(Tag, pk=pk)
    post_list = Post.objects.filter(tags=t).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})


