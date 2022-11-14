class LocationsConstants:
    LOCATIONS_PAGE_TITLE_XPATH = "//span[@class= 'entity-title left']//*[text()='Locations']"

    REFRESH_PAGE_BUTTON_XPATH = "//*[@data-name='refresh']"
    DOWNLOAD_PDF_BUTTON_XPATH = "//*[@data-name='download']"
    SAVE_CHANGES_BUTTON_XPATH = "//*[text()='Save Changes']"
    CLEAR_CHANGES_BUTTON_XPATH = "//*[text()='Clear Changes']"
    CLOSE_WIZARD_XPATH = "//*[@data-name='close']"
    OK_BUTTON_XPATH = '//*[normalize-space()="Ok" or normalize-space()="OK"]'
    NO_BUTTON_XPATH = '//*[normalize-space()="No"]'
    CANCEL_BUTTON_XPATH = '//*[text()="Cancel"]'
    REVERT_CHANGES_XPATH = "//*[text()='Revert Changes']"
    MORE_ACTIONS_XPATH = "//*[@row-index = '0']//*[@data-name = 'more-vertical']"
    EDIT_XPATH = "//*[@data-name = 'edit']"
    CLONE_XPATH = "//*[@data-name = 'copy']"
    DELETE_XPATH = "//*[@data-name = 'trash-2']"
    PIN_ROW_XPATH = "//*[@nbtooltip ='Click to Pin Row']"
    NEW_BUTTON_XPATH = '//*[text()="New"]'
    USER_ICON_AT_RIGHT_CORNER = "//*[@class='control-item icon-btn context-menu-host']"
    LOGOUT_BUTTON_XPATH = "//*[text()='Logout']"
    GO_BACK_BUTTON_XPATH = "//*[text()='Go Back']"
    ENABLE_DISABLE_BUTTON_XPATH = "//div[contains(@class, 'toggle')]"
    INCORRECT_OR_MISSING_VALUES_MESSAGE_XPATH = "//*[text()='Incorrect or missing values']"
    DISPLAYED_ENTITY_XPATH = "//*[text()='{}']"
    ZONES_NAME_COLUMN_XPATH = '//*[@col-id="zone.zoneName"][@tabindex="-1"]//span[@ref="eValue"]'
    LOCATIONS_NAME_COLUMN_XPATH = '//*[@tabindex="-1"][1]//span[@ref="eValue"]'
    DROP_DOWN_MENU_XPATH = '//*[@class="option-list"]//span'

    MAIN_PAGE_NAME_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[1]//input'
    MAIN_PAGE_ZONE_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[2]//input'
    MAIN_PAGE_ENABLED_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[3]//select'

    # Values tab
    VALUES_TAB_NAME_XPATH = '//*[@formcontrolname="locationName"]'

    # Assignments tab
    ASSIGNMENTS_TAB_ZONE_XPATH = '//*[@id="zone"]'
    ASSIGNMENTS_TAB_DESKS_XPATH = '//a[text()=" {} "]'
    ASSIGNMENTS_TAB_USERS_LINK_XPATH = '//a[text()=" {} "]'
    ASSIGNMENTS_TAB_ZONE_LINK_XPATH = '//a[text()=normalize-space(" {} ")]'
