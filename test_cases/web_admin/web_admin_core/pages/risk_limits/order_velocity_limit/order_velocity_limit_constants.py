class OrderVelocityLimitConstants:
    ORDER_VELOCITY_LIMIT_PAGE_TITLE_XPATH = "//span[@class='entity-title left'][text()='Order Velocity Limit ']"

    REFRESH_PAGE_BUTTON_XPATH = "//*[@data-name='refresh']"
    DOWNLOAD_PDF_BUTTON_XPATH = "//*[@data-name='download']"
    SAVE_CHANGES_BUTTON_XPATH = "//*[text()='Save Changes']"
    CLEAR_CHANGES_BUTTON_XPATH = "//*[text()='Clear Changes']"
    CLOSE_WIZARD_XPATH = "//*[@data-name='close']"
    OK_BUTTON_XPATH = '//*[text()="Ok"]'
    CANCEL_BUTTON_XPATH = '//*[text()="Cancel"]'
    REVERT_CHANGES_XPATH = "//*[text()='Revert Changes']"
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

    # Main page
    MAIN_PAGE_NAME_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[1]//input'
    MAIN_PAGE_CLIENT_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[2]//input'
    MAIN_PAGE_SIDE_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[3]//input'
    MAIN_PAGE_INSTR_SYMBOL_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[4]//input'
    MAIN_PAGE_LISTING_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[5]//input'
    MAIN_PAGE_MOVING_TIME_WINDOW_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[6]//input'
    MAIN_PAGE_MAX_QUANTITY_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[7]//input'
    MAIN_PAGE_NAME_XPATH = '//*[@col-id="orderVelocityLimitName"]//span//span[4]'
    MAIN_PAGE_CLIENT_XPATH = '//*[@col-id="accountGroup.accountGroupName"]//span//span[4]'
    MAIN_PAGE_SIDE_XPATH = '//*[@col-id="side"]//span//span[4]'
    MAIN_PAGE_INSTR_SYMBOL_XPATH = '//*[@col-id="instrSymbol"]//span//span[4]'
    MAIN_PAGE_LISTING_XPATH = '//*[@col-id="instr.symbol"]//span//span[4]'
    MAIN_PAGE_MOVING_TIME_WINDOW_XPATH = '//*[@col-id="movingTimeWindow"]//span//span[4]'
    MAIN_PAGE_MAX_QUANTITY_XPATH = '//*[@col-id="maxCumOrdQty"]//span//span[4]'

    # Values tab
    VALUES_TAB_ORDER_VELOCITY_LIMIT_NAME_XPATH = '//*[@formcontrolname="orderVelocityLimitName"]'
    VALUES_TAB_MAX_AMOUNT_XPATH = '//*[@formcontrolname="maxCumOrdAmt"]'
    VALUES_TAB_MOVING_TIME_WINDOW_XPATH = '//*[@formcontrolname="movingTimeWindow"]'
    VALUES_TAB_MAX_QUANTITY_XPATH = '//*[@formcontrolname="maxCumOrdQty"]'
    VALUES_TAB_MAX_ORDER_ACTIONS_XPATH = '//*[@formcontrolname="maxOrderActions"]'
    VALUES_TAB_BLOCKED_RULE_CHECKBOX_XPATH = '//*[text()="Blocked Rule"]/preceding-sibling::span'
    VALUES_TAB_AUTO_RESET_CHECKBOX_XPATH = '//*[text()="Auto Reset"]/preceding-sibling::span'

    # Dimensions tab
    DIMENSIONS_TAB_CLIENT_XPATH = '//*[@id="accountGroup"]'
    DIMENSIONS_TAB_SIDE_XPATH = '//*[@id="side"]'
    DIMENSIONS_TAB_INSTR_SYMBOL_XPATH = '//*[@id="instrSymbol"]'
    DIMENSIONS_TAB_LISTING_XPATH = '//*[@id="instr"]'
    DIMENSIONS_TAB_ALL_ORDERS_CHECKBOX_XPATH = '//*[text()="All Orders"]/preceding-sibling::span'
