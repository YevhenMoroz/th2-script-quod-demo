class FeesConstants:
    FEES_PAGE_TITLE_XPATH = "//span[@class='entity-title left'][normalize-space()='Fees']"

    REFRESH_PAGE_BUTTON_XPATH = "//*[@data-name='refresh']"
    DOWNLOAD_PDF_BUTTON_XPATH = "//*[@data-name='download']"
    DOWNLOAD_PDF_AT_MORE_ACTIONS_XPATH = "//nb-icon[@icon='download-outline']//*[@data-name='download']"
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
    NEW_BUTTON_XPATH = '//*[text()="New"]'
    USER_ICON_AT_RIGHT_CORNER = "//*[@class='control-item icon-btn context-menu-host']"
    LOGOUT_BUTTON_XPATH = "//*[text()='Logout']"
    GO_BACK_BUTTON_XPATH = "//*[text()='Go Back']"
    DISPLAYED_ENTITY_XPATH = "//*[text()='{}']"
    DROP_DOWN_MENU_XPATH = '//*[@class="option-list"]//nb-option | span'
    FOOTER_WARNING_XPATH = '//nb-card-footer//*[@outline="danger"]//span'

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
    ORDER_FEE_PROFILE_COMMISSION_PROFILE_FILTER_XPATH = '//*[normalize-space()="Commission Profile Name"]//*[@placeholder="Filter"]'
    ORDER_FEE_PROFILE_COMMISSION_PROFILE_ENTITY_XPATH = '//*[normalize-space()="Commission Profile Name"]//..//span[@class="ng-star-inserted"][normalize-space()="{}"]'
    ORDER_FEE_PROFILE_COMMISSION_PROFILE_PREVIEW_XPATH = '//*[@class="form-table-details-wrapper ng-star-inserted"]'
    ORDER_FEE_PROFILE_PLUS_BUTTON_XPATH = '//*[@class="cp-instr-table-body"]//*[@nbtooltip="Add"]'
    ORDER_FEE_PROFILE_CHECKMARK_BUTTON_XPATH = '//*[@class="cp-instr-table-body"]//*[@data-name="checkmark"]'
    ORDER_FEE_PROFILE_CANCEL_BUTTON_XPATH = '//*[@class="cp-instr-table-body"]//*[@data-name="close"]'
    ORDER_FEE_PROFILE_EDIT_BUTTON_XPATH = '//*[@class="cp-instr-table-body"]//*[@data-name="edit"]'
    ORDER_FEE_PROFILE_DELETE_BUTTON_XPATH = '//*[@class="cp-instr-table-body"]//*[@data-name="trash-2"]'

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
    COMMISSION_PROFILE_POINTS_PLUS_BUTTON_XPATH = '//*[@class="sub-list-label"]/parent::div//*[@data-name="plus"]'
    COMMISSION_PROFILE_POINTS_CHECKMARK_BUTTON_XPATH = '//*[@class="sub-list-label"]/parent::div//*[@data-name="checkmark"]'
    COMMISSION_PROFILE_POINTS_CANCEL_BUTTON_XPATH = '//*[@class="sub-list-label"]/parent::div//*[@data-name="close"]'
    COMMISSION_PROFILE_POINTS_EDIT_BUTTON_XPATH = '//*[@class="sub-list-label"]/parent::div//*[@data-name="edit"]'
    COMMISSION_PROFILE_POINTS_DELETE_BUTTON_XPATH = '//*[@class="sub-list-label"]/parent::div//*[@data-name="trash-2"]'

    COMMISSION_PROFILE_BASE_VALUE_XPATH = '//*[@placeholder = "Base Value *"]'
    COMMISSION_PROFILE_MIN_COMMISSION_XPATH = '//*[@placeholder = "Min Commission"]'
    COMMISSION_PROFILE_UPPER_LIMIT_XPATH = '//*[@placeholder = "Upper Limit"]'
    UPPER_LIMIT_COLUMN_XPATH = '//*[contains(text(), "Commission Profile Points")]//..//td[4]'
    COMMISSION_PROFILE_SLOPE_XPATH = '//*[@placeholder = "Slope"]'

    # Exec fee profile
    EXEC_FEE_PROFILE_COMMISSION_PROFILE_FILTER_XPATH = '//*[normalize-space()="Commission Profile Name"]//*[@placeholder="Filter"]'
    EXEC_FEE_PROFILE_COMMISSION_PROFILE_NAME_XPATH = "//*[@placeholder = 'Commission Profile Name *']"
    EXEC_FEE_PROFILE_PLUS_BUTTON_XPATH = '//*[@class="cp-instr-table-body"]//*[@nbtooltip="Add"]'
    EXEC_FEE_PROFILE_CHECKMARK_BUTTON_XPATH = '//*[@class="cp-instr-table-body"]//*[@data-name="checkmark"]'
    EXEC_FEE_PROFILE_CANCEL_BUTTON_XPATH = '//*[@class="cp-instr-table-body"]//*[@data-name="close"]'
    EXEC_FEE_PROFILE_EDIT_BUTTON_XPATH = '//*[@class="cp-instr-table-body"]//*[@data-name="edit"]'
    EXEC_FEE_PROFILE_DELETE_BUTTON_XPATH = '//*[@class="cp-instr-table-body"]//*[@data-name="trash-2"]'
    EXEC_FEE_PROFILE_DISPLAYED_PROFILE_XPATH = '//*[normalize-space()="{}"]'

    EXEC_FEE_PROFILE_DESCRIPTION_XPATH = '//*[@formcontrolname = "commProfileDescription"]'
    EXEC_FEE_PROFILE_COMM_XUNIT_XPATH = '//*[@id = "commXUnit"]/button'
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
    DIMENSIONS_TAB_VENUE_LIST_XPATH = '//*[normalize-space()="Dimensions"]//..//*[@id="venueList"]'
    DIMENSIONS_TAB_INSTRUMENT_LIST_XPATH = '//*[@id = "instrumentList"]'
    DIMENSIONS_TAB_INSTRUMENT_GROUP_XPATH = '//*[@id = "instrumentGroup"]'
    DIMENSIONS_TAB_DROP_DOWN_MENU_ITEMS_XPATH = '//*[@class="option-list"]//span'
    DIMENSIONS_TAB_ROUTE_XPATH = '//*[@id="route"]'
    DIMENSIONS_TAB_CLIENT_LIST_XPATH = '//*[@id="clientList"]'
