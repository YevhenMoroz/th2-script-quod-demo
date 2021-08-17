class CommissionsConstants:
    COMMISSIONS_PAGE_TITLE_XPATH = "//span[@class='entity-title left'][text()='Commissions ']"
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

    # main page
    MAIN_PAGE_NAME_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[1]//input'
    MAIN_PAGE_DESCRIPTION_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[2]//input'
    MAIN_PAGE_INSTR_TYPE_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[3]//input'
    MAIN_PAGE_VENUE_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[4]//input'
    MAIN_PAGE_SIDE_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[5]//input'
    MAIN_PAGE_EXECUTION_POLICY_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[6]//input'
    MAIN_PAGE_VIRTUAL_POLICY_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[7]//input'
    MAIN_PAGE_DOWNLOAD_CSV_BUTTON_XPATH = '//*[@data-name="download"]'

    # dimensions tab
    DIMENSIONS_TAB_INSTR_TYPE_XPATH = '//*[@id="instrType"]'
    DIMENSIONS_TAB_VENUE_XPATH = '//*[@id="venue"]'
    DIMENSIONS_TAB_SIDE_XPATH = '//*[@id="side"]'
    DIMENSIONS_TAB_EXECUTION_POLICY_XPATH = '//*[@id="executionPolicy"]'
    DIMENSIONS_TAB_VIRTUAL_ACCOUNT_XPATH = '//*[@id="account"]'
    DIMENSIONS_TAB_CLIENT_XPATH = '//*[@id="accountGroup"]'
    DIMENSIONS_TAB_CLIENT_GROUP_XPATH = '//*[@id="clientGroup"]'
    DIMENSIONS_TAB_CLIENT_LIST_XPATH = '//*[@id="clientList"]'
    DIMENSIONS_TAB_COMMISSION_AMOUNT_TYPE_XPATH = '//*[@id="commissionAmountType"]'
    DIMENSIONS_TAB_COMMISSION_PROFILE_XPATH = '//*[@id="commissionProfile"]'
    DIMENSIONS_TAB_MANAGE_COMMISSION_PROFILE_XPATH = '//*[text()="Manage"]'

    # values tab
    VALUES_TAB_NAME_XPATH = '//*[@formcontrolname="clCommissionName"]'
    VALUES_TAB_DESCRIPTION_XPATH = '//*[@formcontrolname="clCommissionDescription"]'
    VALUES_TAB_RE_CALCULATE_FOR_ALLOCATIONS_XPATH = '//*[text()="Re-Calculate for Allocations"]/preceding-sibling::span'

    # commission profiles
    COMMISSION_PROFILES_COMMISSION_PROFILE_NAME_XPATH = "//*[@placeholder = 'Commission Profile Name *']"
    COMMISSION_PROFILES_PLUS_BUTTON_XPATH = '//*[@class="cp-instr-table-body"]//*[@class="nb-plus ng2-main-add-btn"]'
    COMMISSION_PROFILES_CHECKMARK_BUTTON_XPATH = '//*[@class="cp-instr-table-body"]//*[@class="nb-checkmark"]'
    COMMISSION_PROFILES_CANCEL_BUTTON_XPATH = '//*[@class="cp-instr-table-body"]//*[@class="nb-close ng2-main-cancel-btn"]'
    COMMISSION_PROFILES_EDIT_BUTTON_XPATH = '//*[@class="cp-instr-table-body"]//*[@class="nb-edit ng2-main-edit-btn"]'
    COMMISSION_PROFILES_DELETE_BUTTON_XPATH = '//*[@class="cp-instr-table-body"]//*[@class="nb-trash"]'

    COMMISSION_PROFILES_DESCRIPTION_XPATH = '//*[@formcontrolname = "commProfileDescription"]'
    COMMISSION_PROFILES_COMM_XUNIT_XPATH = '//*[@id = "commXUnit"]'
    COMMISSION_PROFILES_VENUE_COMMISSION_PROFILE_ID_XPATH = '//*[@formcontrolname = "venueCommissionProfileID"]'
    COMMISSION_PROFILES_COMM_TYPE_XPATH = '//*[@id = "commType"]'
    COMMISSION_PROFILES_COMM_ALGORITHM_XPATH = '//*[@id = "commAlgorithm"]'
    COMMISSION_PROFILES_MAX_COMMISSION_XPATH = '//*[@formcontrolname = "maxCommission"]'
    COMMISSION_PROFILES_CURRENCY_XPATH = '//*[@id = "commCurrency"]'
    COMMISSION_PROFILES_ROUNDING_DIRECTION_XPATH = '//*[@id = "commRoundingDirection"]'
    COMMISSION_PROFILES_ROUNDING_PRECISION_XPATH = '//*[@formcontrolname = "commRoundingPrecision"]'
    COMMISSION_PROFILES_ROUNDING_MODULUS_XPATH = '//*[@formcontrolname = "commRoundingModulus"]'

    # Commission Profile Points
    COMMISSION_PROFILE_POINTS_PLUS_BUTTON_XPATH = '//*[@class="points-table-wrapper"]//*[@class="nb-plus piloted-table-action"]'
    COMMISSION_PROFILE_POINTS_CHECKMARK_BUTTON_XPATH = '//*[@class="points-table-wrapper"]//*[@class="nb-checkmark"]'
    COMMISSION_PROFILE_POINTS_CANCEL_BUTTON_XPATH = '//*[@class="points-table-wrapper"]//*[@class="nb-close"]'
    COMMISSION_PROFILE_POINTS_EDIT_BUTTON_XPATH = '//*[@class="points-table-wrapper"]//*[@class="nb-edit piloted-table-action"]'
    COMMISSION_PROFILE_POINTS_DELETE_BUTTON_XPATH = '//*[@class="points-table-wrapper"]//*[@class="nb-trash piloted-table-action"]'

    COMMISSION_PROFILE_BASE_VALUE_XPATH = '//*[@placeholder = "Base Value *"]'
    COMMISSION_PROFILE_MIN_COMMISSION_XPATH = '//*[@placeholder = "Min Commission"]'
    COMMISSION_PROFILE_UPPER_LIMIT_XPATH = '//*[@placeholder = "Upper Limit"]'
