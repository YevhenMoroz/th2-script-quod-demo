class AccountsConstants:
    DOWNLOAD_PDF_BUTTON_XPATH = "//*[@data-name='download']"
    DOWNLOAD_CSV_BUTTON_XPATH = '//nb-card-header//*[@data-name="download"]'
    ACCOUNTS_PAGE_TITLE_XPATH = "//span[@class='entity-title left'][normalize-space()='Accounts']"
    NEW_BUTTON_XPATH = '//*[normalize-space()="Accounts"]//..//*[normalize-space()="New"]'
    MAIN_PAGE_CLEARING_ACCOUNT_TYPE ='//*[@col-id="clearingAccountType"]//*[@class="ag-group-value"]'
    MAIN_PAGE_CLIENT ='//*[@col-id="accountGroup.accountGroupName"]//*[@class="ag-group-value"]'
    ACCOUNT_VALUE_FOR_LOAD = "//*[@id='undefined']"
    LOAD_BUTTON = "//button[text()='Load']"
    CONFIRM_ACTION_BUTTON_XPATH = "//div[@class='confirmation-dialog']//button[normalize-space()='Ok']"
    DISPLAYED_ACCOUNT_XPATH = "//*[text()='{}']"
    REQUEST_FAILED_MESSAGE_XPATH = "//nb-toast[contains(@class, 'danger')]"
    DROP_DOWN_MENU_XPATH = '//*[@class="option-list"]//span'
    MULTISELECT_DROP_DOWN = '//*[@id="textCash Accounts"]'
    MULTISELECT_FORM_LOOK_UP = '//input[@role="textbox"]'
    UNABLE_UNASSIGN_CASH_ACCOUNT_MESSAGE = '//*[@class="overlapping-warning"]'
    CLOSE_WIZARD_BUTTON = '//nb-card-header//*[@data-name="close"]'
    CANCEL_BUTTON = '//button[normalize-space()="Cancel"]'
    NO_BUTTON = '//button[normalize-space()="No"]'
    OK_BUTTON = '//button[normalize-space()="OK"]'

    MAIN_PAGE_CLIENT_MATCHING_ID_XPATH = '(//*[@col-id="clientMatchingID"])[2]//*[@class="ag-group-value"]'

    WIZARD_ID_INPUT_XPATH = "//input[@id='accountID']"
    WIZARD_ID_EDITOR_XPATH = '//*[@class="breadcrumbs entity-title"]'
    WIZARD_EXT_ID_CLIENT_INPUT_XPATH = "//input[@id='clientAccountID']"
    WIZARD_CLIENT_COMBOBOX_XPATH = "//input[@id='accountGroup']"
    WIZARD_NAME_INPUT_XPATH = "//input[@id='accountDesc']"
    WIZARD_POSITION_SOURCE_COMBOBOX_XPATH = "//input[@id='positionSource']"
    WIZARD_CASH_ACCOUNTS_XPATH = '//*[@id="Cash Accounts"]'
    WIZARD_CLEARING_ACCOUNT_TYPE_COMBOBOX_XPATH = "//input[@id='clearingAccountType']"
    WIZARD_CLIENT_ID_SOURCE_COMBOBOX_XPATH = "//input[@id='clientAccountIDSource']"
    WIZARD_DEFAULT_ACCOUNT_CHECKBOX_XPATH = "//nb-checkbox[@formcontrolname='defaultAccount']"
    WIZARD_TRADE_CONFIRM_ELIGIBILITY_CHECKBOX_XPATH = '//nb-checkbox[@formcontrolname="tradeConfirmEligibility"]//span[contains(@class, "custom-checkbox")]'
    WIZARD_CLIENT_MATCHING_ID_INPUT_XPATH = "//input[@formcontrolname='clientMatchingID']"
    WIZARD_BO_FILED_1_INPUT_XPATH = "//input[@id='confirmationMisc0']"
    WIZARD_BO_FILED_2_INPUT_XPATH = "//input[@id='confirmationMisc1']"
    WIZARD_BO_FILED_3_INPUT_XPATH = "//input[@id='confirmationMisc2']"
    WIZARD_BO_FILED_4_INPUT_XPATH = "//input[@id='confirmationMisc3']"
    WIZARD_BO_FILED_5_INPUT_XPATH = "//input[@id='confirmationMisc4']"
    WIZARD_COMMISSION_EXEMPTION_CHECKBOX_XPATH = '//nb-checkbox[@formcontrolname="brokerCommissionExemption"]//span[contains(@class, "custom-checkbox")]'
    WIZARD_COUNTERPART_COMBOBOX_XPATH = "//input[@id='counterpart']"
    WIZARD_DEFAULT_ROUTE_COMBOBOX_XPATH = "//input[@id='defaultRoute']"
    WIZARD_SAVE_BUTTON_XPATH = "//button[normalize-space()='Save Changes']"
    INCORRECT_OR_MISSING_VALUES_XPATH = "//*[text()='Incorrect or missing values']"
    WIZARD_DUMMY_CHECKBOX_XPATH = '//*[text()="Dummy"]/preceding-sibling::span'
    WIZARD_TITLE_XPATH = '//*[@class="breadcrumbs entity-title"]//*[text()="Accounts"]'

    ADD_DIMENSIONS_ENTITY_BUTTON_XPATH = "//*[text()=' Dimensions ']/following-sibling::nb-accordion-item-body//*[@data-name='plus']"
    ADD_ROUTES_ENTITY_BUTTON_XPATH = "//*[text()=' Routes ']/following-sibling::nb-accordion-item-body//*[@data-name='plus']"

    DIMENSIONS_VENUE_ACCOUNT_FILTER_XPATH = "//*[text()=' Dimensions ']/following-sibling::nb-accordion-item-body//thead//tr[2]//th[2]//input"
    DIMENSIONS_VENUE_FILTER_XPATH = "//*[text()=' Dimensions ']/following-sibling::nb-accordion-item-body//thead//tr[2]//th[3]//input"
    DIMENSIONS_ACCOUNT_ID_SOURCE_FILTER_XPATH = "//*[text()=' Dimensions ']/following-sibling::nb-accordion-item-body//thead//tr[2]//th[4]//input"
    DIMENSIONS_DEFAULT_ROUTE_FILTER_XPATH = "//*[text()=' Dimensions ']/following-sibling::nb-accordion-item-body//thead//tr[2]//th[5]//input"
    DIMENSIONS_STAMP_EXEMPT_FILTER_XPATH = "//*[text()=' Dimensions ']/following-sibling::nb-accordion-item-body//thead//tr[2]//th[6]//input"
    DIMENSIONS_LEVY_EXEMPT_FILTER_XPATH = "//*[text()=' Dimensions ']/following-sibling::nb-accordion-item-body//thead//tr[2]//th[7]//input"
    DIMENSIONS_PER_TRANSAC_EXEMPT_FILTER_XPATH = "//*[text()=' Dimensions ']/following-sibling::nb-accordion-item-body//thead//tr[2]//th[8]//input"
    DIMENSIONS_VENUE_CLIENT_ACCOUNT_NAME_FILTER_XPATH = "//*[text()=' Dimensions ']/following-sibling::nb-accordion-item-body//thead//tr[2]//th[9]//input"

    DIMENSIONS_PLUS_BUTTON_XPATH = "//*[text() = ' Dimensions ']/parent::*[@class='expanded']//*[@data-name='plus']"
    DIMENSIONS_EDIT_BUTTON_XPATH = "//*[text() = ' Dimensions ']/parent::*[@class='expanded']//*[@data-name='edit']"
    DIMENSIONS_DELETE_BUTTON_XPATH = "//*[text() = ' Dimensions ']/parent::*[@class='expanded']//*[@data-name='trash-2']"
    DIMENSIONS_CREATE_ENTITY_BUTTON_XPATH = "//*[text() = ' Dimensions ']/parent::*[@class='expanded']//*[@data-name='checkmark']"
    DIMENSIONS_DISCARD_ENTITY_BUTTON_XPATH = "//*[text() = ' Dimensions ']/parent::*[@class='expanded']//*[@data-name='close']"

    DIMENSIONS_VENUE_ACCOUNT_INPUT_XPATH = "//nb-accordion/nb-accordion-item[2]//input[@placeholder='Venue Account *']"
    DIMENSIONS_VENUE_COMBOBOX_XPATH = "//nb-accordion/nb-accordion-item[2]//input[@placeholder='Venue *']"
    DIMENSIONS_ACCOUNT_ID_SOURCE_COMBOBOX_XPATH = "//nb-accordion/nb-accordion-item[2]//input[@placeholder='Account ID Source *']"
    DIMENSIONS_DEFAULT_ROUTE_COMBOBOX_XPATH = "//nb-accordion/nb-accordion-item[2]//input[@placeholder='Default Route']"
    DIMENSIONS_STAMP_EXEMPT_CHECKBOX_XPATH = '//nb-accordion/nb-accordion-item[2]//td[6]//nb-checkbox//span[contains(@class, "custom-checkbox")]'
    DIMENSIONS_LEVY_EXEMPT_CHECKBOX_XPATH = '//nb-accordion/nb-accordion-item[2]//td[7]//nb-checkbox//span[contains(@class, "custom-checkbox")]'
    DIMENSIONS_PER_TRANSAC_EXEMPT_CHECKBOX_XPATH = '//nb-accordion/nb-accordion-item[2]//td[8]//nb-checkbox//span[contains(@class, "custom-checkbox")]'
    DIMENSIONS_VENUE_CLIENT_ACCOUNT_NAME_INPUT_XPATH = "//nb-accordion/nb-accordion-item[2]//input[@placeholder='Venue Client Account Name']"

    ROUTES_ROUTE_ACCOUNT_NAME_FILTER_XPATH = '//*[normalize-space()="Routes"]//parent::nb-accordion-item//tr[2]//th[2]//input'
    ROUTES_ROUTE_FILTER_XPATH = '//*[normalize-space()="Routes"]//parent::nb-accordion-item//tr[2]//th[3]//input'
    ROUTES_ROUTE_ACCOUNT_NAME_INPUT_XPATH = "//nb-accordion/nb-accordion-item[3]//input[@placeholder='Route Account Name *']"
    ROUTES_ROUTE_COMBOBOX_XPATH = "//nb-accordion/nb-accordion-item[3]//input[@placeholder='Route *']"
    ROUTES_DEFAULT_ROUTE_XPATH = '//*[normalize-space()="Routes"]//..//*[@id="defaultRoute"]'
    ROUTES_AGENT_FEE_EXEMPTION_XPATH = '//nb-accordion/nb-accordion-item[3]//*[@class="label"] //span'

    ROUTES_EDIT_BUTTON_XPATH = "//*[text()=' Routes ']/following-sibling::nb-accordion-item-body//*[@data-name='edit']"
    ROUTES_DELETE_BUTTON_XPATH = "//*[text()=' Routes ']/following-sibling::nb-accordion-item-body//*[@data-name='trash-2']"
    ROUTES_CREATE_ENTITY_BUTTON_XPATH = "//*[text()=' Routes ']/following-sibling::nb-accordion-item-body//*[@data-name='checkmark']"
    ROUTES_DISCARD_ENTITY_BUTTON_XPATH = "//*[text()=' Routes ']/following-sibling::nb-accordion-item-body//*[@data-name='close']"

    ROUTES_ROUTE_ACCOUNT_NAME_TABLE_ROW = '//*[normalize-space()="Route Account Name"]//ancestor::p-table//td[2]//span[@class="ng-star-inserted"]'
    ROUTES_ROUTE_TABLE_ROW = '//*[normalize-space()="Route Account Name"]//ancestor::p-table//td[3]//span[@class="ng-star-inserted"]'

    ID_INPUT_GRID_FILTER_XPATH = '//*[@col-id="accountID"]//following::input[@ref="eFloatingFilterText"][1]'
    ID_VALUE_GRID_XPATH = "//div[contains(@class, 'ag-row-first')]//div[@col-id='accountID']//span[contains(@class, 'ag-group-value')]"
    MORE_ACTIONS_BUTTON_GRID_XPATH = "//nb-icon[@title='More Actions']"
    EDIT_ENTITY_BUTTON_GRID_XPATH = "//nb-icon[@nbtooltip='Edit']"
    CLONE_ENTITY_BUTTON_GRID_XPATH = "//nb-icon[@nbtooltip='Clone']"
    DOWNLOAD_PDF_ENTITY_BUTTON_GRID_XPATH = "//nb-icon[@nbtooltip='Download PDF']"
    ENABLE_DISABLE_TOGGLE_BUTTON_GRID_XPATH = "//div[contains(@class, 'toggle')]"

    POPUP_TEXT_XPATH = "//nb-toast//span[@class='title subtitle']"
    EXT_ID_CLIENT_XPATH = "//*[@col-id='clientAccountID']/span[1]/span[4]"