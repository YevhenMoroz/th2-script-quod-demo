from custom import basic_custom_actions as bca
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from web_admin_modules.web_wrapper import call, login, logout


class TestCase:
    def __init__(self, report_id):
        # Case parameters setup
        self.case_id = bca.create_event('[WEB ADMIN] Login-Logout Example', report_id)

        # ChromeDriver
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        # WaitDriver
        self.wait = WebDriverWait(self.driver, 10)

    # Example method
    def something_method(self):
        pass

    # Main method. Must call in demo.py by 'login_example.TestCase(report_id).execute()' command
    def execute(self):
        call(login, self.case_id, self.driver, self.wait)
        ...
        call(self.something_method, self.case_id)
        ...
        call(logout, self.case_id, self.wait)
        self.driver.close()


if __name__ == '__main__':
    pass
