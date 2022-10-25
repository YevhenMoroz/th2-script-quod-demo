class CumTradingLimitsConstants:
    CUM_TRADING_LIMITS_PAGE_TITLE_XPATH = "//span[@class='entity-title left'][text()='Cum Trading Limits ']"
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
    DISPLAYED_CUM_TRADING_LIMIT_XPATH = "//*[text()='{}']"
    DROP_DOWN_MENU_XPATH = '//*[@class="option-list"]//nb-option'

    # Main page
    MAIN_PAGE_DESCRIPTION_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[1]//input'
    MAIN_PAGE_CUM_TRADING_LIMIT_PERCENTAGE_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[2]//input'
    MAIN_PAGE_MAX_QTY_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[3]//input'
    MAIN_PAGE_MAX_AMT_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[4]//input'
    MAIN_PAGE_SOFT_MAX_QTY_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[5]//input'
    MAIN_PAGE_SOFT_MAX_AMT_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[6]//input'
    MAIN_PAGE_CURRENCY_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[7]//input'
    MAIN_PAGE_MAX_SELL_QTY_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[8]//input'

    MAIN_PAGE_CURRENCY_XPATH = '//*[@col-id="maxCumOrdAmtCurrency"]//span/span[4]'


    # Values tab
    VALUES_TAB_DESCRIPTION_XPATH = '//*[@formcontrolname="cumTradingLimitDesc"]'
    VALUES_TAB_EXTERNAL_ID_XPATH = '//*[@formcontrolname="externalCumTradingLimitID"]'
    VALUES_TAB_CURRENCY_XPATH = '//*[@id="maxCumOrdAmtCurrency"]'
    VALUES_TAB_MAX_QUANTITY_XPATH = '//*[@formcontrolname="maxCumOrdQty"]'
    VALUES_TAB_SOFT_MAX_QTY_XPATH = '//*[@formcontrolname="softMaxCumOrdQty"]'
    VALUES_TAB_MAX_AMOUNT_XPATH = '//*[@formcontrolname="maxCumOrdAmt"]'
    VALUES_TAB_SOFT_MAX_AMT_XPATH = '//*[@formcontrolname="softMaxCumOrdAmt"]'
    VALUES_TAB_MAX_BUY_QTY_XPATH = '//*[@formcontrolname="maxCumBuyOrdQty"]'
    VALUES_TAB_SOFT_MAX_BUY_QTY_XPATH = '//*[@formcontrolname="softMaxCumBuyOrdQty"]'
    VALUES_TAB_MAX_BUY_AMT_XPATH = '//*[@formcontrolname="maxCumBuyOrdAmt"]'
    VALUES_TAB_SOFT_MAX_BUY_AMT_XPATH = '//*[@formcontrolname="softMaxCumBuyOrdAmt"]'
    VALUES_TAB_MAX_SELL_QTY_XPATH = '//*[@formcontrolname="maxCumSellOrdQty"]'
    VALUES_TAB_SOFT_MAX_SELL_QTY_XPATH = '//*[@formcontrolname="softMaxCumSellOrdQty"]'
    VALUES_TAB_MAX_SELL_AMT_XPATH = '//*[@formcontrolname="maxCumSellOrdAmt"]'
    VALUES_TAB_SOFT_MAX_SELL_AMT_XPATH = '//*[@formcontrolname="softMaxCumSellOrdAmt"]'
    VALUES_TAB_MAX_OPEN_ORDER_AMOUNT_XPATH = '//*[@formcontrolname="maxCumLeavesOrdAmt"]'

    # Dimensions tab
    DIMENSIONS_TAB_VENUE_XPATH = '//*[normalize-space()="Dimensions"]/..//input[@id="venue"]'
    DIMENSIONS_TAB_SUB_VENUE_XPATH = '//*[normalize-space()="Dimensions"]/..//input[@id="subVenue"]'
    DIMENSIONS_TAB_LISTING_GROUP_XPATH = '//*[normalize-space()="Dimensions"]/..//input[@id="listingGroup"]'
    DIMENSIONS_TAB_LISTING_XPATH = '//*[normalize-space()="Dimensions"]/..//input[@id="listing"]'
    DIMENSIONS_TAB_WILDCARD_LISTING_CHECKBOX_XPATH = '//*[text()="Per Listing"]/preceding-sibling::span'
    DIMENSIONS_TAB_USER_XPATH = '//*[normalize-space()="Dimensions"]/..//input[@id="userBlock"]'
    DIMENSIONS_TAB_DESK_XPATH = '//*[normalize-space()="Dimensions"]/..//input[@id="desk"]'
    DIMENSIONS_TAB_ROUTE_XPATH = '//*[normalize-space()="Dimensions"]/..//input[@id="route"]'
    DIMENSIONS_TAB_INSTRUMENT_TYPE_XPATH = '//*[normalize-space()="Dimensions"]/..//input[@id="instrType"]'
    DIMENSIONS_TAB_CLIENT_XPATH = '//*[normalize-space()="Dimensions"]/..//input[@id="accountGroup"]'
    DIMENSIONS_TAB_CLIENT_GROUP_XPATH = '//*[normalize-space()="Dimensions"]/..//input[@id="clientGroup"]'
    DIMENSIONS_TAB_ACCOUNT_XPATH = '//*[normalize-space()="Dimensions"]/..//input[@id="account"]'
    DIMENSIONS_TAB_INSTR_SYMBOL_XPATH = '//*[normalize-space()="Dimensions"]/..//input[@id="instrSymbol"]'

    # Assignments tab
    INSTITUTION = '//*[@id="institution"]'
