from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.signin, name='login'),
    path('logout/', views.signout, name='logout'),
    path('problem/<str:pk>', views.problem, name='problem'),
    path('problems/<str:problem_type>', views.problem_set, name='problem_set'),
    path('about/', views.about, name='about'),
    path('user/<str:username>', views.profile, name='user_profile'),
    path('change_username', views.change_username, name='change_username'),
    path('change_password', views.change_password, name='change_password'),
]
