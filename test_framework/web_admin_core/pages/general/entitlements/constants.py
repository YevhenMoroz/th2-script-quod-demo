class EntitlementsConstants:
    ENTITLEMENTS_PAGE_TITLE_XPATH = "//span[@class='entity-title left'][normalize-space()='Entitlements']"

    REFRESH_PAGE_BUTTON_XPATH = "//*[@data-name='refresh']"
    DOWNLOAD_PDF_BUTTON_XPATH = "//nb-icon[@icon='download-outline']//*[@data-name='download']"
    SAVE_CHANGES_BUTTON_XPATH = "//*[normalize-space()='Save Changes']"
    CLEAR_CHANGES_BUTTON_XPATH = "//*[normalize-space()='Clear Changes']"
    CLOSE_WIZARD_XPATH = "//*[@data-name='close']"
    OK_BUTTON_XPATH = '//*[normalize-space()="Ok"]'
    CANCEL_BUTTON_XPATH = '//*[normalize-space()="Cancel"]'
    REVERT_CHANGES_XPATH = "//*[text()='Revert Changes']"
    MORE_ACTIONS_XPATH = "//*[@data-name = 'more-vertical']"
    EDIT_XPATH = "//*[@data-name = 'edit']"
    CLONE_XPATH = "//*[@data-name = 'copy']"
    DELETE_XPATH = "//*[@data-name = 'trash-2']"
    PIN_ROW_XPATH = "//*[@nbtooltip ='Click to Pin Row']"
    NEW_BUTTON_XPATH = '//*[normalize-space()="New"]'
    USER_ICON_AT_RIGHT_CORNER = "//*[@class='control-item icon-btn context-menu-host']"
    LOGOUT_BUTTON_XPATH = "//*[text()='Logout']"
    GO_BACK_BUTTON_XPATH = "//*[text()='Go Back']"

    # Main page
    MAIN_PAGE_USER_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[1]//input'
    MAIN_PAGE_DESK_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[2]//input'
    MAIN_PAGE_VENUE_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[3]//input'
    MAIN_PAGE_SUB_VENUE_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[4]//input'
    MAIN_PAGE_LOCATION_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[5]//input'

    # Values tab
    VALUES_TAB_TICK_BY_TICK_DEPTH_CHECKBOX_XPATH = "//*[text()='Tick By Tick Depth']/preceding-sibling::span"
    VALUES_TAB_HISTORICAL_CHECKBOX_XPATH = "//*[text()='Historical']/preceding-sibling::span"
    VALUES_TAB_TIMES_AND_SALES_CHECKBOX_XPATH = "//*[text()='Times And Sales']/preceding-sibling::span"
    VALUES_TAB_DELAYED_QUOTE_CHECKBOX_XPATH = "//*[text()='Delayed Quote']/preceding-sibling::span"
    VALUES_TAB_DELAYED_DEPTH_CHECKBOX_XPATH = "//*[text()='Delayed Depth']/preceding-sibling::span"
    VALUES_TAB_TICK_BY_TICK_QUOTE_CHECKBOX_XPATH = "//*[text()='Tick By Tick Depth']/preceding-sibling::span"
    VALUES_TAB_NEWS_CHECKBOX_XPATH = "//*[text()='News']/preceding-sibling::span"
    VALUES_TAB_INTRADAY_CHECKBOX_XPATH = "//*[text()='Intraday']/preceding-sibling::span"

    # Dimensions tab
    DIMENSIONS_TAB_USER_XPATH = "//*[@id='user']"
    DIMENSIONS_TAB_DESK_XPATH = "//*[@id='desk']"
    DIMENSIONS_TAB_VENUE_XPATH = "//*[@id='venue']"
    DIMENSIONS_TAB_SUB_VENUE_XPATH = "//*[@id='subVenue']"
    DIMENSIONS_TAB_LOCATION_XPATH = "//*[@id='location']"

    BOTH_DESK_AND_LOCATION_CAN_NOT_BE_FILLED_MESSAGE_XPATH = "//*[text()='Both Desk and Location can not be filled']"

