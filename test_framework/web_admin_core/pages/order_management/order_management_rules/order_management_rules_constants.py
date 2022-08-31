class OrderManagementRulesConstants:
    ORDER_MANAGEMENT_RULES_TITLE_XPATH = "//span[@class='title left'][text()='Order Management Rules']"
    ENABLE_DISABLE_BUTTON_XPATH = "//div[contains(@class, 'toggle')]"
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
    INCORRECT_OR_MISSING_VALUES_XPATH = "//*[text()='Incorrect or missing values']"
    NO_RESULTS_HAVE_ADDED_XPATH = "//*[text()='No results have added']"
    SUCH_RECORD_ALREADY_EXISTS = "//*[text()='Such a record already exists']"
    CAN_NOT_CONTAIN_MORE_THAN_10_CONDITIONS = "//*[text()='Can not contain more than 10 conditions']"
    TOTAL_PERCENTAGE_IS_GREATER_THAN_100 = "//*[text()='Total percentage is greater than 100']"
    IS_GATING_RULE_ALREADY_HAS_THE_SAME_CRITERIA_MESSAGE_DISPLAYED = "//*[text()='A gating rule already has the same criteria']"
    DROP_DOWN_ENTITY_XPATH = "//*[@class='option-list']//span"
    ERROR_MESSAGE_XPATH = "//*[@outline='danger']"

    # criteria
    SAVE_CHANGE_CRITERIA_AT_MAIN_MENU_XPATH = "//*[text()='Change criteria']"
    CHANGE_CRITERIA_AT_MAIN_MENU_XPATH = '//*[@data-name="settings"]'
    FIRST_CRITERIA_FIELD_AT_CHANGE_CRITERIA_TAB_XPATH = '//*[@id="gatingRuleCriterion1"]'
    SECOND_CRITERIA_FIELD_AT_CHANGE_CRITERIA_TAB_XPATH = '//*[@id="gatingRuleCriterion2"]'
    THIRD_CRITERIA_FIELD_AT_CHANGE_CRITERIA_TAB_XPATH = '//*[@id="gatingRuleCriterion3"]'

    # main page
    MAIN_PAGE_NAME_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[1]//input'
    MAIN_PAGE_ENABLED_FILTER_LIST_XPATH = '//*[@class="ag-header-container"]/div[2]/div[2]//select//option[text()="{}"]'
    MAIN_PAGE_ENABLED_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[2]//select'
    MAIN_PAGE_LISTING_GROUP_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[3]//input'
    MAIN_PAGE_SETTINGS_VALUES_XPATH = '//*[@class="title left"]//following-sibling::span'

    # Values tab
    VALUES_TAB_NAME_XPATH = '//*[@formcontrolname="gatingRuleName"]'
    VALUES_TAB_DESCRIPTION_XPATH = '//*[@formcontrolname="gatingRuleDescription"]'
    VALUES_TAB_LISTING_GROUP_XPATH = '//*[@id="listingGroup"]'
    VALUES_TAB_VENUE_XPATH = '//*[@id="venue"]'
    VALUES_TAB_INSTR_TYPE_XPATH = '//*[@id="instrType"]'
    VALUES_TAB_SUB_VENUE_XPATH = '//*[@id="subVenue"]'
    VALUES_TAB_CLIENT_XPATH = '//*[@id="accountGroup"]'
    VALUES_TAB_USER_XPATH = '//*[@id="user"]'
    VALUES_TAB_CLIENT_GROUP_XPATH = '//*[@id="clientGroup"]'
    VALUES_TAB_ACCOUNT_XPATH = '//*[@id="account"]'
    VALUES_TAB_STRATEGY_NAME_XPATH = '//*[@id="externalStrategyName"]'

    # Conditions tab
    CONDITIONS_TAB_PLUS_XPATH = '//*[text()=" Conditions "]/parent::nb-accordion-item//*[@data-name="plus"]'
    CONDITIONS_TAB_CANCEL_XPATH = '//*[text()=" Conditions "]/parent::nb-accordion-item//*[@data-name="close"]'
    CONDITIONS_TAB_CHECKMARK_XPATH = '//*[text()=" Conditions "]/parent::nb-accordion-item//*[@data-name="checkmark"]'
    CONDITIONS_TAB_EDIT_XPATH = '//*[text()=" Conditions "]/parent::nb-accordion-item//*[@data-name="edit"]'
    CONDITIONS_TAB_ENABLE_DISABLE_BUTTON_XPATH = '//*[text()=" Conditions "]/parent::nb-accordion-item//div[contains(@class, "toggle")]'

    CONDITIONS_TAB_NAME_XPATH = '//*[@placeholder="Name *"]'
    CONDITIONS_TAB_NAME_FILTER_XPATH = '//*[@class="gatingRuleCondName ng2-smart-th ng-star-inserted"]//input'
    CONDITIONS_TAB_HOLD_ORDER_CHECKBOX = '//*[text()="HoldOrder"]/preceding-sibling::span'
    CONDITIONS_TAB_QTY_PRECISION_XPATH = '//*[@formcontrolname="conditionQtyPrecision"]'

    # Conditional logic
    CONDITIONS_TAB_AND_RADIO_BUTTON = '//*[text()="AND"]/preceding-sibling::span'
    CONDITIONS_TAB_OR_RADIO_BUTTON = '//*[text()="OR"]/preceding-sibling::span'
    CONDITIONS_TAB_CONDITIONAL_LOGIC_ADD_CONDITION_BUTTON_XPATH = '//*[@class="sub-form-accordion"]//*[@data-name="plus"]'
    CONDITIONS_TAB_CONDITIONAL_LOGIC_LEFT_SIDE_XPATH = '//*[@class = "field-wrapper ng-star-inserted"]//button'
    CONDITIONS_TAB_CONDITIONAL_LOGIC_LEFT_SIDE_LIST_OF_ENTITY_XPATH = "//*[@class='cdk-overlay-container']//nb-option[normalize-space(text())='{}']"
    CONDITIONS_TAB_CONDITIONAL_LOGIC_RIGHT_SIDE_XPATH = '//*[@name="autocomplete"]'
    CONDITIONS_TAB_CONDITIONAL_LOGIC_XPATH = "//*[@class='operator-wrapper ng-star-inserted']"
    CONDITIONS_TAB_CONDITIONAL_LOGIC_SELECTION_FIELD_FOR_IN_NOT_IN_LOGIC_XPATH = '//*[contains(@class, "select-button placeholder")]'
    CONDITIONS_TAB_CONDITIONAL_LOGIC_LIST_XPATH = "//*[@class='cdk-overlay-container']//nb-option[text()='{}']"



    # Results sub wizard
    RESULTS_SUB_WIZARD_PLUS_XPATH = '//*[text()=" Results "]/parent::nb-accordion-item//*[@nbtooltip="Add"]'
    RESULTS_SUB_WIZARD_CANCEL_XPATH = '//*[text()=" Results "]/parent::nb-accordion-item//*[@data-name="close"]'
    RESULTS_SUB_WIZARD_CHECKMARK_XPATH = '//*[text()=" Results "]/parent::nb-accordion-item//*[@data-name="checkmark"]'
    RESULTS_SUB_WIZARD_EDIT_XPATH = '//*[text()=" Results "]/parent::nb-accordion-item//*[@data-name="edit"]'
    RESULTS_SUB_WIZARD_DELETE_XPATH = '//*[text()=" Results "]/parent::nb-accordion-item//*[@data-name="trash-2"]'

    RESULTS_SUB_WIZARD_EXEC_POLICY_XPATH = '//*[@placeholder="Exec Policy *"]'
    RESULTS_SUB_WIZARD_EXEC_POLICY_FILTER_XPATH = '//*[@class="gatingRuleExecPolicyResult ng2-smart-th ng-star-inserted"]//input'
    RESULTS_SUB_WIZARD_PERCENTAGE_XPATH = '//*[@placeholder="Percentage *"]'
    RESULTS_SUB_WIZARD_PERCENTAGE_FILTER_XPATH = '//*[@class="ng2-smart-th splitRatio ng-star-inserted"]//input'

    RESULTS_SUB_WIZARD_PRICE_ORIGIN_XPATH = '//*[@id="priceOriginresult-table"]'
    RESULTS_SUB_WIZARD_EXECUTION_STRATEGY_XPATH = '//*[@id="algoPolicyresult-table"]'
    RESULTS_SUB_WIZARD_STRATEGY_TYPE_XPATH = '//*[@id="scenarioresult-table"]'
    RESULTS_SUB_WIZARD_SOR_EXECUTION_STRATEGY_XPATH = '//*[@id="SORAlgoPolicyresult-table"]'
    RESULTS_SUB_WIZARD_VENUE_XPATH = '//*[@id="resultVenueresult-table"]'
    RESULTS_SUB_WIZARD_ROUTE_XPATH = '//*[@id="routeresult-table"]'

    # Default result
    class DefaultResultAtConditions:
        EDIT_XPATH = '//tr[@tabindex="0"][last()]//*[@nbtooltip="Edit"]'
        CHECKMARK_XPATH = '//tr[@tabindex="0"][last()]//*[@data-name="checkmark"]'
        CANCEL_XPATH = '//tr[@tabindex="0"][last()]//*[@data-name="close"]'
        NAME = '//tr[@tabindex="0"][last()]//*[@placeholder="Name *"]'
        HOLD_ORDER_CHECKBOX = '//*[text()="Hold Order"]/preceding-sibling::span'
        QTY_PRECISION = '//*[@formcontrolname = "qtyPrecision"]'

        PLUS_BUTTON_AT_RESULTS_XPATH = '//*[text()=" Results "]//parent::nb-accordion-item//*[@nbtooltip="Add"]'
        CHECKMARK_AT_RESULTS_XPATH = '//*[text()=" Results "]//parent::nb-accordion-item//*[@data-name="checkmark"]'
        CANCEL_AT_RESULTS_XPATH = '//*[text()=" Results "]//parent::nb-accordion-item//*[@data-name="close"]'
        EDIT_AT_RESULTS_XPATH = '//*[text()=" Results "]//parent::nb-accordion-item//*[@data-name="edit"]'
        DELETE_AT_RESULTS_XPATH = '//*[text()=" Results "]//parent::nb-accordion-item//*[@data-name="trash-2"]'
        EXEC_POLICY_AT_RESULTS_XPATH = '//*[@placeholder="Exec Policy *"]'
        EXEC_POLICY_FILTER_XPATH = '(//*[text()=" Results "]//parent::nb-accordion-item//*[@placeholder="Filter"])[1]'
        PERCENTAGE_AT_RESULTS_XPATH = '//*[@placeholder="Percentage *"]'
        PERCENTAGE_FILTER_XPATH = '(//*[text()=" Results "]//parent::nb-accordion-item//*[@placeholder="Filter"])[2]'

        PRICE_ORIGIN_AT_RESULTS_XPATH = '//*[@id="priceOrigin"]'
        EXECUTION_STRATEGY_AT_RESULTS_XPATH = '//*[@id="algoPolicy"]'
        STRATEGY_TYPE_AT_RESULTS_XPATH = '//*[@id="scenario"]'
        SOR_EXECUTION_STRATEGY_AT_RESULTS_XPATH = '//*[@id="SORAlgoPolicy"]'
        VENUE_AT_RESULTS_XPATH = '//*[@id="resultVenue"]'
        ROUTE_AT_RESULTS_XPATH = '//*[@id="route"]'
