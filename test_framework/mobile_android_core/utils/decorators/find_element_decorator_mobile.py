from functools import wraps


def wait_for_element(func):
    @wraps(func)
    def wrapper(self, key, *args, **kwargs):
        """
            Decorator that waits element presence on the screen
            :param key: valueKey set by DEV team on their own application
        """
        # Future implementation: Make timeout configurable / Make finder configurable (by_value_key, by_text, etc)
        self.appium_driver.get_driver().execute_script('flutter:waitFor', self.finder.by_value_key(key), 5000)
        return func(self, key, *args, **kwargs)
    return wrapper
