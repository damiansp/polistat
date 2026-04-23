import requests
from urllib.parse import urljoin


API_VERSION = 'v3'
ROOT_URL = 'https://api.congress.gov/'


class CDGClient:
    'Client to interface with congress.gov'
    def __init__(
            self,
            api_key: str,
            api_version: str = API_VERSION,
            response_format: str = 'json',
            raise_on_error: bool = True):
        self.base_url = urljoin(ROOT_URL, api_version) + '/'
        self._session = requests.Session()
        # don't use url params even if offered. use headers
        self._session.params = {'format': response_format}
        self._session.headers.update({'x-api-key': api_key})
        if raise_on_error:
            self._session.hooks = {
                'response': lambda r, *args, **kwargs: r.raise_for_status()}

    def __getattr__(self, method_name: str):
        'Find the session method dynamically and cache for later'
        method = _MethodWrapper(self, method_name)
        self.__dict__[method_name] = method
        return method


class _MethodWrapper:
    'Wrap request method to facilitate queries. Supports requests signature'
    def __init__(self, parent, http_method):
        self._parent = parent
        self._method = getattr(parent._session, http_method)

    def __call__(self, endpoint, *args, **kwargs):  # full sig passed here
        response = self._method(
            urljoin(self._parent.base_url, endpoint), *args, **kwargs)
        # unpack
        is_json = (
            response
            .headers
            .get('content-type', '')
            .startswith('application/json'))
        if is_json:
            return response.json(), response.status_code
        return response.content, response.status_code
        
        
