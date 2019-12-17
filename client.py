from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop
from tornado.httpclient import AsyncHTTPClient, HTTPClient
from tornado import httpclient
import json
import datetime

SERVER_URL = 'http://localhost:8080'
ADD_DATA_URL = SERVER_URL + '/api/data'
HISTORY_URL = SERVER_URL + '/api/history'

######## Request  #############

class AddData(RequestHandler):
    
    def post(self):
        '''
        introduce la fecha y envia a el servidor
        '''

        data = self.request.body
        data_dict = json.loads(data)
        date_now = datetime.datetime.now().isoformat()
        data_dict['fecha'] = date_now
        data = json.dumps(data_dict)
        http_client = AsyncHTTPClient()

        post_req = httpclient.HTTPRequest(ADD_DATA_URL,
                                        body = data,
                                        method="POST")
        response = http_client.fetch(post_req)
        self.write({'respuesta' : 'OK'})


class History(RequestHandler):

    def get(self):
        http_client = AsyncHTTPClient()

        resp = http_client.fetch(HISTORY_URL)
        self.write(resp.body)




###############################

def main():
    urls = [
        ("/api/data", AddData),
        ("/api/history", History),
    ]

    return Application(urls, debug = True)


#################################


if __name__ == '__main__':
    app = main()
    app.listen(8888)
    IOLoop.instance().start()