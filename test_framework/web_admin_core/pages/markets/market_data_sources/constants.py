class MarketDataSourcesConstants:
    MARKET_DATA_SOURCE_PAGE_TITLE_XPATH = "//span[@class='entity-title left'][text()='Market Data Sources ']"
    DROP_DOWN_MENU_XPATH = '//*[@class="option-list"]//span'

    # main page
    # --more actions
    MORE_ACTIONS_BUTTON_XPATH = "//nb-icon[@title='More Actions']"
    EDIT_AT_MORE_ACTIONS_XPATH = '//*[@data-name="edit"]'
    CLONE_AT_MORE_ACTIONS_XPATH = '//*[@data-name="copy"]'
    DOWNLOAD_PDF_AT_MORE_ACTIONS_XPATH = "//nb-icon[@icon='download-outline']//*[@data-name='download']"
    PIN_TO_ROW_AT_MORE_ACTIONS_XPATH = '//*[@nbtooltip="Click to Pin Row"]'
    DELETE_AT_MORE_ACTIONS_XPATH = '//*[@data-name="trash-2"]'

    OK_BUTTON_XPATH = "//*[text()='Ok']"
    CANCEL_BUTTON_XPATH ="//*[text()='Cancel']"
    NO_BUTTON_XPATH ="//*[text()='No']"


    NEW_BUTTON_XPATH = "//*[text()='New']"
    DOWNLOAD_CSV_BUTTON_XPATH = '//*[@data-name="download"]'
    REFRESH_PAGE_BUTTON_XPATH = '//*[@data-name="refresh"]'

    MAIN_PAGE_SYMBOL_FILTER_XPATH = "//*[@class='ag-header-container']/div[2]//div[1]//input"
    MAIN_PAGE_USER_FILTER_XPATH = "//*[@class='ag-header-container']/div[2]//div[2]//input"
    MAIN_PAGE_VENUE_FILTER_XPATH = "//*[@class='ag-header-container']/div[2]//div[3]//input"
    MAIN_PAGE_MDSOURCE_FILTER_XPATH = "//*[@class='ag-header-container']/div[2]//div[4]//input"

    MAIN_PAGE_SYMBOL_XPATH = "//*[@col-id='instrSymbol']//*[@ref='eValue']"
    MAIN_PAGE_USER_XPATH = "//*[@col-id='userID']//*[@ref='eValue']"
    MAIN_PAGE_VENUE_XPATH = "//*[@col-id='venue.venueName']//*[@ref='eValue']"
    MAIN_PAGE_MDSOURCE_XPATH = "//*[@col-id='MDSource']//*[@ref='eValue']"

    # Wizard
    WIZARD_CLOSE_BUTTON_XPATH = '//*[@data-name="close"]'

    WIZARD_SYMBOL_XPATH = "//*[text()='Symbol *']/preceding-sibling::input"
    WIZARD_USER_XPATH = "//*[text()='User *']/preceding-sibling::input"
    WIZARD_VENUE_XPATH = "//*[text()='Venue *']/preceding-sibling::input"
    WIZARD_MDSOURCE_XPATH = "//*[text()='MD Source *']/preceding-sibling::input"

    SAVE_CHANGES_XPATH = '//*[text()="Save Changes"]'
    CLEAR_CHANGES_XPATH = '//*[text()="Clear Changes"]'
    WIZARD_DOWNLOAD_PDF_XPATH = '//*[@data-name="download"]'

    INCORECT_VALUE_MESSAGE = '//*[text()="Incorrect or missing values"]'