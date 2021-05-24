from custom import basic_custom_actions as bca
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from web_admin_modules.web_wrapper import call, filter_grid_by_field, verify_row_count
import web_admin_modules.locator_xpath as get_xpath
import web_admin_modules.locator_constants as LC


# TODO: начни с меня! вынеси весь текст в константы, но не забудь проконсультироваться по кнопкам и полям!

class TestCase:
    def __init__(self, report_id, web_driver, wait_driver):
        self.case_id = bca.create_event('QAP-758', report_id)
        self.driver = web_driver
        self.wait = wait_driver
        self.test_input = 'TestVenues'

    # Precondition
    def add_sub_venue(self):
        # Navigate to SubVenues tab
        reference_data_tab = self.driver.find_element_by_xpath(
            get_xpath.sidebar_menu_tab_by_title(LC.SidebarTabsTitle.REFERENCE_DATA))
        reference_data_tab.click()
        sub_venues_tab = reference_data_tab.find_element_by_xpath(
            get_xpath.sidebar_menu_sub_tab_by_title(LC.SidebarTabsTitle.SUB_VENUES))
        sub_venues_tab.click()

        # Press New button
        new_btn = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH,
             get_xpath.card_header_by_text(LC.SidebarTabsTitle.SUB_VENUES)
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

        # Check changes in grid
        added_row_count = filter_grid_by_field(self.driver, 'Name', self.test_input)
        verify_row_count(self.case_id, 'Check add, row count on grid', 1, added_row_count)

    def delete_sub_venue(self):
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

        # Check changes in grid
        edited_row_count = filter_grid_by_field(self.driver, 'Name', self.test_input)
        verify_row_count(self.case_id, 'Check delete, row count on grid', 0, edited_row_count)

    # Main method
    # Must call in web_demo.py by QAP_758.TestCase(report_id, chrome_driver, wait_driver).execute() command
    def execute(self):
        call(self.add_sub_venue, self.case_id, 'Add SubVenue (Precondition)')
        # call(self.delete_sub_venue, self.case_id, 'Delete SubVenue')


if __name__ == '__main__':
    pass
