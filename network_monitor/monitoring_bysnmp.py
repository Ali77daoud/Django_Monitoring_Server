import threading
import time
from network_monitor.models import Devices, General_info, Hardware_info
from network_monitor.snmp import Snmp_monitor


def monitor():
    while True:
        if Devices.objects.count() == 0:
            continue
        else:
            devices = Devices.objects.all()
            for d in devices:
                if d.type_of_monitoring == 'monitor by snmp':
                    d_ip = d.ip
                    d_community = d.community
                    m = Snmp_monitor(d_ip, d_community)
                    d_name = m.get_devicename()
                    d_interfaces = m.get_numberofinter()
                    d_uptime = m.get_uptime()
                    cpu_ut = m.get_cpu_utilization()
                    mem_used = m.get_used_memory()
                    mem_free = m.get_free_memory()
                    mem_total = m.get_total_memory()
                    temperature = m.get_temperature_status()

                    l = str(m.get_interfaces())
                    get_interface = l.split("|")
                    # in_p = m.get_snmp_inpkts()
                    # out_p = m.get_snmp_outpkts()
                    # bad_v = m.snmp_badversion()
                    # bad_c = m.snmp_badcommunity()
                    # in_get = m.snmp_ingetrequest()
                    # in_next = m.snmp_ingetnext()
                    # in_se = m.snmp_inset()
                    # in_res = m.snmp_inresponse()
                    # in_tr = m.snmp_intrap()

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

                    # snmp_info = SNMP_info.objects.create(
                    #     device=d,
                    #     in_packets=in_p,
                    #     out_packets=out_p,
                    #     bad_version=bad_v,
                    #     bad_community=bad_c,
                    #     in_getrequset=in_get,
                    #     in_getnext=in_next,
                    #     in_set=in_se,
                    #     in_response=in_res,
                    #     in_trap=in_tr
                    # )
        time.sleep(2)

#
# x = threading.Thread(target=monitor)
# x.start()
