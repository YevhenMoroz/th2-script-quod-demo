from custom import basic_custom_actions as bca
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from web_admin_modules.web_wrapper import call, filter_grid_by_field
import web_admin_modules.locator_constants as get_xpath


class TestCase:
    def __init__(self, report_id, web_driver, wait_driver):
        self.case_id = bca.create_event('QAP-758', report_id)

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
            'delete_btn_xpath': '//*[@nbtooltip="Delete"]/*',
            'confirm_btn_xpath': '//*[text()="Ok"]',
            'sub_venue_deleted_event_xpath': f'//*[text()="SubVenue {self.test_input} Deleted"]',
        }

    # Precondition
    def add_sub_venue(self):
        # Navigate to SubVenues tab
        reference_data_tab = self.driver.find_element_by_xpath(get_xpath.sidebar_menu_tab_by_title('Reference Data'))
        reference_data_tab.click()
        sub_venues_tab = reference_data_tab.find_element_by_xpath(get_xpath.sidebar_menu_sub_tab_by_title('SubVenues'))
        sub_venues_tab.click()

        # Press New button
        new_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, get_xpath.card_header_by_text('SubVenues')
                                                              + get_xpath.button_by_text('New'))))
        new_btn.click()

        # Fill required fields
        name_input = self.wait.until(EC.presence_of_element_located((By.XPATH, get_xpath.input_by_text('Name *'))))
        name_input.send_keys(self.test_input)
        venue_input = self.wait.until(EC.presence_of_element_located((By.XPATH, get_xpath.input_by_text('Venue *'))))
        venue_input.send_keys(self.test_input, Keys.ARROW_DOWN, Keys.ENTER)

        # Submit
        save_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, get_xpath.button_by_text('Save Changes'))))
        save_btn.click()
        self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                        get_xpath.container_event_by_text('SubVenue changes saved'))))

    # Delete SubVenue
    def delete_sub_venue(self):
        # Filter rows
        filter_grid_by_field(self.driver, 'Name', self.test_input)

        # Delete row
        actions_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, get_xpath.actions_btn)))
        actions_btn.click()
        delete_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, get_xpath.action_by_tooltip('Delete'))))
        delete_btn.click()

        # Confirm delete
        confirm_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, get_xpath.button_by_text('Ok'))))
        confirm_btn.click()
        self.wait.until(EC.presence_of_element_located(
            (By.XPATH, get_xpath.container_event_by_text(f'SubVenue {self.test_input} Deleted'))))

    # Main method
    # Must call in web_demo.py by QAP_758.TestCase(report_id, chrome_driver, wait_driver).execute() command
    def execute(self):
        call(self.add_sub_venue, self.case_id, 'Add SubVenue (Precondition)')
        call(self.delete_sub_venue, self.case_id, 'Delete SubVenue')


if __name__ == '__main__':
    pass
