import collections, jinja2, os

# TODO: move to a permanent location
class NotFoundResponse(object):
    status = '404 NOT FOUND'
    headers = []
    output = ''

class LoaderStrategy(object):
    def __init__(self):
        self.strategies = collections.deque()

    def add_strategy(self, cls_or_obj):
        self.strategies.appendleft(cls_or_obj)

    def handle(self):
        for strategy in self.strategies:
            try:
                strategy.handle()
                return strategy
            except Exception:
                # TODO: be more intelligent about responding here
                pass
        return NotFoundResponse()

class TemplateLoader(object):
    def __init__(self, path, request):
        #import pdb;pdb.set_trace()
        paths = [
            os.path.join(os.getcwd(), 'templates'),
            os.getcwd(),
        ]
        loader = jinja2.FileSystemLoader(paths)
        self.jinja = jinja2.Environment(loader=loader)
        self.path = path
        self.request = request

    def handle(self):
        self.status = "200 OK"
        self.headers = []
        try:
            self.output = self.jinja.get_template(self.path).render()
        except jinja2.TemplateNotFound:
            self.status = '404 NOT FOUND'
            self.output = ''
        return self


def find_responder(request):
    requested = request.PATH_INFO[1:]
    if requested == '':
        requested = 'index'

    # TODO: allow configuring responders
    responders = LoaderStrategy()
    responders.add_strategy(TemplateLoader(requested, request))
    responders.add_strategy(TemplateLoader(requested + '.html', request))
    return responders

