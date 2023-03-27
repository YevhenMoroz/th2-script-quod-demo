class PositionsLimitsConstants:
    POSITIONS_LIMITS_PAGE_TITLE_XPATH = "//span[@class='entity-title left'][normalize-space()='Position Limits']"

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
    NEW_BUTTON_XPATH = '//*[normalize-space()="New"]'
    USER_ICON_AT_RIGHT_CORNER = "//*[@class='control-item icon-btn context-menu-host']"
    LOGOUT_BUTTON_XPATH = "//*[text()='Logout']"
    GO_BACK_BUTTON_XPATH = "//*[text()='Go Back']"
    MAIN_PAGE_DOWNLOAD_CSV_BUTTON_XPATH = '//*[@data-name="download"]'
    INCORRECT_OR_MISSING_VALUES_XPATH = "//*[text()='Incorrect or missing values']"
    SEARCHED_VALUE_XPATH = '//*[text()="{}"]'

    # Main page
    MAIN_PAGE_DESCRIPTION_FILTER_XPATH = '//*[@style="width: 200px; left: 0px;"]//input[@ref="eFloatingFilterText"]'
    MAIN_PAGE_MIN_SOFT_QTY_FILTER_XPATH = '//*[@style="width: 200px; left: 200px;"]//input[@ref="eFloatingFilterText"]'
    MAIN_PAGE_MIN_SOFT_AMT_FILTER_XPATH = '//*[@style="width: 200px; left: 400px;"]//input[@ref="eFloatingFilterText"]'
    MAIN_PAGE_MAX_SOFT_QTY_FILTER_XPATH = '//*[@style="width: 200px; left: 600px;"]//input[@ref="eFloatingFilterText"]'
    MAIN_PAGE_MAX_SOFT_AMT_FILTER_XPATH = '//*[@style="width: 200px; left: 800px;"]//input[@ref="eFloatingFilterText"]'
    MAIN_PAGE_MIN_QTY_FILTER_XPATH = '//*[@style="width: 200px; left: 1000px;"]//input[@ref="eFloatingFilterText"]'
    MAIN_PAGE_MIN_AMT_FILTER_XPATH = '//*[@style="width: 200px; left: 1200px;"]//input[@ref="eFloatingFilterText"]'
    MAIN_PAGE_MAX_QTY_FILTER_XPATH = '//*[@style="width: 200px; left: 1400px;"]//input[@ref="eFloatingFilterText"]'
    MAIN_PAGE_MAX_AMT_FILTER_XPATH = '//*[@style="width: 200px; left: 1600px;"]//input[@ref="eFloatingFilterText"]'
    MAIN_PAGE_CURRENCY_FILTER_XPATH = '//*[@style="width: 200px; left: 1800px;"]//input[@ref="eFloatingFilterText"]'

    MAIN_PAGE_DESCRIPTION_VALUE_XPATH = '//*[@col-id="positLimitDesc"]//span[@ref="eValue"]'
    MAIN_PAGE_MIN_SOFT_QTY_VALUE_XPATH = '//*[@col-id="minSoftQty"]//span[@ref="eValue"]'
    MAIN_PAGE_MIN_SOFT_AMT_VALUE_XPATH = '//*[@col-id="minSoftAmt"]//span[@ref="eValue"]'
    MAIN_PAGE_MAX_SOFT_QTY_VALUE_XPATH = '//*[@col-id="maxSoftQty"]//span[@ref="eValue"]'
    MAIN_PAGE_MAX_SOFT_AMT_VALUE_XPATH = '//*[@col-id="maxSoftAmt"]//span[@ref="eValue"]'
    MAIN_PAGE_MIN_QTY_VALUE_XPATH = '//*[@col-id="minHardQty"]//span[@ref="eValue"]'
    MAIN_PAGE_MIN_AMT_VALUE_XPATH = '//*[@col-id="minHardAmt"]//span[@ref="eValue"]'
    MAIN_PAGE_MAX_QTY_VALUE_XPATH = '//*[@col-id="maxHardQty"]//span[@ref="eValue"]'
    MAIN_PAGE_MAX_AMT_VALUE_XPATH = '//*[@col-id="maxHardAmt"]//span[@ref="eValue"]'
    MAIN_PAGE_CURRENCY_VALUE_XPATH = '//*[@col-id="positLimitCurrency"]//span[@ref="eValue"]'

    # Values tab
    VALUES_TAB_SET_DESCRIPTION = '//*[@formcontrolname="positLimitDesc"]'
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

    DIMENSIONS_TAB_INSTRUMENT_XPATH = '//*[normalize-space()="Dimensions"]/..//input[@id="securityBlock"]'
    DIMENSIONS_TAB_INSTRUMENT_GROUP_XPATH = '//*[normalize-space()="Dimensions"]/..//input[@id="instrumentGroup"]'
    DIMENSIONS_TAB_INSTRUMENT_TYPE_XPATH = '//*[normalize-space()="Dimensions"]/..//input[@id="instrType"]'
    DIMENSIONS_TAB_ACCOUNT_XPATH = '//*[normalize-space()="Dimensions"]/..//input[@id="account"]'
    DIMENSIONS_TAB_PER_INSTRUMENT_CHECKBOX_XPATH = '//*[text()="Per Instrument"]/preceding-sibling::span'
    DIMENSIONS_TAB_PER_INSTR_TYPE_CHECKBOX_XPATH = '//*[text()="Per Instr Type"]/preceding-sibling::span'
    DIMENSIONS_TAB_PER_INSTR_GROUP_CHECKBOX_XPATH = '//*[text()="Per Instr Group"]/preceding-sibling::span'

    # Assignments tab
    ASSIGNMENTS_TAB_INSTITUTIONS = '//*[normalize-space()="Assignments"]/..//input[@id="institution"]'

















