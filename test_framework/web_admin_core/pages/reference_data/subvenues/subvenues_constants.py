class SubVenuesConstants:
    SUBVENUES_PAGE_TITLE_XPATH = "//span[@class='entity-title left'][text()='SubVenues ']"
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
    MAIN_PAGE_NAME_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[1]//input'
    MAIN_PAGE_NAME_XPATH = '//*[@col-id="subVenueName"]//span//span[4]'
    MAIN_PAGE_EXT_ID_VENUE_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[2]//input'
    MAIN_PAGE_EXT_ID_VENUE_XPATH = '//*[@col-id="venueSubVenueID"]//span//span[4]'
    MAIN_PAGE_VENUE_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[3]//input'
    MAIN_PAGE_VENUE_XPATH = '//*[@col-id="venue.venueID"]//span//span[4]'
    MAIN_PAGE_MARKET_DATA_SOURCE_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[4]//input'
    MAIN_PAGE_MARKET_DATA_SOURCE_XPATH = '//*[@col-id="MDSource"]//span//span[4]'
    MAIN_PAGE_DEFAULT_SYMBOL_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[5]//input'
    MAIN_PAGE_DEFAULT_SYMBOL_XPATH = '//*[@col-id="defaultMDSymbol"]//span//span[4]'
    MAIN_PAGE_NEWS_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[6]//select'
    MAIN_PAGE_NEWS_XPATH = '//*[@col-id="supportNews"]//label//input'
    MAIN_PAGE_NEWS_SYMBOL_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[7]//input'
    MAIN_PAGE_NEWS_SYMBOL_XPATH = '//*[@col-id="newsMDSymbol"]//span//span[4]'

    # Description tab

    DESCRIPTION_TAB_NAME_XPATH = '//*[@formcontrolname="subVenueName"]'
    DESCRIPTION_TAB_EXT_ID_VENUE_XPATH = '//*[@formcontrolname="venueSubVenueID"]'
    DESCRIPTION_TAB_VENUE_XPATH = '//*[@id="venue"]'
    DESCRIPTION_TAB_DEFAULT_SYMBOL_XPATH = '//*[@formcontrolname="defaultMDSymbol"]'
    DESCRIPTION_TAB_MARKET_DATA_SOURCE_XPATH = '//*[@formcontrolname="MDSource"]'
    DESCRIPTION_TAB_NEWS_CHECKBOX_XPATH = '//*[@formcontrolname="supportNews"]//span'
    DESCRIPTION_TAB_NEWS_SYMBOL_XPATH = '//*[@formcontrolname="newsMDSymbol"]'
    DESCRIPTION_TAB_FEED_SOURCE_XPATH = '//*[@id="feedSourceEnumTable"]'
    # Details tab

    DETAILS_TAB_TRADING_STATUS_XPATH = '//*[@id="tradingStatus"]'
    DETAILS_TAB_PRICE_LIMIT_PROFILE_XPATH = '//*[@id="priceLimitProfile"]'
    DETAILS_TAB_TRADING_PHASE_PROFILE_XPATH = '//*[@id="tradingPhaseProfile"]'
    DETAILS_TAB_TRADING_PHASE_XPATH = '//*[@id="tradingPhase"]'
    DETAILS_TAB_TICK_SIZE_PROFILE_XPATH = '//*[@id="tickSizeProfile"]'
    DETAILS_TAB_MANAGE_PRICE_LIMIT_PROFILE_XPATH = '//*[@class="expanded"]//nb-accordion-item-body//form//div[2]//div[2]//button'
    DETAILS_TAB_MANAGE_TRADING_PHASE_PROFILE_XPATH = '//*[@class="expanded"]//nb-accordion-item-body//form//div[3]//div[2]//button'
    DETAILS_TAB_MANAGE_TICK_SIZE_PROFILE_XPATH = '//*[@class="expanded"]//nb-accordion-item-body//form//div[2]//div[4]//button'

    # Price limit profile manage sub wizard
    PRICE_LIMIT_PROFILE_TAB_PLUS_BUTTON_XPATH = '//*[@class="nb-plus ng2-add-btn"]'
    PRICE_LIMIT_PROFILE_TAB_CHECKMARK_BUTTON_XPATH = '//*[@class="nb-checkmark"]'
    PRICE_LIMIT_PROFILE_TAB_CLOSE_BUTTON_XPATH = '//*[@class="nb-close ng2-cancel-btn"]'
    PRICE_LIMIT_PROFILE_TAB_EDIT_BUTTON_XPATH = '//*[@class="nb-edit ng2-edit-btn"]'
    PRICE_LIMIT_PROFILE_TAB_DELETE_BUTTON_XPATH = '//*[@class="nb-trash"]'
    PRICE_LIMIT_PROFILE_TAB_EXTERNAL_ID_XPATH = '//*[@placeholder="External ID *"]'
    PRICE_LIMIT_PROFILE_TAB_EXTERNAL_ID_FILTER_XPATH = '//*[@class="externalPriceLimitProfileID ng2-smart-th ng-star-inserted"]//input'
    PRICE_LIMIT_PROFILE_TAB_TRADING_REFERENCE_PRICE_TYPE_XPATH = '//*[@placeholder="Trading Reference Price Type *"]'
    PRICE_LIMIT_PROFILE_TAB_TRADING_REFERENCE_PRICE_TYPE_FILTER_XPATH = '//*[@class="ng2-smart-th tradingReferencePriceType ng-star-inserted"]//input'
    PRICE_LIMIT_PROFILE_TAB_PRICE_LIMIT_TYPE_XPATH = '//*[@placeholder="Price Limit Type *"]'
    PRICE_LIMIT_PROFILE_TAB_PRICE_LIMIT_TYPE_FILTER_XPATH = '//*[@class="ng2-smart-th priceLimitType ng-star-inserted"]//input'
    PRICE_LIMIT_PROFILE_TAB_PRICE_LIMIT_FIELD_NAME_XPATH = '//*[@placeholder="Price Limit Field Name"]'
    PRICE_LIMIT_PROFILE_TAB_PRICE_LIMIT_FIELD_NAME_FILTER_XPATH = '//*[@class="ng2-smart-th refPriceFieldName ng-star-inserted"]//input'

    PRICE_LIMIT_POINTS_TAB_PLUS_BUTTON_XPATH = '//*[@class="nb-plus sub-table-action"]'
    PRICE_LIMIT_POINTS_TAB_CHECKMARK_BUTTON_XPATH = '//*[@class="nb-checkmark"]'
    PRICE_LIMIT_POINTS_TAB_CLOSE_BUTTON_XPATH = '//*[@class="nb-close"]'
    PRICE_LIMIT_POINTS_TAB_EDIT_BUTTON_XPATH = '//*[@class="nb-edit sub-table-action"]'
    PRICE_LIMIT_POINTS_TAB_DELETE_BUTTON_XPATH = '//*[@class="nb-trash sub-table-action"]'

    PRICE_LIMIT_POINTS_TAB_LIMIT_PRICE_XPATH = '//*[@placeholder="Limit Price *"]'
    PRICE_LIMIT_POINTS_TAB_LIMIT_PRICE_FILTER_XPATH = '//*[@class="limitPrice ng2-smart-th ng-star-inserted"]//input'

    PRICE_LIMIT_POINTS_TAB_AUCTION_LIMIT_PRICE_XPATH = '//*[@placeholder="Auction Limit Price"]'
    PRICE_LIMIT_POINTS_TAB_AUCTION_LIMIT_PRICE_FILTER_XPATH = '//*[@class="auctionLimitPrice ng2-smart-th ng-star-inserted"]//input'

    PRICE_LIMIT_POINTS_TAB_UPPER_LIMIT_XPATH = '//*[@placeholder="Upper Limit"]'
    PRICE_LIMIT_POINTS_TAB_UPPER_LIMIT_FILTER_XPATH = '//*[@class="ng2-smart-th upperLimit ng-star-inserted"]//input'

    # Trading phase profile manage sub wizard
    TRADING_PHASE_PROFILES_PLUS_BUTTON_XPATH = '//*[@class="nb-plus ng2-add-btn"]'
    TRADING_PHASE_PROFILES_CHECKMARK_BUTTON_XPATH = '//*[@class="nb-checkmark"]'
    TRADING_PHASE_PROFILES_CLOSE_BUTTON_XPATH = '//*[@class="nb-close ng2-cancel-btn"]'
    TRADING_PHASE_PROFILES_EDIT_BUTTON_XPATH = '//*[@class="nb-edit ng2-edit-btn"]'
    TRADING_PHASE_PROFILES_DELETE_BUTTON_XPATH = '//*[@class="nb-trash"]'

    TRADING_PHASE_PROFILES_TRADING_PHASE_PROFILE_DESC_XPATH = '//*[@placeholder="TradingPhaseProfile Desc *"]'
    TRADING_PHASE_PROFILES_TRADING_PHASE_PROFILE_DESC_FILTER_XPATH = '//*[@class="ng2-smart-th tradPhaseProfileDesc ng-star-inserted"]//input'

    # Trading phase profile sequence
    TRADING_PHASE_PROFILE_SEQUENCES_PLUS_BUTTON_XPATH = '//*[@class="nb-plus sub-table-action"]'
    TRADING_PHASE_PROFILE_SEQUENCES_CHECKMARK_BUTTON_XPATH = '//*[@class="nb-checkmark"]'
    TRADING_PHASE_PROFILE_SEQUENCES_CLOSE_BUTTON_XPATH = '//*[@class="nb-close"]'
    TRADING_PHASE_PROFILE_SEQUENCES_EDIT_BUTTON_XPATH = '//*[@class="nb-edit sub-table-action"]'
    TRADING_PHASE_PROFILE_SEQUENCES_DELETE_BUTTON_XPATH = '//*[@class="nb-trash sub-table-action"]'

    TRADING_PHASE_PROFILE_SEQUENCES_SUBMIT_ALLOWED_CHECKBOX_XPATH = '//*[@class="custom-checkbox"]'
    TRADING_PHASE_PROFILE_SEQUENCES_SUBMIT_ALLOWED_CHECKBOX_FILTER_XPATH = '//*[@class="ng2-smart-th submitAllowed ng-star-inserted"]//input'
    TRADING_PHASE_PROFILE_SEQUENCES_TRADING_PHASE_XPATH = '//*[@placeholder="Trading Phase *"]'
    TRADING_PHASE_PROFILE_SEQUENCES_TRADING_PHASE_FILTER_XPATH = '//*[@class="ng2-smart-th tradingPhase ng-star-inserted"]//input'
    TRADING_PHASE_PROFILE_SEQUENCES_STANDART_TRADING_PHASE_XPATH = '//*[@placeholder="Standart Trading Phase"]'
    TRADING_PHASE_PROFILE_SEQUENCES_STANDART_TRADING_PHASE_FILTER_XPATH = '//*[@class="ng2-smart-th standardTradingPhase ng-star-inserted"]//input'
    TRADING_PHASE_PROFILE_SEQUENCES_EXPIRY_CYCLE_XPATH = '//*[@placeholder="Expiry Cycle"]'
    TRADING_PHASE_PROFILE_SEQUENCES_EXPIRY_CYCLE_FILTER_XPATH = '//*[@class="expiryCycle ng2-smart-th ng-star-inserted"]//input'
    TRADING_PHASE_PROFILE_SEQUENCES_BEGIN_TIME_XPATH = '//*[@placeholder="Begin Time"]'
    TRADING_PHASE_PROFILE_SEQUENCES_BEGIN_TIME_FILTER_XPATH = '//*[@class="beginTime_ext ng2-smart-th ng-star-inserted"]//input'
    TRADING_PHASE_PROFILE_SEQUENCES_END_TIME_XPATH = '//*[@placeholder="End Time"]'
    TRADING_PHASE_PROFILE_SEQUENCES_END_TIME_FILTER_XPATH = '//*[@class="endTime_ext ng2-smart-th ng-star-inserted"]//input'

    # tick size profile sub wizard
    TICK_SIZE_PROFILE_TAB_PLUS_BUTTON_XPATH = '//*[@class="nb-plus ng2-add-btn"]'
    TICK_SIZE_PROFILE_TAB_CLOSE_BUTTON_XPATH = '//*[@class="nb-close ng2-cancel-btn"]'
    TICK_SIZE_PROFILE_TAB_CHECKMARK_BUTTON_XPATH = '//*[@class="nb-checkmark"]'
    TICK_SIZE_PROFILE_TAB_EDIT_BUTTON_XPATH = '//*[@class="nb-edit ng2-edit-btn"]'
    TICK_SIZE_PROFILE_TAB_DELETE_BUTTON_XPATH = '//*[@class="nb-trash"]'
    TICK_SIZE_PROFILE_TAB_EXTERNAL_ID_XPATH = '//*[@placeholder="External ID *"]'
    TICK_SIZE_PROFILE_TAB_EXTERNAL_ID_FILTER_XPATH = '//*[@class="externalTickSizeProfileID ng2-smart-th ng-star-inserted"]//input'
    TICK_SIZE_PROFILE_TAB_TICK_SIZE_XAXIS_TYPE_XPATH = '//*[@placeholder="Tick Size XAxis Type"]'
    TICK_SIZE_PROFILE_TAB_TICK_SIZE_XAXIS_TYPE_FILTER_XPATH = '//*[@class="ng2-smart-th tickSizeXAxisType ng-star-inserted"]//input'
    TICK_SIZE_PROFILE_TAB_TICK_SIZE_REFPRICE_TYPE_XPATH = '//*[@placeholder="Tick Size RefPrice Type"]'
    TICK_SIZE_PROFILE_TAB_TICK_SIZE_REFPRICE_TYPE_FILTER_XPATH = '//*[@class="ng2-smart-th tickSizeRefPriceType ng-star-inserted"]//input'

    # tick size points sub wizard
    TICK_SIZE_POINTS_PLUS_BUTTON_XPATH = '//*[@class="nb-plus sub-table-action"]'
    TICK_SIZE_POINTS_CLOSE_BUTTON_XPATH = '//*[@class="nb-close"]'
    TICK_SIZE_POINTS_CHECKMARK_BUTTON_XPATH = '//*[@class="nb-checkmark"]'
    TICK_SIZE_POINTS_EDIT_BUTTON_XPATH = '//*[@class="nb-edit sub-table-action"]'
    TICK_SIZE_POINTS_DELETE_BUTTON_XPATH = '//*[@class="nb-trash sub-table-action"]'

    TICK_SIZE_POINTS_TICK_XPATH = '//*[@placeholder="Tick *"]'
    TICK_SIZE_POINTS_TICK_FILTER_XPATH = '//*[@class="form-control ng-untouched ng-pristine ng-valid"]//input'
    TICK_SIZE_POINTS_UPPER_LIMIT_XPATH = '//*[@placeholder="Upper Limit"]'
    TICK_SIZE_POINTS_UPPER_LIMIT_FILTER_XPATH = '//*[@class="ng2-smart-th upperLimitDouble ng-star-inserted"]//input'

    # Translation

    TRANSLATION_TAB_PLUS_BUTTON_XPATH = '//*[@class="nb-plus"]'
    TRANSLATION_TAB_CHECKMARK_BUTTON_XPATH = '//*[@class="nb-checkmark"]'
    TRANSLATION_TAB_CLOSE_BUTTON_XPATH = '//*[@class="nb-close"]'
    TRANSLATION_TAB_EDIT_BUTTON_XPATH = '//*[@class="nb-edit"]'
    TRANSLATION_TAB_DELETE_BUTTON_XPATH = '//*[@class="nb-trash"]'

    TRANSLATION_TAB_LANGUAGE_FILTER_XPATH = '//*[@class="lang ng2-smart-th ng-star-inserted"]'
    TRANSLATION_TAB_LANGUAGE_XPATH = '//*[@placeholder="Language *"]'

    TRANSLATION_TAB_NAME_FILTER_XPATH = '//*[@class="langSubVenueName ng2-smart-th ng-star-inserted"]'
    TRANSLATION_TAB_NAME_XPATH = '//*[@placeholder="Name *"]'

    TRANSLATION_TAB_DESCRIPTION_FILTER_XPATH = '//*[@class="ng2-smart-th subVenueDesc ng-star-inserted"]'
    TRANSLATION_TAB_DESCRIPTION_XPATH = '//*[@placeholder="Description"]'
