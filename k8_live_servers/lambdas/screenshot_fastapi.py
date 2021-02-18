from osbot_aws.Dependencies import load_dependencies

def run(event, context=None):
    load_dependencies('fastapi,mangum,nest-asyncio')          # These are the additional dependencies required on top of dependencies for browser
    from k8_live_servers.fastapi.app.main import handler
    return handler(event, context)
