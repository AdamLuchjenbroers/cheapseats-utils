
def macro_handler(event, context):
    print(event)
    print(context)
 
    return {
        "requestId" : event["requestId"]
    ,   "status" : "success"
    ,   "fragment": event['fragment']
    }   