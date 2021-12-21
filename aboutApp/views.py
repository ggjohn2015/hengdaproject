from django.shortcuts import render
from django.shortcuts import HttpResponse
from .models import Award

# Create your views here.
def survey(request):
    # html = '<html><body>企业概况</body></html>'
    return render(request, "survey.html" ,{
        "active_menu":"about",
        'sub_menu':'survey',
    })


def honor(request):
    # html = '<html><body>荣誉资质</body></html>'
    awards=Award.objects.all()
    return render(request, "honor.html" ,{
        "active_menu":"about",
        'sub_menu': 'honor',
        'awards':awards,
    })