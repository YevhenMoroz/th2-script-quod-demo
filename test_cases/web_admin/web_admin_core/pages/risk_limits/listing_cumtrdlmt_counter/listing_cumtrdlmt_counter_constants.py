class ListingCumTrdLmtCounterConstants:
    LISTING_CUMTRDLMT_COUNTER_PAGE_TITLE_XPATH = "//span[@class='entity-title left'][text()='Listing CumTrdLmt Counter ']"
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
    MAIN_PAGE_LISTING_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[1]//input'
    MAIN_PAGE_CUM_TRADING_LIMIT_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[2]//input'
    MAIN_PAGE_CUM_BUY_ORD_QTY_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[3]//input'
    MAIN_PAGE_CUM_ORD_AMT_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[4]//input'
    MAIN_PAGE_CUM_SELL_ORD_QTY_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[5]//input'

    # Wizard
    WIZARD_LISTING_XPATH = '//*[id="listing"]'
    WIZARD_CUM_TRADING_LIMIT_XPATH = '//*[@id="cumTradingLimit"]'
    WIZARD_CUM_BUY_ORD_QTY_XPATH = '//*[@formcontrolname="cumBuyOrdQty"]'
    WIZARD_CUM_ORD_AMT_XPATH = '//*[@formcontrolname="cumOrdAmt"]'
    WIZARD_CUM_SELL_ORD_QTY_XPATH = '//*[@formcontrolname="cumSellOrdQty"]'
    WIZARD_CUM_BUY_ORD_AMT_XPATH = '//*[@formcontrolname="cumBuyOrdAmt"]'
    WIZARD_ORD_QTY_XPATH = '//*[@formcontrolname="cumOrdQty"]'
    WIZARD_CUM_SELL_ORD_AMT_XPATH = '//*[@formcontrolname="cumSellOrdAmt"]'
