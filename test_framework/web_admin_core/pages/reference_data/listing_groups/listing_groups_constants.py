class ListingGroupsConstants:
    LISTING_GROUPS_PAGE_TITLE_XPATH = "//*[@title='Listing Groups']//span"
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
    NEW_BUTTON_XPATH = '//*[normalize-space()="Listing Groups"]//..//*[normalize-space()="New"]'
    USER_ICON_AT_RIGHT_CORNER = "//*[@class='control-item icon-btn context-menu-host']"
    LOGOUT_BUTTON_XPATH = "//*[text()='Logout']"
    GO_BACK_BUTTON_XPATH = "//*[text()='Go Back']"

    # Main page
    MAIN_PAGE_NAME_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[1]//input'
    MAIN_PAGE_NAME_XPATH = '//*[@col-id="listingGroupName"]//span//span[4]'
    MAIN_PAGE_EXT_ID_VENUE_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[2]//input'
    MAIN_PAGE_EXT_ID_VENUE_XPATH = '//*[@col-id="venueListingGroupID"]//span//span[4]'
    MAIN_PAGE_SUB_VENUE_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[3]//input'
    MAIN_PAGE_SUB_VENUE_XPATH = '//*[@col-id="subVenue.subVenueName"]//span//span[4]'
    MAIN_PAGE_MARKET_DATA_SOURCE_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[4]//input'
    MAIN_PAGE_MARKET_DATA_SOURCE_XPATH = '//*[@col-id="MDSource"]//span//span[4]'
    MAIN_PAGE_FEED_SOURCE_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[5]//input'
    MAIN_PAGE_FEED_SOURCE_XPATH = '//*[@id="feedSourceEnumTable"]'
    MAIN_PAGE_DEFAULT_SYMBOL_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[6]//input'
    MAIN_PAGE_DEFAULT_SYMBOL_XPATH = '//*[@col-id="defaultMDSymbol"]//span//span[4]'

    # Description tab
    DESCRIPTION_TAB_NAME_XPATH = '//*[@formcontrolname="listingGroupName"]'
    DESCRIPTION_TAB_EXT_ID_VENUE_XPATH = '//*[@formcontrolname="venueListingGroupID"]'
    DESCRIPTION_TAB_SUB_VENUE_XPATH = '//*[@id="subVenue"]'
    DESCRIPTION_TAB_DEFAULT_SYMBOL_XPATH = '//*[@formcontrolname="defaultMDSymbol"]'
    DESCRIPTION_TAB_FEED_SOURCE_XPATH = '//*[@id="feedSourceEnumTable"]'
    DESCRIPTION_TAB_MARKET_DATA_SOURCE_XPATH = '//*[@formcontrolname="MDSource"]'
    DESCRIPTION_TAB_NEWS_CHECKBOX_XPATH = '//*[@formcontrolname="supportNews"]//input/following-sibling::span'
    DESCRIPTION_TAB_NEWS_SYMBOL_XPATH = '//*[@formcontrolname="newsMDSymbol"]'

    # Details tab
    DETAILS_TAB_TRADING_STATUS_XPATH = '//*[@id="tradingStatus"]'
    DETAILS_TAB_PRICE_LIMIT_PROFILE_XPATH = '//*[@id="priceLimitProfile"]'
    DETAILS_TAB_TRADING_PHASE_PROFILE_XPATH = '//*[@id="tradingPhaseProfile"]'
    DETAILS_TAB_TRADING_PHASE_XPATH = '//*[@id="tradingPhase"]'
    DETAILS_TAB_TICK_SIZE_PROFILE_XPATH = '//*[@id="tickSizeProfile"]'

    DETAILS_TAB_PRICE_LIMIT_PROFILE_MANAGE_BUTTON_XPATH = '//*[@form-control-name="priceLimitProfile"]/parent::div/following-sibling::div//button'
    DETAILS_TAB_TRADING_PHASE_PROFILE_MANAGE_BUTTON_XPATH = '//*[@form-control-name="tradingPhaseProfile"]/parent::div/following-sibling::div//button'
    DETAILS_TAB_TICK_SIZE_PROFILE_MANAGE_BUTTON_XPATH = '//*[@form-control-name="tickSizeProfile"]/parent::div/following-sibling::div//button'

    # Translation
    TRANSLATION_TAB_PLUS_BUTTON_XPATH = '//*[text()=" Translation "]/parent::nb-accordion-item//nb-accordion-item-body//*[@class="nb-plus"]'
    TRANSLATION_TAB_CHECKMARK_BUTTON_XPATH = '//*[text()=" Translation "]/parent::nb-accordion-item//nb-accordion-item-body//*[@class="nb-checkmark"]'
    TRANSLATION_TAB_CLOSE_BUTTON_XPATH = '//*[text()=" Translation "]/parent::nb-accordion-item//nb-accordion-item-body//*[@class="nb-close"]'
    TRANSLATION_TAB_EDIT_BUTTON_XPATH = '//*[text()=" Translation "]/parent::nb-accordion-item//nb-accordion-item-body//*[@class="nb-edit"]'
    TRANSLATION_TAB_DELETE_BUTTON_XPATH = '//*[text()=" Translation "]/parent::nb-accordion-item//nb-accordion-item-body//*[@class="nb-trash"]'

    TRANSLATION_TAB_LANGUAGE_FILTER_XPATH = '//*[@class="lang ng2-smart-th ng-star-inserted"]//input'
    TRANSLATION_TAB_LANGUAGE_XPATH = '//*[@placeholder="Language *"]'
    TRANSLATION_TAB_NAME_FILTER_XPATH = '//*[@class="langListingGroupName ng2-smart-th ng-star-inserted"]//input'
    TRANSLATION_TAB_NAME_XPATH = '//*[@placeholder="Name *"]'
    TRANSLATION_TAB_DESCRIPTION_FILTER_XPATH = '//*[@class="listingGroupDesc ng2-smart-th ng-star-inserted"]//input'
    TRANSLATION_TAB_DESCRIPTION_XPATH = '//*[@placeholder="Description"]'

    # --Price limit profile sub tab--
    PRICE_LIMIT_PROFILES_TAB_PLUS_BUTTON_XPATH = '//*[text()="Price Limit Profiles "]/ancestor::nb-card//nb-card-body//*[@class="nb-plus ng2-add-btn"]'
    PRICE_LIMIT_PROFILES_TAB_CHECKMARK_BUTTON_XPATH = '//*[text()="Price Limit Profiles "]/ancestor::nb-card//nb-card-body//*[@class="nb-checkmark"]'
    PRICE_LIMIT_PROFILES_TAB_CLOSE_BUTTON_XPATH = '//*[text()="Price Limit Profiles "]/ancestor::nb-card//nb-card-body//*[@class="nb-close ng2-cancel-btn"]'
    PRICE_LIMIT_PROFILES_TAB_EDIT_BUTTON_XPATH = '//*[text()="Price Limit Profiles "]/ancestor::nb-card//nb-card-body//*[@class="nb-edit ng2-edit-btn"]'
    PRICE_LIMIT_PROFILES_TAB_DELETE_BUTTON_XPATH = '//*[text()="Price Limit Profiles "]/ancestor::nb-card//nb-card-body//*[@class="nb-trash"]'

    PRICE_LIMIT_PROFILES_TAB_EXTERNAL_ID_XPATH = '//*[@placeholder="External ID *"]'
    PRICE_LIMIT_PROFILES_TAB_EXTERNAL_ID_FILTER_XPATH = '//*[@class="externalPriceLimitProfileID ng2-smart-th ng-star-inserted"]//input'
    PRICE_LIMIT_PROFILES_TAB_TRADING_REFERENCE_PRICE_TYPE_XPATH = '//*[@placeholder="Trading Reference Price Type *"]'
    PRICE_LIMIT_PROFILES_TAB_TRADING_REFERENCE_PRICE_TYPE_FILTER_XPATH = '//*[@class="ng2-smart-th tradingReferencePriceType ng-star-inserted"]//input'
    PRICE_LIMIT_PROFILES_TAB_PRICE_LIMIT_TYPE_XPATH = '//*[@placeholder="Price Limit Type *"]'
    PRICE_LIMIT_PROFILES_TAB_PRICE_LIMIT_TYPE_FILTER_XPATH = '//*[@class="ng2-smart-th tradingReferencePriceType ng-star-inserted"]//input'
    PRICE_LIMIT_PROFILES_TAB_PRICE_LIMIT_FIELD_NAME_XPATH = '//*[@placeholder="Price Limit Field Name"]'
    PRICE_LIMIT_PROFILES_TAB_PRICE_LIMIT_FIELD_NAME_FILTER_XPATH = '//*[@class="ng2-smart-th refPriceFieldName ng-star-inserted"]//input'

    # --Price limit points sub tub--
    PRICE_LIMIT_POINTS_TAB_PLUS_BUTTON_XPATH = '//*[text()="Price Limit Points"]/ancestor::nb-card//nb-card-body//*[@class="nb-plus sub-table-action"]'
    PRICE_LIMIT_POINTS_TAB_CHECKMARK_BUTTON_XPATH = '//*[text()="Price Limit Points"]/ancestor::nb-card//nb-card-body//*[@class="nb-checkmark"]'
    PRICE_LIMIT_POINTS_TAB_CLOSE_BUTTON_XPATH = '//*[text()="Price Limit Points"]/ancestor::nb-card//nb-card-body//*[@class="nb-close"]'
    PRICE_LIMIT_POINTS_TAB_EDIT_BUTTON_XPATH = '//*[text()="Price Limit Points"]/ancestor::nb-card//nb-card-body//*[@class="nb-edit sub-table-action"]'
    PRICE_LIMIT_POINTS_TAB_DELETE_BUTTON_XPATH = '//*[text()="Price Limit Points"]/ancestor::nb-card//nb-card-body//*[@class="nb-trash sub-table-action"]'

    PRICE_LIMIT_POINTS_TAB_LIMIT_PRICE_XPATH = '//*[@placeholder="Price Limit Field Name"]'
    PRICE_LIMIT_POINTS_TAB_LIMIT_PRICE_FILTER_XPATH = '//*[@class="limitPrice ng2-smart-th ng-star-inserted"]//input'
    PRICE_LIMIT_POINTS_TAB_AUCTION_LIMIT_PRICE_XPATH = '//*[@placeholder="Price Limit Field Name"]'
    PRICE_LIMIT_POINTS_TAB_AUCTION_LIMIT_PRICE_FILTER_XPATH = '//*[@class="auctionLimitPrice ng2-smart-th ng-star-inserted"]//input'
    PRICE_LIMIT_POINTS_TAB_UPPER_LIMIT_XPATH = '//*[@placeholder="Upper Limit"]'
    PRICE_LIMIT_POINTS_TAB_UPPER_LIMIT_FILTER_XPATH = '//*[@class="ng2-smart-th upperLimit ng-star-inserted"]//input'

    # --Trading phase profiles sub tab--
    TRADING_PHASE_PROFILES_TAB_PLUS_BUTTON_XPATH = '//*[text()="Trading Phase Profiles "]/ancestor::nb-card//nb-card-body//*[@class="nb-plus ng2-add-btn"]'
    TRADING_PHASE_PROFILES_TAB_CHECKMARK_BUTTON_XPATH = '//*[text()="Trading Phase Profiles "]/ancestor::nb-card//nb-card-body//*[@class="nb-checkmark"]'
    TRADING_PHASE_PROFILES_TAB_CLOSE_BUTTON_XPATH = '//*[text()="Trading Phase Profiles "]/ancestor::nb-card//nb-card-body//*[@class="nb-close ng2-cancel-btn"]'
    TRADING_PHASE_PROFILES_TAB_EDIT_BUTTON_XPATH = '//*[text()="Trading Phase Profiles "]/ancestor::nb-card//nb-card-body//*[@class="nb-edit ng2-edit-btn"]'
    TRADING_PHASE_PROFILES_TAB_DELETE_BUTTON_XPATH = '//*[text()="Trading Phase Profiles "]/ancestor::nb-card//nb-card-body//*[@class="nb-trash"]'

    TRADING_PHASE_PROFILES_TAB_TRADING_PHASE_PROFILE_DESC_XPATH = '//*[@placeholder="TradingPhaseProfile Desc *"]'
    TRADING_PHASE_PROFILES_TAB_TRADING_PHASE_PROFILE_DESC_FILTER_XPATH = '//*[@class="ng2-smart-th tradPhaseProfileDesc ng-star-inserted"]//input'

    # --Trading phase profile sequence sub tab--

    TRADING_PHASE_PROFILE_SEQUENCES_TAB_PLUS_BUTTON_XPATH = '//*[text()="Trading Phase Profile Sequences"]/following-sibling::ng2-smart-table//*[@class="nb-plus sub-table-action"]'
    TRADING_PHASE_PROFILE_SEQUENCES_TAB_CHECKMARK_BUTTON_XPATH = '//*[text()="Trading Phase Profile Sequences"]/following-sibling::ng2-smart-table//*[@class="nb-checkmark"]'
    TRADING_PHASE_PROFILE_SEQUENCES_TAB_CLOSE_BUTTON_XPATH = '//*[text()="Trading Phase Profile Sequences"]/following-sibling::ng2-smart-table//*[@class="nb-close"]'
    TRADING_PHASE_PROFILE_SEQUENCES_TAB_EDIT_BUTTON_XPATH = '//*[text()="Trading Phase Profile Sequences"]/following-sibling::ng2-smart-table//*[@class="nb-edit sub-table-action"]'
    TRADING_PHASE_PROFILE_SEQUENCES_TAB_DELETE_BUTTON = '//*[text()="Trading Phase Profile Sequences"]/following-sibling::ng2-smart-table//*[@class="nb-trash sub-table-action"]'

    TRADING_PHASE_PROFILE_SEQUENCES_TAB_SUBMIT_ALLOWED_XPATH = '//*[@class="status-basic ng-untouched ng-pristine ng-valid nb-transition"]//input'
    TRADING_PHASE_PROFILE_SEQUENCES_TAB_SUBMIT_ALLOWED_FILTER_XPATH = '//*[@class="ng2-smart-th submitAllowed ng-star-inserted"]//input'
    TRADING_PHASE_PROFILE_SEQUENCES_TAB_TRADING_PHASE_XPATH = '//*[@placeholder="Trading Phase *"]'
    TRADING_PHASE_PROFILE_SEQUENCES_TAB_TRADING_PHASE_FILTER_XPATH = '//*[@class="ng2-smart-th tradingPhase ng-star-inserted"]//input'
    TRADING_PHASE_PROFILE_SEQUENCES_TAB_STANDART_TRADING_PHASE_XPATH = '//*[@placeholder="Standart Trading Phase"]'
    TRADING_PHASE_PROFILE_SEQUENCES_TAB_STANDART_TRADING_PHASE_FILTER_XPATH = '//*[@class="ng2-smart-th standardTradingPhase ng-star-inserted"]//input'
    TRADING_PHASE_PROFILE_SEQUENCES_TAB_EXPIRY_CYCLE_XPATH = '//*[@placeholder="Expiry Cycle"]'
    TRADING_PHASE_PROFILE_SEQUENCES_TAB_EXPIRY_CYCLE_FILTER_XPATH = '//*[@class="ng2-smart-th standardTradingPhase ng-star-inserted"]//input'
    TRADING_PHASE_PROFILE_SEQUENCES_TAB_BEGIN_TIME_XPATH = '//*[@placeholder="Begin Time"]'
    TRADING_PHASE_PROFILE_SEQUENCES_TAB_BEGIN_TIME_FILTER_XPATH = '//*[@class="beginTime_ext ng2-smart-th ng-star-inserted"]//input'
    TRADING_PHASE_PROFILE_SEQUENCES_TAB_END_TIME_XPATH = '//*[@placeholder="End Time"]'
    TRADING_PHASE_PROFILE_SEQUENCES_TAB_END_TIME_FILTER_XPATH = '//*[@class="endTime_ext ng2-smart-th ng-star-inserted"]//input'

    # --Tick size profiles sub tab--
    TICK_SIZE_PROFILES_TAB_PLUS_BUTTON_XPATH = '//*[text()="Tick Size Profiles "]/ancestor::nb-card//nb-card-body//*[@class="nb-plus ng2-add-btn"]'
    TICK_SIZE_PROFILES_TAB_CHECKMARK_BUTTON_XPATH = '//*[text()="Tick Size Profiles "]/ancestor::nb-card//nb-card-body//*[@class="nb-checkmark"]'
    TICK_SIZE_PROFILES_TAB_CLOSE_BUTTON_XPATH = '//*[text()="Tick Size Profiles "]/ancestor::nb-card//nb-card-body//*[@class="nb-close ng2-cancel-btn"]'
    TICK_SIZE_PROFILES_TAB_EDIT_BUTTON_XPATH = '//*[text()="Tick Size Profiles "]/ancestor::nb-card//nb-card-body//*[@class="nb-edit ng2-edit-btn"]'
    TICK_SIZE_PROFILES_TAB_DELETE_BUTTON_XPATH = '//*[text()="Tick Size Profiles "]/ancestor::nb-card//nb-card-body//*[@class="nb-trash"]'

    TICK_SIZE_PROFILES_TAB_EXTERNAL_ID_XPATH = '//*[@placeholder="External ID *"]'
    TICK_SIZE_PROFILES_TAB_EXTERNAL_ID_FILTER_XPATH = '//*[@class="externalTickSizeProfileID ng2-smart-th ng-star-inserted"]//input'
    TICK_SIZE_PROFILES_TAB_TICK_SIZE_XAXIS_TYPE_XPATH = '//*[@placeholder="Tick Size XAxis Type"]'
    TICK_SIZE_PROFILES_TAB_TICK_SIZE_XAXIS_TYPE_FILTER_XPATH = '//*[@class="ng2-smart-th tickSizeXAxisType ng-star-inserted"]//input'
    TICK_SIZE_PROFILES_TAB_TICK_SIZE_REFPRICE_TYPE_XPATH = '//*[@placeholder="Tick Size RefPrice Type"]'
    TICK_SIZE_PROFILES_TAB_TICK_SIZE_REFPRICE_TYPE_FILTER_XPATH = '//*[@class="ng2-smart-th tickSizeRefPriceType ng-star-inserted"]//input'

    # --Tick size points sub tab--
    TICK_SIZE_POINTS_TAB_PLUS_BUTTON_XPATH = '//*[text()="Tick Size Points"]/following-sibling::ng2-smart-table//*[@class="nb-plus sub-table-action"]'
    TICK_SIZE_POINTS_TAB_CHECKMARK_BUTTON_XPATH = '//*[text()="Tick Size Points"]/following-sibling::ng2-smart-table//*[@class="nb-checkmark"]'
    TICK_SIZE_POINTS_TAB_CLOSE_BUTTON_XPATH = '//*[text()="Tick Size Points"]/following-sibling::ng2-smart-table//*[@class="nb-close"]'
    TICK_SIZE_POINTS_TAB_EDIT_BUTTON_XPATH = '//*[text()="Tick Size Points"]/following-sibling::ng2-smart-table//*[@class="nb-edit sub-table-action"]'
    TICK_SIZE_POINTS_TAB_DELETE_BUTTON_XPATH = '//*[text()="Tick Size Points"]/following-sibling::ng2-smart-table//*[@class="nb-trash sub-table-action"]'

    TICK_SIZE_POINTS_TAB_TICK_XPATH = '//*[@placeholder="Tick *"]'
    TICK_SIZE_POINTS_TAB_TICK_FILTER_XPATH = '//*[@class="ng2-smart-th tickSize ng-star-inserted"]//input'
    TICK_SIZE_POINTS_TAB_UPPER_LIMIT_XPATH = '//*[@placeholder="Upper Limit"]'
    TICK_SIZE_POINTS_TAB_UPPER_LIMIT_FILTER_XPATH = '//*[@class="ng2-smart-th upperLimitDouble ng-star-inserted"]//input'
