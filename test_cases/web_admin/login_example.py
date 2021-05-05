from stubs import Stubs
from custom import basic_custom_actions as bca

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from webdriver_manager.chrome import ChromeDriverManager

from web_admin_modules.web_wrapper import call


class TestCase:
    def __init__(self, report_id):
        # Case parameters setup
        self.case_id = bca.create_event('[WEB ADMIN] Login Example', report_id)

        # ChromeDriver
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        # WaitDriver
        self.wait = WebDriverWait(self.driver, 10)

        # Reference data
        self.start_url = Stubs.custom_config['web_admin_url']
        self.user = Stubs.custom_config['web_admin_login']
        self.password = Stubs.custom_config['web_admin_password']

    # Login method
    def login(self):
        self.driver.get(self.start_url)
        # Wait until find login and password inputs
        login_input = self.wait.until(EC.presence_of_element_located((By.ID, 'mat-input-0')))
        password_input = self.wait.until(EC.presence_of_element_located((By.ID, 'mat-input-1')))
        # Send login and password into inputs
        login_input.send_keys(self.user)
        password_input.send_keys(self.password, Keys.ENTER)

        # Wait until find navigation menu
        self.wait.until(EC.presence_of_element_located((By.ID, 'app-sidenav-menu')))

    # Main method. Must call in demo.py by 'login_example.TestCase(report_id).execute()' command
    def execute(self):
        call(self.login, self.case_id)
        self.driver.close()


if __name__ == '__main__':
    pass
