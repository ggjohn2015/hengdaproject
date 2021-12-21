from django.urls import path
from . import views

app_name = 'serviceApp'

urlpatterns = [
    path('download/', views.download, name='download'),  # 资料下载
    path('platform/', views.platform, name='platform'),  # 人脸识别开放平台

    ###---其他路由
    path('getDoc/<int:id>/',views.getDoc,name='getDoc'),
    path('facedetect/', views.facedetect,name='facedetect'),    ##--test人脸检测接口用的url
    path('facedetectDemo/', views.facedetectDemo, name='facedetectDemo'),  # 在线web，人脸检测api
]