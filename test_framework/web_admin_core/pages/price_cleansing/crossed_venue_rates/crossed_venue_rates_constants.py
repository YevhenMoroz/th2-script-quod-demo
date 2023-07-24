class CrossedVenueRatesConstants:
    CROSSED_VENUE_RATES_PAGE_TITLE_XPATH = "//span[@class='entity-title left'][normalize-space()='Crossed Venue Rates']"
    REFRESH_PAGE_BUTTON_XPATH = "//*[@data-name='refresh']"
    DOWNLOAD_PDF_BUTTON_XPATH = "//*[@data-name='download']"
    SAVE_CHANGES_BUTTON_XPATH = "//*[normalize-space()='Save Changes']"
    CLEAR_CHANGES_BUTTON_XPATH = "//*[normalize-space()='Clear Changes']"
    CLOSE_WIZARD_XPATH = "//*[@data-name='close']"
    OK_BUTTON_XPATH = '//*[normalize-space()="Ok"]'
    CANCEL_BUTTON_XPATH = '//*[normalize-space()="Cancel"]'
    REVERT_CHANGES_XPATH = "//*[normalize-space()='Revert Changes']"
    MORE_ACTIONS_XPATH = "//*[@data-name = 'more-vertical']"
    EDIT_XPATH = "//*[@data-name = 'edit']"
    CLONE_XPATH = "//*[@data-name = 'copy']"
    DELETE_XPATH = "//*[@data-name = 'trash-2']"
    PIN_ROW_XPATH = "//*[@nbtooltip ='Click to Pin Row']"
    NEW_BUTTON_XPATH = '//*[normalize-space()="New"]'
    USER_ICON_AT_RIGHT_CORNER = "//*[@class='control-item icon-btn context-menu-host']"
    LOGOUT_BUTTON_XPATH = "//*[normalize-space()='Logout']"
    GO_BACK_BUTTON_XPATH = "//*[normalize-space()='Go Back']"
    MAIN_PAGE_DOWNLOAD_CSV_BUTTON_XPATH = '//*[@data-name="download"]'
    INCORRECT_OR_MISSING_VALUES_XPATH = "//*[text()='Incorrect or missing values']"
    SEARCHED_ENTITY = '//*[normalize-space()="{}"]'

    # Main page
    MAIN_PAGE_NAME_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[1]//input'
    MAIN_PAGE_REMOVE_DETECTED_PRICE_UPDATES_FILTER_XPATH = '//*[@class="boolean-filter ng-untouched ng-pristine ng-valid"]'
    MAIN_PAGE_VENUE_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[2]//input'
    MAIN_PAGE_LISTING_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[3]//input'
    MAIN_PAGE_SYMBOL_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[4]//input'
    MAIN_PAGE_INSTR_TYPE_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[5]//input'

    MAIN_PAGE_NAME_XPATH = '//*[@col-id="priceCleansingRuleName"]//span//span[4]'
    MAIN_PAGE_REMOVE_DETECTED_PRICE_UPDATES_XPATH = '//*[@class="custom-checkbox checked"]'
    MAIN_PAGE_VENUE_XPATH = '//*[@col-id="venue.venueID"]//span//span[4]'
    MAIN_PAGE_LISTING_XPATH = '//*[@col-id="listing.symbol"]//span//span[4]'
    MAIN_PAGE_SYMBOL_XPATH = '//*[@col-id="instrSymbol"]//span//span[4]'
    MAIN_PAGE_INSTR_TYPE_XPATH = '//*[@col-id="instrType"]//span//span[4]'

    # Values tab
    VALUES_TAB_NAME_XPATH = '//*[@formcontrolname="priceCleansingRuleName"]'
    VALUES_TAB_REMOVE_DETECTED_PRICE_UPDATES_XPATH = '//*[text()="Remove Detected Price Updates"]/preceding-sibling::span'

    # Dimensions tab
    DIMENSIONS_TAB_VENUE_XPATH = '//*[@id="venue"]'
    DIMENSIONS_TAB_LISTING_XPATH = '//*[@id="listing"]'
    DIMENSIONS_TAB_INSTR_TYPE_XPATH = '//*[@id="instrType"]'
    DIMENSIONS_TAB_SYMBOL_XPATH = '//*[@id="instrSymbol"]'

















