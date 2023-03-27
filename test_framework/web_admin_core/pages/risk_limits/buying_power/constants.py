class Constants:
    class MainPage:
        PAGE_TITLE = '//span[@class="entity-title left"][normalize-space()="Buying Power"]'
        GLOBAL_FILTER = '//nb-card-header//*[@placeholder="Filter"]'
        HELP_ICON = '//nb-card-header//*[@nbtooltip="Help"]/a'
        DOWNLOAD_CSV_BUTTON = '//nb-card-header//*[@data-name="download"]'
        FULL_SCREEN_BUTTON = '//nb-card-header//*[@nbtooltip="Full Screen"]/a'
        REFRESH_BUTTON = '//nb-card-header//*[@data-name="refresh"]'
        NEW_BUTTON = '//nb-card-header//*[contains(@class, "new-btn")]'
        NAME_FILTER = '(//input[@class="ag-floating-filter-input"])[1]'
        DESCRIPTION_FILTER = '(//input[@class="ag-floating-filter-input"])[2]'
        OK_BUTTON = '//*[normalize-space()="Ok" or normalize-space()="OK"]'
        CANCEL_BUTTON = '//button[normalize-space()="Cancel"]'
        SEARCHED_ENTITY = '//*[text()="{}"]'
        PINNED_ENTITY = '//*[@ref="eTop"]//*[@col-id="buyingPowerLimitName"]//span[normalize-space()="{}"]'

        class MoreActions:
            MORE_ACTIONS_BUTTON = '//*[@data-name="more-vertical"]'
            EDIT_BUTTON = '//nb-overlay-container//*[@data-name="edit"]'
            CLONE_BUTTON = '//nb-overlay-container//*[@data-name="copy"]'
            DELETE_BUTTON = '//nb-overlay-container//*[@data-name="trash-2"]'
            DOWNLOAD_PDF_BUTTON = '//nb-overlay-container//*[@data-name="download"]'
            PIN_BUTTON = '//nb-overlay-container//*[@icon="unpinned-outline"]'

    class Wizard:
        HELP_ICON = '//nb-card-header//*[@nbtooltip="Help"]/a'
        DOWNLOAD_PDF_BUTTON = '//nb-card-header//*[@data-name="download"]'
        CLOSE_BUTTON = '//nb-card-header//*[@data-name="close"]'
        CLEAR_CHANGES_BUTTON = '//button[normalize-space()="Clear Changes"]'
        SAVE_CHANGES_BUTTON = '//button[normalize-space()="Save Changes"]'
        OK_BUTTON = '//*[normalize-space()="Ok" or normalize-space()="OK"]'
        CANCEL_BUTTON = '//button[normalize-space()="Cancel"]'
        REVERT_CHANGES = '//button[normalize-space()="Revert Changes"]'
        NO_BUTTON = '//button[normalize-space()="No"]'
        DROP_DOWN_MENU = '//*[@class="option-list"]//span'

        class ValuesTab:
            NAME_FIELD = '//input[@id="buyingPowerLimitName"]'
            DESCRIPTION_FIELD = '//input[@id="buyingPowerLimitDesc"]'

        class AssignmentsTab:
            INSTITUTION_FIELD = '//*[@id="institution"]'

        class CashValuesTab:
            CASH_CHECKBOX = '//*[normalize-space()="Cash"]/preceding-sibling::span'
            TEMPORARY_CASH_CHECKBOX = '//*[normalize-space()="Temporary Cash"]/preceding-sibling::span'

        class SecurityValuesTab:
            TRADE_ON_MARGIN_CHECKBOX = '//*[normalize-space()="Trade on Margin"]/preceding-sibling::span'
            GLOBAL_MARGIN_FIELD = '//*[@id="globalMargin"]'

            class Table:
                PLUS_BUTTON = '//*[normalize-space()="Security Values"]//..//button[contains(@class, "add-button")]'
                SAVE_CHECKMARK_BUTTON = '//*[normalize-space()="Security Values"]//..//td//*[@data-name="checkmark"]'
                CANCEL_BUTTON = '//*[normalize-space()="Security Values"]//..//td//*[@data-name="close"]'
                EDIT_BUTTON = '//*[normalize-space()="Security Values"]//..//td//*[@data-name="edit"]'
                DELETE_BUTTON = '//*[normalize-space()="Security Values"]//..//td//*[@data-name="trash-2"]'

                INSTRUMENT_TYPE_FILTER = '(//*[normalize-space()="Security Values"]//..//thead//input[@placeholder="Filter"])[1]'
                INSTRUMENT_GROUP_FILTER = '(//*[normalize-space()="Security Values"]//..//thead//input[@placeholder="Filter"])[2]'
                UNDERLYING_LISTING_FILTER = '(//*[normalize-space()="Security Values"]//..//thead//input[@placeholder="Filter"])[3]'
                HAIRCUT_VALUE_FILTER = '(//*[normalize-space()="Security Values"]//..//thead//input[@placeholder="Filter"])[4]'

                INSTRUMENT_TYPE_FIELD = '//*[normalize-space()="Security Values"]//..//*[@id="instrType"]'
                INSTRUMENT_GROUP_FIELD = '//*[normalize-space()="Security Values"]//..//input[@id="instrumentGroup"]'
                UNDERLYING_LISTING_FIELD = '//*[normalize-space()="Security Values"]//..//input[@id="account"]'
                HAIRCUT_VALUE_FIELD = '//input[@placeholder="Haircut Value"]'

        class RiskMarginTab:
            class Table:
                PLUS_BUTTON = '//*[normalize-space()="Risk Margin"]//..//button[contains(@class, "add-button")]'
                SAVE_CHECKMARK_BUTTON = '//*[normalize-space()="Risk Margin"]//..//td//*[@data-name="checkmark"]'
                CANCEL_BUTTON = '//*[normalize-space()="Risk Margin"]//..//td//*[@data-name="close"]'
                EDIT_BUTTON = '//*[normalize-space()="Risk Margin"]//..//td//*[@data-name="edit"]'
                DELETE_BUTTON = '//*[normalize-space()="Risk Margin"]//..//td//*[@data-name="trash-2"]'

                MARGIN_METHOD_FILTER = '(//*[normalize-space()="Risk Margin"]//..//thead//*[@placeholder="Filter"])[1]'
                INITIAL_MARGIN_FILTER = '(//*[normalize-space()="Risk Margin"]//..//thead//*[@placeholder="Filter"])[2]'
                MAINTENANCE_MARGIN_FILTER = '(//*[normalize-space()="Risk Margin"]//..//thead//*[@placeholder="Filter"])[3]'
                INSTRUMENT_TYPE_FILTER = '(//*[normalize-space()="Risk Margin"]//..//thead//*[@placeholder="Filter"])[4]'
                INSTRUMENT_GROUP_FILTER = '(//*[normalize-space()="Risk Margin"]//..//thead//*[@placeholder="Filter"])[5]'
                INSTRUMENT_FILTER = '(//*[normalize-space()="Risk Margin"]//..//thead//*[@placeholder="Filter"])[6]'
                UNDERLYING_INSTRUMENT_FILTER = '(//*[normalize-space()="Risk Margin"]//..//thead//*[@placeholder="Filter"])[7]'

                MARGIN_METHOD_FIELD = '//*[@id="marginMethod"]'
                INITIAL_MARGIN_FIELD = '//input[@placeholder="Initial Margin *"]'
                MAINTENANCE_MARGIN_FIELD = '//input[@placeholder="Maintenance Margin *"]'
                INSTRUMENT_TYPE_FIELD = '//*[normalize-space()="Risk Margin"]//..//input[@id="instrType"]'
                INSTRUMENT_GROUP_FIELD = '//*[normalize-space()="Risk Margin"]//..//input[@id="instrumentGroup"]'
                INSTRUMENT_FIELD = '//*[normalize-space()="Risk Margin"]//..//input[@id="account"]'
                UNDERLYING_INSTRUMENT_FIELD = '//input[@id="underlyingAccount"]'