class AllocationMatchingProfilesConstants:
    ALLOCATION_MATCHING_PROFILES_PAGE_TITLE_XPATH = '//span[@class="entity-title left"][normalize-space()="Allocation Matching Profiles"]'

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
    NEW_BUTTON_XPATH = '//*[normalize-space()="Allocation Matching Profiles"]//..//*[text()="New"]'
    USER_ICON_AT_RIGHT_CORNER = "//*[@class='control-item icon-btn context-menu-host']"
    LOGOUT_BUTTON_XPATH = "//*[text()='Logout']"
    GO_BACK_BUTTON_XPATH = "//*[text()='Go Back']"
    MAIN_PAGE_DOWNLOAD_CSV_BUTTON_XPATH = '//*[@data-name="download"]'
    INCORRECT_OR_MISSING_VALUES_XPATH = "//*[text()='Incorrect or missing values']"
    DISPLAYED_ENTITY_XPATH = "//*[text()='{}']"

    # Main page
    MAIN_PAGE_FIX_MATCHING_PROFILE_NAME_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[1]//input'
    MAIN_PAGE_INSTRUMENT_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[2]//input'
    MAIN_PAGE_CLIENT_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[3]//input'
    MAIN_PAGE_QUANTITY_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[4]//input'
    MAIN_PAGE_AVG_PRICE_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[5]//input'
    MAIN_PAGE_CURRENCY_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[6]//input'
    MAIN_PAGE_SIDE_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[7]//input'

    MAIN_PAGE_MIN_QTY_VALUE_XPATH = '//*[@col-id="minHardQty"]//span//span[4]'

    #TODO: MUST BE add

    # MAIN_PAGE_FIX_MATCHING_PROFILE_NAME_XPATH = '//*[@col-id=""]//span//span[4]'
    # MAIN_PAGE_INSTRUMENT_XPATH = '//*[@col-id=""]//span//span[4]'
    # MAIN_PAGE_CLIENT_XPATH ='//*[@col-id=""]//span//span[4]'
    # MAIN_PAGE_QUANTITY_XPATH = '//*[@col-id=""]//span//span[4]'
    # MAIN_PAGE_AVG_PRICE_XPATH ='//*[@col-id=""]//span//span[4]'
    # MAIN_PAGE_CURRENCY_XPATH = '//*[@col-id=""]//span//span[4]'
    # MAIN_PAGE_SIDE_XPATH = '//*[@col-id=""]//span//span[4]'

    # Wizard

    WIZARD_FIX_MATCHING_PROFILE_NAME_XPATH = '//*[@formcontrolname="blockMatchingProfileName"]'
    WIZARD_AVG_PRICE_PRECISION_XPATH  = '//*[@formcontrolname="avgPxPrecision"]'
    WIZARD_GROSS_TOLERANCE_XPATH  = '//*[@formcontrolname="grossTradeAmtTolerance"]'
    WIZARD_NET_TOLERANCE_XPATH  = '//*[@formcontrolname="netMoneyTolerance"]'
    WIZARD_TOLERANCE_CURRENCY_XPATH  = '//*[@id="grossTradeAmtToleranceCurr"]'
    WIZARD_NET_TOLERANCE_CURRENCY_XPATH  = '//*[@id="netMoneyToleranceCurr"]'

    # WIZARD_INSTRUMENT_CHECKBOX_XPATH = ''
    # WIZARD_CLIENT_CHECKBOX_XPATH = ''
    # WIZARD_QUANTITY_CHECKBOX_XPATH = ''
    # WIZARD_AVG_PRICE_CHECKBOX_XPATH = ''
    # WIZARD_CURRENCY_CHECKBOX_XPATH = ''
    # WIZARD_SIDE_CHECKBOX_XPATH = ''

    WIZARD_GROSS_AMOUNT_CHECKBOX_XPATH = '//*[text()="Gross Amount"]/preceding-sibling::span'
    WIZARD_NET_AMOUNT_CHECKBOX_XPATH = '//*[text()="Net Amount"]/preceding-sibling::span'
    WIZARD_SETTL_AMOUNT_CHECKBOX_XPATH = '//*[text()="Settl Amount"]/preceding-sibling::span'
    WIZARD_CLIENT_LEI_CHECKBOX_XPATH = '//*[text()="Client LEI"]/preceding-sibling::span'
    WIZARD_SETTL_DATE_CHECKBOX_XPATH = '//*[text()="Settl Date"]/preceding-sibling::span'
    WIZARD_CLIENT_BIC_CHECKBOX_XPATH = '//*[text()="Client BIC"]/preceding-sibling::span'
    WIZARD_CLIENT_COMMISSION_CHECKBOX_XPATH = '//*[text()="Client Commission"]/preceding-sibling::span'
    WIZARD_TRADE_DATE_CHECKBOX_XPATH = '//*[text()="Trade Date"]/preceding-sibling::span'















