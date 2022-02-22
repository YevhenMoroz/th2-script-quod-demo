class PositionsLimitsConstants:
    POSITIONS_LIMITS_PAGE_TITLE_XPATH = "//span[@class='entity-title left'][text()='PositionLimits ']"

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
    MAIN_PAGE_MIN_SOFT_QTY_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[1]//input'
    MAIN_PAGE_MIN_SOFT_AMT_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[2]//input'
    MAIN_PAGE_MAX_SOFT_QTY_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[3]//input'
    MAIN_PAGE_MAX_SOFT_AMT_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[4]//input'
    MAIN_PAGE_MIN_QTY_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[5]//input'
    MAIN_PAGE_MIN_AMT_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[6]//input'
    MAIN_PAGE_MAX_QTY_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[7]//input'
    MAIN_PAGE_MAX_AMT_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[8]//input'
    MAIN_PAGE_MIN_SOFT_QTY_XPATH = '//*[@col-id="minSoftQty"]//span//span[4]'
    MAIN_PAGE_MIN_SOFT_AMT_XPATH = '//*[@col-id="minSoftAmt"]//span//span[4]'
    MAIN_PAGE_MAX_SOFT_QTY_XPATH = '//*[@col-id="maxSoftQty"]//span//span[4]'
    MAIN_PAGE_MAX_SOFT_AMT_XPATH = '//*[@col-id="maxSoftAmt"]//span//span[4]'
    MAIN_PAGE_MIN_QTY_XPATH = '//*[@col-id="minHardQty"]//span//span[4]'
    MAIN_PAGE_MIN_AMT_XPATH = '//*[@col-id="minHardAmt"]//span//span[4]'
    MAIN_PAGE_MAX_QTY_XPATH = '//*[@col-id="maxHardQty"]//span//span[4]'
    MAIN_PAGE_MAX_AMT_XPATH = '//*[@col-id="maxHardAmt"]//span//span[4]'


    # Values tab
    VALUES_TAB_MIN_SOFT_QTY_XPATH = '//*[@formcontrolname="minSoftQty"]'
    VALUES_TAB_MIN_SOFT_AMT_XPATH = '//*[@formcontrolname="minSoftAmt"]'
    VALUES_TAB_MAX_SOFT_QTY_XPATH = '//*[@formcontrolname="maxSoftQty"]'
    VALUES_TAB_MAX_SOFT_AMT_XPATH = '//*[@formcontrolname="maxSoftAmt"]'
    VALUES_TAB_MIN_HARD_QTY_XPATH = '//*[@formcontrolname="minHardQty"]'
    VALUES_TAB_MIN_HARD_AMT_XPATH = '//*[@formcontrolname="minHardAmt"]'
    VALUES_TAB_MAX_HARD_QTY_XPATH = '//*[@formcontrolname="maxHardQty"]'
    VALUES_TAB_MAX_HARD_AMT_XPATH = '//*[@formcontrolname="maxHardAmt"]'
    VALUES_TAB_CURRENCY_XPATH = '//*[@id="positLimitCurrency"]'

    # Dimensions tab

    DIMENSIONS_TAB_INSTRUMENT_XPATH = '//*[@id="securityBlock"]'
    DIMENSIONS_TAB_INSTRUMENT_GROUP_XPATH = '//*[@id="instrumentGroup"]'
    DIMENSIONS_TAB_INSTRUMENT_TYPE_XPATH = '//*[@id="instrType"]'
    DIMENSIONS_TAB_ACCOUNT_XPATH = '//*[@id="account"]'
    DIMENSIONS_TAB_WILD_CARD_INSTRUMENT_CHECKBOX_XPATH = '//*[text()="Wild Card Instrument"]/preceding-sibling::span'
    DIMENSIONS_TAB_WILD_CARD_INSTR_GROUP_CHECKBOX_XPATH = '//*[text()="Wild Card Instr Group"]/preceding-sibling::span'
    DIMENSIONS_TAB_WILD_CARD_INSTR_TYPE_XPATH = '//*[text()="Wild Card Instr Type"]/preceding-sibling::span'

















