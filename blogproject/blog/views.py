from django.shortcuts import render,get_object_or_404

# Create your views here.
from django.http import HttpResponse
from .models import Post,Category,Tag
import markdown
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.views.generic import ListView
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from pure_pagination.mixins import PaginationMixin

# def index(request):
#     post_list = Post.objects.all().order_by('-created_time')
#     #取出全部文章 orderby排序 按创造时间逆序
#     return render(request,'blog/index.html',context={'post_list':post_list})

# ListView 从数据库中获取某个模型列表数据
class IndexView(PaginationMixin,ListView):
    model = Post
    template_name = 'blog/index.html'  # 指定视图渲染的模板
    context_object_name = 'post_list'  # 指定数据保存的变量名，传给模板
    paginate_by = 5  # 分页

def detail(request,pk):
    #根据URL捕获的PK在数据库取出记录，并传给模板渲染（不存在则返回404）
    post = get_object_or_404(Post, pk=pk)
    
    post.increase_views() # 阅读量+1

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

# def category(request, pk):
#     # 记得在开始部分导入 Category 类
#     cate = get_object_or_404(Category, pk=pk)
#     post_list = Post.objects.filter(category=cate).order_by('-created_time')
#     return render(request, 'blog/index.html', context={'post_list': post_list})

class CategoryView(IndexView):
    # model = Post
    # template_name = 'blog/index.html'
    # context_object_name = 'post_list'
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))  # 获得分类
        return super(CategoryView, self).get_queryset().filter(category=cate)  # 拿该类的所有数据


def tag(request, pk):
    # 记得在开始部分导入 Tag 类
    t = get_object_or_404(Tag, pk=pk)
    post_list = Post.objects.filter(tags=t).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})


