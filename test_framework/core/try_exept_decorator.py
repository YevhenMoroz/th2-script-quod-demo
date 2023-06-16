import logging
import traceback
from functools import wraps
from custom import basic_custom_actions as bca

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


def try_except(test_id):
    def get_function(decorated_function):
        @wraps(decorated_function)
        def improved_function(*args, **kwargs):
            try:
                return decorated_function(*args, **kwargs)
            except Exception as e:
                error_message = f"Exception raised in {test_id}, func {decorated_function.__name__.upper()} raised exception - {str(e)}"
                error_traceback = traceback.format_exc()
                full_error_message = f"{error_message}\n\n{error_traceback}"
                logger.exception(error_message)
                bca.create_event(f"Fail test event on the step - {decorated_function.__name__.upper()}",
                                 status="FAILED",
                                 parent_id=args[0].__dict__["test_id"],
                                 body=full_error_message)


            finally:
                pass

        return improved_function

    return get_function
