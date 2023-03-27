class Constants:
    class MainPage:
        TITLE = "//span[@class='entity-title left'][text()='Order Management Rules']"

        GLOBAL_FILTER = '//nb-card-header//*[@placeholder="Filter"]'
        DOWNLOAD_CSV_BUTTON = '//*[@nbtooltip="Download CSV"]//a'
        FULL_SCREEN_BUTTON = '//*[@nbtooltip="Full Screen"]//a'
        REFRESH_PAGE_BUTTON = '//*[@nbtooltip="Refresh Page"]//a'
        NEW_BUTTON = '//*[text()="New"]'

        NAME_FILTER = '//*[@style="width: 200px; left: 0px;"]//input[@ref="eFloatingFilterText"]'
        ENABLED_FILTER = '//*[@style="width: 200px; left: 200px;"]//select'
        TOGGLE_BUTTON = "//div[contains(@class, 'toggle')]"

        OK_BUTTON = '//*[text()="Ok"]'
        CANCEL_BUTTON = '//*[text()="Cancel"]'

        SEARCHED_ENTITY = '//*[text() = "{}"]'
        ENTITY_NAME = '//*[@col-id="gatingRuleName" and @tabindex]//*[@ref="eValue"]'
        ENTITY_STATUS = '//*[@col-id="alive" and @tabindex]//input'

        CONDITION_NAME = '//*[@class="condition-name"]'
        CONDITION_PERCENTAGE = '//*[@class="condition-name"][normalize-space()="{}"]//..//*[@class="percent-indicator"]//div'

        # DROP_DOWN_ENTITY_XPATH = "//*[@class='option-list']//span"
        # ERROR_MESSAGE_XPATH = "//*[@outline='danger']"

    class MoreActions:
        MORE_ACTIONS_BUTTON = '//*[@data-name = "more-vertical"]'
        EDIT = '//*[@data-name = "edit"]'
        CLONE = '//*[@data-name = "copy"]'
        DELETE = '//*[@data-name = "trash-2"]'
        PIN_ROW = '//*[@nbtooltip ="Click to Pin Row"]'
        DOWNLOAD_PDF = '//nb-card//*[@nbtooltip="Download PDF"]'

    class Wizard:
        DOWNLOAD_PDF_BUTTON = '//*[@data-name="download"]'
        SAVE_CHANGES_BUTTON = '//*[text()="Save Changes"]'
        CLEAR_CHANGES_BUTTON = '//*[text()="Clear Changes"]'
        CLOSE_WIZARD_BUTTON = '//*[@data-name="close"]'
        OK_BUTTON = '//*[text()="Ok" or text()="OK"]'
        CANCEL_BUTTON = '//*[normalize-space()="Cancel"]'
        REVERT_CHANGES = '//*[normalize-space()="Revert Changes"]'
        FOOTER_ERROR = '//nb-card-footer//*[contains(@class, "error-alert")]//span'

    class ValuesTab:
        NAME = '//*[@id="gatingRuleName"]'
        DESCRIPTION = '//*[@id="gatingRuleDescription"]'

    class ConditionsTab:
        PLUS_BUTTON = '//*[normalize-space()="Conditions"]//..//*[@nbtooltip="Add"]'
        SAVE_BUTTON = '//*[normalize-space()="Conditions"]//..//*[@data-name="checkmark"]'
        CANCEL_BUTTON = '//*[normalize-space()="Conditions"]//..//*[@data-name="close"]'
        EDIT_BUTTON = '//*[normalize-space()="Conditions"]//..//*[@data-name="edit"]'
        TOGGLE_BUTTON = '//*[normalize-space()="Conditions"]//..//div[contains(@class, "toggle")]'
        UP_BUTTON = '//*[normalize-space()="Conditions"]//..//*[@icon="arrow-up-outline"]'
        DOWN_BUTTON = '//*[normalize-space()="Conditions"]//..//*[@icon="arrow-down-outline"]'
        NAME_FILTER = '//*[normalize-space()="Name"]//..//*[@placeholder="Filter"]'
        NAME = '//*[normalize-space()="Name"]//..//*[@placeholder="Name *"]'

    class ConditionLogic:
        ADD_CONDITION_BUTTON = '//*[normalize-space()="Conditional Logic"]//following::nb-accordion-item-body[1]//*[@data-name="plus"]'
        ADD_CONDITION_SET_BUTTON = '//*[normalize-space()="Conditional Logic"]//following::nb-accordion-item-body[1]//*[@data-name="plus-circle"]'
        CLOSE_BUTTON = '//*[normalize-space()="Conditional Logic"]//following::nb-accordion-item-body[1]//*[@data-name="close"]'
        CRITERIA = '(//*[normalize-space()="Conditional Logic"]//following::nb-accordion-item-body[1]//button)[1]'
        LOGIC = '(//*[normalize-space()="Conditional Logic"]//following::nb-accordion-item-body[1]//nb-select)[2]'
        VALUE = '//*[normalize-space()="Conditional Logic"]//following::nb-accordion-item-body[1]//*[contains(@id, "nb-input-")]'
        VALUE_CHECKBOXES = '//*[normalize-space()="Conditional Logic"]//following::nb-accordion-item-body[1]//nb-select[@id]/button'
        TOLERANCE_PRICE_TYPE = '//*[normalize-space()="Conditional Logic"]//following::nb-accordion-item-body[1]//*[contains(@id, "priceType")]'
        TOLERANCE_REF_PRICE_TYPE = '//*[normalize-space()="Conditional Logic"]//following::nb-accordion-item-body[1]//*[contains(@id, "priceRef")]'

    class ResultsTable:
        PLUS_BUTTON = '//*[normalize-space()="Results"]//..//*[@nbtooltip="Add"]'
        CHECKMARK_BUTTON = '//*[normalize-space()="Results"]//..//*[@data-name="checkmark"]'
        CANCEL_BUTTON = '//*[normalize-space()="Results"]//..//*[@data-name="close"]'
        EDIT_BUTTON = '//*[normalize-space()="Results"]//..//*[@data-name="edit"]'
        DELETE_BUTTON = '//*[normalize-space()="Results"]//..//*[@data-name="trash-2"]'

        ACTION_FILTER = '(//*[normalize-space()="Results"]//..//*[@placeholder="Filter"])[1]'
        ACTION = '//*[normalize-space()="Results"]//..//*[@id="gatingRuleResultAction"]'
        RULE = '//*[normalize-space()="Results"]//..//*[contains(@id,"rule")]'
        REJECTION_TYPE = '//*[normalize-space()="Results"]//..//*[contains(@id, "gatingRuleResultRejectType")]'
        SPLIT = '//*[normalize-space()="Results"]//..//*[contains(@id, "splitRatio")]'
        PRICE_ORIGIN = '//*[normalize-space()="Results"]//..//*[contains(@id, "priceOrigin")]'
        SPLIT_QTY_PRECISION = '//*[normalize-space()="Results"]//..//*[contains(@id, "qtyPrecision")]'
        VENUE = '//*[normalize-space()="Results"]//..//*[contains(@id, "resultVenue")]'
        ROUTE = '//*[normalize-space()="Results"]//..//*[contains(@id, "route")]'
        EXECUTION_STRATEGY = '//*[normalize-space()="Results"]//..//*[contains(@id, "strategy")]//button'
        CHILD_STRATEGY = '//*[normalize-space()="Results"]//..//*[contains(@id, "SORAlgoPolicy")]'
        PROPERTY = '//*[normalize-space()="Results"]//..//*[contains(@id, "gatingRuleResultProperty")]'
        PROPERTY_VALUE = '//*[normalize-space()="Results"]//..//*[contains(@id, "desk") or contains(@type, "button") or contains(@id, "user") or contains(@id, "recoveryDesk_ext")]'
        PROPERTY_VALUE_LIST = '//*[normalize-space()="Results"]//..//*[contains(@id, "recoveryDesk_ext")]'

    class DefaultResult:
        EDIT_BUTTON = '//tr[@tabindex="0"][last()]//*[@nbtooltip="Edit"]'
        CHECKMARK_BUTTON = '//tr[@tabindex="0"][last()]//*[@data-name="checkmark"]'
        CANCEL_BUTTON = '//tr[@tabindex="0"][last()]//*[@data-name="close"]'
        NAME = '//tr[@tabindex="0"][last()]//*[@placeholder="Name *"]'
