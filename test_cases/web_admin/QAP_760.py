from custom import basic_custom_actions as bca
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from custom.verifier import Verifier
from web_admin_modules.web_wrapper import call, filter_grid_by_field


class TestCase:
    def __init__(self, report_id, web_driver, wait_driver):
        self.case_id = bca.create_event('QAP-760', report_id)

        self.driver = web_driver
        self.wait = wait_driver

        self.test_input = 'TestVenues'
        self.test_data = {
            'reference_data_tab_xpath': '//*[@title="Reference Data"]',
            'sub_venues_tab_xpath': '//*[@href="#/pages/sub-venues/view"]',
            'new_btn_xpath': '//nb-card-header//*[contains(text(),"SubVenues")]/following-sibling::button',
            'name_input_id': 'subVenueName',
            'venue_input_id': 'venue',
            'save_btn_xpath': '//*[text()="Save Changes"]',
            'sub_venue_created_event_xpath': '//*[text()="SubVenue changes saved"]',
            'row_container_xpath': '//*[@ref="eCenterContainer"]',
            'name_filter_input_xpath': '//*[@ref="eFloatingFilterText"]',
            'actions_btn_xpath': '//*[@data-name="more-vertical"]',
            'edit_btn_xpath': '//*[@nbtooltip="Edit"]/*'
        }

    # Precondition
    def add_sub_venue(self):
        # Navigate to SubVenues tab
        reference_data_tab = self.driver.find_element_by_xpath(self.test_data['reference_data_tab_xpath'])
        reference_data_tab.click()
        sub_venues_tab = self.driver.find_element_by_xpath(self.test_data['sub_venues_tab_xpath'])
        sub_venues_tab.click()

        # Press New button
        new_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, self.test_data['new_btn_xpath'])))
        new_btn.click()

        # Fill required fields
        name_input = self.wait.until(EC.presence_of_element_located((By.ID, self.test_data['name_input_id'])))
        name_input.send_keys(self.test_input)
        venue_input = self.wait.until(EC.presence_of_element_located((By.ID, self.test_data['venue_input_id'])))
        venue_input.send_keys(self.test_input, Keys.ARROW_DOWN, Keys.ENTER)

        # Submit
        save_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, self.test_data['save_btn_xpath'])))
        save_btn.click()
        self.wait.until(EC.presence_of_element_located((By.XPATH, self.test_data['sub_venue_created_event_xpath'])))

    def edit_sub_venue(self):
        new_test_input = self.test_input + '_NEW'

        # Filter rows
        row_container = self.driver.find_element_by_xpath(self.test_data['row_container_xpath'])
        name_filter_input = self.driver.find_element_by_xpath(self.test_data['name_filter_input_xpath'])
        filter_grid_by_field(row_container, name_filter_input, self.test_input)

        # Edit row
        actions_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, self.test_data['actions_btn_xpath'])))
        actions_btn.click()
        edit_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, self.test_data['edit_btn_xpath'])))
        edit_btn.click()

        # Change required fields
        name_input = self.wait.until(EC.presence_of_element_located((By.ID, self.test_data['name_input_id'])))
        name_input.send_keys(Keys.CONTROL + 'a', Keys.DELETE)
        name_input.send_keys(new_test_input)
        venue_input = self.wait.until(EC.presence_of_element_located((By.ID, self.test_data['venue_input_id'])))
        venue_input.send_keys(Keys.CONTROL + 'a', Keys.DELETE)
        venue_input.send_keys(new_test_input, Keys.ARROW_DOWN, Keys.ENTER)

        # Submit
        save_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, self.test_data['save_btn_xpath'])))
        save_btn.click()
        self.wait.until(EC.presence_of_element_located((By.XPATH, self.test_data['sub_venue_created_event_xpath'])))

        # Check changes in grid
        row_container = self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                                        self.test_data['row_container_xpath'])))
        name_filter_input = self.driver.find_element_by_xpath(self.test_data['name_filter_input_xpath'])
        edit_row_count = filter_grid_by_field(row_container, name_filter_input, new_test_input)
        verifier = Verifier(self.case_id)
        verifier.set_event_name('Check edit row count on grid')
        verifier.compare_values('Count', '1', str(edit_row_count))
        verifier.verify()

    # Main method. Must call in demo.py by 'QAP_760.TestCase(report_id).execute()' command
    def execute(self):
        call(self.add_sub_venue, self.case_id, 'Add SubVenue (Precondition)')
        call(self.edit_sub_venue, self.case_id, 'Edit SubVenue')


if __name__ == '__main__':
    pass
