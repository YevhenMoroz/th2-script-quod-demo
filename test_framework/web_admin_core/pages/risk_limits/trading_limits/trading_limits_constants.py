class TradingLimitsConstants:
    TRADING_LIMITS_PAGE_TITLE_XPATH = "//span[@class='entity-title left'][text()='TradingLimits ']"
    REFRESH_PAGE_BUTTON_XPATH = "//*[@data-name='refresh']"
    DOWNLOAD_PDF_BUTTON_XPATH = "//*[@data-name='download']"
    SAVE_CHANGES_BUTTON_XPATH = "//*[text()='Save Changes']"
    CLEAR_CHANGES_BUTTON_XPATH = "//*[text()='Clear Changes']"
    CLOSE_WIZARD_XPATH = "//*[@data-name='close']"
    OK_BUTTON_XPATH = '//*[text()="Ok"]'
    CANCEL_BUTTON_XPATH = '//*[normalize-space()="Cancel"]'
    REVERT_CHANGES_XPATH = "//*[normalize-space()='Revert Changes']"
    MORE_ACTIONS_XPATH = "//*[@data-name = 'more-vertical']"
    EDIT_XPATH = "//*[@data-name = 'edit']"
    CLONE_XPATH = "//*[@data-name = 'copy']"
    DELETE_XPATH = "//*[@data-name = 'trash-2']"
    PIN_ROW_XPATH = "//*[@nbtooltip ='Click to Pin Row']"
    NEW_BUTTON_XPATH = '//*[text()="New"]'
    USER_ICON_AT_RIGHT_CORNER = "//*[@class='control-item icon-btn context-menu-host']"
    LOGOUT_BUTTON_XPATH = "//*[text()='Logout']"
    GO_BACK_BUTTON_XPATH = "//*[text()='Go Back']"
    MAIN_PAGE_DOWNLOAD_CSV_BUTTON_XPATH = '//*[@data-name="download"]'
    INCORRECT_OR_MISSING_VALUES_XPATH = "//*[text()='Incorrect or missing values']"
    DISPLAYED_ROUTE_XPATH = "//*[text()='{}']"
    DROP_DOWN_MENU_XPATH = '//*[@class="option-list"]//span'

    # Main page
    MAIN_PAGE_DESCRIPTION_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[1]//input'
    MAIN_PAGE_EXTERNAL_ID_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[2]//input'
    MAIN_PAGE_CURRENCY_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[3]//input'
    MAIN_PAGE_MAX_QTY_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[4]//input'
    MAIN_PAGE_MAX_AMT_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[5]//input'
    MAIN_PAGE_MAX_SOFT_QTY_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[6]//input'
    MAIN_PAGE_MAX_SOFT_AMT_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[7]//input'
    MAIN_PAGE_DESCRIPTION_XPATH = '//*[@col-id="tradingLimitDesc"]//span//span[4]'
    MAIN_PAGE_EXTERNAL_ID_XPATH = '//*[@col-id="externalTradingLimitID"]//span//span[4]'
    MAIN_PAGE_CURRENCY_XPATH ='//*[@col-id="maxOrdAmtCurrency"]//span//span[4]'
    MAIN_PAGE_MAX_QTY_VALUE_XPATH = '//*[@col-id="maxOrdQty"]//span//span[4]'
    MAIN_PAGE_MAX_AMT_VALUE_XPATH = '//*[@col-id="maxOrdAmt"]//span//span[4]'
    MAIN_PAGE_MAX_SOFT_QTY_VALUE_XPATH = '//*[@col-id="softMaxOrdQty"]//span//span[4]'
    MAIN_PAGE_MAX_SOFT_AMT_VALUE_XPATH = '//*[@col-id="softMaxOrdAmt"]//span//span[4]'

    # Values tab
    VALUES_TAB_DESCRIPTION_XPATH = '//*[@formcontrolname="tradingLimitDesc"]'
    VALUES_TAB_EXTERNAL_ID_XPATH = '//*[@formcontrolname="externalTradingLimitID"]'
    VALUES_TAB_CURRENCY_XPATH = '//*[@id="maxOrdAmtCurrency"]'
    VALUES_TAB_MAX_QUANTITY_XPATH = '//*[@formcontrolname="maxOrdQty"]'
    VALUES_TAB_MAX_AMOUNT_XPATH = '//*[@formcontrolname="maxOrdAmt"]'
    VALUES_TAB_MAX_SOFT_QUANTITY_XPATH = '//*[@formcontrolname="softMaxOrdQty"]'
    VALUES_TAB_MAX_SOFT_AMOUNT_XPATH = '//*[@formcontrolname="softMaxOrdAmt"]'

    # Dimensions tab
    DIMENSIONS_TAB_VENUE_XPATH = '//*[normalize-space()="Dimensions"]/..//input[@id="venue"]'
    DIMENSIONS_TAB_SUB_VENUE_XPATH = '//*[normalize-space()="Dimensions"]/..//input[@id="subVenue"]'
    DIMENSIONS_TAB_LISTING_GROUP_XPATH = '//*[normalize-space()="Dimensions"]/..//input[@id="listingGroup"]'
    DIMENSIONS_TAB_USER_XPATH = '//*[normalize-space()="Dimensions"]/..//input[@id="userBlock"]'
    DIMENSIONS_TAB_CLIENT_XPATH = '//*[normalize-space()="Dimensions"]/..//input[@id="accountGroup"]'
    DIMENSIONS_TAB_CLIENT_GROUP_XPATH = '//*[normalize-space()="Dimensions"]/..//input[@id="clientGroup"]'
    DIMENSIONS_TAB_DESK_XPATH = '//*[normalize-space()="Dimensions"]/..//input[@id="desk"]'
    DIMENSIONS_TAB_ROUTE_XPATH = '//*[normalize-space()="Dimensions"]/..//input[@id="route"]'
    DIMENSIONS_TAB_INSTRUMENT_TYPE_XPATH = '//*[normalize-space()="Dimensions"]/..//input[@id="instrType"]'
    DIMENSIONS_TAB_INSTR_SYMBOL_XPATH = '//*[normalize-space()="Dimensions"]/..//input[@id="instrSymbol"]'
    DIMENSIONS_TAB_EXECUTION_POLICY_XPATH = '//*[normalize-space()="Dimensions"]/..//input[@id="executionPolicy"]'
    DIMENSIONS_TAB_PHASE_XPATH = '//*[normalize-space()="Dimensions"]/..//input[@id="standardTradingPhase"]'

    # Assignments tab
    ASSIGNMENTS_TAB_INSTITUTIONS = '//*[normalize-space()="Assignments"]/..//input[@id="institution"]'




















