#################################################################################
# Copyright (c) 2016 Evgeniy Alekseev                                           #
#                                                                               #
# Permission is hereby granted, free of charge, to any person obtaining a copy  #
# of this software and associated documentation files (the "Software"), to deal #
# in the Software without restriction, including without limitation the rights  #
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell     #
# copies of the Software, and to permit persons to whom the Software is         #
# furnished to do so, subject to the following conditions:                      #
                                                                                #
# The above copyright notice and this permission notice shall be included in    #
# all copies or substantial portions of the Software.                           #
#################################################################################

import json
import logging
import os
# python 2<>3 compatibility
try:
    from http.server import BaseHTTPRequestHandler
except ImportError:
    from BaseHTTPServer import BaseHTTPRequestHandler


class TelemetryServerHandler(BaseHTTPRequestHandler):

    databases = dict()
    request_path = str()

    def __set_headers(self, code):
        '''
        set default headers
        :param code: code send
        '''
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

    def __write_all_data(self, data):
        '''
        write all data to files
        :param data: raw data from request
        '''
        # check types
        if isinstance(data, dict):
            data = [data]
        elif not isinstance(data, list):
            logging.error('Invalid payload {}'.format(data))
            return False
        # check data keys
        if any('api' not in single_data
               or 'type' not in single_data
               or 'metadata' not in single_data for single_data in data):
            logging.error('No required keys found in {}'.format(data))
            return False
        if any(single_data['type']
               not in self.databases for single_data in data):
            logging.error('Found unknown type in {}'.format(data))
            return False
        # work on request
        for single_data in data:
            filename = self.databases[single_data['type']]['filename'].format(
                **single_data, **self.databases[single_data['type']])
            self.__write_single_data(
                filename, json.dumps(single_data['metadata']))
        return True

    def __write_single_data(self, filename, data):
        '''
        write data to file
        :param filename: filename to write
        :param data: data to write
        '''
        # data error chech
        try:
            with open(filename, 'a+') as database:
                database.write(data)
                database.write(os.linesep)
        except:
            logging.error(
                'Could not write data {} to {}'.format(
                    data, filename), exc_info=True)

    def do_GET(self):
        '''
        GET request handler
        '''
        self.__set_headers(501)
        self.wfile.write(json.dumps({
            'message': 'not implemented'
        }).encode('utf8'))

    def do_HEAD(self):
        '''
        HEAD request handler
        '''
        self.__set_headers(200)

    def do_POST(self):
        '''
        POST request handler
        '''
        if self.path != self.request_path:
            logging.info('Unknown path {}'.format(self.path))
            return self.__set_headers(404)
        if self.headers.get('content-type') != 'application/json':
            logging.info('Invalid content type {}'.format(
                self.headers.get('content-type')))
            return self.__set_headers(415)
        # body
        try:
            post_body = self.rfile.read(
                int(self.headers.get('content-length', 0)))
            if self.__write_all_data(json.loads(post_body.decode('utf8'))):
                self.__set_headers(200)
                self.wfile.write(json.dumps({
                    'message': 'saved'
                }).encode('utf8'))
            else:
                self.__set_headers(400)
                self.wfile.write(json.dumps({
                    'message': 'invalid payload'
                }).encode('utf8'))
        except:
            logging.error('Could handle request', exc_info=True)
            self.__set_headers(500)

    def log_message(self, format, *args):
        '''
        override default method to use global logger
        :param format: format line
        '''
        logging.info('{} - - {}'.format(self.address_string(), format % args))
