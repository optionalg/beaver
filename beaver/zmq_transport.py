# -*- coding: utf-8 -*-
import zmq

import beaver.transport


class ZmqTransport(beaver.transport.Transport):

    def __init__(self, beaver_config, file_config, logger=None):
        super(ZmqTransport, self).__init__(beaver_config, file_config, logger=logger)

        zeromq_address = beaver_config.get('zeromq_address')

        self._ctx = zmq.Context()
        if beaver_config.get('zeromq_pattern') == 'pub':
            self._pub = self._ctx.socket(zmq.PUB)
        else:
            self._pub = self._ctx.socket(zmq.PUSH)

        zeromq_hwm = beaver_config.get('zeromq_hwm')
        if zeromq_hwm:
            self._pub.hwm = zeromq_hwm

        if beaver_config.get('mode') == 'bind':
            self._pub.bind(zeromq_address)
        else:
            self._pub.connect(zeromq_address)

    def callback(self, filename, lines, **kwargs):
        timestamp = self.get_timestamp(**kwargs)

        for line in lines:
            self._pub.send(self.format(filename, timestamp, line))

    def interrupt(self):
        self._pub.close()
        self._ctx.term()

    def unhandled(self):
        return True
