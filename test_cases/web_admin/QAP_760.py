from custom import basic_custom_actions as bca
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from custom.verifier import Verifier
from web_admin_modules.web_wrapper import call, login, logout


class TestCase:
    def __init__(self, report_id):
        self.case_id = bca.create_event('QAP-760', report_id)

        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.wait = WebDriverWait(self.driver, 5)

    def get_precondition(self):
        data = 'TEST'

        reference_data_tab = self.driver.find_element_by_xpath('//*[text()="Reference Data"]')
        reference_data_tab.click()

        sub_venues_tab = reference_data_tab.find_element_by_xpath('//*[text()="SubVenues"]')
        sub_venues_tab.click()

        new_button = self.wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="actions-header"]//*[text()="New"]')))
        new_button.click()

        name_input = self.wait.until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Name"]')))
        name_input.click()
        name_input.send_keys(data)
        venue_input = self.wait.until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Venue"]')))
        venue_input.click()
        venue_input.send_keys(data, Keys.ARROW_DOWN, Keys.ENTER)

        summary_tab = self.driver.find_element_by_xpath('//*[@id="header-wizard-tab-3"]')
        summary_tab.click()

        submit_button = self.driver.find_element_by_xpath('//*[text()="Submit"]')
        submit_button.click()

        self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                        '//*[text()="Sub Venue created with success"]')))

    def remove_precondition(self):
        row = self.driver.find_element_by_xpath('//*[text()="TEST"]')
        row.click()

        delete_btn = self.driver.find_element_by_xpath('//datatable-body-row[contains(@class, "active")]' +
                                                       '//*[@mattooltip="Delete"]')
        delete_btn.click()
        confirm_btn = self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                                      '//*[text()="OK"]')))
        confirm_btn.click()

        self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                        '//*[text()="SubVenue has been deleted with success"]')))

    def edit_sub_venue(self):
        data = 'edited test text'

        row = self.driver.find_element_by_xpath('//*[text()="TEST"]')
        row.click()

        edit_btn = self.driver.find_element_by_xpath('//datatable-body-row[contains(@class, "active")]' +
                                                     '//*[@mattooltip="Edit"]')
        edit_btn.click()

        name_input = self.wait.until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Name"]')))
        name_input.clear()
        name_input.click()
        name_input.send_keys(data)
        news_symbol_input = self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                                            '//input[@placeholder="News Symbol"]')))
        news_symbol_input.click()
        news_symbol_input.send_keys(data)

        summary_tab = self.driver.find_element_by_xpath('//*[@id="header-wizard-tab-3"]')
        summary_tab.click()

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

        submit_button = self.driver.find_element_by_xpath('//*[text()="Submit"]')
        submit_button.click()

        self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[text()="Sub Venue modified with success"]')))

        row = self.driver.find_element_by_xpath('//*[text()="TEST"]')
        row.click()

        edited_values_count = str(len(self.driver
                                      .find_elements_by_xpath('//datatable-body-row[contains(@class, "active")]' +
                                                              f'//span[text()="{data}"]')))

        verifier = Verifier(self.case_id)
        verifier.set_event_name('Check edited fields count on grid')
        verifier.compare_values('Count', '2', edited_values_count)
        verifier.verify()

    # Main method. Must call in demo.py by 'QAP_758.TestCase(report_id).execute()' command
    def execute(self):
        call(login, self.case_id, self.driver, self.wait)
        call(self.get_precondition, self.case_id)
        call(self.edit_sub_venue, self.case_id)
        call(self.remove_precondition, self.case_id)
        call(logout, self.case_id, self.wait)
        self.driver.close()


if __name__ == '__main__':
    pass
