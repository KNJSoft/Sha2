from django.urls import path

from . import views
from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [
    path('', views.index, name='index'),
    path('signup/',views.signup,name="signup"),
    path('signin/',views.signin,name="signin"),
    path('upload/',views.send_file,name="upload"),
    path('api/files/add/',views.CreateFile.as_view()),
    path('api/user/add/',views.AddUser.as_view()),
    path('api/files/list/',views.ListFile.as_view()),
    path('api/user/auth/', obtain_auth_token),
    # path('files/api/add/v2/',views.api_files_post),
    # path('verify/',views.verify,name="verify"),
    # path('messages/',views.notification,name="notification"),
    # path('logout/',views.log_out,name='logout')
]