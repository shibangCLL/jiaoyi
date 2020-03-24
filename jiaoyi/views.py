from django.shortcuts import render, get_object_or_404
from .forms import AddProductForm
from .models import Product, Image, Category
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from .tool import RenderWrite


# Create your views here.

def addproduct(request):
    if request.method == "POST":
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            price = form.clean_price()
            description = form.cleaned_data['description']
            excerpt = form.cleaned_data['excerpt']
            category = form.clean_category()
            pro = Product.objects.create(title=title, price=price, description=description, excerpt=excerpt,
                                         category=category, author=request.user)
            image = form.cleaned_data['image']
            Image.objects.create(imgpath=image, product=pro)
            return HttpResponseRedirect(reverse('jiaoyi:mylisting'))
    else:
        form = AddProductForm()
        title = "添加个人产品"
    return RenderWrite.render_template(request, 'jiaoyi/post-ad.html', {'form': form, 'title': title})


@login_required(login_url='/users/login')
def mylisting(request):
    # user = get_object_or_404(User, pk=pk)
    # return render(request, 'jiaoyi/account.html', locals())
    user = request.user
    # user_profile = get_object_or_404(UserProfile, user=user)
    prolist = Product.objects.filter(author=user)
    # print(prolist)
    # for pro in prolist:
    #     print(pro.image_set.all().first().imgpath)

    paginator = Paginator(prolist, 3, 3)
    try:
        # GET请求方式，get()获取指定Key值所对应的value值
        # 获取index的值，如果没有，则设置使用默认值1
        num = request.GET.get('index', '1')
        # 获取第几页
        number = paginator.page(num)
    except PageNotAnInteger:
        # 如果输入的页码数不是整数，那么显示第一页数据
        number = paginator.page(1)
    except EmptyPage:
        number = paginator.page(paginator.num_pages)

    title = "我的产品清单"
    return RenderWrite.render_template(request, 'jiaoyi/my-listing.html',
                  {'user': user, 'prolist': prolist, 'page': number, 'paginator': paginator, 'title': title})


@login_required(login_url='/users/login')
def listing(request):
    # user = get_object_or_404(User, pk=pk)
    # return render(request, 'jiaoyi/account.html', locals())
    # user = request.user
    # user_profile = get_object_or_404(UserProfile, user=user)
    prolist = Product.objects.all()
    paginator = Paginator(prolist, 3, 3)
    try:
        # GET请求方式，get()获取指定Key值所对应的value值
        # 获取index的值，如果没有，则设置使用默认值1
        num = request.GET.get('index', '1')
        # 获取第几页
        number = paginator.page(num)
    except PageNotAnInteger:
        # 如果输入的页码数不是整数，那么显示第一页数据
        number = paginator.page(1)
    except EmptyPage:
        number = paginator.page(paginator.num_pages)

    title = "所有产品"
    return RenderWrite.render_template(request, 'jiaoyi/list-view2.html',
                  {'prolist': prolist, 'page': number, 'paginator': paginator, 'title': title})


@login_required(login_url='/users/login')
def pro_detail(request, pk):
    # user = get_object_or_404(User, pk=pk)
    # return render(request, 'jiaoyi/account.html', locals())
    pro = get_object_or_404(Product, pk=pk)
    pro.increase_views()
    title = pro.title
    return RenderWrite.render_template(request, 'jiaoyi/single-product2.html', {'pro': pro, 'title': title})


@login_required(login_url='/users/login')
def archive(request, year, month):
    prolist = Product.objects.filter(created_time__year=year,
                                     created_time__month=month
                                     ).order_by('-created_time')
    paginator = Paginator(prolist, 3, 3)
    try:
        # GET请求方式，get()获取指定Key值所对应的value值
        # 获取index的值，如果没有，则设置使用默认值1
        num = request.GET.get('index', '1')
        # 获取第几页
        number = paginator.page(num)
    except PageNotAnInteger:
        # 如果输入的页码数不是整数，那么显示第一页数据
        number = paginator.page(1)
    except EmptyPage:
        number = paginator.page(paginator.num_pages)

    title = "产品列表"
    return RenderWrite.render_template(request, 'jiaoyi/list-view2.html',
                  context={'prolist': prolist, 'page': number, 'paginator': paginator, 'title': title})


@login_required(login_url='/users/login')
def category(request, pk):
    # 记得在开始部分导入 Category 类
    cate = get_object_or_404(Category, pk=pk)
    prolist = Product.objects.filter(category=cate).order_by('-created_time')
    paginator = Paginator(prolist, 3, 3)
    try:
        # GET请求方式，get()获取指定Key值所对应的value值
        # 获取index的值，如果没有，则设置使用默认值1
        num = request.GET.get('index', '1')
        # 获取第几页
        number = paginator.page(num)
    except PageNotAnInteger:
        # 如果输入的页码数不是整数，那么显示第一页数据
        number = paginator.page(1)
    except EmptyPage:
        number = paginator.page(paginator.num_pages)

    title = cate.name
    return RenderWrite.render_template(request, 'jiaoyi/list-view2.html',
                  context={'prolist': prolist, 'page': number, 'paginator': paginator, 'title': title})


def search(request):
    q = request.GET.get('keyword')
    print(q)

    if not q:
        error_msg = "请输入搜索关键词"
        messages.add_message(request, messages.ERROR, error_msg, extra_tags='danger')
        return HttpResponseRedirect(reverse('jiaoyi:listing'))
        # return redirect('blog:index')

    prolist = Product.objects.filter(Q(title__icontains=q) | Q(description__icontains=q))
    paginator = Paginator(prolist, 3, 3)
    try:
        # GET请求方式，get()获取指定Key值所对应的value值
        # 获取index的值，如果没有，则设置使用默认值1
        num = request.GET.get('index', '1')
        # 获取第几页
        number = paginator.page(num)
    except PageNotAnInteger:
        # 如果输入的页码数不是整数，那么显示第一页数据
        number = paginator.page(1)
    except EmptyPage:
        number = paginator.page(paginator.num_pages)
    title = q + "--搜索"
    return RenderWrite.render_template(request, 'jiaoyi/list-view2.html',
                  {'prolist': prolist, 'page': number, 'paginator': paginator, 'title': title})
