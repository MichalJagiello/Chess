import contextlib
import traceback


@contextlib.contextmanager
def critical_part():
    """
    Use it if an exception within the `with` block could cause that
    the state of the program becomes inconsistent.
    """
    try:
        yield
    except Exception:
        raise AssertionError(
            'This should not happen: an exception occurred in a '
            'critical code section!\n{}'.format(traceback.format_exc()))
