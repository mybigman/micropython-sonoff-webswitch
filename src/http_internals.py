import gc
import sys

import machine
import uos


async def get_show(server, reader, writer, querystring, body):
    from template import render
    from rtc import get_dict_from_rtc

    uname = uos.uname()

    await server.send_html_page(
        writer,
        filename='webswitch.html',
        content_iterator=render(
            filename='http_internals.html',
            context={
                'power_timer': server.power_timer,
                'wifi': server.watchdog.wifi,
                'watchdog': server.watchdog,
                'rtc_memory': repr(get_dict_from_rtc()),

                'sysname': uname.sysname,
                'nodename': uname.nodename,
                'id': ':'.join(['%02x' % char for char in reversed(machine.unique_id())]),
                'machine': uname.machine,
                'release': uname.release,
                'mpy_version': uname.version,

                'sys_modules': ', '.join(sorted(sys.modules.keys())),
                'minimal_modules': ', '.join(server.minimal_modules)
            },
            content_iterator=None
        ),
    )


async def get_clear(server, reader, writer, querystring, body):
    from http_utils import send_redirect
    from rtc import clear_rtc_dict
    clear_rtc_dict()
    server.message = 'RTC RAM cleared'
    await send_redirect(writer, url='/internals/show/')  # reload internal page


async def get_reset(server, reader, writer, querystring, body):
    from http_utils import send_redirect
    server.message = 'Reset device... Please reload the page in a few seconds.'

    await send_redirect(writer, url='/internals/show/')  # reload internal page

    from reset import ResetDevice
    ResetDevice(reason='Reset via web page').schedule(period=15000)


async def get_mem_info(server, reader, writer, querystring, body):
    from mem_info import mem_info
    mem_info = mem_info()
    del sys.modules['mem_info']
    gc.collect()

    from template import render
    await server.send_html_page(
        writer,
        filename='webswitch.html',
        content_iterator=render(
            filename='http_internals_mem_info.html',
            context={
                'mem_info': mem_info
            },
            content_iterator=None
        ),
    )
