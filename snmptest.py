import sys

from pysnmp.hlapi import *

def walk(host, oid):
    for (errorIndication,errorStatus,errorIndex,varBinds) in nextCmd(SnmpEngine(), 
        CommunityData('12345'), UdpTransportTarget((host, 161)), ContextData(),
        ObjectType(ObjectIdentity(oid)),  lexicographicMode=False):
        if errorIndication:
            print(errorIndication, file=sys.stderr)
            break
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'), 
                                file=sys.stderr)             
            break
        else:
            for varBind in varBinds:
                print(varBind)

walk('10.50.80.3','1.3.6')