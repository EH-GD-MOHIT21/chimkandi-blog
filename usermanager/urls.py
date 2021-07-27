from django.urls import path
from .import views

urlpatterns = [
    path('generateotp',views.genrateotp),
    path('login',views.loginuser),
    path('signup',views.signupuser),
    path('logout',views.logoutuser),
    path('checkin',views.claim_reward),
]
