from __future__ import unicode_literals

import json
from urllib.request import urlopen


def get_json_api_contents(api_url):
    """
    Gets contents from a json api request and returns a json response with
    content values.

    If the api_url is not available, this method throws a URLError.
    """
    json_contents = urlopen(api_url).read()
    return json.loads(json_contents)
