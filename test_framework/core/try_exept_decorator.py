import logging
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
                logger.exception(
                    f"Exception raised in {test_id}, func {decorated_function.__name__} raised exception: {str(e)}")
                bca.create_event(f'Fail test event on the step - {decorated_function.__name__.upper()}',
                                 status='FAILED',
                                 parent_id=args[0].__dict__['test_id'])
            finally:
                pass
        return improved_function
    return get_function
