from io import StringIO

from dmpy import DistributedMake


class TestDmpyWriter(object):
    def test_puts_something_into_the_stringio_writer(self):
        # given
        writer = StringIO()
        dm = DistributedMake(writer=writer)
        dm.add('output', 'input', 'echo hi world')

        # when
        dm.finalize()

        # then
        assert writer.getvalue() != ''
