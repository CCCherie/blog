from django.contrib import admin

# Register your models here.

from .models import Post,Category,Tag


class PostAdmin(admin.ModelAdmin):
    #post列表页展现的字段
    list_display = ['title','created_time','modified_time','category','author']
    #表单里展现的字段
    fields = ['title','body','excerpt','category','tags']
    #复写save_model方法 将作者、创建时间、修改时间自动填写
    def save_model(self,request,obj,form,change):
        obj.author = request.user
        super().save_model(request,obj,form,change)

admin.site.register(Post,PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)
