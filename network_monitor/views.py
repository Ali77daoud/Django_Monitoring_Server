from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from network_monitor.models import Devices, Ram_info, Cpu_info, Disk_info, Network_info, General_info, Hardware_info, \
    SNMP_info, Get_Interfaces
from django.http import HttpResponse
from network_monitor.ping import myping
from network_monitor.snmpset import snmp_set


# Create your views here.
def login(request):
    username = 'aga'
    password = '123aga456'
    return render(request, 'login.html', {'username': username, 'password': password})

def home(request):
    devices = Devices.objects.all()
    # d = Devices.objects.get(pk=1)
    # d.operating_system = 'Router OS'
    # d.save()
    # alert_info = []
    # for i in range(0, len(devices)):
    #     aa = Alert_info.objects.filter(device_id=devices[i].pk).latest('date')
    #     alert_info.append(aa)



    return render(request, 'index.html', {'devices': devices,})


# def about(request):
# return HttpResponse(request, "HELLO")

# we use id to show the device monitoring details by its id
# we take the id from url
def details(request, d_id):
    device = get_object_or_404(Devices, pk=d_id)
    if device.type_of_monitoring == "monitored by agent":
        a_ram = Ram_info.objects.filter(device_id=d_id).latest('date')
        a_cpu = Cpu_info.objects.filter(device_id=d_id).latest('date')
        cpu_graph = Cpu_info.objects.filter(device_id=d_id).order_by('id')
        aa_disk = Disk_info.objects.filter(device_id=d_id).latest('disk_id')
        aa_net = Network_info.objects.filter(device_id=d_id).latest('network_id')
        x = aa_disk.disk_id
        y = aa_net.network_id
        a_disk = Disk_info.objects.filter(device_id=d_id).filter(disk_id=x)
        a_net = Network_info.objects.filter(device_id=d_id).filter(network_id=y)
        return render(request, 'details.html', {'device': device, 'a_ram': a_ram,
                                                'a_cpu': a_cpu, 'a_disk': a_disk,
                                                'a_net': a_net,
                                                'cpu_graph': cpu_graph}
                                                      )
    else:
        a_general = General_info.objects.filter(device_id=d_id).latest('date')
        a_snmp = SNMP_info.objects.filter(device_id=d_id).latest('date')
        a_hard = Hardware_info.objects.filter(device_id=d_id).latest('date')
        aa_interface = Get_Interfaces.objects.filter(device_id=d_id).latest('date')
        z = aa_interface.interfaces_id
        num_inerface = a_general.num_of_interfaces
        a_interface = Get_Interfaces.objects.filter(device_id=d_id).filter(interfaces_id=z)[:num_inerface]
        cpu_snmp = Hardware_info.objects.filter(device_id=d_id).order_by('id')

        return render(request, 'detail.html', {
            'device': device, 'a_general': a_general, 'a_hard': a_hard, 'a_snmp': a_snmp,
            'a_interface': a_interface, 'cpu_snmp': cpu_snmp
        })

# to add device for snmp
def add_device(request):
    if request.method == 'POST':
        d_ip = request.POST['IP']
        d_community = request.POST['community']
        d_type = request.POST['radio1']
        d_monitor = 'monitored by snmp'
        if Devices.objects.count() == 0:
            device = Devices.objects.create(
                ip=d_ip,
                community=d_community,
                type_of_device=d_type,
                type_of_monitoring=d_monitor,
                operating_system='Cisco IOS',
                if_alert=False
            )

            # alert_data_snmp = Alert_info.objects.create(
            #     device=device,
            #     if_alert=False,
            # )
        # test if the device doesn't exist in the database, add it
        else:
            t = True
            devices = Devices.objects.all()
            for d in devices:
                if d.ip == d_ip:
                    t = False
            if t == True:
                device = Devices.objects.create(
                    ip=d_ip,
                    community=d_community,
                    type_of_device=d_type,
                    type_of_monitoring=d_monitor,
                    operating_system='Cisco IOS',
                    if_alert=False
                )

                # alert_data_snmp = Alert_info.objects.create(
                #     device=device,
                #     if_alert=False,
                # )
                return redirect('home')
    return render(request, 'add-device.html')

def change_interface_status(request):
    if request.method == 'POST':
        data = request.POST['buttonOnOff']
    l = data.split(',')
    state = int(l[0])
    oid = l[1]
    device_id = int(l[2])
    snmp_set(oid, state)
    return redirect('/devices/%s/'%device_id)



# agent data
@csrf_exempt
def agent_devices(request):
    if request.method == 'POST':
        d_os = request.POST['os']
        d_ip = request.POST['ip']
    # if the device is connected add it
    #     if myping(d_ip):
        if Devices.objects.count() == 0:
                device = Devices.objects.create(
                    ip=d_ip,
                    type_of_device='Computer',
                    type_of_monitoring='monitored by agent',
                    operating_system=d_os,
                    if_alert=False
                )
            # test if the device doesn't exist in the database, add it
        else:
                t = True
                devices = Devices.objects.all()
                for d in devices:
                    if d.ip == d_ip:
                        t = False
                if t == True:
                    device = Devices.objects.create(
                        ip=d_ip,
                        type_of_device='Computer',
                        type_of_monitoring='monitored by agent',
                        operating_system=d_os,
                        if_alert=False
                    )
        # else:
        #     print("there is no connection to the device")
    return HttpResponse(request)


@csrf_exempt
def ram_data(request):
    if request.method == 'POST':
        total = request.POST['total']
        available = request.POST['av_space']
        percent = request.POST['percent_used']
        used = request.POST['us_space']
        id = request.POST['ip']
        device = get_object_or_404(Devices, ip=id)
        ram_agent = Ram_info.objects.create(
            device=device,
            total_ram=total,
            available_space=available,
            percent_of_used=percent,
            used_space=used
        )
    return HttpResponse(request)


@csrf_exempt
def cpu_data(request):
    if request.method == 'POST':
        usage = request.POST['usage']
        user = request.POST['user']
        system = request.POST['system']
        idle = request.POST['idle']
        interrupt = request.POST['interrupt']
        cores = request.POST['cores']
        logical = request.POST['logical']
        current = request.POST['current']
        min1 = request.POST['min']
        max1 = request.POST['max']
        id = request.POST['ip']
        device = get_object_or_404(Devices, ip=id)
        cpu_agent = Cpu_info.objects.create(
            device=device,
            usage_of_cpu=usage,
            user_mode=user,
            system_mode=system,
            idle=idle,
            interrupt=interrupt,
            number_of_cores=cores,
            number_of_logical=logical,
            current_freq=current,
            min_freq=min1,
            max_freq=max1
        )
    return HttpResponse(request)


@csrf_exempt
def disk_data(request):
    if request.method == 'POST':
        d_name = request.POST['name']
        d_type = request.POST['type']
        d_size = request.POST['size']
        d_usage = request.POST['usage']
        d_percent = request.POST['percent']
        di_id = request.POST['di_id']
        id = request.POST['ip']
        device = get_object_or_404(Devices, ip=id)
        disk_data_agent = Disk_info.objects.create(
            device=device,
            disk_name=d_name,
            disk_type=d_type,
            disk_size=d_size,
            disk_usage=d_usage,
            disk_percent_used=d_percent,
            disk_id=di_id
        )
    return HttpResponse(request)


@csrf_exempt
def network_data(request):
    if request.method == 'POST':
        n_name = request.POST['name']
        n_mac = request.POST['mac']
        n_ip4 = request.POST['ip4']
        n_subnet = request.POST['subnet']
        n_ip6 = request.POST['ip6']
        n_isup = request.POST['isup']
        n_id = request.POST['ne_id']
        id = request.POST['ip']
        device = get_object_or_404(Devices, ip=id)
        disk_data_agent = Network_info.objects.create(
            device=device,
            nic_name=n_name,
            mac=n_mac,
            ip4=n_ip4,
            subnet=n_subnet,
            ip6=n_ip6,
            network_id=n_id,
            is_up=n_isup
        )
    return HttpResponse(request)
@csrf_exempt
def alert_data(request):
    if request.method == 'POST':
        id = request.POST['ip']
        if_alert = request.POST['if_alert']
        device = get_object_or_404(Devices, ip=id)
        device.if_alert = if_alert
        device.save()
        # alert_data_agent = Alert_info.objects.create(
        #     device=device,
        #     if_alert=if_alert,
        # )
    return HttpResponse(request)