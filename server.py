from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop
import json
import dateutil.parser
listado = []
fields = ['tipo', 'fecha','volumen']

########      API      #############

class AddData(RequestHandler):
    
    def post(self):
        json_dict = json.loads(self.request.body)
        validation = all(elem in json_dict.keys() for elem in fields)

        if validation:
            json_dict['fecha'] = dateutil.parser.parse(json_dict['fecha'])
            listado.append(json_dict)
            self.write({'response' : 'OK'})
        else:
            self.write({'response' : 'ERROR'})


class History(RequestHandler):
    def get(self):
        json = json.dumps(listado)
        self.write(json)




############## MAIN ##########

def main():
    urls = [
        ("/api/data", AddData),
        ("/api/history", History),
    ]

    return Application(urls, debug = True)


#################################


if __name__ == '__main__':
    app = main()
    app.listen(8080)
    IOLoop.instance().start()