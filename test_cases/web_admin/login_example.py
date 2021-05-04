from time import sleep

# TODO: fix Stubs import
# from stubs import Stubs

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from webdriver_manager.chrome import ChromeDriverManager


class TestCase:
    def __init__(self):

        # ChromeDriver
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        # WaitDriver
        self.wait = WebDriverWait(self.driver, 10)

        # preconditions
        # self.start_url = Stubs.custom_config['web_admin_url']
        # self.user = Stubs.custom_config['web_admin_login']
        # self.password = Stubs.custom_config['web_admin_password']

        # TODO: fix Stubs import
        self.start_url = 'http://10.0.22.40:3180/quodadmin/qakharkiv3/'
        self.user = 'adm03'
        self.password = 'adm03'

    # login method
    def login(self):
        # open start url
        self.driver.get(self.start_url)
        # wait until find login and password inputs
        login_input = self.wait.until(EC.presence_of_element_located((By.ID, 'mat-input-0')))
        password_input = self.wait.until(EC.presence_of_element_located((By.ID, 'mat-input-1')))
        # send login and password into inputs
        login_input.send_keys(self.user)
        password_input.send_keys(self.password, Keys.ENTER)
        sleep(60)

    def execute(self):
        self.login()
        self.driver.close()


if __name__ == '__main__':
    TestCase().execute()
