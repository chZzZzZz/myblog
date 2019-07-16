from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import Category, Banner, Article,Tag, Link
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger # 导入分页插件包，对文章进行分页


def global_variable(request):
    allcategory = Category.objects.all() # 通过Category表查出所有分类
    remen = Article.objects.filter(tui__id=2)[:6] # 热门推荐
    tags = Tag.objects.all()
    return locals()
# 首页
def index(request):

    banner = Banner.objects.filter(is_active=True)[:4] # 过filrter查询出所有激活的is_active幻灯图数据，并进行切片，只显示4条数据。
    tui = Article.objects.filter(tui__id=1)[:3] # 查询推荐为id=1的文章
    allarticle = Article.objects.all().order_by('-id')[:10] # 最新文章
    # 推荐文章
    # hot = Article.objects.all().order_by('?')[:10] # 随机推荐
    # hot = Article.objects.filter(tui__id=3)[:10] # 通过推荐进行查询，一推荐ID为3为例
    hot = Article.objects.all().order_by('views')[:10] # 通过浏览量进行排序



    link = Link.objects.all()


    # 将查出来的类封装到上下文里
    # context = {
    #     'allcategory': allcategory,
    #     'banner': banner,
    #     'tui': tui,
    #     'allarticle': allarticle,
    #     'hot': hot,
    #     'remen':remen,
    #     'tags': tags,
    #     'link': link,
    # }
    return render(request,'index.html',locals()) # 将context传到index.html页面

# 列表页
def list(request,lid):
    list = Article.objects.filter(category_id=lid)  # 获取通过URL传进来的lid，然后筛选出对应文章
    cname = Category.objects.get(id=lid)  # 获取当前文章的栏目名


    # 文章分页
    page = request.GET.get('page')  # 在URL中获取当前页面数
    paginator = Paginator(list, 5)  # 对查询到的数据对象list进行分页，设置超过5条数据就分页
    try:
        list = paginator.page(page)  # 获取当前页码的记录
    except PageNotAnInteger:
        list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容

    return render(request, 'list.html', locals()) # locals 作用是返回一个包含当前作用域里的所有变量和他们值的字典

# 内容页
def show(request,sid):
    show = Article.objects.get(id=sid)  # 查询指定ID的文章
    hot = Article.objects.all().order_by('?')[:10]  # 内容下面的您可能感兴趣的文章，随机推荐

    previous_blog = Article.objects.filter(created_time__gt=show.created_time, category=show.category.id).first()
    netx_blog = Article.objects.filter(created_time__lt=show.created_time, category=show.category.id).last()# 通过发布文章时间来筛选，指定查询的文章为当前分类下的文章
    show.views = show.views + 1
    show.save()
    return render(request, 'show.html', locals())

# 标签页 和列表页的展示一样
def tag(request,tag):
    list = Article.objects.filter(tags__name=tag)  # 通过文章标签进行查询文章

    tname = Tag.objects.get(name=tag)  # 获取当前搜索的标签名
    page = request.GET.get('page')

    paginator = Paginator(list, 5)
    try:
        list = paginator.page(page)  # 获取当前页码的记录
    except PageNotAnInteger:
        list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
    return render(request, 'tag.html', locals())

# 搜索页
def search(request):
    ss = request.GET.get('search')  # 获取搜索的关键词
    list = Article.objects.filter(title__icontains=ss)  # 获取到搜索关键词通过标题进行匹配 不区分大小写

    page = request.GET.get('page')

    paginator = Paginator(list, 10)
    try:
        list = paginator.page(page)  # 获取当前页码的记录
    except PageNotAnInteger:
        list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
    return render(request, 'search.html', locals())

# 关于我们
def about(request):

    return render(request, 'page.html', locals())
