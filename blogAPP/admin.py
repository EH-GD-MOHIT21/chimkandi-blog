from django.contrib import admin

# Register your models here.


from .models import *

admin.site.register(User)

admin.site.register(BlogImages)

admin.site.register(Blogs)
admin.site.register(BlogRatings)

admin.site.register(DescFields)
admin.site.register(BlogComments)