from django.urls import path
from network_monitor import views

urlpatterns = [
    path('', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('devices/<int:d_id>/', views.details, name='d_details'),
    path('devices/new/', views.add_device, name='add'),
    # path('about/', views.about, name='about'),
    path('interface/', views.change_interface_status, name='change'),
    # agent urls
    path('agent/', views.agent_devices, name='agent'),
    path('ram/', views.ram_data, name='ram'),
    path('cpu/', views.cpu_data, name='cpu'),
    path('disk/', views.disk_data, name='disk'),
    path('network/', views.network_data, name='network'),
    path('alert/', views.alert_data, name='alert'),
]
