from custom import basic_custom_actions as bca
from web_admin_modules.web_wrapper import call


class TestCase:
    def __init__(self, report_id, web_driver, wait_driver):
        # Case parameters setup
        self.case_id = bca.create_event('Login-Logout example test-case', report_id)

        # ChromeDriver
        self.driver = web_driver
        # WaitDriver
        self.wait = wait_driver

    # Example method with something logic
    def something_method(self):
        pass

    # Main method
    # Must call in web_demo.py by login_logout_example.TestCase(report_id, chrome_driver, wait_driver).execute() command
    def execute(self):
        ...
        call(self.something_method, self.case_id, 'Something method name')
        ...


if __name__ == '__main__':
    pass
