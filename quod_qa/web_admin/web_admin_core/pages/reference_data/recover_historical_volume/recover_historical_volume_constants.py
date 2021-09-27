class RecoverHistoricalVolumeConstants:
    RECOVER_HISTORICAL_VOLUME_PAGE_TITLE_XPATH = "//span[@class='entity-title left'][text()='Recover Historical Volume ']"
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

    # Main page
    MAIN_PAGE_LISTING_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[1]//input'
    MAIN_PAGE_LISTING_XPATH = '//*[@col-id="listing.symbol"]//span//span[4]'
    MAIN_PAGE_QUERY_HISTORIC_DATA_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[2]//select'
    MAIN_PAGE_QUERY_HISTORIC_DATA_XPATH = '//*[@col-id="queryHistoricData"]//span[@class="custom-checkbox"]'
    MAIN_PAGE_SUBSCRIBE_TO_QUOTE_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[3]//select'
    MAIN_PAGE_SUBSCRIBE_TO_QUOTE_XPATH = '//*[@col-id="subscribeToQuote"]//span[@class="custom-checkbox"]'
    MAIN_PAGE_SUBSCRIBE_TO_TRADE_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[4]//select'
    MAIN_PAGE_SUBSCRIBE_TO_TRADE_XPATH = '//*[@col-id="subscribeToQuote"]//span[@class="custom-checkbox"]'
    MAIN_PAGE_SUBSCRIBE_TO_DEPTH_FILTER_XPATH = '//*[@class="subscribeToTrade"]/div[2]/div[5]//select'
    MAIN_PAGE_SUBSCRIBE_TO_DEPTH_XPATH = '//*[@col-id="subscribeToDepth"]//span[@class="custom-checkbox"]'

    # wizard

    WIZARD_LISTING_XPATH = '//*[@id="listing"]'

    WIZARD_QUERY_HISTORIC_DATA_XPATH = '//*[text()="Query Historic Data"]/preceding-sibling::span'
    WIZARD_SUBSCRIBE_TO_QUOTE_XPATH = '//*[text()="Subscribe To Quote"]/preceding-sibling::span'
    WIZARD_SUBSCRIBE_TO_TRADE_XPATH = '//*[text()="Subscribe To Trade"]/preceding-sibling::span'
    WIZARD_SUBSCRIBE_TO_DEPTH_XPATH = '//*[text()="Subscribe To Depth"]/preceding-sibling::span'
