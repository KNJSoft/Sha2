from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/',views.signup,name="signup"),
    path('signup/',views.signin,name="signin"),
    path('upload/',views.send_file,name="upload")
    # path('verify/',views.verify,name="verify"),
    # path('messages/',views.notification,name="notification"),
    # path('logout/',views.log_out,name='logout')
]