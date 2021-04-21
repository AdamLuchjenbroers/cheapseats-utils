
def cidr_to_range(cidr):
    return cidr.split('/')[0]

def cidr_to_netmask(cidr_txt):
    cidr = int(cidr_txt.split('/')[1])
    mask = (0xffffffff >> (32 - cidr)) << (32 - cidr)
    return (str( (0xff000000 & mask) >> 24)   + '.' +
            str( (0x00ff0000 & mask) >> 16)   + '.' +
            str( (0x0000ff00 & mask) >> 8)    + '.' +
            str( (0x000000ff & mask)))

def macro_handler(event, context):
    print(event)
    print(context)
 
    return {
        "requestId" : event["requestId"]
    ,   "status" : "success"
    ,   "fragment": event['fragment']
    }   