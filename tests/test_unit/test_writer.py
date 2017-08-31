from io import StringIO

from dmpy import DMBuilder


class TestDmpyWriter(object):
    def test_puts_something_into_the_stringio_writer(self):
        # given
        writer = StringIO()
        dm = DMBuilder()
        dm.add('output', 'input', 'echo hi world')

        # when
        dm.write_to_filehandle(writer)

        # then
        assert writer.getvalue() != ''
