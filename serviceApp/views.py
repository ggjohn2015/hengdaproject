
from django.shortcuts import render
from django.shortcuts import HttpResponse
from .models import Doc
from pyquery import PyQuery as pq
from django.core.paginator import Paginator
from django.http import StreamingHttpResponse
from django.shortcuts import get_object_or_404
import os

# Create your views here.
def download(request):
    # html = '<html><body>资料下载</body></html>'
    submenu='download'
    docList=Doc.objects.all().order_by('-publishDate')
    p = Paginator(docList, 2)
    if p.num_pages <= 1:
        pageData = ''
    else:
        page = int(request.GET.get('page', 1))
        docList = p.page(page)
        left = []
        right = []
        left_has_more = False
        right_has_more = False
        first = False
        last = False
        total_pages = p.num_pages
        page_range = p.page_range
        if page == 1:
            right = page_range[page:page + 2]
            # print(total_pages)
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
        elif page == total_pages:
            left = page_range[(page - 3) if (page - 3) > 0 else 0:page - 1]
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
        else:
            left = page_range[(page - 3) if (page - 3) > 0 else 0:page - 1]
            right = page_range[page:page + 2]
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
        pageData = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
            'total_pages': total_pages,
            'page': page,
        }

    return render(request,'docList.html',{
        'active_menu': 'news',
        'sub_menu': submenu,
        # 'docName': newName,
        'docList': docList,
        'pageData':pageData,
    })

def read_file(file_name, size):  #分批读取文件,此处为512个字节
    with open(file_name, mode='rb') as fp:
        while True:
            c = fp.read(size)
            if c:
                # print('yield一次：')
                yield c
            else:
                break
def getDoc(request,id):
    # return '<html><body>开始下载罗！1....</body></html>'
    doc = get_object_or_404(Doc, id=id)
    # print(doc.file)
    update_to, filename = str(doc.file).split('/')
    filepath = '%s/media/%s/%s' % (os.getcwd(), update_to, filename)
    response = StreamingHttpResponse(read_file(filepath, 512))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{}"'.format(
        filename)
    return response

#########------
####----人脸识别的后端API,可用test

import numpy as np  # 矩阵运算
import urllib  # url解析
import json  # json字符串使用
import cv2  # opencv包
import os  # 执行操作系统命令
from django.views.decorators.csrf import csrf_exempt  # 跨站点验证
from django.http import JsonResponse  # json字符串响应

face_detector_path='serviceApp/haarcascade_frontalface_default.xml'
face_detector=cv2.CascadeClassifier(face_detector_path)  ##生成人脸检测器
def read_image(stream=None):
    if stream is not None:
        data_temp = stream.read()
    img = np.asarray(bytearray(data_temp), dtype="uint8")
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    return img

@csrf_exempt  ##用于规避跨站点请求站点
def facedetect(request):
    result={}
    if request.method=="POST": ##规定客户端使用post上传图片
        if request.FILES.get("image",None) is not None: ##如果有图片则读取图片
            img=read_image(stream=request.FILES['image'])
        else:
            # result.update({"#faceNum":-1,})  ###或者这么写 result['#faceNum']=-1
            result['#faceNum'] = -1
            return JsonResponse(result)
        if img.shape[2]==3:
            img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)   ##彩色图像转灰度
        ##--进行人脸监测
        values=face_detector.detectMultiScale(img,scaleFactor=1.1,
                                              minNeighbors=5,
                                              minSize=(30,30),
                                              flags=cv2.CASCADE_SCALE_IMAGE)
        ##将监测得到的人脸检测关键点坐标封装
        values=[(int(a),int(b),int(a+c),int(b+d)) for (a,b,c,d) in values]
        result.update({
            '#faceNum':len(values),
            'faces':values,
        })
    return JsonResponse(result)

#####----人脸识别的前端-------
def platform(request):
    # html = '<html><body>人脸识别开放平台</body></html>'
    return render(request,'platForm.html')

import base64

@csrf_exempt
def facedetectDemo(request):   ##这是是web版的人脸识别接口
    result = {}
    if request.method == "POST":
        if request.FILES.get('image') is not None:  #
            img = read_image(stream=request.FILES["image"])
        else:
            result["#faceNum"] = -1
            return JsonResponse(result)   ##----default

        if img.shape[2] == 3:
            imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 彩色图像转灰度图像
        else:
            imgGray = img

        #进行人脸检测
        values = face_detector.detectMultiScale(imgGray,
                                           scaleFactor=1.1,
                                           minNeighbors=5,
                                           minSize=(30, 30),
                                           flags=cv2.CASCADE_SCALE_IMAGE)

        #将检测得到的人脸检测关键点坐标封装
        values = [(int(a), int(b), int(a + c), int(b + d))
                  for (a, b, c, d) in values]

        # 将检测框显示在原图上
        for (w, x, y, z) in values:
            cv2.rectangle(img, (w, x), (y, z), (0, 255, 0), 2)

        retval, buffer_img = cv2.imencode('.jpg', img)  # 在内存中编码为jpg格式
        img64 = base64.b64encode(buffer_img)  # base64编码用于网络传输
        img64 = str(img64, encoding='utf-8')  # bytes转换为str类型
        result["img64"] = img64  # json封装
    return JsonResponse(result)







