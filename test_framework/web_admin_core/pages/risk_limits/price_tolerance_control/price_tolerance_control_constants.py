class PriceToleranceControlConstants:
    PRICE_TOLERANCE_CONTROL_PAGE_TITLE_XPATH = "//span[@class='entity-title left'][text()='Price Tolerance Control ']"
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
    NEW_BUTTON_XPATH = '//*[text()="New"]'
    USER_ICON_AT_RIGHT_CORNER = "//*[@class='control-item icon-btn context-menu-host']"
    LOGOUT_BUTTON_XPATH = "//*[text()='Logout']"
    GO_BACK_BUTTON_XPATH = "//*[text()='Go Back']"
    MAIN_PAGE_DOWNLOAD_CSV_BUTTON_XPATH = '//*[@data-name="download"]'
    INCORRECT_OR_MISSING_VALUES_XPATH = "//*[text()='Incorrect or missing values']"

    # Main page
    MAIN_PAGE_NAME_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[1]//input'
    MAIN_PAGE_ID_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[2]//input'
    MAIN_PAGE_CLIENT_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[3]//input'
    MAIN_PAGE_USER_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[4]//input'
    MAIN_PAGE_VENUE_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[5]//input'
    MAIN_PAGE_CLIENT_GROUP_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[6]//input'
    MAIN_PAGE_LISTING_GROUP_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[7]//input'
    MAIN_PAGE_NAME_XPATH = '//*[@col-id="priceControlApplName"]//span//span[4]'
    MAIN_PAGE_ID_XPATH = '//*[@col-id="externalPriceControlApplID"]//span//span[4]'
    MAIN_PAGE_CLIENT_XPATH = '//*[@col-id="accountGroupID"]//span//span[4]'
    MAIN_PAGE_USER_XPATH = '//*[@col-id="userID"]//span//span[4]'
    MAIN_PAGE_VENUE_XPATH = '//*[@col-id="venueID"]//span//span[4]'
    MAIN_PAGE_CLIENT_GROUP_XPATH = '//*[@col-id="clientGroup.clientGroupName"]//span//span[4]'
    MAIN_PAGE_LISTING_GROUP_XPATH = '//*[@col-id="listingGroup.listingGroupName"]//span//span[4]'
    SEARCHED_VALUE_XPATH = '//*[text()="{}"]'


    # Values tab

    VALUES_TAB_NAME_XPATH = '//*[@formcontrolname="priceControlApplName"]'
    VALUES_TAB_EXTERNAL_ID_XPATH = '//*[@formcontrolname="externalPriceControlApplID"]'
    VALUES_TAB_LISTING_GROUP_XPATH = '//*[@id="listingGroup"]'
    VALUES_TAB_INSTR_TYPE_XPATH = '//*[@id="instrType"]'
    VALUES_TAB_LISTING_XPATH = '//*[@id="listing"]'
    VALUES_TAB_WILDCARD_LISTING_CHECKBOX_XPATH = '//*[text()="Wildcard Listing"]/preceding-sibling::span'
    VALUES_TAB_USER_XPATH = '//*[@id="user"]'
    VALUES_TAB_CLIENT_XPATH = '//*[@id="accountGroup"]'
    VALUES_TAB_CLIENT_GROUP_XPATH = '//*[@id="clientGroup"]'
    VALUES_TAB_VENUE_XPATH = '//*[@id="venue"]'
    VALUES_TAB_SUB_VENUE_XPATH = '//*[@id="subVenue"]'


    # Ordr tab

    ORDR_TAB_PLUS_BUTTON_XPATH = '//*[@class="nb-plus ng2-main-add-btn"]'
    ORDR_TAB_CHECKMARK_BUTTON_XPATH = '//*[@class="nb-checkmark"]'
    ORDR_TAB_CLOSE_BUTTON_XPATH = '//*[@class="nb-close ng2-main-cancel-btn"]'
    ORDR_TAB_EDIT_BUTTON_XPATH = '//*[@class="nb-edit ng2-main-edit-btn"]'
    ORDR_TAB_DELETE_BUTTON_XPATH = '//*[@class="nb-trash"]'

    ORDR_TAB_ORD_TYPE_XPATH = '//*[@placeholder="Ord Type *"]'
    ORDR_TAB_ORD_TYPE_FILTER_XPATH = '//*[@class="ng2-smart-th ordType ng-star-inserted"]//input'

    ORDR_TAB_SIDE_XPATH = '//*[@id="side"]'
    ORDR_TAB_TRADING_PHASE_XPATH = '//*[@id="standardTradingPhase"]'
    ORDR_TAB_MAX_QTY_ADV_XPATH = '//*[@formcontrolname="maxQtyADVPercent"]'
    ORDR_TAB_AGGRESSOR_INDICATOR_XPATH = '//*[text()="Aggressor Indicator"]/preceding-sibling::span'
    ORDR_TAB_STATIC_PROFILE_XPATH = '//*[@id="staticPriceCtrlProfile"]'
    ORDR_TAB_DYNAMIC_PROFILE_XPATH = '//*[@id="dynamicPriceCtrlProfile"]'
    ORDR_TAB_DYNAMIC_PROFILE_MANAGE_BUTTON_XPATH = '//*[text()="Manage"]'

    # Manage Dynamic profile sub wizard

    DYNAMIC_PROFILE_SUB_WIZARD_PLUS_BUTTON_XPATH = '//*[@class="nb-plus ng2-add-btn"]'
    DYNAMIC_PROFILE_SUB_WIZARD_CHECKMARK_BUTTON_XPATH = '//*[@class="nb-checkmark"]'
    DYNAMIC_PROFILE_SUB_WIZARD_CLOSE_BUTTON_XPATH = '//*[@class="nb-close ng2-cancel-btn"]'
    DYNAMIC_PROFILE_SUB_WIZARD_EDIT_BUTTON_XPATH = '//*[@class="nb-edit ng2-main-edit-btn"]'
    DYNAMIC_PROFILE_SUB_WIZARD_DELETE_BUTTON_XPATH = '//*[@class="nb-trash"]'

    DYNAMIC_PROFILE_SUB_WIZARD_EXTERNAL_PRICE_CTRL_PROFILE_ID_FILTER_XPATH = '//*[@class="externalPriceCtrlProfileID ng2-smart-th ng-star-inserted"]//input'
    DYNAMIC_PROFILE_SUB_WIZARD_EXTERNAL_PRICE_CTRL_PROFILE_ID_XPATH = '//*[@placeholder="External Price Ctrl Profile ID *"]'
    DYNAMIC_PROFILE_SUB_WIZARD_PRICE_CONTROL_TYPE_FILTER_XPATH = '//*[@class="ng2-smart-th priceControlType ng-star-inserted"]//input'
    DYNAMIC_PROFILE_SUB_WIZARD_PRICE_CONTROL_TYPE_XPATH = '//*[@placeholder="Price Control Type *"]'
    DYNAMIC_PROFILE_SUB_WIZARD_REFERENCE_PRICE_TYPE_1_FILTER_XPATH = '//*[@class="ng2-smart-th referencePriceType1 ng-star-inserted"]//input'
    DYNAMIC_PROFILE_SUB_WIZARD_REFERENCE_PRICE_TYPE_1_XPATH = '//*[@placeholder="Reference Price Type 1 *"]'
    DYNAMIC_PROFILE_SUB_WIZARD_REFERENCE_PRICE_TYPE_2_FILTER_XPATH = '//*[@class="ng2-smart-th referencePriceType2 ng-star-inserted"]//input'
    DYNAMIC_PROFILE_SUB_WIZARD_REFERENCE_PRICE_TYPE_2_XPATH = '//*[@placeholder="Reference Price Type 2"]'
    DYNAMIC_PROFILE_SUB_WIZARD_REFERENCE_PRICE_TYPE_3_FILTER_XPATH = '//*[@class="ng2-smart-th referencePriceType3 ng-star-inserted"]//input'
    DYNAMIC_PROFILE_SUB_WIZARD_REFERENCE_PRICE_TYPE_3_XPATH = '//*[@placeholder="Reference Price Type 3"]'
    DYNAMIC_PROFILE_SUB_WIZARD_REFERENCE_PRICE_TYPE_4_FILTER_XPATH = '//*[@class="ng2-smart-th referencePriceType4 ng-star-inserted"]//input'
    DYNAMIC_PROFILE_SUB_WIZARD_REFERENCE_PRICE_TYPE_4_XPATH = '//*[@placeholder="Reference Price Type 4"]'
    DYNAMIC_PROFILE_SUB_WIZARD_OK_BUTTON_XPATH = '//*[text()="OK"]'

    # Price control profile points

    PRICE_CONTROL_PROFILE_POINTS_SUB_WIZARD_PLUS_BUTTON_XPATH = '//*[@class="nb-plus sub-table-action"]'
    PRICE_CONTROL_PROFILE_POINTS_SUB_WIZARD_CHECKMARK_BUTTON_XPATH = '//*[@class="nb-checkmark"]'
    PRICE_CONTROL_PROFILE_POINTS_SUB_WIZARD_CLOSE_BUTTON_XPATH = '//*[@class="nb-close"]'
    PRICE_CONTROL_PROFILE_POINTS_SUB_WIZARD_EDIT_BUTTON_XPATH = '//*[@class="nb-edit sub-table-action"]'
    PRICE_CONTROL_PROFILE_POINTS_SUB_WIZARD_DELETE_BUTTON_XPATH = '//*[@class="nb-trash sub-table-action"]'

    PRICE_CONTROL_PROFILE_POINTS_SUB_WIZARD_HARD_LIMIT_PRICE_FILTER_XPATH = '//*[@class="hardLimitPrice ng2-smart-th ng-star-inserted"]//input'
    PRICE_CONTROL_PROFILE_POINTS_SUB_WIZARD_HARD_LIMIT_PRICE_XPATH = '//*[@placeholder="Hard Limit Price *"]'
    PRICE_CONTROL_PROFILE_POINTS_SUB_WIZARD_SOFT_LIMIT_PRICE_FILTER_XPATH = '//*[@class="ng2-smart-th softLimitPrice ng-star-inserted"]//input'
    PRICE_CONTROL_PROFILE_POINTS_SUB_WIZARD_SOFT_LIMIT_PRICE_XPATH = '//*[@placeholder="Soft Limit Price"]'
    PRICE_CONTROL_PROFILE_POINTS_SUB_WIZARD_UPPER_LIMIT_FILTER_XPATH = '//*[@class="ng2-smart-th upperLimit ng-star-inserted"]//input'
    PRICE_CONTROL_PROFILE_POINTS_SUB_WIZARD_UPPER_LIMIT_XPATH = '//*[@placeholder="Upper Limit"]'

    # Assignments tab
    ASSIGNMENTS_TAB_INSTITUTIONS = '//*[normalize-space()="Assignments"]/..//input[@id="institution"]'



















































