import io

import pytest

from dmpy import DistributedMake


class TestDmpyAdd(object):
    def test_raises_on_adding_same_target_twice(self):
        # given
        dm = DistributedMake()
        dm.add('hi', 'world', 'echo')

        # when
        with pytest.raises(Exception) as excinfo:
            dm.add('hi', 'world', 'echo')
        assert 'Tried to add target twice' in str(excinfo.value)
