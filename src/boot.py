print('boot.py')   # noqa isort:skip
import gc

import esp
import micropython
import utime

for no in range(2, 0, -1):
    print('%i boot.py wait...' % no)
    utime.sleep(1)

esp.osdebug(None)  # turn off vendor O/S debugging messages
esp.sleep_type(esp.SLEEP_NONE)  # Don't go into sleep mode

micropython.alloc_emergency_exception_buf(128)

gc.enable()

# https://forum.micropython.org/viewtopic.php?f=2&t=7345&p=42365#p42365
gc.threshold(gc.mem_alloc() + gc.mem_free())

print('boot.py END')
