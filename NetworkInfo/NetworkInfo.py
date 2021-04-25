import boto3
import jmespath

cfn = boto3.client('cloudformation')

def parse_cidr(cidr)
    (subnet, size) = cidr.split('/')

    return (subnet, int(size))

def compute_netmask(size):
    mask = (0xffffffff >> (32 - size)) << (32 - size)
    return (str( (0xff000000 & mask) >> 24)   + '.' +
            str( (0x00ff0000 & mask) >> 16)   + '.' +
            str( (0x0000ff00 & mask) >> 8)    + '.' +
            str( (0x000000ff & mask)))

def export_to_cidr(export_name):
    list = cfn.list_exports()
    
    data = jmespath.search('Exports[*].[Name, Value]', list)
    for row in data:
        if row[0] == export_name:
            return row[1]

def macro_handler(event, context):
    if 'CIDR' in event['params']: 
        cidr = event['params']['CIDR']
    elif 'CIDR-export' in event['params']:
        cidr = export_to_cidr(event['params']['CIDR-export'])

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