from custom import basic_custom_actions as bca
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from web_admin_modules.web_wrapper import call, filter_grid_by_field, verify_row_count
import web_admin_modules.locator_xpath as get_xpath
import web_admin_modules.locator_constants as LC


class TestCase:
    def __init__(self, report_id, web_driver, wait_driver):
        self.case_id = bca.create_event('QAP_801', report_id)
        self.driver = web_driver
        self.wait = wait_driver
        self.test_input = 'TestCounterparts'

    def add_sub_counterpart(self, data):
        # Fill Sub counterpart required field
        add_btn = self.driver.find_element_by_xpath(
            get_xpath.plus_button_by_header_text(LC.CreationEntityHeaderText.SUB_COUNTERPARTS))
        add_btn.click()

        name_input = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, get_xpath.input_by_text(LC.InputText.NAME_REQ, LC.CreationEntityHeaderText.SUB_COUNTERPARTS))))
        name_input.send_keys(data)

        party_id_input = self.driver.find_element_by_xpath(
            get_xpath.input_by_text(LC.InputText.PARTY_ID_REQ, LC.CreationEntityHeaderText.SUB_COUNTERPARTS))
        party_id_input.send_keys(data)

        ext_id_client_input = self.driver.find_element_by_xpath(
            get_xpath.input_by_text(LC.InputText.EXT_ID_CLIENT_REQ, LC.CreationEntityHeaderText.SUB_COUNTERPARTS))
        ext_id_client_input.send_keys(data)

        party_sub_id_type_input = self.driver.find_element_by_xpath(
            get_xpath.input_by_text(LC.InputText.PARTY_SUB_ID_TYPE_REQ, LC.CreationEntityHeaderText.SUB_COUNTERPARTS))
        party_sub_id_type_input.send_keys(Keys.ARROW_DOWN, Keys.ENTER)

        apply_btn = self.driver.find_element_by_xpath(
            get_xpath.creation_action_by_header_text(LC.CreationEntityHeaderText.SUB_COUNTERPARTS,
                                                     LC.CreationEntityActionClass.APPLY))
        apply_btn.click()

    def add_party_role(self, data):
        # Fill Party Role required field
        add_btn = self.driver.find_element_by_xpath(
            get_xpath.plus_button_by_header_text(LC.CreationEntityHeaderText.PARTY_ROLES))
        add_btn.click()

        party_id_source_input = self.wait.until(EC.presence_of_element_located((By.XPATH, get_xpath.input_by_text(
            LC.InputText.PARTY_ID_SOURCE_REQ, LC.CreationEntityHeaderText.PARTY_ROLES))))
        party_id_source_input.send_keys(Keys.ARROW_DOWN, Keys.ENTER)

        venue_counterpart_id_input = self.driver.find_element_by_xpath(
            get_xpath.input_by_text(LC.InputText.VENUE_COUNTERPART_ID_REQ, LC.CreationEntityHeaderText.PARTY_ROLES))
        venue_counterpart_id_input.send_keys(data)

        party_role_input = self.driver.find_element_by_xpath(
            get_xpath.input_by_text(LC.InputText.PARTY_ROLE_REQ, LC.CreationEntityHeaderText.PARTY_ROLES))
        party_role_input.send_keys(Keys.ARROW_DOWN, Keys.ENTER)

        ext_id_client_input = self.driver.find_element_by_xpath(
            get_xpath.input_by_text(LC.InputText.EXT_ID_CLIENT_REQ, LC.CreationEntityHeaderText.PARTY_ROLES))
        ext_id_client_input.send_keys(data)

        party_role_qualifier_input = self.driver.find_element_by_xpath(
            get_xpath.input_by_text(LC.InputText.PARTY_ROLE_QUALIFIER_REQ, LC.CreationEntityHeaderText.PARTY_ROLES))
        party_role_qualifier_input.send_keys(Keys.ARROW_DOWN, Keys.ENTER)

        venue_input = self.driver.find_element_by_xpath(
            get_xpath.input_by_text(LC.InputText.VENUE_REQ, LC.CreationEntityHeaderText.PARTY_ROLES))
        venue_input.send_keys(Keys.ARROW_DOWN, Keys.ENTER)

        apply_btn = self.driver.find_element_by_xpath(
            get_xpath.creation_action_by_header_text(LC.CreationEntityHeaderText.PARTY_ROLES,
                                                     LC.CreationEntityActionClass.APPLY))
        apply_btn.click()

    def delete_entity(self, entity_name):
        delete_btn = self.driver.find_element_by_xpath(
            get_xpath.creation_action_by_header_text(entity_name,
                                                     LC.CreationEntityActionClass.DELETE))
        delete_btn.click()

    # Precondition
    def add_counterpart(self):
        # Navigate to Counterparts tab
        others_tab = self.driver.find_element_by_xpath(get_xpath.sidebar_menu_tab_by_title(LC.SidebarTabTitle.OTHERS))
        others_tab.click()
        counterparts_tab = others_tab.find_element_by_xpath(
            get_xpath.sidebar_menu_sub_tab_by_title(LC.SidebarTabTitle.COUNTERPARTS))
        counterparts_tab.click()

        # Press New button
        new_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, get_xpath.card_header_by_text(
            LC.SidebarTabTitle.COUNTERPARTS) + get_xpath.button_by_text(LC.ButtonText.NEW))))
        new_btn.click()

        # Fill Values required field
        name_input = self.wait.until(
            EC.presence_of_element_located((By.XPATH, get_xpath.input_by_text(LC.InputText.NAME_REQ))))
        name_input.send_keys(self.test_input)

        # Add Sub counterpart and Party role
        self.add_sub_counterpart(self.test_input)
        self.add_party_role(self.test_input)

        # Submit
        save_btn = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, get_xpath.button_by_text(LC.ButtonText.SAVE_CHANGES))))
        save_btn.click()
        self.wait.until(EC.presence_of_element_located(
            (By.XPATH, get_xpath.container_event_by_text(LC.EventText.COUNTERPART_CHANGES_SUCCESS))))

        # Check changes in grid
        added_row_count = filter_grid_by_field(self.driver, LC.FilterFieldName.NAME, self.test_input)
        verify_row_count(self.case_id, 'Check add, row count on grid', 1, added_row_count)

    def edit_counterpart(self):
        new_test_input = self.test_input + '_NEW'

        # Edit row
        actions_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, get_xpath.actions_btn)))
        actions_btn.click()
        edit_btn = self.wait.until(
            EC.presence_of_element_located((By.XPATH, get_xpath.action_by_tooltip(LC.TooltipAction.EDIT))))
        edit_btn.click()

        # Change Counterpart name
        name_input = self.wait.until(
            EC.presence_of_element_located((By.XPATH, get_xpath.input_by_text(LC.InputText.NAME_REQ))))
        name_input.send_keys(Keys.CONTROL + 'a', Keys.DELETE)
        name_input.send_keys(new_test_input)

        # Remove Sub counterpart
        self.delete_entity(LC.CreationEntityHeaderText.SUB_COUNTERPARTS)

        # Create new Sub counterpart
        self.add_sub_counterpart(new_test_input)

        # Remove Party role
        self.delete_entity(LC.CreationEntityHeaderText.PARTY_ROLES)

        # Create new Party role
        self.add_party_role(new_test_input)

        # Submit
        save_btn = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, get_xpath.button_by_text(LC.ButtonText.SAVE_CHANGES))))
        save_btn.click()
        self.wait.until(EC.presence_of_element_located(
            (By.XPATH, get_xpath.container_event_by_text(LC.EventText.COUNTERPART_CHANGES_SUCCESS))))

        # Check changes in grid
        edited_row_count = filter_grid_by_field(self.driver, LC.FilterFieldName.NAME, new_test_input)
        verify_row_count(self.case_id, 'Check edit, row count on grid', 1, edited_row_count)

    # Main method. Must call in demo.py by 'QAP_801.TestCase(report_id).execute()' command
    def execute(self):
        call(self.add_counterpart, self.case_id, 'Add Counterparts (Precondition)')
        call(self.edit_counterpart, self.case_id, 'Edit Counterparts')


if __name__ == '__main__':
    pass
