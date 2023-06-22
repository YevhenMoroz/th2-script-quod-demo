class ZonesConstants:
    ZONES_PAGE_TITLE_XPATH = '//span[@class="entity-title left"][normalize-space()="Zones"]'
    ZONES_WIZARD_PAGE_TITLE_XPATH = '//div[@class="breadcrumbs entity-title"]//*[text()="Zones"]'
    DISPLAYED_ENTITY_XPATH = "//*[text()='{}']"
    INSTITUTIONS_COLUMN_XPATH = '//*[@col-id="institution.institutionName"][@tabindex="-1"]//span[@ref="eValue"]'
    ZONES_NAME_COLUMN_XPATH = '//*[@col-id="zoneName"][@tabindex="-1"]//span[@ref="eValue"]'
    DROP_DOWN_MENU_XPATH = '//*[@class="option-list"]//span'
    CONFIRMATION_POP_UP = '//nb-dialog-container'

    REFRESH_PAGE_BUTTON_XPATH = "//*[@data-name='refresh']"
    DOWNLOAD_PDF_BUTTON_XPATH = "//*[@nbtooltip = 'Download PDF']//*[@data-name='download']"
    SAVE_CHANGES_BUTTON_XPATH = "//*[normalize-space()='Save Changes']"
    CLEAR_CHANGES_BUTTON_XPATH = "//*[normalize-space()='Clear Changes']"
    CLOSE_WIZARD_XPATH = "//*[@data-name='close']"
    OK_BUTTON_XPATH = '//*[text()="Ok" or text()="OK"]'
    NO_BUTTON_XPATH = '//*[normalize-space()="No"]'
    CANCEL_BUTTON_XPATH = '//*[normalize-space()="Cancel"]'
    REVERT_CHANGES_XPATH = "//*[text()='Revert Changes']"
    MORE_ACTIONS_XPATH = "//*[@row-index = '0']//*[@data-name = 'more-vertical']"
    EDIT_XPATH = "//*[@data-name = 'edit']"
    CLONE_XPATH = "//*[@data-name = 'copy']"
    DELETE_XPATH = "//*[@data-name = 'trash-2']"
    PIN_ROW_XPATH = "//*[@nbtooltip ='Click to Pin Row']"
    NEW_BUTTON_XPATH = '//*[normalize-space()="New"]'
    USER_ICON_AT_RIGHT_CORNER = "//*[@class='control-item icon-btn context-menu-host']"
    LOGOUT_BUTTON_XPATH = "//*[text()='Logout']"
    GO_BACK_BUTTON_XPATH = "//*[text()='Go Back']"
    INCORRECT_OR_MISSING_VALUES_MESSAGE_XPATH = "//*[text()='Incorrect or missing values']"
    SUCH_RECORD_ALREADY_EXISTS_MASSEGE_XPATH = "//*[text()='Such a record already exists']"
    ENABLE_DISABLE_BUTTON_XPATH = "//div[contains(@class, 'toggle')]"

    MAIN_PAGE_DOWNLOAD_CSV_XPATH = "//*[@data-name='download']"
    MAIN_PAGE_NAME_FILTER_XPATH = '//*[@col-id="zoneName"]//following::input[@ref="eFloatingFilterText"][1]'
    MAIN_PAGE_INSTITUTION_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[2]//input'
    MAIN_PAGE_ENABLED_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[3]//select'

    # Values tab
    VALUES_TAB_NAME_XPATH = '//*[@formcontrolname="zoneName"]'
    VALUES_TAB_XPATH = '//*[text()=" Values "]'

    # Assignments tab
    ASSIGNMENTS_TAB_INSTITUTION_XPATH = '//*[@id="institution"]'
    ASSIGNMENTS_TAB_LOCATIONS_LINK_XPATH = '//a[text()=" {} "]'
    ASSIGNMENTS_TAB_USERS_LINK_XPATH = '//a[text()=" {} "]'
    ASSIGNMENTS_TAB_LOCATIONS_LIST_XPATH = '//*[normalize-space()="Locations"]//ancestor::div[@class="linked-entities-list"]//a'
    ASSIGNMENTS_TAB_USERS_LIST_XPATH = '//*[normalize-space()="Users"]//ancestor::div[@class="linked-entities-list"]//a'

