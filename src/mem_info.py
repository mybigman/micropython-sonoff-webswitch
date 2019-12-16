import gc

import micropython
import uio
import uos


class DupTerm:
    def __enter__(self):
        self.stream = uio.StringIO()
        uos.dupterm(self.stream, 0)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        uos.dupterm(None, 0)
        gc.collect()

    def getvalue(self):
        return self.stream.getvalue()


def mem_info():
    with DupTerm() as d:
        micropython.mem_info(1)
    mem_info = d.getvalue()
    del d
    gc.collect()
    return mem_info
