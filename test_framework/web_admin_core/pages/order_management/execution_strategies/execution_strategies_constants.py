class ExecutionStrategiesConstants:
    EXECUTION_STRATEGIES_PAGE_TITLE_XPATH = "//span[@class='title left'][text()='Execution Strategies']"
    DROP_DOWN_MENU_XPATH = '//*[@class="option-list"]//span'

    # --MAIN MENU--
    ENABLE_DISABLE_BUTTON_XPATH = "//div[contains(@class, 'toggle')]"
    OK_BUTTON_XPATH="//*[text()='Ok']"
    DISPLAYED_EXECUTION_STRATEGY_XPATH = '//*[text()="{}"]'
    # --more actions
    MORE_ACTIONS_BUTTON_XPATH = "//nb-icon[@title='More Actions']"
    EDIT_AT_MORE_ACTIONS_XPATH = '//*[@data-name="edit"]'
    CLONE_AT_MORE_ACTIONS_XPATH = '//*[@data-name="copy"]'
    DOWNLOAD_PDF_AT_MORE_ACTIONS_XPATH = "//nb-icon[@icon='download-outline']//*[@data-name='download']"
    PIN_TO_ROW_AT_MORE_ACTIONS_XPATH = '//*[@nbtooltip="Click to Pin Row"]'
    # --------------filters
    NEW_BUTTON_AT_MAIN_MENU_XPATH = '//*[normalize-space()="Execution Strategies"]//..//..//*[normalize-space()="New"]'
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
    ENABLED_FILTER_LIST_AT_MAIN_MENU_XPATH = '//*[@class="ag-header-container"]/div[2]/div[6]//select//*[text()="{}"]'
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
    NAME_AT_VALUES_TAB_XPATH = '//*[@id="algoPolicyName"]'
    STRATEGY_TYPE_AT_VALUES_TAB_XPATH = '//*[@id="scenario"]'
    DESCRIPTION_AT_VALUES_TAB_XPATH = '//*[@id="algoPolicyDesc"]'
    USER_AT_VALUES_TAB_XPATH = '//*[@id="user"]'
    CLIENT_AT_VALUES_TAB_XPATH = '//*[@id="accountGroup"]'
    SUB_VENUE_AT_VALUES_TAB_XPATH = '//*[text()="SubVenue"]/preceding-sibling::input'
    EXT_ID_CLIENT_AT_VALUES_TAB_XPATH = '//*[@id="clientAlgoPolicyID"]'
    EXT_ID_VENUE_AT_VALUES_TAB_XPATH = '//*[@id="venueAlgoPolicyID"]'
    PEGGED_AT_VALUES_TAB_XPATH = '//*[text()="Pegged"]/preceding-sibling::span'

    ORD_TYPY_XPATH = '//*[@id="defaultOrdType"]'
    TIF_XPATH = '//*[@id="defaultTIF"]'
    LIMIT_PRICE_OFFSET_VALUE = '//*[@id="limitPriceOffsetValue"]'
    LIMIT_PRICE_OFFSET_TYPE = '//*[@id="limitPriceOffsetType"]'
    LIMIT_PRICE_REFERENCE = '//*[@id="limitPriceReference"]'

    AGGRESSOR_INDICATOR_AT_VALUES_TAB_XPATH = '//*[text()="Aggressor Indicator"]/preceding-sibling::input'

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
    PLUS_BUTTON_AT_PARAMETERS_SUB_WIZARD ='//*[@data-name="plus"]'
    CHECKMARK_BUTTON_AT_PARAMETERS_SUB_WIZARD ='//*[@data-name="checkmark"]'
    CANCEL_BUTTON_AT_PARAMETERS_SUB_WIZARD ='//*[@data-name="close"]'
    EDIT_BUTTON_AT_PARAMETERS_SUB_WIZARD ='//*[@data-name="edit"]'
    DELETE_BUTTON_AT_PARAMETERS_SUB_WIZARD ='//*[@data-name="trash-2"]'

    PARAMETER_FIELD_AT_PARAMETERS_SUB_WIZARD = "//*[@placeholder='Parameter *']"
    PARAMETER_FILTER_AT_PARAMETERS_SUB_WIZARD ='(//*[@placeholder="Filter"])[1]'

    VISIBLE_CHECKBOX_AT_PARAMETERS_SUB_WIZARD = '(//*[contains(@class, "custom-checkbox")])[1]'
    VISIBLE_FILTER_AT_PARAMETERS_SUB_WIZARD = '//*[@class="isVisible ng2-smart-th ng-star-inserted"]//input'

    EDITABLE_CHECKBOX_AT_PARAMETERS_SUB_WIZARD = '(//*[contains(@class, "custom-checkbox")])[2]'
    EDITABLE_FILTER_AT_PARAMETERS_SUB_WIZARD = '//*[@class="isEditable ng2-smart-th ng-star-inserted"]//input'

    REQUIRED_CHECKBOX_AT_PARAMETERS_SUB_WIZARD = '(//*[contains(@class, "custom-checkbox")])[3]'
    REQUIRED_FILTER_AT_PARAMETERS_SUB_WIZARD = '//*[@class="ng2-smart-th scenarioParameterRequired ng-star-inserted"]//input'

    VALUE_FIELD_AT_PARAMETERS_SUB_WIZARD ='//*[@formcontrolname="algoParameterValue" or @id="algoParameterValue"]'
    VALUE_AT_PARAMETERS_SUB_WIZARD ='//*[@class="parameters-settings"]//following::td[last()]'
    VALUE_FILTER_AT_PARAMETERS_SUB_WIZARD ='//*[@class="algoParameterFEValue ng2-smart-th ng-star-inserted"]//input'
    CHECKBOX_FOR_ALL_PARAMETERS_AT_SUB_WIZARD = "//*[@formcontrolname='algoParameterValue']//*[contains(@class, 'custom-checkbox')]"

    START_TIME_AT_SUB_WIZARD = '//*[text()="StartTime *"]/preceding-sibling::input'
    PLUS_AND_MINUS_AT_SUB_WIZARD = '//*[text()="+/-"]/preceding-sibling::input'
    OFFSET_AT_SUB_WIZARD ='//*[text()="Offset *"]/preceding-sibling::input'
    ABSOLUTE_VALUE_AT_SUB_WIZARD ='//*[text()="Absolute Value *"]/preceding-sibling::input'

    VALUES_OF_PARAMETERS_IN_SUB_WIZARD = '//tr//td[3]//span[@class="ng-star-inserted"]'
    # JUST FOR ACTIONS SUB WIZARD
    PLUS_BUTTON_AT_ACTIONS_SUB_WIZARD = '//*[@class="form-table-details-wrapper"]//ancestor::p-table//*[@nbtooltip="Add"]'
    CHECKMARK_BUTTON_AT_ACTIONS_SUB_WIZARD = '//*[@class="form-table-details-wrapper"]//ancestor::p-table//*[@data-name="checkmark"]'
    CANCEL_BUTTON_AT_ACTIONS_SUB_WIZARD = '//*[@class="form-table-details-wrapper"]//ancestor::p-table//*[@data-name="close"]'
    DELETE_BUTTON_AT_ACTIONS_SUB_WIZARD = '//*[@class="form-table-details-wrapper"]//ancestor::p-table//*[@data-name="trash-2"]'
    VALUE_FIELD_AT_ACTIONS_SUB_WIZARD = "//*[@placeholder='Value *']"
    VALUE_FILTER_AT_ACTIONS_SUB_WIZARD = "//*[@class='ng2-smart-th secondValue ng-star-inserted']//input"
    VENUE_FIELD_AT_ACTIONS_SUB_WIZARD = '//*[@id="algoParameterValue"]'
    VENUE_FILTER_AT_ACTIONS_SUB_WIZARD = "//*[@class='form-table-details-old_wrappers']//*[@class='form-control ng-untouched ng-pristine ng-valid'] "
    STRATEGY_AT_SUB_WIZARD = '//*[@class="nb-form-control-container"]//*[@id="algoParameterValue"]'

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
    ALL_NAMES_AT_DARK_BLOCK = "//*[@id='dark-parameters']//nb-list//nb-list-item//*[@class='parameter-label']"
    ALL_VALUES_AT_DARK_BLOCK = "//*[@id='dark-parameters']//nb-list//nb-list-item//*[@class='parameter-value']"
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





















