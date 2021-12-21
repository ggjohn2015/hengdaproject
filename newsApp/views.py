from django.shortcuts import render
from django.shortcuts import HttpResponse


# Create your views here.
# def company(request):
#     html = '<html><body>公司要闻</body></html>'
#     return HttpResponse(html)
#
#
# def industry(request):
#     html = '<html><body>行业新闻</body></html>'
#     return HttpResponse(html)
#
#
# def notice(request):
#     html = '<html><body>通知公告</body></html>'
#     return HttpResponse(html)

from .models import MyNew
from django.core.paginator import Paginator
from pyquery import PyQuery as pq

def news(request, newName):
    submenu=newName
    if newName=='company':
        newName="企业要闻"
    elif newName=='industry':
        newName='行业新闻'
    else:
        newName='通知公告'
    ##--从数据库获取数据，过滤，排序
    newList=MyNew.objects.all().filter(newType=newName).order_by('-publishDate' )
    ##--给每一条记录对象添加文字内容属性
    for mynew in newList:
        html=pq(mynew.description)
        mynew.mytxt=pq(html)('p').text()  ##取出html段落文字。
    ##--分页--
    ##--分页--
    p=Paginator(newList,5)
    # print('gg分的页数：',p.num_pages)
    if p.num_pages<=1:
        pageData=''
    else:
        page=int(request.GET.get('page',1))
        newList=p.page(page)   ##--copy代码的时候需注意：此处需要改newList
        left=[]
        right=[]
        left_has_more=False
        right_has_more=False
        first=False
        last=False
        total_pages=p.num_pages
        page_range=p.page_range
        if page==1:
            right=page_range[page:page+2]
            # print(total_pages)
            if right[-1]<total_pages-1:
                right_has_more=True
            if right[-1] <total_pages:
                last=True
        elif page==total_pages:
            left=page_range[(page-3) if (page-3)>0 else 0:page-1]
            if left[0]>2:
                left_has_more=True
            if left[0]>1:
                first=True
        else:
            left=page_range[(page-3) if (page-3)>0 else 0:page-1]
            right=page_range[page:page+2]
            if left[0]>2:
                left_has_more=True
            if left[0]>1:
                first=True
            if right[-1]<total_pages-1:
                right_has_more=True
            if right[-1]<total_pages:
                last=True
        pageData={
            'left':left,
            'right':right,
            'left_has_more':left_has_more,
            'right_has_more':right_has_more,
            'first':first,
            'last':last,
            'total_pages':total_pages,
            'page':page,
        }

    # print(pageData)
    return render(request, 'newList.html',{
        'active_menu':'news',
        'sub_menu':submenu,
        'newName':newName,
        'newList':newList,
        'pageData':pageData,
    })

###---新闻详情页视图-----
from django.shortcuts import get_object_or_404

def newDetail(request,id):
    mynew=get_object_or_404(MyNew,id=id)
    mynew.views+=1
    mynew.save()
    return render(request,'newDetail.html',{
        'active_menu':'news',
        'mynew':mynew,
    })
###--搜索--
def search(request):
    keyword=request.GET.get('keyword')
    newList=MyNew.objects.filter(title__icontains=keyword)
    newName='关于'+'\"' + keyword + '\"' +'的搜索结果'
    return render(request,'searchList.html',{
        'active_menu':'news',
        'newName':newName,
        'newList':newList,
    })





