class Constants:
    class MainPage:
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

        class CashValuesTab:
            CASH_CHECKBOX = '//nb-checkbox[@formcontrolname="includeCash"]//span[@class="custom-checkbox"]'
            TEMPORARY_CASH_CHECKBOX = '//nb-checkbox[@formcontrolname="includeTempCash"]//span[@class="custom-checkbox"]'
            CASH_LOAN_CHECKBOX = '//nb-checkbox[@formcontrolname="includeCashLoan"]//span[@class="custom-checkbox"]'
            COLLATERAL_CHECKBOX = '//nb-checkbox[@formcontrolname="includeCollateralCash"]//span[@class="custom-checkbox"]'
            ALLOW_COLLATERAL_ON_NEGATIVE_LEADER_CHECKBOX = '//nb-checkbox[@formcontrolname="allowCashOnNegativeLedger"]//span[@class="custom-checkbox"]'

        class SecurityValuesTab:
            INCLUDE_SECURITIES_CHECKBOX = '//nb-checkbox[@formcontrolname="includeSecurities"]//span[@class="custom-checkbox"]'
            REFERENCE_VALUE_FIELD = '//input[@id="buyingPowerRefPriceType"]'
            HOLDINGS_RATIO_FIELD = '//input[@id="holdingsRatio"]'
            ALLOW_SECURITIES_ON_NEGATIVE_LEDGERS_CHECKBOX = '//nb-checkbox[@formcontrolname="allowSecuritiesOnNegLedger"]//span[@class="custom-checkbox"]'
            DISALLOW_FOR_SAME_LISTING_CHECKBOX = '//nb-checkbox[@formcontrolname="disallowSameListing"]//span[@class="custom-checkbox"]'
            DISALLOW_FOR_DELIVERABLE_CONTRACTS_CHECKBOX = '//nb-checkbox[@formcontrolname="disallowDelivContracts"]//span[@class="custom-checkbox"]'

            class Table:
                PLUS_BUTTON = '//button[contains(@class, "add-button")]'
                SAVE_CHECKMARK_BUTTON = '//td//*[@data-name="checkmark"]'
                CANCEL_BUTTON = '//td//*[@data-name="close"]'
                EDIT_BUTTON = '//td//*[@data-name="edit"]'
                DELETE_BUTTON = '//td//*[@data-name="trash-2"]'
                SETTLEMENT_PERIOD_FILTER = '(//input[@placeholder="Filter"])[1]'
                POSITION_VALIDITY_FILTER = '(//input[@placeholder="Filter"])[2]'
                MARGIN_METHOD_FILTER = '(//input[@placeholder="Filter"])[3]'
                CUSTOM_PERCENTAGE_FILTER = '(//input[@placeholder="Filter"])[4]'
                SETTLEMENT_PERIOD_FIELD = '//input[@id="settlType"]'
                POSITION_VALIDITY_FIELD = '//input[@id="posValidity"]'
                MARGIN_METHOD_FIELD = '//input[@id="marginMethod"]'
                CUSTOM_PERCENTAGE_FIELD = '//input[@placeholder="Custom %"]'
