class FeesConstants:
    FEES_PAGE_TITLE_XPATH = "//span[@class='entity-title left'][text()='Fees ']"

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

    MAIN_PAGE_DESCRIPTION_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[1]//input'
    MAIN_PAGE_MISC_FEE_TYPE_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[2]//input'
    MAIN_PAGE_CHANGE_TYPE_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[3]//input'
    MAIN_PAGE_EXEC_SCOPE_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[4]//input'
    MAIN_PAGE_EXEC_COMMISSION_PROFILE_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[5]//input'
    MAIN_PAGE_ORDER_SCOPE_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[6]//input'
    MAIN_PAGE_ORDER_COMMISSION_PROFILE_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[7]//input'

    # Values tab
    VALUES_TAB_DESCRIPTION_XPATH = '//*[@formcontrolname = "commDescription"]'
    VALUES_TAB_MISC_FEE_TYPE_XPATH = '//*[@id = "miscFeeType"]'
    VALUES_TAB_CHARGE_TYPE_XPATH = '//*[@id = "miscFeeCategory"]'
    VALUES_TAB_ORDER_SCOPE_XPATH = '//*[@id = "commOrderScope"]'
    VALUES_TAB_ORDER_FEE_PROFILE_XPATH = '//*[@id = "orderCommissionProfile"]'
    VALUES_TAB_EXEC_SCOPE_XPATH = '//*[@id = "commExecScope"]'
    VALUES_TAB_EXEC_FEE_PROFILE_XPATH = '//*[@id = "execCommissionProfile"]'
    VALUES_TAB_RE_CALCULATE_FOR_ALLOCATIONS_CHECKBOX = "//*[text()='Re-Calculate for Allocations']/preceding-sibling::span"

    VALUES_TAB_MANAGE_ORDER_FEE_PROFILE = '//nb-accordion/nb-accordion-item[1]/nb-accordion-item-body/div/div/form/div[2]/div[3]/button'
    VALUES_TAB_MANAGE_EXEC_FEE_PROFILE = '//nb-accordion/nb-accordion-item[1]/nb-accordion-item-body/div/div/form/div[3]/div[3]/button'

    # Order fee profile sub wizard
    ORDER_FEE_PROFILE_COMMISSION_PROFILE_NAME_XPATH = "//*[@placeholder = 'Commission Profile Name *']"
    ORDER_FEE_PROFILE_PLUS_BUTTON_XPATH = '//*[@class="cp-instr-table-body"]//*[@class="nb-plus ng2-main-add-btn"]'
    ORDER_FEE_PROFILE_CHECKMARK_BUTTON_XPATH = '//*[@class="cp-instr-table-body"]//*[@class="nb-checkmark"]'
    ORDER_FEE_PROFILE_CANCEL_BUTTON_XPATH = '//*[@class="cp-instr-table-body"]//*[@class="nb-close ng2-main-cancel-btn"]'
    ORDER_FEE_PROFILE_EDIT_BUTTON_XPATH = '//*[@class="cp-instr-table-body"]//*[@class="nb-edit ng2-main-edit-btn"]'
    ORDER_FEE_PROFILE_DELETE_BUTTON_XPATH = '//*[@class="cp-instr-table-body"]//*[@class="nb-trash"]'

    ORDER_FEE_PROFILE_DESCRIPTION_XPATH = '//*[@formcontrolname = "commProfileDescription"]'
    ORDER_FEE_PROFILE_COMM_XUNIT_XPATH = '//*[@id = "commXUnit"]'
    ORDER_FEE_PROFILE_VENUE_COMMISSION_PROFILE_ID_XPATH = '//*[@formcontrolname = "venueCommissionProfileID"]'
    ORDER_FEE_PROFILE_COMM_TYPE_XPATH = '//*[@id = "commType"]'
    ORDER_FEE_PROFILE_COMM_ALGORITHM_XPATH = '//*[@id = "commAlgorithm"]'
    ORDER_FEE_PROFILE_MAX_COMMISSION_XPATH = '//*[@formcontrolname = "maxCommission"]'
    ORDER_FEE_PROFILE_CURRENCY_XPATH = '//*[@id = "commCurrency"]'
    ORDER_FEE_PROFILE_ROUNDING_DIRECTION_XPATH = '//*[@id = "commRoundingDirection"]'
    ORDER_FEE_PROFILE_ROUNDING_PRECISION_XPATH = '//*[@formcontrolname = "commRoundingPrecision"]'
    ORDER_FEE_PROFILE_ROUNDING_MODULUS_XPATH = '//*[@formcontrolname = "commRoundingModulus"]'

    # Commission Profile Points
    COMMISSION_PROFILE_POINTS_PLUS_BUTTON_XPATH = '//*[@class="sub-list-label"]/parent::div//*[@class="nb-plus piloted-table-action"]'
    COMMISSION_PROFILE_POINTS_CHECKMARK_BUTTON_XPATH = '//*[@class="sub-list-label"]/parent::div//*[@class="nb-checkmark"]'
    COMMISSION_PROFILE_POINTS_CANCEL_BUTTON_XPATH = '//*[@class="sub-list-label"]/parent::div//*[@class="nb-close"]'
    COMMISSION_PROFILE_POINTS_EDIT_BUTTON_XPATH = '//*[@class="sub-list-label"]/parent::div//*[@class="nb-edit piloted-table-action"]'
    COMMISSION_PROFILE_POINTS_DELETE_BUTTON_XPATH = '//*[@class="sub-list-label"]/parent::div//*[@class="nb-trash piloted-table-action"]'

    COMMISSION_PROFILE_BASE_VALUE_XPATH = '//*[@placeholder = "Base Value *"]'
    COMMISSION_PROFILE_MIN_COMMISSION_XPATH = '//*[@placeholder = "Min Commission"]'
    COMMISSION_PROFILE_UPPER_LIMIT_XPATH = '//*[@placeholder = "Upper Limit"]'

    # Exec fee profile
    EXEC_FEE_PROFILE_COMMISSION_PROFILE_NAME_XPATH = "//*[@placeholder = 'Commission Profile Name *']"
    EXEC_FEE_PROFILE_PLUS_BUTTON_XPATH = '//*[@class="cp-instr-table-body"]//*[@class="nb-plus ng2-main-add-btn"]'
    EXEC_FEE_PROFILE_CHECKMARK_BUTTON_XPATH = '//*[@class="cp-instr-table-body"]//*[@class="nb-checkmark"]'
    EXEC_FEE_PROFILE_CANCEL_BUTTON_XPATH = '//*[@class="cp-instr-table-body"]//*[@class="nb-close ng2-main-cancel-btn"]'
    EXEC_FEE_PROFILE_EDIT_BUTTON_XPATH = '//*[@class="cp-instr-table-body"]//*[@class="nb-edit ng2-main-edit-btn"]'
    EXEC_FEE_PROFILE_DELETE_BUTTON_XPATH = '//*[@class="cp-instr-table-body"]//*[@class="nb-trash"]'

    EXEC_FEE_PROFILE_DESCRIPTION_XPATH = '//*[@formcontrolname = "commProfileDescription"]'
    EXEC_FEE_PROFILE_COMM_XUNIT_XPATH = '//*[@id = "commXUnit"]'
    EXEC_FEE_PROFILE_VENUE_COMMISSION_PROFILE_ID_XPATH = '//*[@formcontrolname = "venueCommissionProfileID"]'
    EXEC_FEE_PROFILE_COMM_TYPE_XPATH = '//*[@id = "commType"]'
    EXEC_FEE_PROFILE_COMM_ALGORITHM_XPATH = '//*[@id = "commAlgorithm"]'
    EXEC_FEE_PROFILE_MAX_COMMISSION_XPATH = '//*[@formcontrolname = "maxCommission"]'
    EXEC_FEE_PROFILE_CURRENCY_XPATH = '//*[@id = "commCurrency"]'
    EXEC_FEE_PROFILE_ROUNDING_DIRECTION_XPATH = '//*[@id = "commRoundingDirection"]'
    EXEC_FEE_PROFILE_ROUNDING_PRECISION_XPATH = '//*[@formcontrolname = "commRoundingPrecision"]'
    EXEC_FEE_PROFILE_ROUNDING_MODULUS_XPATH = '//*[@formcontrolname = "commRoundingModulus"]'


    # Dimensions tab
    DIMENSIONS_TAB_INSTR_TYPE_XPATH = '//*[@id = "instrType"]'
    DIMENSIONS_TAB_SIDE_XPATH = '//*[@id = "side"]'
    DIMENSIONS_TAB_COUNTRY_OF_ISSUE_XPATH = '//*[@id = "countryOfIssue_ext"]'
    DIMENSIONS_TAB_VENUE_XPATH = '//*[@id = "venue"]'
    DIMENSIONS_TAB_INSTRUMENT_LIST_XPATH = '//*[@id = "instrumentList"]'
    DIMENSIONS_TAB_INSTRUMENT_GROUP_XPATH = '//*[@id = "instrumentGroup"]'
