class UserInstrSymbBlackOutConstants:
    USER_INSTR_SYMB_BLACK_OUT_PAGE_TITLE_XPATH = "//span[@class='entity-title left'][text()='User Instr Symb Black Out ']"
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

    # Main page
    MAIN_PAGE_SYMBOL_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[1]//input'
    MAIN_PAGE_SYMBOL_XPATH = '//*[@col-id="instrSymbol"]//span//span[4]'
    MAIN_PAGE_USER_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[2]//input'
    MAIN_PAGE_USER_XPATH = '//*[@col-id="user.userID"]//span//span[4]'

    # Values tab
    VALUES_TAB_SYMBOL_XPATH = '//*[@id="instrSymbol"]'
    VALUES_TAB_USER_XPATH = '//*[@id="user"]'

    # Periods tab
    PERIODS_TAB_PLUS_BUTTON_XPATH = '//*[@class="nb-plus"]'
    PERIODS_TAB_CHECKMARK_BUTTON_XPATH = '//*[@class="nb-checkmark"]'
    PERIODS_TAB_CLOSE_BUTTON_XPATH = '//*[@class="nb-close"]'
    PERIODS_TAB_EDIT_BUTTON_XPATH = '//*[@class="nb-edit"]'
    PERIODS_TAB_DELETE_BUTTON_XPATH = '//*[@class="nb-trash"]'

    PERIODS_TAB_BLACK_OUT_PERIOD_FILTER_XPATH = '//*[@class="blackOutPeriod ng2-smart-th ng-star-inserted"]//input'
    PERIODS_TAB_BLACK_OUT_PERIOD_XPATH = '//*[@placeholder="Black Out Period *"]'
    PERIODS_TAB_UPPER_QTY_FILTER_XPATH = '//*[@class="ng2-smart-th upperQty ng-star-inserted"]//input'
    PERIODS_TAB_UPPER_QTY_XPATH = '//*[@placeholder="Upper Qty"]'
