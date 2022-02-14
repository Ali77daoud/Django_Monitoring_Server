from pysnmp.hlapi import *
from datetime import timedelta


class Snmp_monitor:
    def __init__(self, ip, community):
        self.ip = ip
        self.community = community

    # return device name

    def get_devicename(self):
        errorIndication, errorStatus, errorIndex, varBinds = next(
            getCmd(SnmpEngine(),
                   CommunityData(self.community),
                   UdpTransportTarget((self.ip, 161)),
                   ContextData(),
                   ObjectType(ObjectIdentity('.1.3.6.1.2.1.1.5.0')))
        )

        if errorIndication:
            print(errorIndication)
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        else:
            for varBind in varBinds:
                return varBind[1]

    # return the interfaces using getnext

    def get_interfaces(self):
        s = ()
        iterator = nextCmd(SnmpEngine(),
                           CommunityData(self.community),
                           UdpTransportTarget((self.ip, 161)),
                           ContextData(),
                           ObjectType(ObjectIdentity('.1.3.6.1.2.1.2.2.1.2')),
                           maxCalls=self.get_numberofinter()
                           )

        for errorIndication, errorStatus, errorIndex, varBinds in iterator:
            if errorIndication:
                print(errorIndication)
                break

            elif errorStatus:
                print('%s at %s' % (errorStatus.prettyPrint(),
                                    errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
                break

            else:
                for varBind in varBinds:
                    s = s + (varBind[1] + '|')

        return s

    # return status of interface
    def get_interfaces_status(self):
        s = []
        iterator = nextCmd(SnmpEngine(),
                           CommunityData(self.community),
                           UdpTransportTarget((self.ip, 161)),
                           ContextData(),
                           ObjectType(ObjectIdentity('.1.3.6.1.2.1.2.2.1.7')),
                           maxCalls=self.get_numberofinter()
                           )

        for errorIndication, errorStatus, errorIndex, varBinds in iterator:
            if errorIndication:
                print(errorIndication)
                break

            elif errorStatus:
                print('%s at %s' % (errorStatus.prettyPrint(),
                                    errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
                break

            else:
                for varBind in varBinds:
                    s.append(varBind[1])
        list(s)
        return s
    #get the oid of interface
    def get_interfaces_oid_number(self):
        s = []
        iterator = nextCmd(SnmpEngine(),
                           CommunityData(self.community),
                           UdpTransportTarget((self.ip, 161)),
                           ContextData(),
                           ObjectType(ObjectIdentity('.1.3.6.1.2.1.2.2.1.1')),
                           maxCalls=self.get_numberofinter()
                           )

        for errorIndication, errorStatus, errorIndex, varBinds in iterator:
            if errorIndication:
                print(errorIndication)
                break

            elif errorStatus:
                print('%s at %s' % (errorStatus.prettyPrint(),
                                    errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
                break

            else:
                for varBind in varBinds:
                    s.append(varBind[1])
        list(s)
        return s
    # return the number of interfaces using get

    def get_numberofinter(self):
        errorIndication, errorStatus, errorIndex, varBinds = next(
            getCmd(SnmpEngine(),
                   CommunityData(self.community),
                   UdpTransportTarget((self.ip, 161)),
                   ContextData(),
                   ObjectType(ObjectIdentity('.1.3.6.1.2.1.2.1.0')))
        )

        if errorIndication:
            print(errorIndication)
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        else:
            for varBind in varBinds:
                return varBind[1]

    # return uptime of the device
    def get_uptime(self):
        errorIndication, errorStatus, errorIndex, varBinds = next(
            getCmd(SnmpEngine(),
                   CommunityData(self.community),
                   UdpTransportTarget((self.ip, 161)),
                   ContextData(),
                   ObjectType(ObjectIdentity('.1.3.6.1.2.1.1.3.0')))
        )

        if errorIndication:
            print(errorIndication)
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        else:
            for varBind in varBinds:
                # # print(varBind[1])
                s = int(varBind[1])
                s=s/100
                hour = int(s/3600)
                
                reminder = int(s-hour*3600)
                minute = reminder/60

                reminder = reminder-minute*60
                second = reminder

                # second = s % 60
                # minute = (s / 60)%60
                # hour = (s/60)/60
                up_time = timedelta(hours=hour, minutes=minute, seconds=second)
                # up_time = "%d:%02d.%02d" % (hour, minute, second)
                return up_time

    # return cpu utilization

    def get_cpu_utilization(self):
        errorIndication, errorStatus, errorIndex, varBinds = next(
            getCmd(SnmpEngine(),
                   CommunityData(self.community),
                   UdpTransportTarget((self.ip, 161)),
                   ContextData(),
                   ObjectType(ObjectIdentity('.1.3.6.1.4.1.9.9.109.1.1.1.1.6.1')))
        )

        if errorIndication:
            print(errorIndication)
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        else:
            for varBind in varBinds:
                return varBind[1]

    # ////////////////memory///////////////////////////////////////////////////////////////////////////
    # return used processor memory
    def get_used_processor_memory(self):
        errorIndication, errorStatus, errorIndex, varBinds = next(
            getCmd(SnmpEngine(),
                   CommunityData(self.community),
                   UdpTransportTarget((self.ip, 161)),
                   ContextData(),
                   ObjectType(ObjectIdentity('1.3.6.1.4.1.9.9.48.1.1.1.5.1')))
        )

        if errorIndication:
            print(errorIndication)
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        else:
            for varBind in varBinds:
                return varBind[1]

    # return used I/O memory
    def get_used_IO_memory(self):
        errorIndication, errorStatus, errorIndex, varBinds = next(
            getCmd(SnmpEngine(),
                   CommunityData(self.community),
                   UdpTransportTarget((self.ip, 161)),
                   ContextData(),
                   ObjectType(ObjectIdentity('1.3.6.1.4.1.9.9.48.1.1.1.5.2')))
        )

        if errorIndication:
            print(errorIndication)
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        else:
            for varBind in varBinds:
                return varBind[1]

    # return used  memory
    def get_used_memory(self):
        total = self.get_used_processor_memory() + self.get_used_IO_memory()
        return total

    # return free processor memory
    def get_free_processor_memory(self):
        errorIndication, errorStatus, errorIndex, varBinds = next(
            getCmd(SnmpEngine(),
                   CommunityData(self.community),
                   UdpTransportTarget((self.ip, 161)),
                   ContextData(),
                   ObjectType(ObjectIdentity('1.3.6.1.4.1.9.9.48.1.1.1.6.1')))
        )

        if errorIndication:
            print(errorIndication)
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        else:
            for varBind in varBinds:
                return varBind[1]

    # return free I/O memory
    def get_free_IO_memory(self):
        errorIndication, errorStatus, errorIndex, varBinds = next(
            getCmd(SnmpEngine(),
                   CommunityData(self.community),
                   UdpTransportTarget((self.ip, 161)),
                   ContextData(),
                   ObjectType(ObjectIdentity('1.3.6.1.4.1.9.9.48.1.1.1.6.2')))
        )

        if errorIndication:
            print(errorIndication)
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        else:
            for varBind in varBinds:
                return varBind[1]

    # return free  memory
    def get_free_memory(self):
        total = self.get_free_processor_memory() + self.get_free_IO_memory()
        return total

    # return free  memory
    def get_total_memory(self):
        total = self.get_used_memory() + self.get_free_memory()
        return total

    # return temperature status
    def get_temperature_status(self):
        errorIndication, errorStatus, errorIndex, varBinds = next(
            getCmd(SnmpEngine(),
                   CommunityData(self.community),
                   UdpTransportTarget((self.ip, 161)),
                   ContextData(),
                   ObjectType(ObjectIdentity('1.3.6.1.4.1.9.9.13.1.3.1.6.1')))
        )

        if errorIndication:
            print(errorIndication)
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        else:
            for varBind in varBinds:
                return varBind[1]

    # ////// Monitoring SNMP Protocol on the Device //////////////////////////////////////////////
    # return snmp in_packets
    def get_snmp_inpkts(self):
        errorIndication, errorStatus, errorIndex, varBinds = next(
            getCmd(SnmpEngine(),
                   CommunityData(self.community),
                   UdpTransportTarget((self.ip, 161)),
                   ContextData(),
                   ObjectType(ObjectIdentity('.1.3.6.1.2.1.11.1.0')))
        )

        if errorIndication:
            print(errorIndication)
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        else:
            for varBind in varBinds:
                return varBind[1]

    # get snmp out packets
    def get_snmp_outpkts(self):
        errorIndication, errorStatus, errorIndex, varBinds = next(
            getCmd(SnmpEngine(),
                   CommunityData(self.community),
                   UdpTransportTarget((self.ip, 161)),
                   ContextData(),
                   ObjectType(ObjectIdentity('.1.3.6.1.2.1.11.2.0')))
        )

        if errorIndication:
            print(errorIndication)
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        else:
            for varBind in varBinds:
                return varBind[1]

    # The total number of SNMP messages which were delivered to
    # the SNMP entity and were for an unsupported SNMP version.
    def snmp_badversion(self):
        errorIndication, errorStatus, errorIndex, varBinds = next(
            getCmd(SnmpEngine(),
                   CommunityData(self.community),
                   UdpTransportTarget((self.ip, 161)),
                   ContextData(),
                   ObjectType(ObjectIdentity('.1.3.6.1.2.1.11.3.0')))
        )

        if errorIndication:
            print(errorIndication)
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        else:
            for varBind in varBinds:
                return varBind[1]

    # The total number of SNMP messages delivered to the SNMP
    # entity which used a SNMP community name not known for it
    def snmp_badcommunity(self):
        errorIndication, errorStatus, errorIndex, varBinds = next(
            getCmd(SnmpEngine(),
                   CommunityData(self.community),
                   UdpTransportTarget((self.ip, 161)),
                   ContextData(),
                   ObjectType(ObjectIdentity('.1.3.6.1.2.1.11.4.0')))
        )

        if errorIndication:
            print(errorIndication)
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        else:
            for varBind in varBinds:
                return varBind[1]

    # The total number of SNMP Get-Request PDUs which
    # have been accepted and processed by the SNMP protocol entity.
    def snmp_ingetrequest(self):
        errorIndication, errorStatus, errorIndex, varBinds = next(
            getCmd(SnmpEngine(),
                   CommunityData(self.community),
                   UdpTransportTarget((self.ip, 161)),
                   ContextData(),
                   ObjectType(ObjectIdentity('.1.3.6.1.2.1.11.15.0')))
        )

        if errorIndication:
            print(errorIndication)
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        else:
            for varBind in varBinds:
                return varBind[1]

    # The total number of SNMP Get-next PDUs which
    # have been accepted and processed by the SNMP protocol entity.
    def snmp_ingetnext(self):
        errorIndication, errorStatus, errorIndex, varBinds = next(
            getCmd(SnmpEngine(),
                   CommunityData(self.community),
                   UdpTransportTarget((self.ip, 161)),
                   ContextData(),
                   ObjectType(ObjectIdentity('.1.3.6.1.2.1.11.16.0')))
        )

        if errorIndication:
            print(errorIndication)
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        else:
            for varBind in varBinds:
                return varBind[1]

    # The total number of SNMP set PDUs which
    # have been accepted and processed by the SNMP protocol entity.
    def snmp_inset(self):
        errorIndication, errorStatus, errorIndex, varBinds = next(
            getCmd(SnmpEngine(),
                   CommunityData(self.community),
                   UdpTransportTarget((self.ip, 161)),
                   ContextData(),
                   ObjectType(ObjectIdentity('.1.3.6.1.2.1.11.17.0')))
        )

        if errorIndication:
            print(errorIndication)
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        else:
            for varBind in varBinds:
                return varBind[1]

    # The total number of SNMP Response PDUs which
    # have been accepted and processed by the SNMP protocol entity.
    def snmp_inresponse(self):
        errorIndication, errorStatus, errorIndex, varBinds = next(
            getCmd(SnmpEngine(),
                   CommunityData(self.community),
                   UdpTransportTarget((self.ip, 161)),
                   ContextData(),
                   ObjectType(ObjectIdentity('.1.3.6.1.2.1.11.18.0')))
        )

        if errorIndication:
            print(errorIndication)
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        else:
            for varBind in varBinds:
                return varBind[1]

    # The total number of SNMP Trap PDUs which
    # have been accepted and processed by the SNMP protocol entity.
    def snmp_intrap(self):
        errorIndication, errorStatus, errorIndex, varBinds = next(
            getCmd(SnmpEngine(),
                   CommunityData(self.community),
                   UdpTransportTarget((self.ip, 161)),
                   ContextData(),
                   ObjectType(ObjectIdentity('.1.3.6.1.2.1.11.19.0')))
        )

        if errorIndication:
            print(errorIndication)
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        else:
            for varBind in varBinds:
                return varBind[1]



#
# m = Snmp_monitor('192.168.137.3', 'ali')
# n = m.get_snmp_outpkts()
# print(n)

