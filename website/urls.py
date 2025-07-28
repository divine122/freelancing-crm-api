from django.urls import path
from . import views
urlpatterns = [
    path('', views.home , name='home'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('record/<int:pk>', views.customer_record, name='record'),
    path('delete_record/<int:pk>', views.delete_record, name='delete_record'),
    path('add_record', views.add_record, name='add_record'),
    path('update_record/<int:pk>', views.update_record, name='update_record'),
    path('verify_email/<str:email>', views.verify_email, name='verify-email'),
    path("login", views.signin, name="signin"),
    path("resend-otp", views.resend_otp, name="resend-otp"),
]
