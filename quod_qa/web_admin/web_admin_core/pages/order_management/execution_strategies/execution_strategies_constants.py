class ExecutionStrategiesConstants:
    EXECUTION_STRATEGIES_PAGE_TITLE_XPATH = "//span[@class='title left'][text()='Execution Strategies']"

    # --MAIN MENU--
    ENABLE_DISABLE_BUTTON_XPATH = "//div[contains(@class, 'toggle')]"
    OK_BUTTON_XPATH="//*[text()='Ok']"
    # --more actions
    MORE_ACTIONS_BUTTON_XPATH = "//nb-icon[@title='More Actions']"
    EDIT_AT_MORE_ACTIONS_XPATH = '//*[@data-name="edit"]'
    CLONE_AT_MORE_ACTIONS_XPATH = '//*[@data-name="copy"]'
    DOWNLOAD_PDF_AT_MORE_ACTIONS_XPATH = "//nb-icon[@icon='download-outline']//*[@data-name='download']"
    PIN_TO_ROW_AT_MORE_ACTIONS_XPATH = '//*[@nbtooltip="Click to Pin Row"]'
    # --------------filters
    NEW_BUTTON_AT_MAIN_MENU_XPATH = '//*[text()="New"]'
    REFRESH_PAGE_AT_MAIN_MENU_XPATH = '//*[@data-name="refresh"]'
    SAVE_CHANGE_CRITERIA_AT_MAIN_MENU_XPATH = "//*[text()='Change criteria']"
    CHANGE_CRITERIA_AT_MAIN_MENU_XPATH = '//*[@data-name="settings"]'
    FIRST_CRITERIA_FIELD_AT_CHANGE_CRITERIA_TAB_XPATH = '//*[@id="algoPolicyCriterion1"]'
    SECOND_CRITERIA_FIELD_AT_CHANGE_CRITERIA_TAB_XPATH = '//*[@id="algoPolicyCriterion2"]'
    NAME_FILTER_AT_MAIN_MENU_XPATH = '//*[@class="ag-header-container"]/div[2]/div[1]//input'
    DESCRIPTION_FILTER_AT_MAIN_MENU_XPATH = '//*[@class="ag-header-container"]/div[2]/div[2]//input'
    STRATEGY_TYPE_FILTER_AT_MAIN_MENU_XPATH = '//*[@class="ag-header-container"]/div[2]/div[3]//input'
    EXT_ID_CLIENT_FILTER_AT_MAIN_MENU_XPATH = '//*[@class="ag-header-container"]/div[2]/div[4]//input'
    EXT_ID_VENUE_FILTER_AT_MAIN_MENU_XPATH = '//*[@class="ag-header-container"]/div[2]/div[5]//input'
    ENABLED_FILTER_AT_MAIN_MENU_XPATH = '//*[@class="ag-header-container"]/div[2]/div[6]//select'
    ENABLED_FILTER_LIST_AT_MAIN_MENU_XPATH = '//*[@class="ag-header-container"]/div[2]/div[6]//select//*[text()={}]'
    USER_FILTER_AT_MAIN_MENU_XPATH = '//*[@class="ag-header-container"]/div[2]/div[7]//input'
    CLIENT_FILTER_AT_MAIN_MENU_XPATH = '//*[@class="ag-header-container"]/div[2]/div[8]//input'
    GLOBAL_FILTER_AT_MAIN_MENU_XPATH = '//*[@class="lookup-input size-small status-basic shape-rectangle nb-transition"]'
    # -------------values
    NAME_VALUE_AT_MAIN_MENU_XPATH = "//*[@class='ag-center-cols-container']//div[1]//div[1]"
    DESCRIPTION_VALUE_AT_MAIN_MENU_XPATH = "//*[@class='ag-center-cols-container']//div[1]//div[2]"
    STRATEGY_TYPE_VALUE_AT_MAIN_MENU_XPATH = "//*[@class='ag-center-cols-container']//div[1]//div[3]"

    # --EXECUTION STR WIZARD--
    SAVE_CHANGES_AT_WIZARD = '//*[text()="Save Changes"]'
    CLEAR_CHANGES_AT_WIZARD = '//*[text()="Clear Changes"]'
    REVERT_CHANGES_AT_WIZARD = "//*[text()='Revert Changes']"
    CLOSE_WIZARD = '//*[@data-name="close"]'
    # --VALUES TAB--
    NAME_AT_VALUES_TAB_XPATH = '//*[text()="Name *"]/preceding-sibling::input'
    STRATEGY_TYPE_AT_VALUES_TAB_XPATH = '//*[text()="Strategy Type *"]/preceding-sibling::input'
    DESCRIPTION_AT_VALUES_TAB_XPATH = '//*[text()="Description"]/preceding-sibling::input'
    USER_AT_VALUES_TAB_XPATH = '//*[text()="User"]/preceding-sibling::input'
    CLIENT_AT_VALUES_TAB_XPATH = '//*[text()="Client"]/preceding-sibling::input'
    SUB_VENUE_AT_VALUES_TAB_XPATH = '//*[text()="SubVenue"]/preceding-sibling::input'
    EXT_ID_CLIENT_AT_VALUES_TAB_XPATH = '//*[text()="Ext ID Client"]/preceding-sibling::input'
    EXT_ID_VENUE_AT_VALUES_TAB_XPATH = '//*[text()="Ext ID Venue"]/preceding-sibling::input'
    DEFAULT_TIF_AT_VALUES_TAB_XPATH = '//*[text()="Default TIF"]/preceding-sibling::input'
    DEFAULT_ORD_TYPE_AT_VALUES_TAB_XPATH = '//*[text()="Default Ord Type"]/preceding-sibling::input'
    AGGRESSOR_INDICATOR_AT_VALUES_TAB_XPATH = '//*[text()="Aggressor Indicator"]/preceding-sibling::input'
    PEGGED_AT_VALUES_TAB_XPATH = '//*[text()="Pegged"]/preceding-sibling::span'

    # --PARAMETERS TAB--
    GENERAL_AT_PARAMETERS_TAB_XPATH = '//*[@class="full-height top-parameter-region"]//*[text()="General"]'
    DARK_AT_PARAMETERS_TAB_XPATH = '//*[@class="full-height top-parameter-region"]//*[text()="Dark"]'
    GENERAL_IN_LIT_BLOCK_AT_PARAMETERS_TAB_XPATH = '//*[@class="third-height parameter-region"]//*[text()="General"]'
    AGGRESSIVE_IN_LIT_BLOCK_AT_PARAMETERS_TAB_XPATH = '//*[@class="parameter-region"]//*[text()="Aggressive"]'
    PASSIVE_IN_LIT_BLOCK_AT_PARAMETERS_TAB_XPATH = '//*[@class="parameter-region"]//*[text()="Passive"]'
    SWEEPING_IN_LIT_BLOCK_AT_PARAMETERS_TAB_XPATH = '//*[@class="parameter-region"]//*[text()="Sweeping"]'
    DARK_IN_LIT_BLOCK_AT_PARAMETERS_TAB_XPATH = '//*[@class="third-height parameter-region"]//*[text()="Dark"]'
    DARK_DISABLED_IN_LIT_BLOCK_AT_PARAMETERS_TAB_XPATH ='//*[@class="third-height parameter-region region-disabled"]//*[text()="Dark"]'

    #JUST FOR PARAMETERS TAB
    PLUS_BUTTON_AT_PARAMETERS_SUB_WIZARD ="//*[@class='nb-plus ng2-main-add-btn']"
    CHECKMARK_BUTTON_AT_PARAMETERS_SUB_WIZARD ="//*[@class='nb-checkmark']"
    CANCEL_BUTTON_AT_PARAMETERS_SUB_WIZARD ="//*[@class='nb-close ng2-main-cancel-btn']"
    EDIT_BUTTON_AT_PARAMETERS_SUB_WIZARD ="//*[@class='nb-edit ng2-main-edit-btn']"
    DELETE_BUTTON_AT_PARAMETERS_SUB_WIZARD ="//*[@class='ng2-smart-action ng2-smart-action-delete-delete ng-star-inserted']//*[@class='nb-trash']"

    PARAMETER_FIELD_AT_PARAMETERS_SUB_WIZARD = "//*[@placeholder='Parameter *']"
    PARAMETER_FILTER_AT_PARAMETERS_SUB_WIZARD ='//*[@class="ng2-smart-th scenarioParameter ng-star-inserted"]//input'

    VISIBLE_CHECKBOX_AT_PARAMETERS_SUB_WIZARD = '//*[@class="ng-star-inserted"]//td[3]//*[@class="custom-checkbox"]'
    VISIBLE_FILTER_AT_PARAMETERS_SUB_WIZARD = '//*[@class="isVisible ng2-smart-th ng-star-inserted"]//input'

    EDITABLE_CHECKBOX_AT_PARAMETERS_SUB_WIZARD = '//*[@class="ng-star-inserted"]//td[4]//*[@class="custom-checkbox"]'
    EDITABLE_FILTER_AT_PARAMETERS_SUB_WIZARD = '//*[@class="isEditable ng2-smart-th ng-star-inserted"]//input'

    REQUIRED_CHECKBOX_AT_PARAMETERS_SUB_WIZARD = '//*[@class="ng-star-inserted"]//td[5]//*[@class="custom-checkbox"]'
    REQUIRED_FILTER_AT_PARAMETERS_SUB_WIZARD = '//*[@class="ng2-smart-th scenarioParameterRequired ng-star-inserted"]//input'

    VALUE_FIELD_AT_PARAMETERS_SUB_WIZARD ="//*[@id='algoParameterValue']"
    VALUE_AT_PARAMETERS_SUB_WIZARD ="//*[@class='parameters-settings']//tr[1]//td[6]//div//div[@class='ng-star-inserted']"
    VALUE_FILTER_AT_PARAMETERS_SUB_WIZARD ='//*[@class="algoParameterFEValue ng2-smart-th ng-star-inserted"]//input'
    CHECKBOX_FOR_ALL_PARAMETERS_AT_SUB_WIZARD = "//*[@formcontrolname='algoParameterValue']//*[@class='custom-checkbox']"

    START_TIME_AT_SUB_WIZARD = '//*[text()="StartTime *"]/preceding-sibling::input'
    PLUS_AND_MINUS_AT_SUB_WIZARD = '//*[text()="+/-"]/preceding-sibling::input'
    OFFSET_AT_SUB_WIZARD ='//*[text()="Offset *"]/preceding-sibling::input'
    ABSOLUTE_VALUE_AT_SUB_WIZARD ='//*[text()="Absolute Value *"]/preceding-sibling::input'


    # JUST FOR ACTIONS SUB WIZARD
    PLUS_BUTTON_AT_ACTIONS_SUB_WIZARD = "//*[@class='nb-plus piloted-table-action']"
    CHECKMARK_BUTTON_AT_ACTIONS_SUB_WIZARD = "//*[@class='form-table-details-wrapper']//*[@class='nb-checkmark']"
    CANCEL_BUTTON_AT_ACTIONS_SUB_WIZARD = "//*[@class='form-table-details-wrapper']//*[@class='nb-close']"
    DELETE_BUTTON_AT_ACTIONS_SUB_WIZARD = "//*[@class='nb-trash piloted-table-action']"
    VALUE_FIELD_AT_ACTIONS_SUB_WIZARD = "//*[@placeholder='Value *']"
    VALUE_FILTER_AT_ACTIONS_SUB_WIZARD = "//*[@class='ng2-smart-th secondValue ng-star-inserted']//input"
    VENUE_FIELD_AT_ACTIONS_SUB_WIZARD = "//*[@class='nb-form-control-container']//*[@placeholder='Venue']"
    VENUE_FILTER_AT_ACTIONS_SUB_WIZARD = "//*[@class='form-table-details-wrapper']//*[@class='form-control ng-untouched ng-pristine ng-valid'] "
    STRATEGY_AT_SUB_WIZARD = "//*[@class='nb-form-control-container']//*[@placeholder='Strategy']"

    #Venue priority sub wizard
    PLUS_BUTTON_AT_VENUE_PRIORITY_SUB_WIZARD ="//*[@class='row ng-star-inserted']//*[@class='nb-plus']"
    CHECKMARK_BUTTON_AT_VENUE_PRIORITY_SUB_WIZARD ="//*[@class='row ng-star-inserted']//*[@class='nb-checkmark']"
    CANCEL_BUTTON_AT_VENUE_PRIORITY_SUB_WIZARD ="//*[@class='row ng-star-inserted']//*[@class='nb-close']"
    DELETE_BUTTON_AT_VENUE_PRIORITY_SUB_WIZARD ="//*[@class='row ng-star-inserted']//*[@class='nb-trash']"
    VENUE_PRIORITY_FIELD_AT_VENUE_PRIORITY_SUB_WIZARD = "//*[@placeholder='Venue Priority']"
    VENUE_PRIORITY_FILTER_AT_VENUE_PRIORITY_SUB_WIZARD = "//*[@class='row ng-star-inserted']//*[@class='form-control ng-untouched ng-pristine ng-valid']"
    #AT SUB WIZARD
    GO_BACK_BUTTON_AT_SUB_WIZARD = '//*[text()="Go Back"]'

    #Label and value at all parameters
    PARAMETER_NAME_AT_DARK_BLOCK ="//*[@id='dark-parameters']//nb-list//nb-list-item[1]//*[@class='parameter-label']"
    PARAMETER_VALUE_AT_DARK_BLOCK ="//*[@id='dark-parameters']//nb-list//nb-list-item[1]//*[@class='parameter-value']"

    PARAMETER_NAME_AT_LIT_GENERAL_BLOCK ="//*[@id='lit-general-parameters']//nb-list//nb-list-item[1]//*[@class='parameter-label']"
    PARAMETER_VALUE_AT_LIT_GENERAL_BLOCK="//*[@id='lit-general-parameters']//nb-list//nb-list-item[1]//*[@class='parameter-value']"

    PARAMETER_NAME_AT_LIT_DARK_BLOCK = "//*[@id='lit-dark-parameters']//nb-list//nb-list-item[1]//*[@class='parameter-label']"
    PARAMETER_VALUE_AT_LIT_DARK_BLOCK = "//*[@id='lit-dark-parameters']//nb-list//nb-list-item[1]//*[@class='parameter-value']"

    PARAMETER_NAME_AT_LIT_PASSIVE_BLOCK ="//*[@id='lit-passive-parameters']//nb-list//nb-list-item[1]//*[@class='parameter-label']"
    PARAMETER_VALUE_AT_LIT_PASSIVE_BLOCK ="//*[@id='lit-passive-parameters']//nb-list//nb-list-item[1]//*[@class='parameter-value']"

    PARAMETER_NAME_AT_LIT_AGGRESSIVE_BLOCK ="//*[@id='lit-aggressive-parameters']//nb-list//nb-list-item[1]//*[@class='parameter-label']"
    PARAMETER_VALUE_AT_LIT_AGGRESSIVE_BLOCK ="//*[@id='lit-aggressive-parameters']//nb-list//nb-list-item[1]//*[@class='parameter-value']"

    PARAMETER_NAME_AT_GENERAL_BLOCK ="//*[@id='general-parameters']//nb-list//nb-list-item[1]//*[@class='parameter-label']"
    PARAMETER_VALUE_AT_GENERAL_BLOCK ="//*[@id='general-parameters']//nb-list//nb-list-item[1]//*[@class='parameter-value']"

    PARAMETER_NAME_AT_SWEEPING_BLOCK = "//*[@id='lit-sweeping-parameters']//nb-list//nb-list-item[1]//*[@class='parameter-label']"
    PARAMETER_VALUE_AT_SWEEPING_BLOCK = "//*[@id='lit-sweeping-parameters']//nb-list//nb-list-item[1]//*[@class='parameter-value']"
    # Error type at web admin page
    INCORRECT_OR_MISSING_VALUES_ERROR = "//*[text()='Incorrect or missing values']"





















