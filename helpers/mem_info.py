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

    def getvalue(self):
        return self.stream.getvalue()


if __name__ == '__main__':
    with DupTerm() as d:
        micropython.mem_info(1)

    print(repr(d.getvalue()))
