from custom import basic_custom_actions as bca
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from ExactPro_examples.web_admin_modules.web_wrapper import call, filter_grid_by_field, verify_row_count
import ExactPro_examples.web_admin_modules.locator_xpath as get_xpath
import ExactPro_examples.web_admin_modules.locator_constants as LC


class TestCase:
    def __init__(self, report_id, web_driver, wait_driver):
        self.case_id = bca.create_event('QAP_T4031', report_id)
        self.driver = web_driver
        self.wait = wait_driver
        self.test_input = 'TestVenues'

    # Precondition
    def add_sub_venue(self):
        # Navigate to SubVenues tab
        reference_data_tab = self.driver.find_element_by_xpath(
            get_xpath.sidebar_menu_tab_by_title(LC.SidebarTabTitle.REFERENCE_DATA))
        reference_data_tab.click()
        sub_venues_tab = reference_data_tab.find_element_by_xpath(
            get_xpath.sidebar_menu_sub_tab_by_title(LC.SidebarTabTitle.SUB_VENUES))
        sub_venues_tab.click()

        # Press New button
        new_btn = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, get_xpath.card_header_by_text(LC.SidebarTabTitle.SUB_VENUES) + get_xpath.button_by_text(
                LC.ButtonText.NEW))))
        new_btn.click()

        # Fill required fields
        name_input = self.wait.until(
            EC.presence_of_element_located((By.XPATH, get_xpath.input_by_text(LC.InputText.NAME_REQ))))
        name_input.send_keys(self.test_input)
        venue_input = self.wait.until(
            EC.presence_of_element_located((By.XPATH, get_xpath.input_by_text(LC.InputText.VENUE_REQ))))
        venue_input.send_keys(self.test_input, Keys.ARROW_DOWN, Keys.ENTER)

        # Submit
        save_btn = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, get_xpath.button_by_text(LC.ButtonText.SAVE_CHANGES))))
        save_btn.click()
        self.wait.until(EC.presence_of_element_located(
            (By.XPATH, get_xpath.container_event_by_text(LC.EventText.SUB_VENUE_CHANGES_SUCCESS))))

        # Check changes in grid
        added_row_count = filter_grid_by_field(self.driver, LC.FilterFieldName.NAME, self.test_input)
        verify_row_count(self.case_id, 'Check add, row count on grid', 1, added_row_count)

    def edit_sub_venue(self):
        new_test_input = self.test_input + '_NEW'

        # Edit row
        actions_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, get_xpath.actions_btn)))
        actions_btn.click()
        edit_btn = self.wait.until(
            EC.presence_of_element_located((By.XPATH, get_xpath.action_by_tooltip(LC.TooltipAction.EDIT))))
        edit_btn.click()

        # Change required fields
        name_input = self.wait.until(
            EC.presence_of_element_located((By.XPATH, get_xpath.input_by_text(LC.InputText.NAME_REQ))))
        name_input.send_keys(Keys.CONTROL + 'a', Keys.DELETE)
        name_input.send_keys(new_test_input)
        venue_input = self.wait.until(
            EC.presence_of_element_located((By.XPATH, get_xpath.input_by_text(LC.InputText.VENUE_REQ))))
        venue_input.send_keys(Keys.CONTROL + 'a', Keys.DELETE)
        venue_input.send_keys(new_test_input, Keys.ARROW_DOWN, Keys.ENTER)

        # Submit
        save_btn = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, get_xpath.button_by_text(LC.ButtonText.SAVE_CHANGES))))
        save_btn.click()
        self.wait.until(EC.presence_of_element_located(
            (By.XPATH, get_xpath.container_event_by_text(LC.EventText.SUB_VENUE_CHANGES_SUCCESS))))

        # Check changes in grid
        edited_row_count = filter_grid_by_field(self.driver, LC.FilterFieldName.NAME, new_test_input)
        verify_row_count(self.case_id, 'Check edit, row count on grid', 1, edited_row_count)

    # Main method. Must call in demo.py by 'QAP_T4031.TestCase(report_id).execute()' command
    def execute(self):
        call(self.add_sub_venue, self.case_id, 'Add SubVenue (Precondition)')
        call(self.edit_sub_venue, self.case_id, 'Edit SubVenue')


if __name__ == '__main__':
    pass
