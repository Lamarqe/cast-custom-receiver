import os
from bottle import default_app, route, response, request, abort, static_file

forward_map = {}

@route('/')
def static_entrypage():
  return static_file('index.htm', root=os.path.dirname(__file__))


@route('/storeforwardurl', method='POST')
def store():
  global forward_map
  localForwardURL = request.forms.getunicode('localForwardURL')
  client_ip = request.environ.get('HTTP_X_FORWARDED_FOR') or request.environ.get('REMOTE_ADDR')
  if localForwardURL == '':
      if client_ip in forward_map.keys():
        del forward_map[client_ip]
        return [client_ip + ' will not be forwarded anymore.']
      else:
        return ['Nothing to do.']
  else:
    forward_map[client_ip] = localForwardURL
    return [client_ip + ' will be forwarded to ' + localForwardURL]


@route('/getforwardurl')
def get_url():
  global forward_map
  client_ip = request.environ.get('HTTP_X_FORWARDED_FOR') or request.environ.get('REMOTE_ADDR')
  if client_ip in forward_map.keys():
    forwardtarget = forward_map[client_ip]
  else:
    forwardtarget = ""

  return [forwardtarget]


@route('/forward')
def redirect():
  global forward_map
  client_ip = request.environ.get('HTTP_X_FORWARDED_FOR') or request.environ.get('REMOTE_ADDR')

  if client_ip in forward_map.keys():
    response.status = 302
    response.set_header('Location', forward_map[client_ip])
  else:
    abort(404)


application = default_app()


