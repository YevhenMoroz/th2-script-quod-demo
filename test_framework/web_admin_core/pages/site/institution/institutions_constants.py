class InstitutionsConstants:
    INSTITUTIONS_PAGE_TITLE_XPATH = '//span[@class="entity-title left"][normalize-space()="Institutions"]'

    REFRESH_PAGE_BUTTON_XPATH = "//*[@data-name='refresh']"
    DOWNLOAD_PDF_BUTTON_XPATH = "//*[@data-name='download']"
    SAVE_CHANGES_BUTTON_XPATH = "//*[normalize-space()='Save Changes']"
    CLEAR_CHANGES_BUTTON_XPATH = "//*[normalize-space()='Clear Changes']"
    CLOSE_WIZARD_XPATH = "//*[@data-name='close']"
    OK_BUTTON_XPATH = '//*[normalize-space()="Ok" or normalize-space()="OK"]'
    NO_BUTTON_XPATH = '//*[normalize-space()="No"]'
    CANCEL_BUTTON_XPATH = '//*[normalize-space()="Cancel"]'
    REVERT_CHANGES_XPATH = "//*[text()='Revert Changes']"
    MORE_ACTIONS_XPATH = "//*[@row-index='0']//*[@data-name = 'more-vertical']"
    EDIT_XPATH = "//*[@data-name = 'edit']"
    CLONE_XPATH = "//*[@data-name = 'copy']"
    DELETE_XPATH = "//*[@data-name = 'trash-2']"
    PIN_ROW_XPATH = "//*[@nbtooltip ='Click to Pin Row']"
    NEW_BUTTON_XPATH = '//*[normalize-space()="New"]'
    USER_ICON_AT_RIGHT_CORNER = "//*[@class='control-item icon-btn context-menu-host']"
    LOGOUT_BUTTON_XPATH = "//*[text()='Logout']"
    GO_BACK_BUTTON_XPATH = "//*[text()='Go Back']"
    ENABLE_DISABLE_TOGGLE_BUTTON_XPATH = "//div[contains(@class, 'toggle')]"
    ENABLE_DISABLE_TOGGLE_INPUT_XPATH = "//*[contains(@role, 'switch')]"
    SUCH_RECORD_ALREADY_EXISTS_MASSEGE_XPATH = "//*[text()='Such a record already exists']"
    DISPLAYED_ENTITY_XPATH = "//*[text()='{}']"
    DOWNLOAD_CSV_BUTTON_XPATH = '//*[@nbtooltip="Download CSV"]'
    DISPLAYED_INSTITUTIONS_XPATH = '//*[@ref="eCenterContainer"]//*[@role="row"]'
    DROP_DOWN_MENU_XPATH = '//nb-option//span'
    CROSS_CURRENCY_HAIR_CUT_FILTER = '//*[@style="width: 200px; left: 1000px;"]//*[@class="ag-floating-filter-input"]'
    CROSS_CURRENCY_HAIR_CUT = '//*[@col-id="settlCurrFxHairCut"]//*[@ref="eValue"]'
    CASH_ACCOUNT_CURRENCY_RATE_FILTER = '//*[@style="width: 200px; left: 1200px;"]//*[@class="ag-floating-filter-input"]'
    CASH_ACCOUNT_CURRENCY_RATE = '//*[@col-id="settlCurrFxRateSource"]//*[@ref="eValue"]'
    CONFIRMATION_POP_UP = '//nb-dialog-container'

    # Main page

    MAIN_PAGE_INSTITUTION_NAME_FILTER_XPATH = '//*[@col-id="institutionName"]//following::input[@ref="eFloatingFilterText"][1]'
    MAIN_PAGE_LEI_FILTER_XPATH = '//*[@col-id="institutionLEI"]//following::input[@ref="eFloatingFilterText"][2]'
    MAIN_PAGE_CTM_BIC_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[3]//input'
    MAIN_PAGE_COUNTERPART_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[4]//input'
    MAIN_PAGE_ENABLED_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[5]//select'

    MAIN_PAGE_INSTITUTION_NAME_XPATH = '//*[@col-id="institutionName"]//span/span[4]'
    MAIN_PAGE_LEI_XPATH = '//*[@col-id="institutionLEI"]//span/span[4]'
    MAIN_PAGE_CTM_BIC_XPATH = '//*[@col-id="BIC"]//span/span[4]'
    MAIN_PAGE_COUNTERPART_XPATH = '//*[@col-id="counterpart.counterpartName"]//span/span[4]'
    MAIN_PAGE_ENABLED_XPATH = '//*[@col-id="alive"]//span'

    # Values tab
    VALUES_TAB = '//*[@class="institution-detail-settings"]//*[text()=" Values "]'
    VALUES_TAB_INSTITUTION_NAME = '//*[@formcontrolname="institutionName"]'
    VALUES_TAB_LEI_NAME = '//*[@formcontrolname="institutionLEI"]'
    VALUES_TAB_CTM_BIC_NAME = '//*[@formcontrolname="BIC"]'
    VALUES_TAB_COUNTERPART_NAME = '//*[@id="counterpart"]'
    VALUES_TAB_MANAGE_COUNTERPART_BUTTON_XPATH = '//*[@class="col-sm"]//button'
    VALUES_TAB_CLIENT_TIME_ZONE_XPATH = '//*[@id="clientTimeZone"]'
    VALUES_TAB_POSITION_FLATTENING_PERIOD = '//*[@id="posFlatteningTime"]'
    VALUES_TAB_UNKNOWN_ACCOUNTS = '//*[@formcontrolname="enableUnknownAccounts"]//*[contains(@class, "custom-checkbox")]'
    VALUES_TAB_CROSS_CURRENCY_HAIR_CUT = '//*[@id="settlCurrFxHairCut"]'
    VALUES_TAB_CROSS_CURRENCY_SETTLEMENT_CHECKBOX = '//*[@formcontrolname="crossCurrencySettlement"]//*[contains(@class, "custom-checkbox")]'
    VALUES_TAB_CASH_ACCOUNT_CURRENCY_RATE_SOURCE = '//*[@id="settlCurrFxRateSource"]'

    # Assignments tab
    ASSIGNMENTS_TAB_ZONES_LINK_XPATH = '//a[text()=" {} "]'
    ASSIGNMENTS_TAB_USERS_LINK_XPATH = '//a[text()=" {} "]'
