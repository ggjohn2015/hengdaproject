from django.contrib import admin

# Register your models here.

from .models import Award

class AwardAdmin00(admin.ModelAdmin):
    # list_display = ['description','photo']
    pass

admin.site.register(Award, AwardAdmin00)

admin.site.site_header="企业门户网站后台管理系统"
admin.site.site_title="企业门户网站后台管理系统"


