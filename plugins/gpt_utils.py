import platform
import re

def join_url(url, *paths):
    if platform.python_version()[:3] == '3.7':
        from urllib.parse import urljoin
        for path in paths:
            url = urljoin(url, path)
        return url
    for path in paths:
        url = re.sub(r'/?$', re.sub(r'^/?', '/', path), url)
    return url
