import contextlib
import traceback


@contextlib.contextmanager
def critical_part():
    """
    Use it if any exception within the `with` block would mean that
    the state of the program is inconsistent.
    """
    try:
        yield
    except Exception:
        raise AssertionError(
            'This should not happen: an exception occurred in a '
            'critical code section!\n{}'.format(traceback.format_exc()))
