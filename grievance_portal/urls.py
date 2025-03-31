

from django.urls import path
from grievance_portal import views
from student_grievance_portal import settings


urlpatterns=[
    path('', views.login, name="login"),
    path("signup/", views.signup, name="signup"),
    path('home/', views.home, name="home"),
    path('file-complaint/', views.file_complaint, name="file_complaint"),
    path('view-complaints/', views.view_complaints, name="view_complaints"),
    path('manage-complaints/', views.manage_complaints, name="manage_complaints"),
    path("withdraw-complaint/<int:complaint_id>/", views.withdraw_complaint, name="withdraw_complaint"),
    path("edit-complaint/<int:complaint_id>/", views.edit_complaint, name="edit_complaint"),
    path('forgot-password/', views.forgot_password, name="forgot_password"),
    path('base/', views.base, name="base"),
    path('about/', views.about, name="about"),
    path('profile/', views.profile, name="profile"),
    path('query/', views.query, name="query"),
    path('logout/', views.student_logout, name='logout'),
] 