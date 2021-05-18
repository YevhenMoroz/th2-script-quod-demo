from custom import basic_custom_actions as bca
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from custom.verifier import Verifier
from web_admin_modules.web_wrapper import call, login, logout, check_exists_by_xpath, check_is_clickable

from time import sleep


class TestCase:
    def __init__(self, report_id):
        self.case_id = bca.create_event('QAP-761', report_id)

        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.wait = WebDriverWait(self.driver, 5)

    def create_listing_group(self):
        data = 'TEST'

        reference_data_tab = self.driver.find_element_by_xpath('//*[text()="Reference Data"]')
        reference_data_tab.click()

        listing_groups_tab = reference_data_tab.find_element_by_xpath('//*[text()="ListingGroups"]')
        listing_groups_tab.click()

        new_button = self.wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="actions-header"]//*[text()="New"]')))
        new_button.click()

        wizard_xpath = '//wizard'
        wizard = self.wait.until(EC.presence_of_element_located((By.XPATH, wizard_xpath)))

        clean_btn = wizard.find_element_by_xpath('//*[text()="Clean"]/parent::button')
        summary_btn = wizard.find_element_by_xpath('//*[text()="Go to Summary"]/parent::button')
        previous_btn = wizard.find_element_by_xpath('//*[text()="Previous"]/parent::button')
        next_btn = wizard.find_element_by_xpath('//*[text()="Next"]/parent::button')

        verifier = Verifier(self.case_id)
        verifier.set_event_name('Check available buttons on wizard tab')
        verifier.compare_values('Clean button', 'True', str(check_is_clickable(clean_btn)))
        verifier.compare_values('Summary button', 'False', str(check_is_clickable(summary_btn)))
        verifier.compare_values('Previous button', 'False', str(check_is_clickable(previous_btn)))
        verifier.compare_values('Next button', 'True', str(check_is_clickable(next_btn)))
        verifier.verify()

        name_input = wizard.find_element_by_xpath('//input[@placeholder="Name"]')
        name_input.click()
        name_input.send_keys(data)
        sub_venue_input = wizard.find_element_by_xpath('//input[@placeholder="SubVenue"]')
        sub_venue_input.click()
        sub_venue_input.send_keys(data, Keys.ARROW_DOWN, Keys.ENTER)

        summary_btn.click()

        symbol = self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                                 '//*[text()="Symbol"]/following-sibling::span'))).text
        sub_venue = self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                                    '//*[text()="SubVenue"]' +
                                                                    '/following-sibling::span'))).text

        verifier = Verifier(self.case_id)
        verifier.set_event_name('Check required fields on Summary tab')
        verifier.compare_values('Name', data, symbol)
        verifier.compare_values('SubVenue', data, sub_venue)
        verifier.verify()

        submit_button = wizard.find_element_by_xpath('//*[text()="Submit"]')
        submit_button.click()

        self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                        '//*[text()="Listing Group created with success"]')))
        self.wait.until_not(EC.presence_of_element_located((By.XPATH, wizard_xpath)))

        verifier = Verifier(self.case_id)
        verifier.set_event_name('Check displayed of wizard')
        verifier.compare_values('Wizard displayed', 'False', str(check_exists_by_xpath(self.driver, wizard_xpath)))
        verifier.verify()

    # Main method. Must call in demo.py by 'QAP_761.TestCase(report_id).execute()' command
    def execute(self):
        call(login, self.case_id, self.driver, self.wait)
        call(self.create_listing_group, self.case_id)
        call(logout, self.case_id, self.wait)
        self.driver.close()


if __name__ == '__main__':
    pass
