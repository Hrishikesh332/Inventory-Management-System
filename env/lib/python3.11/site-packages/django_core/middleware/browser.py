from __future__ import unicode_literals


class IECompatibleMiddleware(object):
    """ Configures how windows internet explorer renders the webpage by setting the
    user agenet compatability mode to edge.

    Internet Explorer uses a browser and document mode to determine how to
    render a web page. Without the X-UA-Compatible header, Internet Explorer will attempt
    to pick the rendering mode based a number of different criteria. This may result in a
    web page running in IE8 or IE9 rendering as if it were in IE7.
    Setting the X-UA-Compatible header ensures that Internet Explorer always renders
    the page as the latest version of the browser it is being viewed in.

    See: http://www.alistapart.com/articles/beyonddoctype
    See: http://msdn.microsoft.com/en-us/library/cc288325%28v=vs.85%29.aspx

    """
    def process_response(self, request, response):
        if 'text/html' in response.get('Content-Type', ''):
            response['X-UA-Compatible'] = 'IE=edge'

        return response
