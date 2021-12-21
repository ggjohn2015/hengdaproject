from django.urls import path
from . import views

app_name = 'newsApp'

urlpatterns = [
    # path('company/', views.company, name='company'),     # 公司要闻
    # path('industry/', views.industry, name='industry'),  # 行业新闻
    # path('notice/', views.notice, name='notice'),        # 通知公告
    path('news/<str:newName>/', views.news,name='news'),    ##新闻列表
    path('newDetail/<int:id>/', views.newDetail,name='newDetail'),    ##新闻详情
    path('search/',views.search,name='search'),       ##是基于模糊查询的新闻标题搜索，不是haystack的路由。haystack的路由不经过App目录（经根目录）
]