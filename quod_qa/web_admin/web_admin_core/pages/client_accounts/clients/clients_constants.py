class ClientsConstants:
    CLIENTS_PAGE_TITLE_XPATH = "//span[@class='entity-title left'][text()='Clients ']"

    REFRESH_PAGE_BUTTON_XPATH = "//*[@data-name='refresh']"
    DOWNLOAD_PDF_BUTTON_XPATH = "//*[@nbtooltip = 'Download PDF']//*[@data-name='download']"
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
    ENABLE_DISABLE_TOGGLE_BUTTON_XPATH = "//div[contains(@class, 'toggle')]"
    INCORRECT_OR_MISSING_VALUES_MESSAGE_XPATH = "//*[text()='Incorrect or missing values']"
    REQUEST_FAILED_MESSAGE_XPATH = "//*[text()='Request failed, verify the input data. If the problem persists, please contact the administrator for full details']"

    # main page
    MAIN_PAGE_NAME_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[1]//input'
    MAIN_PAGE_DESCRIPTION_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[2]//input'
    MAIN_PAGE_CLEARING_ACCOUNT_TYPE_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[3]//input'
    MAIN_PAGE_BOOKING_INS_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[4]//input'
    MAIN_PAGE_ALLOCATION_PREFERENCE_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[5]//input'
    MAIN_PAGE_DISCLOSE_EXEC_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[6]//input'
    MAIN_PAGE_CLIENT_GROUP_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[7]//input'
    MAIN_PAGE_CLEARING_ACCOUNT_TYPE_XPATH = '//*[@col-id="clearingAccountType"]//span//span[4]'

    # values tab
    VALUES_TAB_ID_XPATH = '//*[@formcontrolname="accountGroupID"]'
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
    VALUES_TAB_MANAGE_COUNTERPART_XPATH = '//*[@class= "sm"]//button'
    VALUES_TAB_SHORT_SELL_ACCOUNT_CHECKBOX_XPATH = '//*[text()="Short Sell Account"]/preceding-sibling::span'
    VALUES_TAB_DUMMY_CHECKBOX_XPATH = '//*[text()="Dummy"]/preceding-sibling::span'
    VALUES_TAB_PRICE_PRECISION_XPATH = '//*[@formcontrolname="pxPrecision"]'

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

    INSTR_TYPES_TAB_PLUS_BUTTON_XPATH = '//*[text()=" Instr Types "]/parent::nb-accordion-item//*[@class="nb-plus"]'
    INSTR_TYPES_TAB_CHECKMARK_BUTTON_XPATH = '//*[text()=" Instr Types "]/parent::nb-accordion-item//*[@class="nb-checkmark"]'
    INSTR_TYPES_TAB_CANCEL_BUTTON_XPATH = '//*[text()=" Instr Types "]/parent::nb-accordion-item//*[@class="nb-close"]'
    INSTR_TYPES_TAB_EDIT_BUTTON_XPATH = '//*[text()=" Instr Types "]/parent::nb-accordion-item//*[@class="nb-edit"]'
    INSTR_TYPES_TAB_DELETE_BUTTON_XPATH = '//*[text()=" Instr Types "]/parent::nb-accordion-item//*[@class="nb-trash"]'

    INSTR_TYPES_TAB_INSTR_TYPE_XPATH = '//*[@placeholder="Instr Type *"]'
    INSTR_TYPES_TAB_INSTR_TYPE_FILTER_XPATH = '//*[@class="instrType ng2-smart-th ng-star-inserted"]//input'
    INSTR_TYPES_TAB_POS_KEEPING_MODE_XPATH = '//*[@placeholder="Pos Keeping Mode"]'
    INSTR_TYPES_TAB_POS_KEEPING_MODE_FILTER_XPATH = '//*[@class="ng2-smart-th posKeepingMode ng-star-inserted"]//input'

    # Venues tab
    VENUES_TAB_PLUS_BUTTON_XPATH = '//*[text()=" Venues "]/parent::nb-accordion-item//*[@class="nb-plus"]'
    VENUES_TAB_CHECKMARK_BUTTON_XPATH = '//*[text()=" Venues "]/parent::nb-accordion-item//*[@class="nb-checkmark"]'
    VENUES_TAB_CANCEL_BUTTON_XPATH = '//*[text()=" Venues "]/parent::nb-accordion-item//*[@class="nb-close"]'
    VENUES_TAB_EDIT_BUTTON_XPATH = '//*[text()=" Venues "]/parent::nb-accordion-item//*[@class="nb-edit"]'
    VENUES_TAB_DELETE_BUTTON_XPATH = '//*[text()=" Venues "]/parent::nb-accordion-item//*[@class="nb-trash"]'

    VENUES_TAB_VENUE_XPATH = '//*[@placeholder="Venue *"]'
    VENUES_TAB_VENUE_FILTER_XPATH = '//*[@class="ng2-smart-th venue ng-star-inserted"]//input'
    VENUES_TAB_VENUE_CLIENT_NAME_XPATH = '//*[@placeholder="Venue Client Name *"]'
    VENUES_TAB_VENUE_CLIENT_NAME_FILTER_XPATH = '//*[@class="ng2-smart-th venueActGrpName ng-star-inserted"]//input'
    VENUES_TAB_VENUE_CLIENT_ACCOUNT_GROUP_NAME_XPATH = '//*[@placeholder="Venue Client AccountGroup Name"]'
    VENUES_TAB_VENUE_CLIENT_ACCOUNT_GROUP_NAME_FILTER_XPATH = '//*[@class="ng2-smart-th venueClientActGrpName ng-star-inserted"]//input'
    VENUES_TAB_DEFAULT_ROUTE_XPATH = '//*[@placeholder="Default Route"]'
    VENUES_TAB_DEFAULT_ROUTE_FILTER_XPATH = '//*[@class="defaultRoute ng2-smart-th ng-star-inserted"]//input'
    VENUES_TAB_ROUTING_PARAM_GROUP_XPATH = '//*[@placeholder="Routing Param Group"]'
    VENUES_TAB_ROUTING_PARAM_GROUP_FILTER_XPATH = '//*[@class="ng2-smart-th routingParamGroup ng-star-inserted"]//input'
    VENUES_TAB_MAX_COMMISSION_TYPE_XPATH = '//*[@placeholder="Max Commission Type"]'
    VENUES_TAB_MAX_COMMISSION_TYPE_FILTER_XPATH = '//*[@class="maxCommType ng2-smart-th ng-star-inserted"]//input'
    VENUES_TAB_MAX_COMMISSION_VALUE_XPATH = '//*[@placeholder="Max Commission Value"]'
    VENUES_TAB_MAX_COMMISSION_VALUE_FILTER_XPATH = '//*[@class="maxCommissionValue ng2-smart-th ng-star-inserted"]//input'
    VENUES_TAB_PRICE_PRECISION_XPATH = '//*[@placeholder="Max Commission Value"]'
    VENUES_TAB_PRICE_PRECISION_FILTER_XPATH = '//*[@class="ng2-smart-th pxPrecision ng-star-inserted"]//input'
    VENUES_TAB_STAMP_FEE_EXEMPTION_CHECKBOX_XPATH = '/html/body/ngx-app/ngx-pages/ngx-one-column-layout/nb-layout/div[1]/div/div/div/div/nb-layout-column/ngx-components/account-group-wizard/div/nb-card/nb-card-body/div/nb-accordion/nb-accordion-item[7]/nb-accordion-item-body/div/div/div/ng2-smart-table/table/thead/tr[3]/td[10]/ng2-smart-table-cell/table-cell-edit-mode/div/table-cell-custom-editor/checkbox-custom-editor/form/nb-checkbox/label/span[1]'
    VENUES_TAB_LEVY_FEE_EXEMPTION_CHECKBOX_XPATH = '/html/body/ngx-app/ngx-pages/ngx-one-column-layout/nb-layout/div[1]/div/div/div/div/nb-layout-column/ngx-components/account-group-wizard/div/nb-card/nb-card-body/div/nb-accordion/nb-accordion-item[7]/nb-accordion-item-body/div/div/div/ng2-smart-table/table/thead/tr[3]/td[11]/ng2-smart-table-cell/table-cell-edit-mode/div/table-cell-custom-editor/checkbox-custom-editor/form/nb-checkbox/label/span[1]'
    VENUES_TAB_PER_TRANSAC_FEE_EXEMPTION_CHECKBOX_XPATH = '/html/body/ngx-app/ngx-pages/ngx-one-column-layout/nb-layout/div[1]/div/div/div/div/nb-layout-column/ngx-components/account-group-wizard/div/nb-card/nb-card-body/div/nb-accordion/nb-accordion-item[7]/nb-accordion-item-body/div/div/div/ng2-smart-table/table/thead/tr[3]/td[12]/ng2-smart-table-cell/table-cell-edit-mode/div/table-cell-custom-editor/checkbox-custom-editor/form/nb-checkbox/label/span[1]'

    # Routes tab
    ROUTES_TAB_PLUS_BUTTON_XPATH = '//*[text()=" Routes "]/parent::nb-accordion-item//*[@class="nb-plus ng2-add-btn"]'
    ROUTES_TAB_CHECKMARK_BUTTON_XPATH = '//*[text()=" Routes "]/parent::nb-accordion-item//*[@class="nb-checkmark"]'
    ROUTES_TAB_CANCEL_BUTTON_XPATH = '//*[text()=" Routes "]/parent::nb-accordion-item//*[@class="nb-plus ng2-add-btn"]'
    ROUTES_TAB_EDIT_BUTTON_XPATH = '//*[text()=" Routes "]/parent::nb-accordion-item//*[@class="nb-plus ng2-add-btn"]'
    ROUTES_TAB_DELETE_BUTTON_XPATH = '//*[text()=" Routes "]/parent::nb-accordion-item//*[@class="nb-plus ng2-add-btn"]'

    ROUTES_TAB_ROUTE_XPATH = '//*[@placeholder="Route *"]'
    ROUTES_TAB_ROUTE_FILTER_XPATH = '//*[@class="ng2-smart-th route ng-star-inserted"]//input'
    ROUTES_TAB_ROUTE_CLIENT_NAME_XPATH = '//*[@placeholder="Route Client Name *"]'
    ROUTES_TAB_ROUTE_CLIENT_NAME_FILTER_XPATH = '//*[@class="ng2-smart-th routeActGrpName ng-star-inserted"]//input'

    # Trade confirm
    TRADE_CONFIRM_TAB_PLUS_BUTTON_XPATH = '//*[text()=" Trade Confirm "]/parent::nb-accordion-item//*[@class="nb-plus sub-table-action"]'
    TRADE_CONFIRM_TAB_CHECKMARK_BUTTON_XPATH = '//*[text()=" Trade Confirm "]/parent::nb-accordion-item//*[@class="nb-checkmark"]'
    TRADE_CONFIRM_TAB_CANCEL_BUTTON_XPATH = '//*[text()=" Trade Confirm "]/parent::nb-accordion-item//*[@class="nb-close"]'
    TRADE_CONFIRM_TAB_EDIT_BUTTON_XPATH = '//*[text()=" Trade Confirm "]/parent::nb-accordion-item//*[@class="nb-edit sub-table-action"]'
    TRADE_CONFIRM_TAB_DELETE_BUTTON_XPATH = '//*[text()=" Trade Confirm "]/parent::nb-accordion-item//*[@class="nb-trash sub-table-action"]'

    TRADE_CONFIRM_TRADE_CONFIRM_GENERATION_XPATH = '//*[@id="tradeConfirmGeneration"]'
    TRADE_CONFIRM_TRADE_CONFIRM_PREFERENCE_XPATH = '//*[@id="tradeConfirmPreference"]'
    TRADE_CONFIRM_NET_GROSS_IND_TYPE_XPATH = '//*[@id="netGrossIndType"]'
    TRADE_CONFIRM_EMAIL_ADDRESS_XPATH = '//*[@placeholder="Email Address *"]'
    TRADE_CONFIRM_EMAIL_ADDRESS_FILTER_XPATH = '//*[@class="emailAddress ng2-smart-th ng-star-inserted"]//input'
    TRADE_CONFIRM_RECIPIENT_TYPES_XPATH = '//*[@placeholder="Recipient Types *"]'
    TRADE_CONFIRM_RECIPIENT_TYPES_FILTER_XPATH = '//*[@class="emailAddress ng2-smart-th ng-star-inserted"]//input'
