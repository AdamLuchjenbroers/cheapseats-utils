import boto3
import jmespath
import re

cfn = boto3.client('cloudformation')

ip_pattern = re.compile('(?P<subnet>([0-9]+\.){3}([0-9]+))\/(?P<size>[0-9]+)$')

def parse_cidr(cidr):
    ip_info = ip_pattern.search(cidr)
    if ip_info:
        subnet = ip_info.group('subnet')
        size = int(ip_info.group('size'))

        return (subnet, size)
    else:
        raise ValueError('Malformed or invalid Subnet CIDR: %s' % cidr)

def compute_netmask(size):
    mask = (0xffffffff >> (32 - size)) << (32 - size)
    return (str( (0xff000000 & mask) >> 24)   + '.' +
            str( (0x00ff0000 & mask) >> 16)   + '.' +
            str( (0x0000ff00 & mask) >> 8)    + '.' +
            str( (0x000000ff & mask)))

def fetch_stack_export(export_name):
    list = cfn.list_exports()
    
    data = jmespath.search('Exports[*].[Name, Value]', list)
    for row in data:
        if row[0] == export_name:
            return row[1]

def macro_handler(event, context):
    try:
        if 'CIDR' in event['params']: 
            cidr = event['params']['CIDR']
        elif 'CIDR-export' in event['params']:
            cidr = fetch_stack_export(event['params']['CIDR-export'])

        (subnet, size) = parse_cidr(cidr)

        return {
            "requestId" : event["requestId"]
        ,   "status" : "success"
        ,   "fragment": {
            "CIDR" : cidr,
            "subnet" : subnet,
            "netmask"  : compute_netmask(size)
            }
        }
    except Exception as e:
        return {
            "requestId" : event["requestId"]
        ,   "status" : "failure"
        ,   "fragment": {}
        ,   "errorMessage" : str(e)            
        }
