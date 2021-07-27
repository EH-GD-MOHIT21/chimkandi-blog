from django.contrib import admin

# Register your models here.


from .models import *

admin.site.register(CustomUserModel)

admin.site.register(BlogImages)

admin.site.register(Blogs)

admin.site.register(DescFields)