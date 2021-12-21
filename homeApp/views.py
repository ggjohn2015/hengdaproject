from django.shortcuts import render
from django.shortcuts import HttpResponse
from newsApp.models import MyNew
from django.db.models import Q
from productsApp.models import Product

# Create your views here.
def home(request):
    ##新闻展报
    newList=MyNew.objects.all().filter(~Q(newType='通知公告')).order_by('-publishDate')
    postList=set()
    postNum=0
    for s in newList:
        if s.photo:
            postList.add(s)
            postNum+=1
        if postNum==3: #只截取最近的3个展报
            break
    ##新闻列表
    if (len(newList)>7):
        newList=newList[0:7]  ##只显示7条新闻

    ##通知公告
    noteList=MyNew.objects.all().filter(
        Q(newType='通知公告')).order_by('-publishDate')
    if (len(noteList)>4):
        noteList=noteList[0:4]

    ###--产品中心---
    productList=Product.objects.all().order_by('-views')
    if len(productList)>4:
        productList=productList[0:4]


    ##返回结果,render到html页面。
    return render(request,'home.html',{
        'active_menu':'home',
        'postList':postList,
        'newList':newList,
        'noteList':noteList,
        'productList':productList,
    })








