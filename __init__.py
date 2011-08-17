# coding=utf-8

from libs.httplib2 import Http

class VavagException(Exception):
    status = None
    msg = None
    def __init__(self, status, msg):
        super(self.__class__, self).__init__()
        self.status = status
        self.msg = msg

class VavagRequest(Http):
    headers = { 'User-Agent' : 'Georemindme:0.1' }
    URL_get_info_url = 'http://vavag.com/api/%(version)s/%(method)s/%(login)s/%(apikey)s/get_info_url?url='
    URL_get_pack = 'http://vavag.com/api/%(version)s/%(method)s/%(login)s/%(apikey)s/get_pack?packhash='
    URL_set_pack = 'http://vavag.com/api/%(version)s/%(method)s/%(login)s/%(apikey)s/set_pack?packchain='
    
    def __init__(self, login, api_key, version='v2', method = 'json', **kwargs):
        super(self.__class__, self).__init__(timeout=20, **kwargs)
        self.version = version
        self.api_key = api_key
        self.login = login
        self.method = method

    def _encode(self, url):
        from base64 import urlsafe_b64encode
        return url
        return urlsafe_b64encode(url)
    
    def get_info(self, url):
        request_url = self.URL_get_info_url % {
                                       'version': self.version,
                                       'method': self.method,
                                       'login': self.login,
                                       'apikey': self.api_key
                                       }
        request_url = request_url + self._encode(url)
        print request_url
        return self._do_request(request_url)
    
    def get_pack(self, packHash):
        request_url = self.URL_get_pack % {
                                       'version': self.version,
                                       'method': self.method,
                                       'login': self.login,
                                       'apikey': self.api_key
                                       }
        request_url = request_url + packHash
        return self._do_request(request_url)
    
    def set_pack(self, pack):
        if type(pack) != 'list':
            pack = list(pack)
        request_url = self.URL_set_pack % {
                                       'version': self.version,
                                       'method': self.method,
                                       'login': self.login,
                                       'apikey': self.api_key
                                       }
        
        pack = '|'.join([self._encode(url) for url in pack])
        request_url = request_url + pack
        return self._do_request(request_url)
    
    def _do_request(self, url, method='GET', body=None):
        """
            Realiza una peticion por GET a la direccion recibida
            
                :param url: direccion url a donde hacer la peticion
                :type url: string
                
                :returns: diccionario con el resultado
                :raises: :class:`GPAPIError`
        """
        response, content = self.request(url, method=method, body=body, headers=self.headers)
        if response['status'] != 200:
            raise VavagException(status=response['status'], msg='ERROR IN REQUEST')
        from django.utils import simplejson
        json = simplejson.loads(content)
        if json['status'] == 200:
            return json['results']
        return json['statusMsg']
        raise VavagException(status=json['status'], msg=json['statusMsg'])
