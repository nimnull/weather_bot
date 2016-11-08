import asyncio
import re
import serial.aio


class Output(asyncio.Protocol):
    packet = None

    def __init__(self, loop, queue):
        self.loop = loop
        self.q = queue

    def connection_made(self, transport):
        self.transport = transport
        print('port opened')
        transport.serial.rts = False

    def data_received(self, data):
        try:
            data = data.decode()
            start = re.match('^(T.*)$', data)
            end = re.match('^(.*\d\n)$', data)
            if start and not end and self.packet is None:
                self.packet = start.group(0)
            elif end and not start and self.packet:
                self.packet += end.group(0)
                self.loop.create_task(self.q.put(self.packet.strip()))
                self.packet = None
        except UnicodeDecodeError as ex:
            print('data received %s' % data)
            print("Something went wrong: %s" % ex)

    def connection_lost(self, exc):
        print('port closed')
        self.loop.stop()

    def eof_received(self):
        self.transport.close()


async def create_serial_connection(loop, queue, protocol_factory, *args, **kwargs):
    ser = serial.serial_for_url(*args, **kwargs)
    protocol = protocol_factory(loop, queue)
    transport = serial.aio.SerialTransport(loop, protocol, ser)
    return (transport, protocol)

