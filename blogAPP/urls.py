from django.urls import path
from .import views
urlpatterns = [
    path('',views.RenderHome),
    path('dashboard',views.RenderDashboard),
    path('addref',views.checkforReferal),
    path('blog',views.RenderBlogPage),
    path('postblog',views.postblog),
    path('post/blogdata',views.acceptblogdata),
    path('blogs/<slug:blogurl>',views.RenderUniqueBlogPage),
    path('search',views.RenderSearchFields),
    path('changepp',views.changepp),
]
