class Constants:
    class MainPage:
        PAGE_TITLE = "//span[@class='entity-title left'][normalize-space()='Cash Positions']"
        PAGE_ICON = '//span[@class="entity-title left"]//*[@data-name="bar-chart"]//*[@d]'
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
        TRANSACTION_TYPE_DROP_MENU = '//*[@class="option-list"]//nb-option'

    class Wizard:
        SAVE_CHANGES_BUTTON = "//*[text()='Save Changes']"
        CLEAR_CHANGES_BUTTON = "//*[text()='Clear Changes']"
        CLOSE_WIZARD_BUTTON = "//*[@data-name='close']"
        CANCEL_BUTTON = '//button[normalize-space()="Cancel"]'
        OK_BUTTON = '//button[normalize-space()="OK"]'
        LEAVE_CONFIRMATION_POP_UP = '//close-dialog'
        REVERT_CHANGES_BUTTON = "//*[text()='Revert Changes']"
        DOWNLOAD_PDF_BUTTON = '//*[@nbtooltip="Download PDF"]//*[@data-name="download"]'
        FOOTER_ERROR_TEXT = '//app-footer-form//span'
        DROP_DOWN_MENU = '//*[@class="option-list"]//span'
        MULTISELECT_FORM_NO_RESULT_TEXT = '//li[contains(@class, "ui-multiselect-empty-message")]'
        MULTISELECT_FORM_LOOK_UP = '//input[@role="textbox"]'
        MULTISELECT_FORM_ITEM = '//p-multiselectitem//li//span[@id]'

        class ValuesTab:
            NAME = '//*[@formcontrolname="cashAccountName"]'
            CLIENT_CASH_ACCOUNT_ID = '//*[@formcontrolname="clientCashAccountID"]'
            VENUE_CASH_ACCOUNT_ID = '//*[@formcontrolname="venueCashAccountID"]'
            CURRENCY = '//*[@id="currency"]'
            CLIENT = '//*[@id="accountGroup"]'
            MARGIN_ACCOUNT_CHECKBOX = '//*[@formcontrolname="isMarginAccount"]//span'
            DEFAULT_CASH_POSITION_CHECKBOX = '//*[@formcontrolname="defaultCashAccount"]//span'
            SECURITY_ACCOUNTS = '//*[@id="Security Accounts"]'
            SECURITY_ACCOUNTS_VALUES = '//*[@id="Security Accounts"]//*[@id="multiselect-values-Security Accounts"]'
            WARNING_MESSAGE = '//*[@class="overlapping-warning"]'

        class PositionsTab:
            ACTUAL_BALANCE = '//*[normalize-space()="Actual Balance"]/following::div[1]'
            INITIAL_BALANCE = '//*[normalize-space()="Initial Balance"]/following::div[1]'
            UNSETTLED_SELL_AMOUNT = '//*[normalize-space()="Unsettled Sell Amount"]/following::div[1]'
            CASH_DEPOSITED = '//*[normalize-space()="Cash Deposited"]/following::div[1]'
            CASH_LOAN = '//*[normalize-space()="Cash Loan"]/following::div[1]'
            TEMPORARY_CASH = '//*[normalize-space()="Temporary Cash"]/following::div[1]'
            COLLATERAL = '//*[normalize-space()="Collateral"]/following::div[1]'

            AVAILABLE_BALANCE = '//*[normalize-space()="Available Balance"]/following::div[1]'
            RESERVED_AMOUNT = '//*[normalize-space()="Reserved Amount"]/following::div[1]'
            UNSETTLED_BUY_AMOUNT = '//*[normalize-space()="Unsettled Buy Amount"]/following::div[1]'
            CASH_WITHDRAWN = '//*[normalize-space()="Cash Withdrawn"]/following::div[1]'
            CASH_HELD_BY_TRANSACTIONS = '//*[normalize-space()="Cash Held by Transactions"]/following::div[1]'
            BOOKED_CASH_LOAN = '//*[normalize-space()="Booked Cash Loan"]/following::div[1]'
            BOOKED_TEMPORARY_CASH = '//*[normalize-space()="Booked Temporary Cash"]/following::div[1]'
            BOOKED_COLLATERAL = '//*[normalize-space()="Booked Collateral"]/following::div[1]'























