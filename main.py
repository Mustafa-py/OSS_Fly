import argparse
import itertools
import pprint
import os
import re

from pysnmp.hlapi import *

NEIGHBOUR_PORT_OID = '1.0.8802.1.1.2.1.4.1.1.8.0'
NEIGHBOUR_NAME_OID = '1.0.8802.1.1.2.1.4.1.1.9'
PARENT_NAME_OID = '1.0.8802.1.1.2.1.3.3'


class MissingOidParameter(Exception):
    pass


def is_file_valid(filepath):

    if not os.path.exists(filepath):
        raise ValueError('Invalid filepath')
    return filepath


def get_cli_arguments():

    parser = argparse.ArgumentParser(description="")
    parser.add_argument(
        '-f',
        '--file',
        type=is_file_valid,
        help='Path to the switches file'
    )
    return parser


def get_switches_from_file():

    args = get_cli_arguments().parse_args()
    switches_info = []
    with open(args.file) as switches_info_fp:
        for line in switches_info_fp:
            line = line.rstrip().split(',')
            switches_info.append({
                'community': line[0].strip(),
                'snmp_port': line[1].strip(),
                'ip': line[2].strip(),
            })
    return switches_info


def parse_neighbours_ports_result(result):

    if not result:
        raise MissingOidParameter('No OID provided.')

    value = result.split(' = ')
    if not value:
        return 'Missing entire value for OID={}'.format(result)
    else:
        oid, port = value
        local_port = re.search(r'{}\.(\d+)'.format(NEIGHBOUR_PORT_OID[2:]), oid).group(1)

        if port:
            remote_port = re.search(r'(\d+)', port).group(1)
        else:
            remote_port = 'Unknown'

    return 'local_port', local_port, 'remote_port', remote_port


def parse_parent_name(result):

    if not result:
        raise MissingOidParameter('No OID provided.')

    value = result.split(' = ')
    if not value:
        return 'Missing entire value for OID={}'.format(result)
    else:
        return 'Unknown' if not value[-1] else value[-1]


def parse_neighbour_names_results(result):


    if not result:
        raise MissingOidParameter('No OID provided.')

    value = result.split(' = ')
    if not value:
        return 'Missing entire value for OID={}'.format(result)
    else:
        return ('name', 'Unknown') if not value[-1] else ('name', value[-1])


def main():
    data = {}
    switches_filedata = get_switches_from_file()

    for switch in switches_filedata:
        community = switch.get('community')
        snmp_port = switch.get('snmp_port')
        ip = switch.get('ip')

        name = ''
        for (error_indication, error_status, error_index, var_binds) in nextCmd(
                SnmpEngine(),
                CommunityData(community),
                UdpTransportTarget((ip, snmp_port)),
                ContextData(),
                ObjectType(ObjectIdentity(PARENT_NAME_OID)),
                lexicographicMode=False
        ):
            # this should always return one result
            name = parse_parent_name(str(var_binds[0]))

        if not name:
            print('Could not retrieve name of switch. Moving to the next one...')
            continue

        neighbour_names = []
        neighbour_local_remote_ports = []

        for (error_indication, error_status, error_index, var_binds) in nextCmd(
                SnmpEngine(),
                CommunityData(community),
                UdpTransportTarget((ip, snmp_port)),
                ContextData(),
                ObjectType(ObjectIdentity(NEIGHBOUR_NAME_OID)),
                lexicographicMode=False
        ):
            for var_bind in var_binds:
                neighbour_names.append(
                    parse_neighbour_names_results(str(var_bind))
                )

        for (error_indication, error_status, error_index, var_binds) in nextCmd(
                SnmpEngine(),
                CommunityData(community),
                UdpTransportTarget((ip, snmp_port)),
                ContextData(),
                ObjectType(ObjectIdentity(NEIGHBOUR_PORT_OID)),
                lexicographicMode=False
        ):
            for var_bind in var_binds:
                neighbour_local_remote_ports.append(
                    parse_neighbours_ports_result(str(var_bind))
                )

        neighbours = []
        for a, b in itertools.zip_longest(
                neighbour_names,
                neighbour_local_remote_ports,
                fillvalue='unknown'
        ):
            neighbours.append({
                a[0]: a[1],
                b[0]: b[1],
                b[2]: b[3]
            })

        data[name] = {
            'ip': ip,
            'neighbors': neighbours
        }

    return data


if __name__ == '__main__':
    all_data = main()
    pprint.pprint(all_data, indent=4)
