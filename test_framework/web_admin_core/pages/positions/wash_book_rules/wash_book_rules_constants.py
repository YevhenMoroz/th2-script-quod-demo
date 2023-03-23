class WashBookRulesConstants:
    WASH_BOOK_RULES_PAGE_TITLE_XPATH = "//span[@class='entity-title left'][normalize-space()='Wash Book Rules']"
    DROP_DOWN_MENU_XPATH = '//*[@class="option-list"]//span'
    SEARCHED_ENTITY_XPATH = '//*[text()="{}"]'

    # main page
    # --more actions
    MORE_ACTIONS_BUTTON_XPATH = "//nb-icon[@title='More Actions']"
    EDIT_AT_MORE_ACTIONS_XPATH = '//*[@data-name="edit"]'
    CLONE_AT_MORE_ACTIONS_XPATH = '//*[@data-name="copy"]'
    DOWNLOAD_PDF_AT_MORE_ACTIONS_XPATH = "//nb-icon[@icon='download-outline']//*[@data-name='download']"
    PIN_TO_ROW_AT_MORE_ACTIONS_XPATH = '//*[@nbtooltip="Click to Pin Row"]'
    DELETE_AT_MORE_ACTIONS_XPATH = '//*[@data-name="trash-2"]'

    OK_BUTTON_XPATH = "//*[text()='Ok']"
    CANCEL_BUTTON_XPATH = "//*[text()='Cancel']"
    NO_BUTTON_XPATH = '//button[normalize-space()="No"]'

    NEW_BUTTON_XPATH = "//*[text()='New']"
    DOWNLOAD_CSV_BUTTON_XPATH = '//*[@data-name="download"]'
    REFRESH_PAGE_BUTTON_XPATH = '//*[@data-name="refresh"]'

    MAIN_PAGE_NAME_FILTER_XPATH = "//*[@class='ag-header-container']/div[2]//div[1]//input"
    MAIN_PAGE_CLIENT_FILTER_XPATH = "//*[@class='ag-header-container']/div[2]//div[2]//input"
    MAIN_PAGE_INSTR_TYPE_FILTER_XPATH = "//*[@class='ag-header-container']/div[2]//div[3]//input"
    MAIN_PAGE_EXECUTION_POLICY_FILTER_XPATH = "//*[@class='ag-header-container']/div[2]//div[4]//input"
    MAIN_PAGE_WASH_BOOK_ACCOUNT_FILTER_XPATH = "//*[@class='ag-header-container']/div[2]//div[5]//input"
    MAIN_PAGE_USER_FILTER_XPATH = "//*[@class='ag-header-container']/div[2]//div[6]//input"
    MAIN_PAGE_DESK_FILTER_XPATH = "//*[@class='ag-header-container']/div[2]//div[7]//input"

    MAIN_PAGE_NAME_XPATH = "//*[@col-id='washBookRuleName']//*[@ref='eValue']"
    MAIN_PAGE_CLIENT_XPATH = "//*[@col-id='accountGroupID']//*[@ref='eValue']"
    MAIN_PAGE_INSTR_TYPE_XPATH = "//*[@col-id='instrType']//*[@ref='eValue']"
    MAIN_PAGE_EXECUTION_POLICY_XPATH = "//*[@col-id='executionPolicy']//*[@ref='eValue']"
    MAIN_PAGE_WASH_BOOK_ACCOUNT_XPATH = "//*[@col-id='washBookAccountID']//*[@ref='eValue']"
    MAIN_PAGE_USER_XPATH = "//*[@col-id='userID']//*[@ref='eValue']"
    MAIN_PAGE_DESK_XPATH = "//*[@col-id='desk.deskName']//*[@ref='eValue']"

    # wizard

    WIZARD_NAME_XPATH = "//*[text()='Name *']/preceding-sibling::input"
    WIZARD_INSTR_TYPE_XPATH = "//*[text()='Instr Type']/preceding-sibling::input"
    WIZARD_EXECUTION_POLICY_XPATH = "//*[text()='Execution Policy']/preceding-sibling::input"
    WIZARD_ACCOUNT_XPATH = "//*[text()='Account *']/preceding-sibling::input"
    WIZARD_CLIENT_XPATH = "//*[text()='Client']/preceding-sibling::input"
    WIZARD_USER_XPATH = "//*[text()='User']/preceding-sibling::input"
    WIZARD_DESK_XPATH = "//*[text()='Desk']/preceding-sibling::input"
    WIZARD_INSTITUTION_XPATH = "//*[@id='institution']"
    WIZARD_CLOSE_BUTTON_XPATH = '//*[@data-name="close"]'
    INSTITUTION_LINK_NAME_AT_ASSIGNMENTS_TAB = '//a[normalize-space()="{}"]'


    SAVE_CHANGES_XPATH = '//*[text()="Save Changes"]'
    CLEAR_CHANGES_XPATH = '//*[text()="Clear Changes"]'
    WIZARD_DOWNLOAD_PDF_XPATH = '//*[@data-name="download"]'

    INCORECT_VALUE_MESSAGE = '//*[text()="Incorrect or missing values"]'


















