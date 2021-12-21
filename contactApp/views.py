from django.shortcuts import render
from django.shortcuts import HttpResponse
from .models import Ad
from .forms import ResumeForm

# Create your views here.
def contact(request):
    # html = '<html><body>欢迎咨询</body></html>'
    return render(request,'contact.html')


def recruit(request):
    # html = '<html><body>加入恒达</body></html>'
    # AdList=Ad.objects.all().order_by('-publishDate')
    # return render(request,'recruit.html',{
    #     'active_menu':'contactus',
    #     'sub_menu':'recruit',
    #     'AdList':AdList
    # })
    ###--------加了模型表单之后的写法------
    AdList=Ad.objects.all().order_by('-publishDate')
    if request.method=='POST':
        resumeForm=ResumeForm(data=request.POST,files=request.FILES)
        print(resumeForm.is_valid())
        if resumeForm.is_valid():
            resumeForm.save()
            return render(request,'success.html',{
                'active_menu':'contactus',
                'sub_menu':'recruit',
            })
    else:
        resumeForm=ResumeForm()
    return render(request,'recruit.html',{
            'active_menu': 'contactus',
            'sub_menu': 'recruit',
            'AdList':AdList,
            'resumeForm':resumeForm,
        }
    )


