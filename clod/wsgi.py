from clod.loaders import find_responder

class Request(object):
    def __init__(self, env):
        self.env = env

    def __getattr__(self, key):
        return self.env[key]

def application(env, start_response):
    request = Request(env)
    responder = find_responder(request)
    response = responder.handle()

    start_response(response.status, response.headers)
    return [str(response.output)]

