class CashPositionsConstants:
    CASH_POSITIONS_PAGE_TITLE_XPATH = "//span[@class='entity-title left'][normalize-space()='Cash Positions']"
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
    MAIN_PAGE_DOWNLOAD_CSV_BUTTON_XPATH = '//*[@data-name="download"]'
    INCORRECT_OR_MISSING_VALUES_XPATH = "//*[text()='Incorrect or missing values']"
    DISPLAYED_CASH_POSITIONS_XPATH = "//*[text()='{}']"

    # Main page
    MAIN_PAGE_NAME_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[1]//input'
    MAIN_PAGE_CURRENCY_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[2]//input'
    MAIN_PAGE_CLIENT_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[3]//input'
    MAIN_PAGE_VENUE_CASH_ACCOUNT_ID_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[4]//input'
    MAIN_PAGE_CLIENT_CASH_ACCOUNT_ID_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[5]//input'
    MAIN_PAGE_ENABLED_FILTER_XPATH = '//*[@class="boolean-filter ng-untouched ng-pristine ng-valid"]'

    MAIN_PAGE_NAME_XPATH = '//*[@col-id="cashAccountName"]//span//span[4]'
    MAIN_PAGE_CURRENCY_XPATH = '//*[@col-id="currency"]//span//span[4]'
    MAIN_PAGE_CLIENT_XPATH = '//*[@col-id="accountGroupName"]//span//span[4]'
    MAIN_PAGE_VENUE_CASH_ACCOUNT_ID_XPATH = '//*[@col-id="venueCashAccountID"]//span//span[4]'
    MAIN_PAGE_CLIENT_CASH_ACCOUNT_ID_XPATH = '//*[@col-id="clientCashAccountID"]//span//span[4]'
    MAIN_PAGE_ENABLED_XPATH = '//*[@class="custom-checkbox checked"]//nb-icon'


    # Wizard
    WIZARD_NAME_XPATH = '//*[@formcontrolname="cashAccountName"]'
    WIZARD_CLIENT_CASH_ACCOUNT_ID_XPATH = '//*[@formcontrolname="clientCashAccountID"]'
    WIZARD_VENUE_CASH_ACCOUNT_ID_XPATH = '//*[@formcontrolname="venueCashAccountID"]'
    WIZARD_CURRENCY_XPATH = '//*[@id="currency"]'
    WIZARD_CLIENT_XPATH = '//*[@id="accountGroup"]'























