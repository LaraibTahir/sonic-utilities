import click
import config.main as config
import operator
import os
import pytest
import sys

from click.testing import CliRunner
from utilities_common.db import Db

test_path = os.path.dirname(os.path.abspath(__file__))
modules_path = os.path.dirname(test_path)
scripts_path = os.path.join(modules_path, "scripts")
sys.path.insert(0, modules_path)

@pytest.fixture(scope='module')
def ctx(scope='module'):
    db = Db()
    obj = {'config_db':db.cfgdb, 'namespace': ''}
    yield obj

class TestConfigFabric(object):
    @classmethod
    def setup_class(cls):
        print("SETUP")
        os.environ["PATH"] += os.pathsep + scripts_path
        os.environ["UTILITIES_UNIT_TESTING"] = "1"

    def basic_check(self, command_name, para_list, ctx):
        # This function issues command of "config fabric xxxx",
        # and returns the result of the command.
        runner = CliRunner()
        result = runner.invoke(config.config.commands["fabric"].commands[command_name], para_list, obj = ctx)
        print(result.output)
        return result

    def test_config_isolation(self, ctx):
        # Issue command "config fabric port isolate 0",
        # check if the result is expected.
        result = self.basic_check("port", ["isolate", "0"], ctx)
        expect_result = 0
        assert operator.eq(result.exit_code, expect_result)

        # Issue command "config fabric port isolate 1",
        # check if the result has the error message as port 1 is not in use.
        result = self.basic_check("port", ["isolate", "1"], ctx)
        assert "Port 1 is not in use" in result.output

        # Issue command "config fabric port unisolate 0",
        # check if the result is expected.
        result = self.basic_check("port", ["unisolate", "0"], ctx)
        expect_result = 0
        assert operator.eq(result.exit_code, expect_result)

        # Issue command "config fabric port unisolate 1",
        # check if the result has the error message as port 1 is not in use.
        result = self.basic_check("port", ["unisolate", "1"], ctx)
        assert "Port 1 is not in use" in result.output

    def test_config_fabric_monitor_threshold(self, ctx):
        # Issue command "config fabric port monitor error threshold <#> <#>"
        # with an out of range number, check if the result has the error message.
        result = self.basic_check("port", ["monitor", "error", "threshold", "1", "2000"], ctx)
        assert "rxCells must be in range 10000...100000000" in result.output

        result = self.basic_check("port", ["monitor", "error", "threshold", "10000", "20000"], ctx)
        assert "crcCells must be in range 1...1000" in result.output

        # Issue command "config fabric port monitor error threshold <#> <#>"
        # with a number in the range, check if the result is expected.
        result = self.basic_check("port", ["monitor", "error", "threshold", "1", "20000"], ctx)
        expect_result = 0
        assert operator.eq(result.exit_code, expect_result)

        # Issue command "config fabric port monitor poll threshold isolation <#>"
        # with an out of range number, check if the result has the error message.
        result = self.basic_check("port", ["monitor", "poll", "threshold", "isolation", "15"], ctx)
        assert "pollCount must be in range 1...10" in result.output

        # Issue command "config fabric port monitor poll threshold isolation <#>"
        # with a number in the range, check if the result is expected.
        result = self.basic_check("port", ["monitor", "poll", "threshold", "isolation", "3"], ctx)
        expect_result = 0
        assert operator.eq(result.exit_code, expect_result)

        # Issue command "config fabric port monitor poll threshold recovery <#>"
        # with an out of range number, check if the result has the error message.
        result = self.basic_check("port", ["monitor", "poll", "threshold", "recovery", "15"], ctx)
        assert "pollCount must be in range 1...10" in result.output

        # Issue command "config fabric port monitor poll threshold recovery <#>"
        # with a number in the range, check if the result is expected.
        result = self.basic_check("port", ["monitor", "poll", "threshold", "recovery", "8"], ctx)
        expect_result = 0
        assert operator.eq(result.exit_code, expect_result)
