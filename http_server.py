#!/usr/bin/python

import optparse
import SimpleHTTPServer
import SocketServer
import urlparse
import time
import random
import my_logging

logger = my_logging.get_logger('mup', _logger_file='mup_http_server.log')
URL = "http://10.64.41.155:8000"


class MyHttpHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    TYPE = ('sugg_only', 'sugg_link', 'action_required', 'action_taken',
            'attention_need', 'attention_need_max', 'problem_solved')
    STATUS = ('posted', 'action_taken', 'action_received', 'problem_solved',
              'action_not_received', 'problem_not_solved')
    IMAGE_TYPE = ('protected', 'information', 'exclamation', 'risk')

    current_index = 0

    def do_GET(self):
        logger.debug('receive a GET request')
        logger.debug('basic info >>>>>>>')
        client_info = self.get_client_basic_info()
        logger.debug(client_info)
        logger.debug('basic info <<<<<<<')
        time.sleep(3)
        self.send_response(200)
        self.end_headers()
        _type = self.TYPE[random.randint(0, len(self.TYPE) - 1)]
        logger.debug('type: ' + _type)
        self.wfile.write(self.create_new_notf(_type, True))
        # self.wfile.write(self.create_new_notf(_type, False))

    def do_POST(self):
        logger.debug('receive a POST request')
        logger.debug('basic info >>>>>>>')
        client_info = self.get_client_basic_info()
        logger.debug(client_info)
        logger.debug('basic info <<<<<<<')
        time.sleep(3)
        self.send_response(200)
        self.end_headers()

    def do_DELETE(self):
        logger.debug('receive a DELETE request')
        logger.debug('basic info >>>>>>>')
        client_info = self.get_client_basic_info()
        logger.debug(client_info)
        logger.debug('basic info <<<<<<<')
        time.sleep(3)
        self.send_response(200)
        self.end_headers()

    def get_client_basic_info(self):
        o = urlparse.urlparse(self.path)
        print 'o: ', o
        print 'params: ', urlparse.parse_qs(o.query)
        return {'client addr': self.client_address,
                'request path': self.path,
                'command': self.command,
                'client content': self.rfile.read(int(self.headers.getheader('content-length', 0)))}

    def create_new_notf(self, _type, flag):
        image_type = '"' + self.IMAGE_TYPE[random.randint(0, len(self.IMAGE_TYPE) - 1)] + '"'
        if _type in self.TYPE[0:3]:
            status = '"' + self.STATUS[0] + '"'
        elif _type in (self.TYPE[3], ):
            status = '"' + self.STATUS[random.randint(1, 2)] + '"'
        elif _type in self.TYPE[4:6]:
            status = '"' + self.STATUS[random.randint(4, 5)] + '"'
        elif _type in (self.TYPE[6], ):
            status = '"' + self.STATUS[3] + '"'

        if _type in (self.TYPE[0], self.TYPE[1], self.TYPE[3], self.TYPE[5], self.TYPE[6]):
            is_actionable = 'false'
        else:
            is_actionable = 'true'

        if _type in (self.TYPE[0], ):
            advice = '""'
        else:
            advice = '"Fake advice from Peace"'

        advice_link = URL

        return ('''{''' + '''"list":[''' if flag else '') + '''{"id": ''' + '"' + str(time.time()) + '", ' + '''"account_id": "12345",
            "device_id": "aabbccddee",
            "pid": "MSM1",
            "device_name": "Bob's HAL 9000",
            "type": "av_protection_disabled",
            "alert_text": "Your AV protection has been disabled. Click here to find out more.",
            "status": ''' + status + ''',
            "is_unread": true,
            "posted_time": 1428413964,
            "last_unread_time": ''' + str(int(round(time.time()))) + ''',
            "action_taken_time": 0,
            "action_tries": 0,
            "is_actionable": ''' + is_actionable + ''',
            "payload": {\"virus_name\": \"SLAMMER9X\"},
            "l10n": {
                "status_image": ''' + image_type + ''',
                "description": "Protection against viruses and spyware...etc.",
                "title": "Restart Required: Virus Cleanup",
                "more_description_link": "''' + URL + '", ' + '''"advice_title": "For your safety, this is our suggestion",
                "advice_description": ''' + advice + ''',
                "advice_link": "''' + advice_link + '''"}}''' + ('''], "unread":1, "total":123, "nextPageKey":"0"}''' if flag else '')


if __name__ == '__main__':
    parser = optparse.OptionParser('Usage: %prog [Options]')
    parser.add_option('-d', '--debug', action='store_true', dest='debug', default=False,
                      help='switch on debug mode for more detailed output')
    parser.add_option('-p', '--port', action='store', dest='port', default=8000,
                      help='set the server port')
    opt, args = parser.parse_args()

    if opt.debug:
        print 'opt: ', opt
        print 'args: ', args
    httpd = SocketServer.TCPServer(("", opt.port), MyHttpHandler)
    httpd.serve_forever()
