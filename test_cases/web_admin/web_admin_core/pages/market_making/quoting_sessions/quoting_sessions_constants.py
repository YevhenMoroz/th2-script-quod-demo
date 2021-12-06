class QuotingSessionsConstants:
    QUOTING_SESSIONS_PAGE_TITLE_XPATH = "//span[@class='entity-title left'][text()='Quoting Sessions ']"

    REFRESH_PAGE_BUTTON_XPATH = "//*[@data-name='refresh']"
    DOWNLOAD_PDF_BUTTON_XPATH = "//*[@data-name='download']"
    DOWNLOAD_PDF_BUTTON_AT_MORE_ACTIONS_XPATH = "//*[@class= 'cdk-overlay-container']//*[@data-name='download']"
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
    # main page

    MAIN_PAGE_NAME_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]//div[1]//input'
    MAIN_PAGE_CONCURRENTLY_ACTIVE_QUOTES_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]//div[2]//input'
    MAIN_PAGE_QUOTE_UPDATE_INTERVAL_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]//div[3]//input'
    MAIN_PAGE_PUBLISHED_QUOTE_ID_FORMAT_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]//div[4]//input'

    # Values tab

    VALUES_TAB_NAME_XPATH = '//*[@formcontrolname="quotingSessionName"]'
    VALUES_TAB_CONCURRENTLY_ACTIVE_QUOTES_AGE_XPATH = '//*[@formcontrolname="concurrentlyActiveQuoteAge"]'
    VALUES_TAB_QUOTE_UPDATE_INTERVAL_XPATH = '//*[@formcontrolname="updateInterval"]'
    VALUES_TAB_PUBLISHED_QUOTE_ID_FORMAT_XPATH = '//*[@formcontrolname="clientQuoteIDFormat"]'
    VALUES_TAB_QUOTE_UPDATE_FORMAT_XPATH = '//*[@id="MDUpdateType"]'

    # checkbox
    VALUES_TAB_ALWAYS_ACKNOWLEDGE_CHECKBOX = '//*[text()="Always Acknowledge Orders"]/preceding-sibling::span'
    VALUES_TAB_ALWAYS_USER_NEW_MD_ENTRY_ID_CHECKBOX = '//*[text()="Always Use New MDEntry ID"]/preceding-sibling::span'
    VALUES_TAB_WAIT_FOR_MARKET_DATE_SUBSCRIPTIONS_CHECKBOX = '//*[text()="Wait For Market Data Subscriptions"]/preceding-sibling::span'
    VALUES_TAB_USE_SAME_SESSION_FOR_MARKET_DATA_AND_TRADING_CHECKBOX = '//*[text()="Use Same Session For Market Data and Trading"]/preceding-sibling::span'

    # Client Tiers tab

    CLIENT_TIERS_TAB_PLUS_BUTTON_XPATH = '//*[text()=" Client Tiers "]/parent::*[@class="expanded"]//*[@data-name="plus"]'
    CLIENT_TIERS_TAB_CLOSE_BUTTON_XPATH = '//*[text()=" Client Tiers "]/parent::*[@class="expanded"]//*[@data-name="close"]'
    CLIENT_TIERS_TAB_CHECKMARK_BUTTON_XPATH = '//*[text()=" Client Tiers "]/parent::*[@class="expanded"]//*[@data-name="checkmark"]'
    CLIENT_TIERS_TAB_EDIT_BUTTON_XPATH = '//*[text()=" Client Tiers "]/parent::*[@class="expanded"]//*[@data-name="edit"]'
    CLIENT_TIERS_TAB_DELETE_BUTTON_XPATH = '//*[text()=" Client Tiers "]/parent::*[@class="expanded"]//*[@data-name="trash-2"]'

    CLIENT_TIERS_TAB_BROADCAST_CLIENT_CLIENT_TIER_ID_XPATH = '//*[@placeholder="Broadcast Client Client Tier ID"]'
    CLIENT_TIERS_TAB_BROADCAST_CLIENT_CLIENT_TIER_ID_FILTER = '//*[@class = "broadcastClientClientTierID ng2-smart-th ng-star-inserted"]//input'
    CLIENT_TIERS_TAB_CLIENT_TIER_ID_XPATH = '//*[@placeholder="Client Tier *"]'
    CLIENT_TIERS_TAB_CLIENT_TIER_ID_FILTER = '//*[@class = "clientTier ng2-smart-th ng-star-inserted"]'

    # Client tier symbols
    CLIENT_TIER_SYMBOLS_TAB_PLUS_BUTTON_XPATH = '//*[text()=" Client Tier Symbols "]/parent::*[@class="expanded"]//*[@data-name="plus"]'
    CLIENT_TIER_SYMBOLS_TAB_CLOSE_BUTTON_XPATH = '//*[text()=" Client Tier Symbols "]/parent::*[@class="expanded"]//*[@data-name="close"]'
    CLIENT_TIER_SYMBOLS_TAB_CHECKMARK_BUTTON_XPATH = '//*[text()=" Client Tier Symbols "]/parent::*[@class="expanded"]//*[@data-name="checkmark"]'
    CLIENT_TIER_SYMBOLS_TAB_EDIT_BUTTON_XPATH = '//*[text()=" Client Tier Symbols "]/parent::*[@class="expanded"]//*[@data-name="edit"]'
    CLIENT_TIER_SYMBOLS_TAB_DELETE_BUTTON_XPATH = '//*[text()=" Client Tier Symbols "]/parent::*[@class="expanded"]//*[@data-name="trash-2"]'

    CLIENT_TIER_SYMBOLS_TAB_SYMBOL_XPATH = '//*[@placeholder="Symbol *"]'
    CLIENT_TIER_SYMBOLS_TAB_SYMBOL_FILTER_XPATH = '//*[@class = "instrSymbol ng2-smart-th ng-star-inserted"]//input'
    CLIENT_TIER_SYMBOLS_TAB_CLIENT_TIER_XPATH = '//*[@placeholder="Client Tier *"]'
    CLIENT_TIER_SYMBOLS_TAB_CLIENT_TIER_FILTER_XPATH = '//*[@class = "clientTier ng2-smart-th ng-star-inserted"]//input'
    CLIENT_TIER_SYMBOLS_TAB_BROADCAST_CLIENT_CLIENT_TIER_ID_XPATH = '//*[@placeholder="Broadcast Client Client Tier ID"]'
    CLIENT_TIER_SYMBOLS_TAB_BROADCAST_CLIENT_CLIENT_TIER_ID_FILTER = '//*[@class = "broadcastClientClientTierID ng2-smart-th ng-star-inserted"]//input'

    # Client client tiers
    CLIENT_CLIENT_TIERS_TAB_PLUS_BUTTON_XPATH = '//*[text()=" Client Client Tiers "]/parent::*[@class="expanded"]//*[@data-name="plus"]'
    CLIENT_CLIENT_TIERS_TAB_CLOSE_BUTTON_XPATH = '//*[text()=" Client Client Tiers "]/parent::*[@class="expanded"]//*[@data-name="close"]'
    CLIENT_CLIENT_TIERS_TAB_CHECKMARK_BUTTON_XPATH = '//*[text()=" Client Client Tiers "]/parent::*[@class="expanded"]//*[@data-name="checkmark"]'
    CLIENT_CLIENT_TIERS_TAB_EDIT_BUTTON_XPATH = '//*[text()=" Client Client Tiers "]/parent::*[@class="expanded"]//*[@data-name="edit"]'
    CLIENT_CLIENT_TIERS_TAB_DELETE_BUTTON_XPATH = '//*[text()=" Client Client Tiers "]/parent::*[@class="expanded"]//*[@data-name="trash-2"]'

    CLIENT_CLIENT_TIERS_TAB_CLIENT_CLIENT_TIER_ID_XPATH = '//*[@placeholder="Client Client Tier ID *"]'
    CLIENT_CLIENT_TIERS_TAB_CLIENT_CLIENT_TIER_ID_FILTER_XPATH = '//*[@class = "clientClientTierID ng2-smart-th ng-star-inserted"]//input'
    CLIENT_CLIENT_TIERS_TAB_CLIENT_TIER_XPATH = '//*[@placeholder="Client Tier *"]'
    CLIENT_CLIENT_TIERS_TAB_CLIENT_TIER_FILTER_XPATH = '//*[@class = "clientTier ng2-smart-th ng-star-inserted"]//input'
