"""
Test custom Django management commands
"""

from unittest.mock import (
    patch,
)  # in order to mock behavior (of the db to simulate the db returns value or not

from psycopg2 import (
    OperationalError as Psycopg2Error,
)  # Handle: the possibilities of the errors that we might get when we try and connect to the database before the database is ready.

from django.core.management import (
    call_command,
)  # which is a helper function provided by Django that allows us to simulate or to actually call a command by the name. -> this allows us to actually call the command that we're testing.

from django.db.utils import (
    OperationalError,
)  # which is another exception that may get thrown by the database depending on what stage of the start up process it is.

from django.test import (
    SimpleTestCase,
)  # which is the base test course that we're going to use for testing out our unit test or creating our unit test.

# we use a simple test case because we are testing behavior that the database is not available and therefore we do not need migrations and things like that to be applied to the test database because we're just actually simulating behavior of that database.


# mock that behavior by doing that patch (test db) --> do it for the all different test methods
@patch("core.management.commands.wait_for_db.Command.check")
# this is basically the command that we're going to be mocking.
# we've provided the path here which is core the management or commands.
# It allows us to check the DB's status


# because we've added Patch here, it's going to add a new argument to each of the calls that we make to our test methods.
# we need to define the parameter as `patched_check`
class CommandTests(SimpleTestCase):
    """Test commands."""

    def test_wait_for_db_ready(self, patch_check):
        # the patched_check object, the magic mock object that is replaced or that replaces check by patch, is going to be passed in as an argument.
        # then we can use that to customize the behavior.
        """Test waiting for database if it is ready."""
        # this just says when we call check or when check is called inside our command, inside our test case
        patch_check.return_value = True

        # this will call `wait_for_db`: this will actually execute the code inside wait_for_db.
        call_command("wait_for_db")

        # check that this check method has been called so it will be patched
        # this basically ensures that the marked value here, the mocked object (core.management.commands.wait_for_db.Command.check), which is the check method inside our command, is called with these parameters.
        patch_check.assert_called_once_with(database=["default"])

    @patch(
        "time.sleep"
    )  # the more you add on top, the more it adds to the end (as arguments) here.
    def test_wait_for_db_delay(self, patch_sleep, patch_check):
        """Test waiting for database when getting OperationalError."""

        # this is how the mocking works when you want to raise an exception
        # it means we want it to actually raise some exceptions that would be raised if the database wasn't ready.
        # the way that you make it raise an exception instead of actually pretend to get value is you use the `side_effect`
        # the side_effect allows you to pass in various different items that get handled differently depending on that type
        # so if we pass in an exception, then the mocking library knows that it should raise that exception.
        # If we pass in a boolean, then it will return the boolean value.
        # The first we raise 2 times the Psycopg2Error, next things we raise 3 times the OperationalError
        # In that case, Django raises the operational error from Django's exceptions
        # After 5 times, we call the db successfully
        patch_check.side_effect = [Psycopg2Error] * 2 + [OperationalError] * 3 + [True]

        call_command("wait_for_db")

        self.assertEqual(
            patch_check.call_count, 6
        )  # after call w Exception error 5 times (side_effect)

        # to make sure that it is called with the correct values.
        patch_check.assert_called_once_with(database=["default"])

        # the last thing we need to do for this test case is we need to mark the sleep method.
