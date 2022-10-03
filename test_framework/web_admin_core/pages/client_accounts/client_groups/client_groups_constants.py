class ClientGroupsConstants:
    CLIENT_GROUPS_PAGE_TITLE_CSS_XPATH = "//span[@class='entity-title left'][text()='ClientGroups ']"

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
    DISPLAYED_ENTITY_XPATH = "//*[text()='{}']"
    DROP_DOWN_MENU_XPATH = '//*[@class="option-list"]//span'

    #   Main page

    MAIN_PAGE_NAME_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[1]//input'
    MAIN_PAGE_DESCRIPTION_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[2]//input'
    MAIN_PAGE_FIX_USER_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[3]//input'
    MAIN_PAGE_BOOKING_INST_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[4]//input'
    MAIN_PAGE_ALLOCATION_PREFERENCE_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[5]//input'
    MAIN_PAGE_ROUNDING_DIRECTION_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[6]//input'
    MAIN_PAGE_PRICE_PRECISION_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[7]//input'
    MAIN_PAGE_SELF_HELP_BEHAVIOR_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[8]//input'

    MAIN_PAGE_NAME_XPATH = '//*[@col-id="clientGroupName"]//span/span[4]'
    MAIN_PAGE_DESCRIPTION_XPATH = '//*[@col-id="clientGroupDesc"]//span/span[4]'
    MAIN_PAGE_FIX_USER_XPATH = '//*[@col-id="FIXUserID"]//span/span[4]'
    MAIN_PAGE_BOOKING_INST_XPATH = '//*[@col-id="bookingInst"]//span/span[4]'
    MAIN_PAGE_ALLOCATION_PREFERENCE_XPATH = '//*[@col-id="allocationInst"]//span/span[4]'
    MAIN_PAGE_ROUNDING_DIRECTION_XPATH = '//*[@col-id="roundingDirection"]//span/span[4]'
    MAIN_PAGE_PRICE_PRECISION_XPATH = '//*[@col-id="pxPrecision"]//span/span[4]'
    MAIN_PAGE_SELF_HELP_BEHAVIOR_XPATH = '//*[@col-id="selfHelpBehavior"]//span/span[4]'

    #   Values tab
    VALUES_TAB_NAME_XPATH = '//*[@formcontrolname="clientGroupName"]'
    VALUES_TAB_DESCRIPTION_XPATH = '//*[@formcontrolname="clientGroupDesc"]'
    VALUES_TAB_SELF_HELP_BEHAVIOR_XPATH = '//*[@id="selfHelpBehavior"]'
    VALUES_TAB_CONFIRMATION_SERVICE_XPATH = '//*[@id="confirmationService"]'
    VALUES_TAB_BLOCK_APPROVAL_XPATH = '//*[@id="blockApproval"]'
    VALUES_TAB_USER_MANAGER_XPATH = '//*[@id="FIXUser"]'
    VALUES_TAB_BOOKING_INST_XPATH = '//*[@id="bookingInst"]'
    VALUES_TAB_ALLOCATION_INST_XPATH = '//*[@id="allocationInst"]'
    VALUES_TAB_ROUNDING_DIRECTION_XPATH = '//*[@id="roundingDirection"]'
    VALUES_TAB_PRICE_PRECISION_XPATH = '//*[@formcontrolname="pxPrecision"]'

    #   Dimensions tab
    DIMENSIONS_TAB_DEFAULT_EXECUTION_STRATEGY_TYPE_XPATH = '//*[@id="defaultAlgoType"]'
    DIMENSIONS_TAB_DEFAULT_EXECUTION_STRATEGY_XPATH = '//*[@id="defaultAlgoPolicy"]'
    DIMENSIONS_TAB_DEFAULT_CHILD_EXECUTION_STRATEGY_XPATH = '//*[@id="defaultSORAlgoPolicy"]'
    DIMENSIONS_TAB_CUSTOM_VALIDATION_RULES_XPATH = '//*[@id="validParamGroup"]'
    DIMENSIONS_TAB_CUSTOM_VALIDATION_RULES_MANAGE_BUTTON_XPATH = '//*[@class="col-sm"]//button'

    #   Valid Param Groups
    VALID_PARAM_GROUPS_TAB_PLUS_XPATH = '//*[@class="nb-plus ng2-add-btn"]'
    VALID_PARAM_GROUPS_TAB_CHECKMARK_XPATH = '//*[@class="nb-checkmark"]'
    VALID_PARAM_GROUPS_TAB_CLOSE_XPATH = '//*[@class="nb-close ng2-cancel-btn"]'
    VALID_PARAM_GROUPS_TAB_EDIT_XPATH = '//*[@class="nb-edit ng2-edit-btn"]'
    VALID_PARAM_GROUPS_TAB_DELETE_XPATH = '//*[@class="nb-trash"]'
    VALID_PARAM_GROUPS_TAB_NAME_XPATH = '//*[@placeholder="Name *"]'
    VALID_PARAM_GROUPS_TAB_NAME_FILTER_XPATH = '//*[@class="ng2-smart-th paramGroupName ng-star-inserted"]//input'

    VALID_PARAM_GROUPS_PARAMETERS_TAB_PLUS_XPATH = '//*[text()="Valid Param Group Parameters"]/following-sibling::ng2-smart-table//*[@class="nb-plus sub-table-action"]'
    VALID_PARAM_GROUPS_PARAMETERS_TAB_CHECKMARK_XPATH = '//*[text()="Valid Param Group Parameters"]/following-sibling::ng2-smart-table//*[@class="nb-checkmark"]'
    VALID_PARAM_GROUPS_PARAMETERS_TAB_CLOSE_XPATH = '//*[text()="Valid Param Group Parameters"]/following-sibling::ng2-smart-table//*[@class="nb-close"]'
    VALID_PARAM_GROUPS_PARAMETERS_TAB_EDIT_XPATH = '//*[text()="Valid Param Group Parameters"]/following-sibling::ng2-smart-table//*[@class="nb-edit sub-table-action"]'
    VALID_PARAM_GROUPS_PARAMETERS_TAB_DELETE_XPATH = '//*[text()="Valid Param Group Parameters"]/following-sibling::ng2-smart-table//*[@class="nb-trash sub-table-action"]'
    VALID_PARAM_GROUPS_PARAMETERS_TAB_PARAMETER_XPATH = '//*[@placeholder="Parameter *"]'
    VALID_PARAM_GROUPS_PARAMETERS_TAB_PARAMETER_FILTER_XPATH = '//*[@class="customParam ng2-smart-th ng-star-inserted"]//input'
    VALID_PARAM_GROUPS_PARAMETERS_TAB_VALUE_XPATH = '//*[@placeholder="Value *"]'
    VALID_PARAM_GROUPS_PARAMETERS_TAB_VALUE_FILTER_XPATH = '//*[@class="customParamValue ng2-smart-th ng-star-inserted"]//input'
    VALID_PARAM_GROUPS_PARAMETERS_TAB_RULE_XPATH = '//*[@placeholder="Rule *"]'
    VALID_PARAM_GROUPS_PARAMETERS_TAB_RULE_FILTER_XPATH = '//*[@class="brokenValidRule ng2-smart-th ng-star-inserted"]//input'
