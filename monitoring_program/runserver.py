from django.core.management import call_command
from django.core.wsgi import get_wsgi_application
import os
import threading
import time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "monitoring_program.settings")
import django

django.setup()
from network_monitor.models import Devices, General_info, Hardware_info, Get_Interfaces, SNMP_info
from network_monitor.snmp import Snmp_monitor


application = get_wsgi_application()


def monitor():
    i = 0
    while True:
        time.sleep(1)
        if Devices.objects.count() == 0:
            continue
        else:
            if_alert = False
            devices = Devices.objects.all()
            for d in devices:
                if d.type_of_monitoring == 'monitored by snmp':
                    d_ip = d.ip
                    d_community = d.community
                    m = Snmp_monitor(d_ip, d_community)
                    d_name = m.get_devicename()
                    d_interfaces = m.get_numberofinter()
                    d_uptime = m.get_uptime()
                    cpu_ut = m.get_cpu_utilization()
                    if cpu_ut >=80 :
                        if_alert = True
                    mem_used = m.get_used_memory()
                    mem_used = round(mem_used/(1024*1024), 2)
                    mem_free = m.get_free_memory()
                    mem_free = round(mem_free/(1024*1024), 2)
                    mem_total = m.get_total_memory()
                    mem_total = round(mem_total/(1024*1024), 2)
                    mem_percentofused = round((mem_used/mem_total)*100, 2)
                    if mem_percentofused >= 80:
                        if_alert = True
                    temp = m.get_temperature_status()
                    if temp == 1:
                        temperature = "Normal"
                    else:
                        if temp == 2:
                            temperature = "Warning"
                        else:
                            if temp == 3:
                                temperature = "Critical"
                            else:
                                temperature = "Not Present"
                    if temperature == "Warning":
                        if_alert = True
                    n = m.get_interfaces_status()
                    st = ''
                    for j in range(0, len(n)):
                        if n[j] == 1:
                            st += 'up' + '|'
                        else:
                            if n[j] == 2:
                                st += 'down' + '|'
                            else:
                                st += " "
                    get_status = st.split('|')
                    get_oid = m.get_interfaces_oid_number()
                    l = str(m.get_interfaces())
                    get_interface = l.split("|")
                    in_p = m.get_snmp_inpkts()
                    out_p = m.get_snmp_outpkts()
                    bad_v = m.snmp_badversion()
                    bad_c = m.snmp_badcommunity()
                    in_get = m.snmp_ingetrequest()
                    in_next = m.snmp_ingetnext()
                    in_se = m.snmp_inset()
                    in_res = m.snmp_inresponse()
                    in_tr = m.snmp_intrap()

                    general_info = General_info.objects.create(
                        device=d,
                        device_name=d_name,
                        num_of_interfaces=d_interfaces,
                        uptime=d_uptime,
                    )
                    hardware_info = Hardware_info.objects.create(
                        device=d,
                        cpu_utilization=cpu_ut,
                        used_memory=mem_used,
                        free_memory=mem_free,
                        total_memory=mem_total,
                        temp_status=temperature
                    )
                    i = i + 1
                    for u in range(0, len(get_interface)-1):
                        Get_Interfaces.objects.create(
                                device=d,
                                interface_name=get_interface[u],
                                interface_status=get_status[u],
                                interface_oid_number=get_oid[u],
                                interfaces_id=i
                            )
                    snmp_info = SNMP_info.objects.create(
                        device=d,
                        in_packets=in_p,
                        out_packets=out_p,
                        bad_version=bad_v,
                        bad_community=bad_c,
                        in_getrequset=in_get,
                        in_getnext=in_next,
                        in_set=in_se,
                        in_response=in_res,
                        in_trap=in_tr
                    )
                    d.if_alert = if_alert


x = threading.Thread(target=monitor)
x.start()
call_command('runserver', '127.0.0.1:8000')


