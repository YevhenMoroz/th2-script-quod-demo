class Constants:
    class MainPage:
        PAGE_TITLE = "//span[@class='entity-title left'][normalize-space()='Cash Positions']"
        REFRESH_PAGE_BUTTON = "//*[@data-name='refresh']"
        OK_BUTTON = '//*[text()="Ok"]'
        CANCEL_BUTTON = '//*[text()="Cancel"]'
        NEW_BUTTON = '//*[text()="New"]'
        DOWNLOAD_CSV_BUTTON = '//*[@data-name="download"]'
        DISPLAYED_CASH_POSITIONS = "//*[text()='{}']"
        TOGGLE_BUTTON = '//nb-toggle'
        TRANSACTION_BUTTON = '//*[@nbtooltip="Transaction"]//*[@data-name="swap"]'
        TRANSACTION_POP_UP = '//cash-account-transfer-popup'

        NAME_FILTER = '//*[@class="ag-header-container"]/div[2]/div[1]//input'
        CURRENCY_FILTER = '//*[@class="ag-header-container"]/div[2]/div[2]//input'
        CLIENT_FILTER = '//*[@class="ag-header-container"]/div[2]/div[3]//input'
        VENUE_CASH_ACCOUNT_ID_FILTER = '//*[@class="ag-header-container"]/div[2]/div[4]//input'
        CLIENT_CASH_ACCOUNT_ID_FILTER = '//*[@class="ag-header-container"]/div[2]/div[5]//input'
        ENABLED_FILTER = '//*[@class="boolean-filter ng-untouched ng-pristine ng-valid"]'

        NAME = '//*[@col-id="cashAccountName"]//span//span[4]'
        CURRENCY = '//*[@col-id="currency"]//span//span[4]'
        CLIENT = '//*[@col-id="accountGroupName"]//span//span[4]'
        VENUE_CASH_ACCOUNT_ID = '//*[@col-id="venueCashAccountID"]//span//span[4]'
        CLIENT_CASH_ACCOUNT_ID = '//*[@col-id="clientCashAccountID"]//span//span[4]'
        ENABLED = '//*[@class="custom-checkbox checked"]//nb-icon'

        MORE_ACTIONS_BUTTON = "//*[@data-name='more-vertical']"
        EDIT_BUTTON = "//*[@data-name='edit']"
        CLONE_BUTTON = "//*[@data-name='copy']"
        PIN_ROW_BUTTON = "//*[@nbtooltip ='Click to Pin Row']"
        DOWNLOAD_PDF_BUTTON = "//*[@data-name='download']"

        TRANSACTION_TYPE = '//*[@id="cashActTransferType"]'
        AMOUNT = '//*[@id="transferAmt"]'
        REFERENCE = '//*[@id="freeNotes"]'

    class Wizard:
        SAVE_CHANGES_BUTTON = "//*[text()='Save Changes']"
        CLEAR_CHANGES_BUTTON = "//*[text()='Clear Changes']"
        CLOSE_WIZARD_BUTTON = "//*[@data-name='close']"
        REVERT_CHANGES_BUTTON = "//*[text()='Revert Changes']"
        DOWNLOAD_PDF_BUTTON = '//*[@nbtooltip="Download PDF"]//*[@data-name="download"]'
        FOOTER_ERROR_TEXT = '//app-footer-form//span'
        DROP_DOWN_MENU = '//*[@class="option-list"]//span'

        class ValuesTab:
            NAME = '//*[@formcontrolname="cashAccountName"]'
            CLIENT_CASH_ACCOUNT_ID = '//*[@formcontrolname="clientCashAccountID"]'
            VENUE_CASH_ACCOUNT_ID = '//*[@formcontrolname="venueCashAccountID"]'
            CURRENCY = '//*[@id="currency"]'
            CLIENT = '//*[@id="accountGroup"]'
            MARGIN_ACCOUNT_CHECKBOX = '//*[@formcontrolname="isMarginAccount"]//input'
            DEFAULT_CASH_POSITION_CHECKBOX = '//*[@formcontrolname="defaultCashAccount"]//span'
            SECURITY_ACCOUNTS = '//*[@id="Security Accounts"]'

        class PositionsTab:
            TEMPORARY_CASH = '//*[normalize-space()="Temporary Cash"]/following::div[1]'
            RESERVED_LIMIT = '//*[normalize-space()="Reserved Amount"]/following::div[1]'
            COLLATERAL_LIMIT = '//*[normalize-space()="Collateral"]/following::div[1]'























