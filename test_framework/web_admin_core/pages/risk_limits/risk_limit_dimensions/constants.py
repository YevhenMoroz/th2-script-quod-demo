class Constants:
    class MainPage:
        TITLE = '//span[@class="entity-title left"][normalize-space()="Risk Limit Dimensions"]'

        USER_ICON_AT_RIGHT_CORNER = '//*[@class="control-item icon-btn context-menu-host"]'
        LOGOUT_BUTTON = '//*[text()="Logout"]'

        GLOBAL_FILTER = '//nb-card-header//*[@placeholder="Filter"]'
        DOWNLOAD_CSV_BUTTON = '//*[@nbtooltip="Download CSV"]//a'
        FULL_SCREEN_BUTTON = '//*[@nbtooltip="Full Screen"]//a'
        REFRESH_PAGE_BUTTON = '//*[@nbtooltip="Refresh Page"]//a'
        NEW_BUTTON = '//*[text()="New"]'

        NAME_FILTER = '//*[@style="width: 200px; left: 0px;"]//input[@ref="eFloatingFilterText"]'
        DESCRIPTION_FILTER = '//*[@style="width: 200px; left: 200px;"]//input[@ref="eFloatingFilterText"]'
        POS_VALIDITY_FILTER = '//*[@style="width: 200px; left: 400px;"]//input[@ref="eFloatingFilterText"]'
        SIDE_FILTER = '//*[@style="width: 200px; left: 600px;"]//input[@ref="eFloatingFilterText"]'
        POSITION_TYPE_FILTER = '//*[@style="width: 200px; left: 800px;"]//input[@ref="eFloatingFilterText"]'
        LISTING_GROUP_FILTER = '//*[@style="width: 200px; left: 1000px;"]//input[@ref="eFloatingFilterText"]'
        EXECUTION_POLICY_FILTER = '//*[@style="width: 200px; left: 1200px;"]//input[@ref="eFloatingFilterText"]'
        INSTR_TYPE_FILTER = '//*[@style="width: 200px; left: 1400px;"]//input[@ref="eFloatingFilterText"]'
        SETTL_TYPE_FILTER = '//*[@style="width: 200px; left: 1600px;"]//input[@ref="eFloatingFilterText"]'
        SUB_VENUE_FILTER = '//*[@style="width: 200px; left: 1800px;"]//input[@ref="eFloatingFilterText"]'
        CLIENT_LIST_FILTER = '//*[@style="width: 200px; left: 2000px;"]//input[@ref="eFloatingFilterText"]'
        LISTING_FILTER = '//*[@style="width: 200px; left: 2200px;"]//input[@ref="eFloatingFilterText"]'
        ROUTE_FILTER = '//*[@style="width: 200px; left: 2400px;"]//input[@ref="eFloatingFilterText"]'
        VENUE_FILTER = '//*[@style="width: 200px; left: 2600px;"]//input[@ref="eFloatingFilterText"]'
        ALIVE_FILTER = '//*[@style="width: 200px; left: 2800px;"]//input[@ref="eFloatingFilterText"]'

        OK_BUTTON = '//*[text()="Ok"]'
        CANCEL_BUTTON = '//*[text()="Cancel"]'

        SEARCHED_ENTITY = '//*[text() = "{}"]'

        class MoreAction:
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
        CHECKBOX_DROP_DOWN_MENU = '//p-multiselectitem//li[@style="display: block;"]//span[@id]'
        DROP_DOWN_MENU = '//nb-option//span'
        DIMENSIONS_LIMIT_INFO_MESSAGE = '//*[text()="Maximum 4 different dimensions"]'
        SELECT_ALL_CHECKBOX = '//div[contains(@class, "ui-widget-header")]//span[contains(@class, "ui-chkbox")]'
        MULTISELECT_FRAME_FILTER = '//input[contains(@class, "ui-inputtext")]'
        MULTISELECT_FRAME_ENTITY_CHECKBOX = '//span[normalize-space()="{}"]//..//span[contains(@class, "ui-chkbox")]'
        MULTISELECT_FRAME_SELECT_ALL_CHECKBOX = '//div[contains(@class, "ui-multiselect-header")]//div[@role="checkbox"]'

        class ValuesTab:
            NAME = '//*[@formcontrolname="riskLimitDimensionName"]'
            DESCRIPTION = '//*[@formcontrolname="riskLimitDimensionDesc"]'
            TRADING_LIMITS = '//*[@id="Trading Limits"]'
            CUM_TRADING_LIMITS = '//*[@id="Cum Trading Limits"]'
            POSITION_LIMITS = '//*[@id="Position Limits"]'
            BUYING_POWERS = '//*[@id="Buying Powers"]'

        class DimensionsTab:
            ACCOUNT_DIMENSIONS = '//*[@id="typeCCA"]'
            ACCOUNTS = '//*[@id="Accounts"]'
            CLIENTS = '//*[@id="Clients"]'
            CLIENT_LIST = '//*[@id="clientList"]'
            USER_DIMENSIONS = '//*[@id="typeDU"]'
            DESKS = '//*[@id="Desks"]'
            USERS = '//*[@id="Users"]'
            REFERENCE_DATA_DIMENSIONS = '//*[@id="typeVSLL"]'
            VENUES = '//*[@id="venue"]'
            SUB_VENUE = '//*[@id="subVenue"]'
            LISTING_GROUP = '//*[@id="listingGroup"]'
            LISTING = '//*[@id="securityBlock"]'
            INSTRUMENT_TYPE = '//*[@id="instrType"]'
            TRADING_PHASE = '//*[@id="standardTradingPhase"]'
            ROUTE = '//*[@id="route"]'
            EXECUTION_POLICY = '//*[@id="executionPolicy"]'
            POSITION_TYPE = '//*[@id="positionType"]'
            POSITION_VALIDITY = '//*[@id="posValidity"]'
            SETTLEMENT_PERIOD = '//*[@id="settlType"]'
            SIDE = '//*[@id="side"]'
            POSITION_LIMITS = '//*[normalize-space(text()) = "Dimensions"]//..//*[normalize-space(text())="Position Limits"]'
            ORDER_TYPE = '//*[@id="ordType"]'
            DISPLAY_ORDER_CHECKBOX = '//*[normalize-space()="Display Order"]//..//*[contains(@class, "custom-checkbox")]'

        class AssignmentsTab:
            INSTITUTION = '//*[@id="institution"]'
