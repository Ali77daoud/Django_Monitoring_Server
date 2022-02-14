from pysnmp.hlapi import *

def snmp_set(x,y):
    next(
        setCmd(SnmpEngine(),
               CommunityData("ali"),
               UdpTransportTarget(("192.168.137.3", 161)),
               ContextData(),
               ObjectType(ObjectIdentity(".1.3.6.1.2.1.2.2.1.7.{}".format(x)), Integer(y)))
    )

