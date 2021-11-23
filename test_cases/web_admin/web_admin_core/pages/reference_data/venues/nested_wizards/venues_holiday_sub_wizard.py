from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.pages.reference_data.venues.venues_constants import VenuesConstants
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class VenuesHolidaySubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_plus_button(self):
        self.find_by_xpath(VenuesConstants.HOLIDAYS_TAB_PLUS_BUTTON_XPATH).click()

    def click_on_checkmark(self):
        self.find_by_xpath(VenuesConstants.HOLIDAYS_TAB_CHECKMARK_BUTTON_XPATH).click()

    def click_on_close(self):
        self.find_by_xpath(VenuesConstants.HOLIDAYS_TAB_CLOSE_BUTTON_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(VenuesConstants.HOLIDAYS_TAB_EDIT_BUTTON_XPATH).click()

    def click_on_delete(self):
        self.find_by_xpath(VenuesConstants.HOLIDAYS_TAB_DELETE_BUTTON_XPATH).click()

    def set_holiday_name(self, value):
        self.set_text_by_xpath(VenuesConstants.HOLIDAYS_TAB_HOLIDAY_NAME_XPATH, value)

    def get_holiday_name(self):
        self.get_text_by_xpath(VenuesConstants.HOLIDAYS_TAB_HOLIDAY_NAME_XPATH)

    def set_holiday_name_filter(self, value):
        self.set_text_by_xpath(VenuesConstants.HOLIDAYS_TAB_HOLIDAY_NAME_FILTER_XPATH, value)

    # --------------------------- holiday calendars
    def click_on_plus_button_at_holiday_calendars(self):
        self.find_by_xpath(VenuesConstants.HOLIDAYS_CALENDAR_TAB_PLUS_BUTTON_XPATH).click()

    def click_on_checkmark_at_holiday_calendars(self):
        self.find_by_xpath(VenuesConstants.HOLIDAYS_CALENDAR_TAB_CHECKMARK_BUTTON_XPATH).click()

    def click_on_close_at_holiday_calendars(self):
        self.find_by_xpath(VenuesConstants.HOLIDAYS_CALENDAR_TAB_CLOSE_BUTTON_XPATH).click()

    def click_on_edit_at_holiday_calendars(self):
        self.find_by_xpath(VenuesConstants.HOLIDAYS_CALENDAR_TAB_EDIT_BUTTON_XPATH).click()

    def click_on_delete_at_holiday_calendars(self):
        self.find_by_xpath(VenuesConstants.HOLIDAYS_CALENDAR_TAB_DELETE_BUTTON_XPATH).click()

    def set_date(self, value):
        self.set_text_by_xpath(VenuesConstants.HOLIDAYS_CALENDAR_TAB_DATE_XPATH, value)

    def get_date(self):
        return self.get_text_by_xpath(VenuesConstants.HOLIDAYS_CALENDAR_TAB_DATE_XPATH)

    def set_date_filter(self, value):
        self.set_text_by_xpath(VenuesConstants.HOLIDAYS_CALENDAR_TAB_DATE_FILTER_XPATH, value)

    def set_description(self, value):
        self.set_text_by_xpath(VenuesConstants.HOLIDAYS_CALENDAR_TAB_DESCRIPTION_XPATH, value)

    def get_description(self):
        return self.get_text_by_xpath(VenuesConstants.HOLIDAYS_CALENDAR_TAB_DESCRIPTION_XPATH)

    def set_description_filter(self, value):
        self.set_text_by_xpath(VenuesConstants.HOLIDAYS_CALENDAR_TAB_DESCRIPTION_FILTER_XPATH, value)
