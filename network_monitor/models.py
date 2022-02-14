from django.db import models

# Create your models here.


# Create your models here.
class Devices(models.Model):
    ip = models.CharField(max_length=50, unique=True)
    community = models.CharField(max_length=50, null=True)
    type_of_device = models.CharField(max_length=50)
    type_of_monitoring = models.CharField(max_length=50)
    operating_system = models.CharField(max_length=50)
    if_alert = models.BooleanField()
    date = models.DateTimeField(auto_now_add=True)
#snmp tables
class General_info(models.Model):
    device = models.ForeignKey(Devices, related_name='general', on_delete=models.CASCADE)
    device_name = models.CharField(max_length=50)
    num_of_interfaces = models.IntegerField()
    uptime = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)
class Hardware_info(models.Model):
    device = models.ForeignKey(Devices, related_name='hardware', on_delete=models.CASCADE)
    cpu_utilization = models.IntegerField()
    used_memory = models.FloatField()
    free_memory = models.FloatField()
    total_memory = models.FloatField()
    temp_status = models.CharField(max_length=30)
    date = models.DateTimeField(auto_now_add=True)
class SNMP_info(models.Model):
    device = models.ForeignKey(Devices, related_name='snmp', on_delete=models.CASCADE)
    in_packets = models.IntegerField()
    out_packets = models.IntegerField()
    bad_version = models.IntegerField()
    bad_community = models.IntegerField()
    in_getrequset = models.IntegerField()
    in_getnext = models.IntegerField()
    in_set = models.IntegerField()
    in_response = models.IntegerField()
    in_trap = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
class Get_Interfaces(models.Model):
    device = models.ForeignKey(Devices, related_name='interfaces', on_delete=models.CASCADE)
    interface_name = models.CharField(max_length=50)
    interface_status = models.CharField(max_length=50)
    interface_oid_number = models.IntegerField()
    interfaces_id = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

#agent tables
class Ram_info(models.Model):
    device = models.ForeignKey(Devices, related_name='ram', on_delete=models.CASCADE)
    total_ram = models.FloatField()
    available_space = models.FloatField()
    percent_of_used = models.FloatField()
    used_space = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

class Cpu_info(models.Model):
    device = models.ForeignKey(Devices, related_name='cpu', on_delete=models.CASCADE)
    usage_of_cpu = models.FloatField()
    user_mode = models.FloatField()
    system_mode = models.FloatField()
    idle = models.FloatField()
    interrupt = models.FloatField()
    number_of_cores = models.IntegerField()
    number_of_logical = models.IntegerField()
    current_freq = models.FloatField()
    min_freq = models.FloatField()
    max_freq = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
class Disk_info(models.Model):
    device = models.ForeignKey(Devices, related_name='disk', on_delete=models.CASCADE)
    disk_name = models.CharField(max_length=50)
    disk_type = models.CharField(max_length=50)
    disk_size = models.FloatField()
    disk_usage = models.FloatField()
    disk_percent_used = models.FloatField()
    disk_id = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
class Network_info(models.Model):
    device = models.ForeignKey(Devices, related_name='network', on_delete=models.CASCADE)
    nic_name = models.CharField(max_length=100)
    mac = models.CharField(max_length=50)
    ip4 = models.CharField(max_length=50)
    subnet = models.CharField(max_length=50)
    ip6 = models.CharField(max_length=50)
    is_up = models.BooleanField()
    network_id = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
# class Alert_info(models.Model):
#     device = models.ForeignKey(Devices, related_name='alert', on_delete=models.CASCADE)
#     if_alert = models.BooleanField()
#     date = models.DateTimeField(auto_now_add=True)