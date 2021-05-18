from custom import basic_custom_actions as bca
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from web_admin_modules.web_wrapper import call, login, logout


class TestCase:
    def __init__(self, report_id):
        self.case_id = bca.create_event('QAP-758', report_id)

        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.wait = WebDriverWait(self.driver, 5)

    def get_precondition(self):
        data = 'TEST'

        # Navigate to SubVenues tab
        reference_data_tab = self.driver.find_element_by_xpath('//*[text()="Reference Data"]')
        reference_data_tab.click()
        sub_venues_tab = reference_data_tab.find_element_by_xpath('//*[text()="SubVenues"]')
        sub_venues_tab.click()

        # Press New button
        new_button = self.wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="actions-header"]//*[text()="New"]')))
        new_button.click()

        # Fill required fields
        name_input = self.wait.until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Name"]')))
        name_input.click()
        name_input.send_keys(data)
        venue_input = self.wait.until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Venue"]')))
        venue_input.click()
        venue_input.send_keys(data, Keys.ARROW_DOWN, Keys.ENTER)

        # Go to Summary tab
        summary_tab = self.driver.find_element_by_xpath('//*[@id="header-wizard-tab-3"]')
        summary_tab.click()

        # Submit
        submit_button = self.driver.find_element_by_xpath('//*[text()="Submit"]')
        submit_button.click()
        self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                        '//*[text()="Sub Venue created with success"]')))

    def delete_sub_venue(self):
        # Find TEST row
        row = self.driver.find_element_by_xpath('//*[text()="TEST"]')
        row.click()

        # Delete tow
        delete_btn = self.driver.find_element_by_xpath('//datatable-body-row[contains(@class, "active")]' +
                                                       '//*[@mattooltip="Delete"]')
        delete_btn.click()

        # Confirm delete
        confirm_btn = self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                                      '//*[text()="OK"]')))
        confirm_btn.click()
        self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                        '//*[text()="SubVenue has been deleted with success"]')))

    # Main method. Must call in demo.py by 'QAP_758.TestCase(report_id).execute()' command
    def execute(self):
        call(login, self.case_id, self.driver, self.wait)
        call(self.get_precondition, self.case_id)
        call(self.delete_sub_venue, self.case_id)
        call(logout, self.case_id, self.wait)
        self.driver.close()


if __name__ == '__main__':
    pass
