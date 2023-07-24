class DesksConstants:
    DESKS_PAGE_TITLE_XPATH = "//*[@class='entity-title left'][normalize-space()='Desks']"
    NEW_BUTTON_XPATH = '//button[normalize-space()="New"]'
    REFRESH_BUTTON_XPATH = '//*[@data-name="refresh"]'
    MORE_ACTIONS_XPATH = "//*[@row-index = '0']//*[@data-name = 'more-vertical']"
    EDIT_AT_MORE_ACTIONS_XPATH = '//*[@data-name="edit"]'
    CLONE_AT_MORE_ACTIONS_XPATH = '//*[@data-name="copy"]'
    DELETE_AT_MORE_ACTIONS_XPATH = '//*[@data-name="trash-2"]'
    CANCEL_BUTTON_XPATH = '//*[normalize-space()="Cancel"]'
    CLOSE_WIZARD_XPATH = "//*[@data-name='close']"
    OK_BUTTON_XPATH = '//*[text()="Ok" or text()="OK"]'
    NO_BUTTON_XPATH = '//*[normalize-space()="No"]'
    INCORRECT_OR_MISSING_VALUES_MESSAGE_XPATH = "//*[text()='Incorrect or missing values']"
    ENABLE_DISABLE_BUTTON_XPATH = '//div[contains(@class, "toggle")]'
    DISPLAYED_DESK_XPATH = '//*[text()="{}"]'
    LOCATIONS_COLUMN_XPATH = '//*[@col-id="location.locationName"][@tabindex="-1"]//span[@ref="eValue"]'
    DESKS_NAME_COLUMN_XPATH = '//*[@tabindex="-1"][1]//span[@ref="eValue"]'
    DROP_DOWN_MENU_XPATH = '//*[@class="option-list"]//span'
    CTM_BIC_AT_MAIN_PAGE = '//*[@col-id="BIC"]//*[@class="ag-group-value"]'
    CONFIRMATION_POP_UP = '//nb-dialog-container'

    # Filters at main page
    NAME_FILTER_AT_MAIN_PAGE_XPATH = "(//input[@ref='eFloatingFilterText'])[1]"
    MODE_FILTER_AT_MAIN_PAGE_XPATH = "(//input[@ref='eFloatingFilterText'])[2]"
    LOCATION_FILTER_AT_MAIN_PAGE_XPATH = "(//input[@ref='eFloatingFilterText'])[3]"

    # Values tab
    NAME_AT_VALUES_TAB_XPATH = '//*[@id="deskName"]'
    DESK_MODE_AT_VALUES_TAB_XPATH = '//*[@id="deskMode"]'
    CTM_BIC_AT_VALUES_TAB = '//*[@id="BIC"]'

    LOCATION_AT_ASSIGNMENTS_TAB_XPATH = '//*[@id="location"]'
    ASSIGNMENTS_TAB_LOCATION_LINK_XPATH = '//*[normalize-space(text())="{}"]'
    ASSIGNMENTS_TAB_USER_LINK_XPATH = '//*[normalize-space(text())="{}"]'
    ASSIGNMENTS_TAB_USERS_XPATH = '//*[@class="linked-entities-label"][normalize-space()="Users"]//..//a'

    SAVE_CHANGES_BUTTON_XPATH = "//*[normalize-space()='Save Changes']"
    REVERT_CHANGES_BUTTON_XPATH = "//*[text()='Revert Changes']"
