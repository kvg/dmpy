from io import StringIO

from dmpy import DMBuilder
from dmpy.testing.makefile_parser import *


class TestDmpyWriter(object):
    def test_sets_pipefail_option(self):
        # given
        writer = StringIO()
        dm = DMBuilder()
        dm.add('output', 'input', 'echo $HI')

        # when
        dm.write_to_filehandle(writer)

        # then
        variables = extract_variables_from_makefile(writer.getvalue().split("\n"))

        assert "pipefail" in variables["SHELL"]

    def test_puts_something_into_the_stringio_writer(self):
        # given
        writer = StringIO()
        dm = DMBuilder()
        dm.add('output', 'input', 'echo hi world')

        # when
        dm.write_to_filehandle(writer)

        # then
        assert writer.getvalue() != ''

    def test_inserts_test_in_recipe(self):
        writer = StringIO()
        dm = DMBuilder()
        dm.add('output', 'input', 'echo hi world')

        # when
        dm.write_to_filehandle(writer)

        # then
        rules = extract_rules_from_makefile(writer.getvalue().split("\n"))
        assert rules[0].recipe[0].startswith("@test ")

    def test_escapes_dollar_signs(self):
        # given
        writer = StringIO()
        dm = DMBuilder()
        dm.add('output', 'input', 'echo $HI')

        # when
        dm.write_to_filehandle(writer)

        # then
        rules = extract_rules_from_makefile(writer.getvalue().split("\n"))
        assert rules[0].recipe[1] == 'echo $$HI'

    def test_changes_shell(self):
        # given
        dm = DMBuilder()
        dm.shell = "bla"
        writer = StringIO()

        # when
        dm.write_to_filehandle(writer)

        # then
        assert writer.getvalue().split("\n")[0].endswith("bla")
