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
    path('flows/', views.flows, name='flows'),
    path('modify_flow/<str:pk>', views.modify_flow, name='modify_flow'),
    path('get_all_problems', views.get_all_problems, name='get_all_problems'),
    path('flow/<str:pk>', views.flow, name='flow'),
    path('all_problems_view', views.all_problems_view, name='all_problems_view'),
]
