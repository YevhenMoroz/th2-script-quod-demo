class InstrumentSymbolsConstants:
    INSTRUMENT_SYMBOLS_PAGE_TITLE_XPATH = "//span[@class='entity-title left'][normalize-space()='Instrument Symbols']"
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
    INCORRECT_OR_MISSING_VALUES_XPATH = "//*[text()='Incorrect or missing values']"
    DROP_DOWN_MENU_XPATH = '//*[@class="option-list"]//span'

    # Main page

    MAIN_PAGE_INSTR_SYMBOL_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[1]//input'
    MAIN_PAGE_CUM_TRADING_LIMIT_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[2]//input'
    MAIN_PAGE_MD_MAX_SPREAD_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[3]//input'
    MAIN_PAGE_CROSS_THROUGH_USD_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[4]//select'
    MAIN_PAGE_CROSS_THROUGH_EUR_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[5]//select'
    MAIN_PAGE_CROSS_THROUGH_EUR_TO_USD_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[6]//select'
    MAIN_PAGE_CROSS_THROUGH_USD_TO_EUR_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[7]//select'

    MAIN_PAGE_INSTR_SYMBOL_XPATH = '//*[@col-id="instrSymbol"]//span/span[4]'
    MAIN_PAGE_CUM_TRADING_LIMIT_XPATH = '//*[@col-id="instrSymbolCumTrdLmtPct"]//span/span[4]'
    MAIN_PAGE_MD_MAX_SPREAD_XPATH = '//*[@col-id="MDMaxSpread"]//span/span[4]'
    MAIN_PAGE_CROSS_THROUGH_USD_XPATH = '//*[@col-id="crossThroughUSD"]//*[@class="custom-checkbox"]'
    MAIN_PAGE_CROSS_THROUGH_EUR_XPATH = '//*[@col-id="crossThroughEUR"]//*[@class="custom-checkbox"]'
    MAIN_PAGE_CROSS_THROUGH_EUR_TO_USD_XPATH = '//*[@col-id="crossThroughEURToUSD"]//*[@class="custom-checkbox"]'
    MAIN_PAGE_CROSS_THROUGH_USD_TO_EUR_XPATH = '//*[@col-id="crossThroughUSDToEUR"]//*[@class="custom-checkbox"]'

    WIZARD_INSTR_SYMBOL_XPATH = '//*[@id="instrSymbol"]'
    WIZARD_CUM_TRADING_LIMIT_PERCENTAGE_XPATH = '//*[@formcontrolname="instrSymbolCumTrdLmtPct"]'
    WIZARD_MD_MAX_SPREAD_XPATH = '//*[@formcontrolname="MDMaxSpread"]'
    WIZARD_CROSS_THROUGH_EUR_CHECKBOX_XPATH = '//*[@formcontrolname="crossThroughEUR"]//span'
    WIZARD_CROSS_THROUGH_USD_CHECKBOX_XPATH = '//*[@formcontrolname="crossThroughUSD"]//span'
    WIZARD_CROSS_THROUGH_USD_TO_EUR_CHECKBOX_XPATH = '//*[@formcontrolname="crossThroughUSDToEUR"]//span'
    WIZARD_CROSS_THROUGH_EUR_TO_USD_CHECKBOX_XPATH = '//*[@formcontrolname="crossThroughEURToUSD"]//span'
    WIZARD_ERROR_MESSAGE_XPATH = '//nb-toast[contains(@class, "danger")]'
