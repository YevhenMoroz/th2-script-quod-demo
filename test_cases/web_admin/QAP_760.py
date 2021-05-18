from custom import basic_custom_actions as bca
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from custom.verifier import Verifier
from web_admin_modules.web_wrapper import call, login, logout, check_exists_by_xpath


class TestCase:
    def __init__(self, report_id):
        self.case_id = bca.create_event('QAP-760', report_id)

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

    def edit_sub_venue(self):
        data = 'edited test text'

        # Find TEST row
        row = self.driver.find_element_by_xpath('//*[text()="TEST"]')
        row.click()
        edit_btn = self.driver.find_element_by_xpath('//datatable-body-row[contains(@class, "active")]' +
                                                     '//*[@mattooltip="Edit"]')
        edit_btn.click()

        # Wait wizard
        wizard_xpath = '//wizard'
        wizard = self.wait.until(EC.presence_of_element_located((By.XPATH, wizard_xpath)))

        # Edit some fields
        name_input = wizard.find_element_by_xpath('//input[@placeholder="Name"]')
        name_input.clear()
        name_input.click()
        name_input.send_keys(data)
        news_symbol_input = wizard.find_element_by_xpath('//input[@placeholder="News Symbol"]')
        news_symbol_input.click()
        news_symbol_input.send_keys(data)

        # Go to Summary tab
        summary_tab = self.driver.find_element_by_xpath('//*[@id="header-wizard-tab-3"]')
        summary_tab.click()

        # Check edited fields
        name = self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                               '//*[text()="Name"]/following-sibling::span'))).text
        news_symbol = self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                                      '//*[text()="News Symbol"]' +
                                                                      '/following-sibling::span'))).text
        verifier = Verifier(self.case_id)
        verifier.set_event_name('Check fields on Summary tab')
        verifier.compare_values('Name', data, name)
        verifier.compare_values('News Symbol', data, news_symbol)
        verifier.verify()

        # Submit
        submit_button = self.driver.find_element_by_xpath('//*[text()="Submit"]')
        submit_button.click()
        self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[text()="Sub Venue modified with success"]')))

        # Check wizard
        self.wait.until_not(EC.presence_of_element_located((By.XPATH, wizard_xpath)))
        verifier = Verifier(self.case_id)
        verifier.set_event_name('Check displayed of wizard')
        verifier.compare_values('Wizard displayed', 'False', str(check_exists_by_xpath(self.driver, '//wizard')))
        verifier.verify()

        # Find edited row
        row = self.driver.find_element_by_xpath('//*[text()="TEST"]')
        row.click()

        # Check edited fields on grid
        edited_values_count = len(self.driver
                                  .find_elements_by_xpath('//datatable-body-row[contains(@class, "active")]' +
                                                          f'//span[text()="{data}"]'))
        verifier = Verifier(self.case_id)
        verifier.set_event_name('Check edited fields count on grid')
        verifier.compare_values('Count', '2', str(edited_values_count))
        verifier.verify()

    # Main method. Must call in demo.py by 'QAP_760.TestCase(report_id).execute()' command
    def execute(self):
        call(login, self.case_id, self.driver, self.wait)
        call(self.get_precondition, self.case_id)
        call(self.edit_sub_venue, self.case_id)
        call(logout, self.case_id, self.wait)
        self.driver.close()


if __name__ == '__main__':
    pass
