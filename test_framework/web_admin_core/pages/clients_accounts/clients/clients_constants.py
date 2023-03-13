class ClientsConstants:
    CLIENTS_PAGE_TITLE_XPATH = '//span[@class="entity-title left"][normalize-space()="Clients"]'
    WIZARD_PAGE_TITLE_XPATH = '//*[@class="breadcrumbs entity-title"]'

    REFRESH_PAGE_BUTTON_XPATH = "//*[@data-name='refresh']"
    DOWNLOAD_PDF_BUTTON_XPATH = "//*[@nbtooltip = 'Download PDF']//*[@data-name='download']"
    SAVE_CHANGES_BUTTON_XPATH = "//*[contains(text(), 'Save Changes')]"
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
    NEW_BUTTON_XPATH = '//*[normalize-space()="Clients"]//..//*[normalize-space()="New"]'
    USER_ICON_AT_RIGHT_CORNER = "//*[@class='control-item icon-btn context-menu-host']"
    LOGOUT_BUTTON_XPATH = "//*[text()='Logout']"
    GO_BACK_BUTTON_XPATH = "//*[text()='Go Back']"
    ENABLE_DISABLE_TOGGLE_BUTTON_XPATH = "//div[contains(@class, 'toggle')]"
    INCORRECT_OR_MISSING_VALUES_MESSAGE_XPATH = "//*[text()='Incorrect or missing values']"
    REQUEST_FAILED_MESSAGE_XPATH = "//nb-toast[contains(@class, 'danger')]"
    CLIENT_LOAD_FILTER = "//*[@id='lookup-input']"
    LOAD_BUTTON = "//button[contains(@class, 'lookup-btn')]"
    POPUP_TEXT_XPATH = "//nb-toast//span[@class='title subtitle']"
    DISPLAYED_CLIENT_XPATH = "//*[text()='{}']"
    FOOTER_WARNING_XPATH = '//nb-card-footer//nb-alert[@outline="danger"]'
    DROP_DOWN_MENU_XPATH = '//*[@class="option-list"]//span'


    # main page
    MAIN_PAGE_NAME_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[1]//input'
    MAIN_PAGE_DESCRIPTION_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[2]//input'
    MAIN_PAGE_CLEARING_ACCOUNT_TYPE_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[3]//input'
    MAIN_PAGE_BOOKING_INS_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[4]//input'
    MAIN_PAGE_ALLOCATION_PREFERENCE_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[5]//input'
    MAIN_PAGE_DISCLOSE_EXEC_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[6]//input'
    MAIN_PAGE_CLIENT_GROUP_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[7]//input'
    MAIN_PAGE_CLEARING_ACCOUNT_TYPE_XPATH = '//*[@col-id="clearingAccountType"]//span//span[4]'
    MAIN_PAGE_CLIENT_NAME = '(//*[@ref="eCenterViewport"]//span[@ref="eValue"])[1]'

    # values tab
    VALUES_TAB_ID_XPATH = '//*[@id="accountGroupID"]'
    VALUES_NAME_XPATH = '//*[@formcontrolname="accountGroupName"]'
    VALUES_TAB_EXT_ID_CLIENT_XPATH = '//*[@formcontrolname="clientAccountGroupID"]'
    VALUES_TAB_CLEARING_ACCOUNT_TYPE_XPATH = '//*[@id="clearingAccountType"]'
    VALUES_TAB_DESCRIPTION_XPATH = '//*[@formcontrolname="accountGroupDesc"]'
    VALUES_TAB_DISCLOSE_EXEC_XPATH = '//*[@id="discloseExec"]'
    VALUES_TAB_CLIENT_GROUP_XPATH = '//*[@id="clientGroup"]'
    VALUES_TAB_INVALID_TICK_SIZE_POLICY_XPATH = '//*[@id="invalidTickSizePolicy"]'
    VALUES_TAB_VIRTUAL_ACCOUNT_XPATH = '//*[@id="virtualAccount"]'
    VALUES_TAB_EXTERNAL_ORD_ID_FORMAT_XPATH = '//*[@formcontrolname="externalOrdIDFormat"]'
    VALUES_TAB_BOOKING_INST_XPATH = '//*[@id="bookingInst"]'
    VALUES_TAB_ALLOCATION_PREFERENCE_XPATH = '//*[@id="allocationInst"]'
    VALUES_TAB_CONFIRMATION_SERVICE_XPATH = '//*[@id="confirmationService"]'
    VALUES_TAB_BLOCK_APPROVAL_XPATH = '//*[@id="blockApproval"]'
    VALUES_TAB_ROUNDING_DIRECTION_XPATH = '//*[@id="roundingDirection"]'
    VALUES_TAB_FIX_MATCHING_PROFILE_XPATH = '//*[@id="blockMatchingProfile"]'
    VALUES_TAB_COUNTERPART_XPATH = '//*[@id="counterpart"]'
    VALUES_TAB_MANAGE_COUNTERPART_XPATH = '//*[@id="counterpart"]//ancestor::div[@class="row"]//button'
    VALUES_TAB_SHORT_SELL_ACCOUNT_CHECKBOX_XPATH = '//*[text()="Short Sell Account"]/preceding-sibling::span'
    VALUES_TAB_DUMMY_CHECKBOX_XPATH = '//*[text()="Dummy"]/preceding-sibling::span'
    VALUES_TAB_PRICE_PRECISION_XPATH = '//*[@formcontrolname="pxPrecision"]'
    VALUES_TAB_ALLOCATION_MATCHING_SERVICE_XPATH = '//*[@id="confirmationService"]'
    VALUES_TAB_GIVE_UP_SERVICE = '//*[@id="giveUpService"]'
    VALUES_TAB_EXTERNAL_GIVE_UP_SERVICE = '//*[@id="extGiveUpService"]'
    VALUES_TAB_GIVE_UP_MATCHING_ID = '//*[@id="giveUpMatchingID"]'
    VALUES_TAB_EXTERNAL_GIVE_UP_SERVICE_MANAGE_BUTTON = '//*[@id="extGiveUpService"]//ancestor::div[@class="row"]//button[@nbbutton]'
    VALUES_TAB_EXTERNAL_ALLOCATION_MATCHING_SERVICE_XPATH = '//div[@id="External Allocation Matching Service"]'
    VALUES_TAB_MANAGE_EXTERNAL_ALLOCATION_MATCHING_SERVICE_BUTTON_XPATH = '//*[@id="actGrpExtConfirmService"]//following::button[1]'
    VALUES_TAB_DEFAULT_ACCOUNT_XPATH = '//*[@id="defaultAccount"]'
    VALUES_TAB_ORDER_ATTRIBUTE = '//*[@id="orderAttributeType"]'

    # Assignments tab
    ASSIGNMENTS_TAB_USER_MANAGER_XPATH = '//*[@id="accountMgrUser"]'
    ASSIGNMENTS_TAB_USER_MANAGER_LABEL_XPATH = '//label[@for="accountMgrUser"][text()="User Manager"]'
    ASSIGNMENTS_TAB_DESK_XPATH = '//div[@id="Desks *"]'
    ASSIGNMENTS_TAB_DESK_LABEL_XPATH = '//label[@for="managerDesk"][text()="Desks"]'
    ASSIGNMENTS_TAB_ACCOUNTS_XPATH = '//div[text()="Accounts"]/../..//*[@class="linked-entities-wrapper"]//a'
    ASSIGNMENTS_TAB_ACCOUNT_NAME_XPATH = '//*[normalize-space()="Assignments"]//..//*[@class="linked-entities-wrapper"]//*[normalize-space()="{}"]'
    ASSIGNMENTS_TAB_CLIENT_LISTS_XPATH = '//div[text()="Client List"]/../..//*[@class="linked-entities-wrapper"]//a'

    # External sources tab
    EXTERNAL_SOURCES_TAB_BIC_VENUE_ACT_GRP_NAME = '//*[@id="BIC"]'
    EXTERNAL_SOURCES_TAB_DTCC_VENUE_ACT_GRP_NAME = '//*[@id="DTCC"]'
    EXTERNAL_SOURCES_TAB_OMGEO_VENUE_ACT_GRP_NAME = '//*[@id="OMGEO"]'
    EXTERNAL_SOURCES_TAB_OTHER_VENUE_ACT_GRP_NAME = '//*[@id="Other"]'
    EXTERNAL_SOURCES_TAB_SID_VENUE_ACT_GRP_NAME = '//*[@id="SID"]'
    EXTERNAL_SOURCES_TAB_TFM_VENUE_ACT_GRP_NAME = '//*[@id="TFM"]'

    EXTERNAL_SOURCES_TAB_BO_FIELD1 = '//*[@formcontrolname="allocInstructionMisc0"]'
    EXTERNAL_SOURCES_TAB_BO_FIELD2 = '//*[@formcontrolname="allocInstructionMisc1"]'
    EXTERNAL_SOURCES_TAB_BO_FIELD3 = '//*[@formcontrolname="allocInstructionMisc2"]'
    EXTERNAL_SOURCES_TAB_BO_FIELD4 = '//*[@formcontrolname="allocInstructionMisc3"]'
    EXTERNAL_SOURCES_TAB_BO_FIELD5 = '//*[@formcontrolname="allocInstructionMisc4"]'

    # Managements tab

    MANAGEMENTS_TAB_USER_MANAGER_XPATH = '//*[@id="accountMgrUser"]'
    MANAGEMENTS_TAB_DESK_MANAGER_XPATH = '//*[@id="accountMgrDesk"]'
    MANAGEMENTS_TAB_FIX_ORDER_RECIPIENT_USER_XPATH = '//*[@id="FIXOrderRecipientUser"]'
    MANAGEMENTS_TAB_FIX_ORDER_RECIPIENT_DESK_XPATH = '//*[@id="FIXOrderRecipientDesk"]'
    MANAGEMENTS_TAB_BENEFICIARY_DESK_XPATH = '//*[@id="beneficiaryDesk"]'
    MANAGEMENTS_TAB_MIDDLE_OFFICE_USER_XPATH = '//*[@id="middleOfficeUser"]'
    MANAGEMENTS_TAB_MIDDLE_OFFICE_DESK_XPATH = '//*[@id="middleOfficeDesk"]'

    # Policies tab

    POLICIES_TAB_DEFAULT_EXECUTION_STRATEGY_XPATH = '//*[@id="defaultAlgoPolicy"]'
    POLICIES_TAB_DEFAULT_SOR_EXECUTION_STRATEGY_XPATH = '//*[@id="defaultSORAlgoPolicy"]'
    POLICIES_TAB_DEFAULT_ROUTING_INSTRUCTION_XPATH = '//*[@id="defaultRoutingInstruction"]'
    POLICIES_TAB_DEFAULT_ALGO_TYPE_XPATH = '//*[@id="defaultAlgoType"]'
    POLICIES_TAB_CUSTOM_VALIDATION_RULES_XPATH = '//*[@id="validParamGroup"]'
    POLICIES_TAB_MANAGE_CUSTOM_VALIDATION_RULES_XPATH = '//*[@class="col-sm"]'
    POLICIES_TAB_LIST_OF_DEFAULT_STRATEGIES_XPATH = "//*[@class='empty-option font-italic nb-transition ng-star-inserted']//*[text()='Default']"
    # MANAGE sub wizard
    VALID_PARAM_GROUPS_TAB_PLUS_BUTTON_XPATH = '//*[@class="account-group-valid-param-group-settings"]//*[@class="nb-plus ng2-add-btn"]'
    VALID_PARAM_GROUPS_TAB_CHECKMARK_BUTTON_XPATH = '//*[@class="account-group-valid-param-group-settings"]//*[@class="nb-checkmark"]'
    VALID_PARAM_GROUPS_TAB_CANCEL_BUTTON_XPATH = '//*[@class="account-group-valid-param-group-settings"]//*[@class="nb-close ng2-cancel-btn"]'
    VALID_PARAM_GROUPS_TAB_EDIT_BUTTON_XPATH = '//*[@class="account-group-valid-param-group-settings"]//*[@class="nb-edit ng2-edit-btn"]'
    VALID_PARAM_GROUPS_TAB_DELETE_BUTTON_XPATH = '//*[@class="account-group-valid-param-group-settings"]//*[@class="nb-trash"]'

    VALID_PARAM_GROUPS_TAB_NAME_XPATH = '//*[@placeholder="Name *"]'
    VALID_PARAM_GROUPS_TAB_NAME_FILTER_XPATH = '//*[@class="ng2-smart-th paramGroupName ng-star-inserted"]//*[@placeholder="Filter"]'

    VALID_PARAM_GROUPS_PARAMETERS_TAB_PLUS_BUTTON_XPATH = '//*[text()="Valid Param Group Parameters"]/following-sibling::ng2-smart-table//*[@class="nb-plus sub-table-action"]'
    VALID_PARAM_GROUPS_PARAMETERS_TAB_CHECKMARK_BUTTON_XPATH = '//*[text()="Valid Param Group Parameters"]/following-sibling::ng2-smart-table//*[@class="nb-checkmark"]'
    VALID_PARAM_GROUPS_PARAMETERS_TAB_CANCEL_BUTTON_XPATH = '//*[text()="Valid Param Group Parameters"]/following-sibling::ng2-smart-table//*[@class="nb-close"]'
    VALID_PARAM_GROUPS_PARAMETERS_TAB_EDIT_BUTTON_XPATH = '//*[text()="Valid Param Group Parameters"]/following-sibling::ng2-smart-table//*[@class="nb-edit sub-table-action"]'
    VALID_PARAM_GROUPS_PARAMETERS_TAB_DELETE_BUTTON_XPATH = '//*[text()="Valid Param Group Parameters"]/following-sibling::ng2-smart-table//*[@class="nb-trash sub-table-action"]'
    VALID_PARAM_GROUPS_PARAMETERS_TAB_PARAMETER_XPATH = '//*[@placeholder="Parameter *"]'
    VALID_PARAM_GROUPS_PARAMETERS_TAB_PARAMETER_FILTER_XPATH = '//*[@class="customParam ng2-smart-th ng-star-inserted"]//input'
    VALID_PARAM_GROUPS_PARAMETERS_TAB_VALUE_XPATH = '//*[@placeholder="Value *"]'
    VALID_PARAM_GROUPS_PARAMETERS_TAB_VALUE_FILTER_XPATH = '//*[@class="customParamValue ng2-smart-th ng-star-inserted"]//input'
    VALID_PARAM_GROUPS_PARAMETERS_TAB_RULE_XPATH = '//*[@placeholder="Rule *"]'
    VALID_PARAM_GROUPS_PARAMETERS_TAB_RULE_FILTER_XPATH = '//*[@class="form-control ng-untouched ng-pristine ng-valid"]//input'

    # Pos Maintenance tab
    POS_MAINTENANCE_TAB_POSITION_MAINTENANCE_XPATH = '//*[@id="posMaintenance"]'
    POS_MAINTENANCE_TAB_CASH_MAINTENANCE_XPATH = '//*[@id="cashMaintenance"]'
    POS_MAINTENANCE_TAB_UNDERL_POSITION_MAINTENANCE_XPATH = '//*[@id="underlPosMaintenance"]'
    POS_MAINTENANCE_TAB_POSIT_PRICE_CURRENCY_XPATH = '//*[@id="positPriceCurr"]'

    POS_MAINTENANCE_TAB_VALIDATE_POSLIMIT_CHECKBOX_XPATH = '//*[text()="Validate PosLimit"]/preceding-sibling::span'
    POS_MAINTENANCE_TAB_PNL_MAINTENANCE_CHECKBOX_XPATH = '//*[text()="PNL Maintenance"]/preceding-sibling::span'
    POS_MAINTENANCE_TAB_VALIDATE_UNDERL_POSLIMIT_CHECKBOX_XPATH = '//*[text()="Validate Underl PosLimit"]/preceding-sibling::span'

    # Instr types

    INSTR_TYPES_TAB_PLUS_BUTTON_XPATH = '//*[text()=" Instr Types "]/parent::nb-accordion-item//*[@data-name="plus"]'
    INSTR_TYPES_TAB_CHECKMARK_BUTTON_XPATH = '//*[text()=" Instr Types "]/parent::nb-accordion-item//*[@data-name="checkmark"]'
    INSTR_TYPES_TAB_CANCEL_BUTTON_XPATH = '//*[text()=" Instr Types "]/parent::nb-accordion-item//*[@data-name="close"]'
    INSTR_TYPES_TAB_EDIT_BUTTON_XPATH = '//*[text()=" Instr Types "]/parent::nb-accordion-item//*[@data-name="edit"]'
    INSTR_TYPES_TAB_DELETE_BUTTON_XPATH = '//*[text()=" Instr Types "]/parent::nb-accordion-item//*[@data-name="trash-2"]'

    INSTR_TYPES_TAB_INSTR_TYPE_XPATH = '//*[@id="instrType"]'
    INSTR_TYPES_TAB_INSTR_TYPE_FILTER_XPATH = '//*[@class="instrType ng2-smart-th ng-star-inserted"]//input'
    INSTR_TYPES_TAB_POS_KEEPING_MODE_XPATH = '//*[@id="posKeepingMode"]'
    INSTR_TYPES_TAB_POS_KEEPING_MODE_FILTER_XPATH = '//*[@class="ng2-smart-th posKeepingMode ng-star-inserted"]//input'

    # Venues tab
    VENUES_TAB_PLUS_BUTTON_XPATH = '//*[text()=" Venues "]/parent::nb-accordion-item//*[@data-name="plus"]'
    VENUES_TAB_CHECKMARK_BUTTON_XPATH = '//*[text()=" Venues "]/parent::nb-accordion-item//*[@data-name="checkmark"]'
    VENUES_TAB_CANCEL_BUTTON_XPATH = '//*[text()=" Venues "]/parent::nb-accordion-item//*[@data-name="close"]'
    VENUES_TAB_EDIT_BUTTON_XPATH = '//*[text()=" Venues "]/parent::nb-accordion-item//*[@data-name="edit"]'
    VENUES_TAB_DELETE_BUTTON_XPATH = '//*[text()=" Venues "]/parent::nb-accordion-item//*[@data-name="trash-2"]'

    VENUES_TAB_VENUE_XPATH = '//*[@placeholder="Venue *"]'
    VENUES_TAB_VENUE_FILTER_XPATH = '(//nb-accordion-item-header[normalize-space()="Venues"]//..//thead//input)[1]'
    VENUES_TAB_VENUE_CLIENT_NAME_XPATH = '//*[@placeholder="Venue Client Name *"]'
    VENUES_TAB_VENUE_CLIENT_NAME_FILTER_XPATH = '(//nb-accordion-item-header[normalize-space()="Venues"]//..//thead//input)[2]'
    VENUES_TAB_VENUE_CLIENT_ACCOUNT_GROUP_NAME_XPATH = '//*[@placeholder="Venue Client AccountGroup Name"]'
    VENUES_TAB_VENUE_CLIENT_ACCOUNT_GROUP_NAME_FILTER_XPATH = '(//nb-accordion-item-header[normalize-space()="Venues"]//..//thead//input)[3]'
    VENUES_TAB_DEFAULT_ROUTE_XPATH = '//*[@placeholder="Default Route"]'
    VENUES_TAB_DEFAULT_ROUTE_FILTER_XPATH = '(//nb-accordion-item-header[normalize-space()="Venues"]//..//thead//input)[4]'
    VENUES_TAB_ROUTING_PARAM_GROUP_XPATH = '//*[@placeholder="Routing Param Group"]'
    VENUES_TAB_ROUTING_PARAM_GROUP_FILTER_XPATH = '(//nb-accordion-item-header[normalize-space()="Venues"]//..//thead//input)[5]'
    VENUES_TAB_MAX_COMMISSION_TYPE_XPATH = '//*[@placeholder="Max Commission Type"]'
    VENUES_TAB_MAX_COMMISSION_TYPE_FILTER_XPATH = '(//nb-accordion-item-header[normalize-space()="Venues"]//..//thead//input)[6]'
    VENUES_TAB_MAX_COMMISSION_VALUE_XPATH = '//*[@placeholder="Max Commission Value"]'
    VENUES_TAB_MAX_COMMISSION_VALUE_FILTER_XPATH = '(//nb-accordion-item-header[normalize-space()="Venues"]//..//thead//input)[7]'
    VENUES_TAB_PRICE_PRECISION_XPATH = '//*[@placeholder="Max Commission Value"]'
    VENUES_TAB_PRICE_PRECISION_FILTER_XPATH = '(//nb-accordion-item-header[normalize-space()="Venues"]//..//thead//input)[8]'
    VENUES_TAB_STAMP_FEE_EXEMPTION_CHECKBOX_XPATH = '//nb-accordion-item-header[normalize-space()="Venues"]//..//p-table//td[10]//nb-checkbox'
    VENUES_TAB_LEVY_FEE_EXEMPTION_CHECKBOX_XPATH = '//nb-accordion-item-header[normalize-space()="Venues"]//..//p-table//td[11]//nb-checkbox'
    VENUES_TAB_PER_TRANSAC_FEE_EXEMPTION_CHECKBOX_XPATH = '//nb-accordion-item-header[normalize-space()="Venues"]//..//p-table//td[12]//nb-checkbox'
    VENUES_TAB_SAVED_VENUE_XPATH = "//nb-accordion-item//*[text()=' Venues ']/following-sibling::nb-accordion-item-body//tbody//td[2]"

    # Routes tab
    ROUTES_TAB_PLUS_BUTTON_XPATH = '//*[text()=" Routes "]/parent::nb-accordion-item//*[@data-name="plus"]'
    ROUTES_TAB_CHECKMARK_BUTTON_XPATH = '//*[text()=" Routes "]/parent::nb-accordion-item//*[@data-name="checkmark"]'
    ROUTES_TAB_CANCEL_BUTTON_XPATH = '//*[text()=" Routes "]/parent::nb-accordion-item//*[@data-name="close"]'
    ROUTES_TAB_EDIT_BUTTON_XPATH = '//*[text()=" Routes "]/parent::nb-accordion-item//*[@data-name="edit"]'
    ROUTES_TAB_DELETE_BUTTON_XPATH = '//*[text()=" Routes "]/parent::nb-accordion-item//*[@data-name="trash-2"]'

    ROUTES_TAB_ROUTE_XPATH = '//*[@placeholder="Route *"]'
    ROUTES_TAB_ROUTE_FILTER_XPATH = '(//*[text()=" Routes "]//parent::nb-accordion-item//*[@placeholder="Filter"])[1]'
    ROUTES_TAB_ROUTE_CLIENT_NAME_XPATH = '//*[@placeholder="Route Client Name *"]'
    ROUTES_TAB_ROUTE_CLIENT_NAME_FILTER_XPATH = '(//*[text()=" Routes "]//parent::nb-accordion-item//*[@placeholder="Filter"])[2]'
    ROUTES_TAB_ROUTE_AGENT_FEE_EXEMPTION = '//*[text()=" Agent Fee Exemption "]//following::span[contains(@class, "custom-checkbox")]'

    # Trade confirm
    TRADE_CONFIRM_TAB_PLUS_BUTTON_XPATH = '//*[text()=" Trade Confirm "]/parent::nb-accordion-item//*[@data-name="plus"]'
    TRADE_CONFIRM_TAB_CHECKMARK_BUTTON_XPATH = '//*[text()=" Trade Confirm "]/parent::nb-accordion-item//*[@data-name="checkmark"]'
    TRADE_CONFIRM_TAB_CANCEL_BUTTON_XPATH = '//*[text()=" Trade Confirm "]/parent::nb-accordion-item//*[@data-name="close"]'
    TRADE_CONFIRM_TAB_EDIT_BUTTON_XPATH = '//*[text()=" Trade Confirm "]/parent::nb-accordion-item//*[@data-name="edit"]'
    TRADE_CONFIRM_TAB_DELETE_BUTTON_XPATH = '//*[text()=" Trade Confirm "]/parent::nb-accordion-item//*[@data-name="trash-2"]'

    TRADE_CONFIRM_TRADE_CONFIRM_GENERATION_XPATH = '//*[@id="tradeConfirmGeneration"]'
    TRADE_CONFIRM_TRADE_CONFIRM_PREFERENCE_XPATH = '//*[@id="tradeConfirmPreference"]'
    TRADE_CONFIRM_NET_GROSS_IND_TYPE_XPATH = '//*[@id="netGrossIndType"]'
    TRADE_CONFIRM_EMAIL_ADDRESS_XPATH = '//*[@placeholder="Email Address *"]'
    TRADE_CONFIRM_EMAIL_ADDRESS_FILTER_XPATH = '//*[@class="emailAddress ng2-smart-th ng-star-inserted"]//input'
    TRADE_CONFIRM_RECIPIENT_TYPES_XPATH = '//*[@id="recipientType"]'
    TRADE_CONFIRM_RECIPIENT_TYPES_FILTER_XPATH = '//*[@class="emailAddress ng2-smart-th ng-star-inserted"]//input'

    class ExternalAllocationMatchingService:
        PLUS_BUTTON = '//*[@nbtooltip="Add"]'
        SAVE_CHECKMARK = '//*[@data-name="checkmark"]'
        CANCEL_CHECKMARK = '//*[@nbtooltip="Cancel"]'
        EDIT_BUTTON = '//*[@data-name="edit"]'
        DELETE_BUTTON = '//*[@data-name="trash-2"]'
        NAME_FILTER = '(//input[@placeholder="Filter"])[1]'
        GATEWAY_INSTANCE_FILTER = '(//input[@placeholder="Filter"])[2]'
        NAME = '//input[@placeholder="Name *"]'
        GATEWAY_INSTANCE = '//input[@placeholder="Gateway Instance *"]'
        UNSOLICITED_CHECKBOX = '//nb-checkbox//span[@class="custom-checkbox"]'

    class ExternalGiveUpService:
        PLUS_BUTTON = '//*[@nbtooltip="Add"]'
        SAVE_CHECKMARK = '//*[@data-name="checkmark"]'
        CANCEL_CHECKMARK = '//*[@nbtooltip="Cancel"]'
        EDIT_BUTTON = '//*[@data-name="edit"]'
        DELETE_BUTTON = '//*[@data-name="trash-2"]'
        NAME_FILTER = '(//input[@placeholder="Filter"])[1]'
        GATEWAY_INSTANCE_FILTER = '(//input[@placeholder="Filter"])[2]'
        NAME = '//input[@placeholder="Name *"]'
        GATEWAY_INSTANCE = '//input[@placeholder="Gateway Instance *"]'
        UNSOLICITED_CHECKBOX = '//nb-checkbox//span[@class="custom-checkbox"]'
        GATEWAY_PREFIX = '//input[@placeholder="Gateway Prefix"]'
