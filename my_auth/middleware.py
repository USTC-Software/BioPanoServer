__author__ = 'feiyicheng'

import json


class CookieToTokenMiddleware(object):
    def process_request(self, request):
        if 'token' in request.REQUEST:
            request.COOKIES['sessionid'] = request.REQUEST['token']
            del request.REQUEST['token']
        else:
            pass

    def process_response(self, response, *args, **kwargs):
        try:
            dic = json.loads(response.content)
        except Exception:
            pass
        else:
            if 'sessionid' in response.cookies.keys():
                dic['token'] = response.cookies['sessionid']
                response.content = json.dumps(dic)
            else:
                pass