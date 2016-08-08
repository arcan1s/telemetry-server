import logging
from telemetryserver.telemetryserverhandler import TelemetryServerHandler
# python 2<>3 compatibility
try:
    import configparser
    from http.server import HTTPServer
except ImportError:
    import ConfigParser as configparser
    from BaseHTTPServer import HTTPServer


class TelemetryServer(object):

    def __init__(self, *args, **kwargs):
        '''
        class init method
        :param config: path to configuration file
        '''
        self.__settings = self.read_settings(
            kwargs.get('config', '/etc/telemetry-server.cfg'))

    @staticmethod
    def read_settings(cfg_path):
        '''
        read settings from file
        :param cfg_path: path to configuration file
        return: settings dictionary
        '''
        config = configparser.SafeConfigParser()
        config.read(cfg_path)
        # global settings
        settings = {
            'address': config.get('server', 'address'),
            'port': config.getint('server', 'port'),
            'request_path': config.get('server', 'request_path')
        }
        # databases
        settings['databases'] = dict()
        for section in config.sections():
            if not section.startswith('group:'):
                continue
            logging.info('Group {} found'.format(section))
            settings['databases'][section.replace('group:', '')] = {
                'filename': config.get(section, 'database_filename')
            }
        return settings

    def run(self):
        '''
        run server
        '''
        # init vars
        TelemetryServerHandler.databases = self.__settings['databases']
        TelemetryServerHandler.request_path = self.__settings['request_path']
        # start server
        location = (self.__settings['address'], self.__settings['port'])
        httpd = HTTPServer(location, TelemetryServerHandler)
        logging.info('Server started at {}'.format(location))
        httpd.serve_forever()
