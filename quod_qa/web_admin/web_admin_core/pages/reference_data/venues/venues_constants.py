class VenuesConstants:
    VENUES_PAGE_TITLE_XPATH = "//span[@class='entity-title left'][text()='Venues ']"
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

    # --Main page--
    MAIN_PAGE_NAME_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[1]//input'
    MAIN_PAGE_NAME_XPATH = '//*[@col-id="venueName"]//span//span[4]'
    MAIN_PAGE_ID_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[2]//input'
    MAIN_PAGE_ID_XPATH = '//*[@col-id="venueID"]//span//span[4]'
    MAIN_PAGE_MIC_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[3]//input'
    MAIN_PAGE_MIC_XPATH = '//*[@col-id="MIC"]//span//span[4]'
    MAIN_PAGE_COUNTRY_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[4]//input'
    MAIN_PAGE_COUNTRY_XPATH = '//*[@col-id="countryEnumTable.countryName"]/span/span[4]'
    MAIN_PAGE_CATEGORY_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[5]//input'
    MAIN_PAGE_CATEGORY_XPATH = '//*[@col-id="venueCategory"]//span//span[4]'
    MAIN_PAGE_QUALIFIER_FILTER_XPATH = '//*[@class="ag-header-container"]//div[2]/div[6]//input'
    MAIN_PAGE_QUALIFIER_XPATH = '//*[@col-id="venueQualifier"]//span//span[4]'
    MAIN_PAGE_ANTI_CROSSING_FILTER_XPATH = '//*[@class="ag-header-container"]//div[2]//div[7]//input'
    MAIN_PAGE_ANTI_CROSSING_XPATH = '//*[@col-id="antiCrossingPeriod"]//span//span[4]'
    MAIN_PAGE_COUNTERPART_FILTER_XPATH = '//*[@class="ag-header-container"]//div[2]//div[8]//input'
    MAIN_PAGE_COUNTERPART_XPATH = '//*[@col-id="counterpart.counterpartName"]//span//span[4]'

    # --Description tab--
    DESCRIPTION_TAB_NAME_XPATH = '//*[@formcontrolname="venueName"]'
    DESCRIPTION_TAB_ID_XPATH = '//*[@formcontrolname="venueID"]'
    DESCRIPTION_TAB_MIC_XPATH = '//*[@formcontrolname="MIC"]'
    DESCRIPTION_TAB_COUNTRY_XPATH = '//*[@id="countryEnumTable"]'
    DESCRIPTION_TAB_CATEGORY_XPATH = '//*[@formcontrolname="venueCategory"]'
    DESCRIPTION_TAB_SHORT_NAME_XPATH = '//*[@formcontrolname="venueShortName"]'
    DESCRIPTION_TAB_VERY_SHORT_NAME_XPATH = '//*[@formcontrolname="venueVeryShortName"]'
    DESCRIPTION_TAB_CLIENT_VENUE_ID_XPATH = '//*[@formcontrolname="clientVenueID"]'
    DESCRIPTION_TAB_ROUTE_VENUE_ID_XPATH = '//*[@formcontrolname="routeVenueID"]'
    DESCRIPTION_TAB_TYPE_XPATH = '//*[@id="venueType"]'
    DESCRIPTION_TAB_COUNTERPART_XPATH = '//*[@id="counterpart"]'
    DESCRIPTION_TAB_COUNTERPART_MANAGE_XPATH = '//*[@class="venue-detail-settings"]//nb-accordion//nb-accordion-item[1]//*[text()="Manage"]'
    DESCRIPTION_TAB_BIC_XPATH = '//*[@formcontrolname="BIC"]'

    # --Profiles tab--
    PROFILES_TAB_PRICE_LIMIT_PROFILE_XPATH = '//*[@id="priceLimitProfile"]'
    PROFILES_TAB_PRICE_LIMIT_PROFILE_MANAGE_BUTTON_XPATH = '//*[@form-control-name="priceLimitProfile"]/parent::div/following-sibling::div//button'
    PROFILES_TAB_TICK_SIZE_PROFILE_XPATH = '//*[@id="tickSizeProfile"]'
    PROFILES_TAB_TICK_SIZE_PROFILE_MANAGE_BUTTON_XPATH = '//*[@form-control-name="tickSizeProfile"]/parent::div/following-sibling::div//button'
    PROFILES_TAB_HOLIDAY_XPATH = '//*[@id="holiday"]'
    PROFILES_TAB_HOLIDAY_MANAGE_BUTTON_XPATH = '//*[@form-control-name="holiday"]/parent::div/following-sibling::div//button'
    PROFILES_TAB_ANTI_CROSSING_PERIOD_XPATH = '//*[@formcontrolname="antiCrossingPeriod"]'
    PROFILES_TAB_TRADING_PHASE_PROFILE_XPATH = '//*[@id="tradingPhaseProfile"]'
    PROFILES_TAB_TRADING_PHASE_PROFILE_MANAGE_BUTTON_XPATH = '//*[@form-control-name="tradingPhaseProfile"]/parent::div/following-sibling::div//button'
    PROFILES_TAB_ROUTING_PARAM_GROUP_XPATH = '//*[@id="routingParamGroup"]'
    PROFILES_TAB_ROUTING_PARAM_GROUP_MANAGE_BUTTON_XPATH = '//*[@form-control-name="routingParamGroup"]/parent::div/following-sibling::div//button'
    PROFILES_TAB_WEEKEND_DAY_XPATH = '//*[@formcontrolname="weekendDay"]'

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

    # -- Holiday calendars sub tab--
    HOLIDAYS_TAB_PLUS_BUTTON_XPATH = '//*[text()="Holidays "]/ancestor::nb-card//nb-card-body//*[@class="nb-plus ng2-add-btn"]'
    HOLIDAYS_TAB_CHECKMARK_BUTTON_XPATH = '//*[text()="Holidays "]/ancestor::nb-card//nb-card-body//*[@class="nb-checkmark"]'
    HOLIDAYS_TAB_CLOSE_BUTTON_XPATH = '//*[text()="Holidays "]/ancestor::nb-card//nb-card-body//*[@class="nb-close ng2-cancel-btn"]'
    HOLIDAYS_TAB_EDIT_BUTTON_XPATH = '//*[text()="Holidays "]/ancestor::nb-card//nb-card-body//*[@class="nb-edit ng2-edit-btn"]'
    HOLIDAYS_TAB_DELETE_BUTTON_XPATH = '//*[text()="Holidays "]/ancestor::nb-card//nb-card-body//*[@class="nb-trash"]'

    HOLIDAYS_TAB_HOLIDAY_NAME_XPATH = '//*[@placeholder="Holiday Name *"]'
    HOLIDAYS_TAB_HOLIDAY_NAME_FILTER_XPATH = '//*[@class="holidayName ng2-smart-th ng-star-inserted"]//input'

    HOLIDAYS_CALENDAR_TAB_PLUS_BUTTON_XPATH = '//*[text()="Holiday Calendars"]/ancestor::nb-card//nb-card-body//*[@class="nb-plus sub-table-action"]'
    HOLIDAYS_CALENDAR_TAB_CHECKMARK_BUTTON_XPATH = '//*[text()="Holiday Calendars"]/ancestor::nb-card//nb-card-body//*[@class="nb-checkmark"]'
    HOLIDAYS_CALENDAR_TAB_CLOSE_BUTTON_XPATH = '//*[text()="Holiday Calendars"]/ancestor::nb-card//nb-card-body//*[@class="nb-close"]'
    HOLIDAYS_CALENDAR_TAB_EDIT_BUTTON_XPATH = '//*[text()="Holiday Calendars"]/ancestor::nb-card//nb-card-body//*[@class="nb-edit sub-table-action"]'
    HOLIDAYS_CALENDAR_TAB_DELETE_BUTTON_XPATH = '//*[text()="Holiday Calendars"]/ancestor::nb-card//nb-card-body//*[@class="nb-trash sub-table-action"]'

    HOLIDAYS_CALENDAR_TAB_DATE_XPATH = '//*[@placeholder="Date *"]'
    HOLIDAYS_CALENDAR_TAB_DATE_FILTER_XPATH = '//*[@class="holidayDate ng2-smart-th ng-star-inserted"]//input'
    HOLIDAYS_CALENDAR_TAB_DESCRIPTION_XPATH = '//*[@placeholder="Description"]'
    HOLIDAYS_CALENDAR_TAB_DESCRIPTION_FILTER_XPATH = '//*[@class="holidayDescription ng2-smart-th ng-star-inserted"]//input'

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

    # --Routing param groups sub tab--

    ROUTING_PARAM_GROUPS_TAB_PLUS_BUTTON_XPATH = '//*[text()="Routing Param Groups "]/ancestor::nb-card//nb-card-body//*[@class="nb-plus ng2-add-btn"]'
    ROUTING_PARAM_GROUPS_TAB_CHECKMARK_BUTTON_XPATH = '//*[text()="Routing Param Groups "]/ancestor::nb-card//nb-card-body//*[@class="nb-checkmark"]'
    ROUTING_PARAM_GROUPS_TAB_CLOSE_BUTTON_XPATH = '//*[text()="Routing Param Groups "]/ancestor::nb-card//nb-card-body//*[@class="nb-close ng2-cancel-btn"]'
    ROUTING_PARAM_GROUPS_TAB_EDIT_BUTTON_XPATH = '//*[text()="Routing Param Groups "]/ancestor::nb-card//nb-card-body//*[@class="nb-edit ng2-edit-btn"]'
    ROUTING_PARAM_GROUPS_TAB_DELETE_BUTTON_XPATH = '//*[text()="Routing Param Groups "]/ancestor::nb-card//nb-card-body//*[@class="nb-trash"]'

    ROUTING_PARAM_GROUPS_TAB_NAME_XPATH = '//*[@placeholder="Name *"]'
    ROUTING_PARAM_GROUPS_TAB_NAME_FILTER_XPATH = '//*[@class="ng2-smart-th routingParamGroupName ng-star-inserted"]//input'
    ROUTING_PARAM_GROUPS_TAB_POSITIVE_ROUTES_XPATH = '//*[text()="Positive Routes *"]'
    ROUTING_PARAM_GROUPS_TAB_POSITIVE_ROUTES_FILTER_XPATH = '//*[@class="ng2-smart-th positiveRoute_ext ng-star-inserted"]//input'
    ROUTING_PARAM_GROUPS_TAB_NEGATIVE_ROUTES_XPATH = '//*[text()="Negative Routes *"]'
    ROUTING_PARAM_GROUPS_TAB_NEGATIVE_ROUTES_FILTER_XPATH = '//*[@class="negativeRoute_ext ng2-smart-th ng-star-inserted"]//input'
    ROUTING_PARAM_GROUPS_TAB_NEGATIVE_AND_POSITIVE_ROUTES_LIST_XPATH = "//*[@class='cdk-overlay-pane']//*[text()='{}']"

    # --Routing parameters tab--
    ROUTING_PARAMETERS_TAB_PLUS_BUTTON_XPATH = '//*[text()="Parameters"]/following-sibling::ng2-smart-table//*[@class="nb-plus sub-table-action"]'
    ROUTING_PARAMETERS_TAB_CHECKMARK_BUTTON_XPATH = '//*[text()="Parameters"]/following-sibling::ng2-smart-table//*[@class="nb-checkmark"]'
    ROUTING_PARAMETERS_TAB_CLOSE_BUTTON_XPATH = '//*[text()="Parameters"]/following-sibling::ng2-smart-table//*[@class="nb-close"]'
    ROUTING_PARAMETERS_TAB_EDIT_BUTTON_XPATH = '//*[text()="Parameters"]/following-sibling::ng2-smart-table//*[@class="nb-edit sub-table-action"]'
    ROUTING_PARAMETERS_TAB_PLUS_DELETE_BUTTON_XPATH = '//*[text()="Parameters"]/following-sibling::ng2-smart-table//*[@class="nb-trash sub-table-action"]'

    ROUTING_PARAMETERS_TAB_PARAMETER_XPATH = '//*[@placeholder="Parameter *"]'
    ROUTING_PARAMETERS_TAB_PARAMETER_FILTER_XPATH = '//*[@class="customParam ng2-smart-th ng-star-inserted"]//input'
    ROUTING_PARAMETERS_TAB_VALUE_XPATH = '//*[@placeholder="Value *"]'
    ROUTING_PARAMETERS_TAB_VALUE_FILTER_XPATH = '//*[@class="customParamValue ng2-smart-th ng-star-inserted"]//input'

    # --Spport feed types tab--
    SUPPORT_FEED_TYPES_TAB_STATUS_CHECKBOX_XPATH = '//*[@formcontrolname="supportStatus"]//input'
    SUPPORT_FEED_TYPES_TAB_QUOTE_CHECKBOX_XPATH = '//*[@formcontrolname="supportQuote"]//input'
    SUPPORT_FEED_TYPES_TAB_QUOTE_BOOK_CHECKBOX_XPATH = '//*[@formcontrolname="supportQuoteBook"]//input'
    SUPPORT_FEED_TYPES_TAB_TICKERS_CHECKBOX_XPATH = '//*[@formcontrolname="supportTickers"]//input'
    SUPPORT_FEED_TYPES_TAB_MARKET_TIME_CHECKBOX_XPATH = '//*[@formcontrolname="supportMarketTime"]//input'
    SUPPORT_FEED_TYPES_TAB_DISCRETION_INST_CHECKBOX_XPATH = '//*[@formcontrolname="supportDiscretionInst"]//input'
    SUPPORT_FEED_TYPES_TAB_BROKER_QUEUE_CHECKBOX_XPATH = '//*[@formcontrolname="supportBrokerQueue"]//input'
    SUPPORT_FEED_TYPES_TAB_MARKET_DEPTH_CHECKBOX_XPATH = '//*[@formcontrolname="supportMarketDepth"]//input'
    SUPPORT_FEED_TYPES_TAB_MOVERS_CHECKBOX_XPATH = '//*[@formcontrolname="supportMovers"]//input'
    SUPPORT_FEED_TYPES_TAB_NEWS_CHECKBOX_XPATH = '//*[@formcontrolname="supportNews"]//input'
    SUPPORT_FEED_TYPES_TAB_TERM_QUOTE_REQUEST_CHECKBOX_XPATH = '//*[@formcontrolname="supportTermQuoteRequest"]//input'
    SUPPORT_FEED_TYPES_TAB_QUOTE_CANCEL_CHECKBOX_XPATH = '//*[@formcontrolname="supportQuoteCancel"]//input'
    SUPPORT_FEED_TYPES_TAB_INTRADAY_CHECKBOX_XPATH = '//*[@formcontrolname="supportIntradayData"]//input'
    SUPPORT_FEED_TYPES_TAB_ORDER_BOOK_CHECKBOX_XPATH = '//*[@formcontrolname="supportOrderBook"]//input'
    SUPPORT_FEED_TYPES_TAB_TIMES_AND_SALES_CHECKBOX_XPATH = '//*[@formcontrolname="supportTimesAndSales"]//input'
    SUPPORT_FEED_TYPES_TAB_TRADE_CHECKBOX_XPATH = '//*[@formcontrolname="supportTrade"]//input'
    SUPPORT_FEED_TYPES_TAB_SIZED_MD_REQUEST_CHECKBOX_XPATH = '//*[@formcontrolname="supportSizedMDRequest"]//input'

    # --Market data tab--
    MARKET_DATA_TAB_DEFAULT_MD_SYMBOL_XPATH = '//*[@formcontrolname="defaultMDSymbol"]'
    MARKET_DATA_TAB_TICKER_MD_SYMBOL_XPATH = '//*[@formcontrolname="tickerMDSymbol"]'
    MARKET_DATA_TAB_MD_SOURCE_XPATH = '//*[@formcontrolname="MDSource"]'
    MARKET_DATA_TAB_TRADING_PHASE_XPATH = '//*[@id="tradingPhase"]'
    MARKET_DATA_TAB_TIMES_SALES_MD_SYMBOL_XPATH = '//*[@formcontrolname="timesSalesMDSymbol"]'
    MARKET_DATA_TAB_MARKET_TIME_MD_SYMBOL_XPATH = '//*[@formcontrolname="marketTimeMDSymbol"]'
    MARKET_DATA_TAB_FEED_SOURCE_XPATH = '//*[@id="feedSourceEnumTable"]'
    MARKET_DATA_TAB_TRADING_STATUS_XPATH = '//*[@id="tradingStatus"]'
    MARKET_DATA_TAB_NEWS_MD_SYMBOLS_XPATH = '//*[@formcontrolname="newsMDSymbol"]'
    MARKET_DATA_TAB_MOVERS_MD_SYMBOL_XPATH = '//*[@formcontrolname="moversMDSymbol"]'
    MARKET_DATA_TAB_TRADING_SESSION_XPATH = '//*[@formcontrolname="tradingSession"]'

    # --Features tab--
    FEATURES_TAB_SUPPORT_PUBLIC_QUOTE_REQ_CHECKBOX_XPATH = '//*[@formcontrolname="supportPublicQuoteReq"]//input'
    FEATURES_TAB_QUOTE_RESPONCE_LEVEL_XPATH = '//*[@id="quoteResponseLevel"]'
    FEATURES_TAB_MULTILEG_REPORT_TYPE_XPATH = '//*[@id="multilegReportType"]'
    FEATURES_TAB_MIN_RESIDENT_TIME_XPATH = '//*[@formcontrolname="minResidentTime"]'
    FEATURES_TAB_OPEN_TIME_XPATH = '//*[@id="openTime_ext"]'
    FEATURES_TAB_HOLD_FIX_SELL_CHECKBOX_XPATH = '//*[@formcontrolname="holdFIXShortSell"]//input'
    FEATURES_TAB_TIME_ZONE_XPATH = '//*[@formcontrolname="timeZone"]'
    FEATURES_TAB_DEFAULT_EXECUTION_STRATEGY_XPATH = '//*[@id="defaultAlgoPolicy"]'
    FEATURES_TAB_VENUE_STO_XPATH = '//*[@id="venueSTO"]'
    FEATURES_TAB_SUPPORT_REVERSE_CAL_SPREAD_CHECKBOX_XPATH = '//*[@formcontrolname="supportReverseCalSpread"]//input'
    FEATURES_TAB_GTD_HOLIDAY_CHECK_CHECKBOX_XPATH = '//*[@formcontrolname="GTDHolidayCheck"]//input'
    FEATURES_TAB_INSTR_CREATION_POLICY_XPATH = '//*[@id="instrCreationPolicy"]'
    FEATURES_TAB_DISABLE_SELL_PRICE_FALL_XPATH = '//*[@formcontrolname="disableShortSellPrcFallPct"]'
    FEATURES_TAB_CLOSE_TIME_XPATH = '//*[@id="closeTime_ext"]'
    FEATURES_TAB_REGULATED_SELL_CHECKBOX_XPATH = '//*[@formcontrolname="regulatedShortSell"]//input'
    FEATURES_TAB_VALIDATE_VENUE_ACT_GRP_NAME_CHECKBOX_XPATH = '//*[@formcontrolname="validateVenueActGrpName"]//input'
    FEATURES_TAB_SUPPORT_TRADING_PHASE_CHECKBOX_XPATH = '//*[@formcontrolname="supportTradingPhase"]//input'
    FEATURES_TAB_MARKET_ORDER_TIME_IN_FORCE_XPATH = '//*[@id="marketOrderTimeInForce"]'
    FEATURES_TAB_ALGO_INCLUDED_CHECKBOX_XPATH = '//*[@formcontrolname="algoIncluded"]//input'
    FEATURES_TAB_MAX_VALIDITY_DAYS_XPATH = '//*[@formcontrolname="maxValidityDays"]'
    FEATURES_TAB_VENUE_QUALIFIER_XPATH = '//*[@id="venueQualifier"]'
    FEATURES_TAB_SHORT_TIME_ZONE_XPATH = '//*[@formcontrolname="shortTimeZone"]'
    FEATURES_TAB_VALIDATE_VENUE_CLIENT_ACCOUNT_NAME_CHECKBOX_XPATH = '//*[@formcontrolname="valVenueClientAccountName"]//input'
    FEATURES_TAB_AUTO_RFQ_TIMEOUT_XPATH = '//*[@formcontrolname="autoRFQTimeout"]'

    # --Default tab--
    DEFAULT_TAB_PREFERED_LISTING_XPATH = '//*[@id="preferredListing"]'
    DEFAULT_TAB_QUOTEREQ_RES_TIME_XPATH = '//*[@formcontrolname="quoteReqResponseTime"]'
    DEFAULT_TAB_QUOTE_MSG_ID_FORMAT_XPATH = '//*[@formcontrolname="quoteMsgIDFormat"]'
    DEFAULT_TAB_TRADE_REPORT_ID_FORMAT_XPATH = '//*[@formcontrolname="tradeReportIDFormat"]'
    DEFAULT_TAB_QUOTE_SIDE_RESPONCE_LEVEL_XPATH = '//*[@id="quoteSideResponseLevel"]'
    DEFAULT_TAB_SUPPORT_BROKEN_DATE_FEED_CHECKBOX_XPATH = '//*[@formcontrolname="supportBrokenDateFeed"]//input'
    DEFAULT_TAB_QUOTE_TTL_XPATH = '//*[@formcontrolname="quoteTTL"]'
    DEFAULT_TAB_CLQUOTEREQ_ID_FORMAT_XPATH = '//*[@formcontrolname="clQuoteReqIDFormat"]'
    DEFAULT_TAB_CLORD_ID_FORMAT_XPATH = '//*[@formcontrolname="clOrdIDFormat"]'
    DEFAULT_TAB_DEFAULT_SETTL_TYPE_XPATH = '//*[@id="defaultSettlType"]'
    DEFAULT_TAB_GENERATE_BID_ID_CHECKBOX_XPATH = '//*[@formcontrolname="generateBidOfferID"]//input'
    DEFAULT_TAB_QUOTEREQ_TTL_XPATH = '//*[@formcontrolname="quoteReqTTL"]'
    DEFAULT_TAB_LEGREF_ID_FORMAT_XPATH = '//*[@formcontrolname="legRefIDFormat"]'
    DEFAULT_TAB_CLIENT_QUOTE_ID_FORMAT_XPATH = '//*[@formcontrolname="clientQuoteIDFormat"]'
    DEFAULT_TAB_DEFAULT_SETTL_CURRENCY_XPATH = '//*[@id="defaultSettlCurrency"]'
    DEFAULT_TAB_GENERATE_QUOTE_ID_CHECKBOX_XPATH = '//*[@formcontrolname="generateQuoteMsgID"]//input'

    # --Sor criteria tab--
    SOR_CRITERIA_TAB_SETTLEMENT_RANK_XPATH = '//*[@formcontrolname="settlementRank"]'
    SOR_CRITERIA_TAB_LATENCY_XPATH = '//*[@formcontrolname="latency"]'

    # --Translation tab--
    TRANSLATION_TAB_PLUS_BUTTON_XPATH = '//*[text()=" Translation "]/parent::nb-accordion-item//nb-accordion-item-body//*[@class="nb-plus"]'
    TRANSLATION_TAB_CHECKMARK_BUTTON_XPATH = '//*[text()=" Translation "]/parent::nb-accordion-item//nb-accordion-item-body//*[@class="nb-checkmark"]'
    TRANSLATION_TAB_CLOSE_BUTTON_XPATH = '//*[text()=" Translation "]/parent::nb-accordion-item//nb-accordion-item-body//*[@class="nb-close"]'
    TRANSLATION_TAB_EDIT_BUTTON_XPATH = '//*[text()=" Translation "]/parent::nb-accordion-item//nb-accordion-item-body//*[@class="nb-edit"]'
    TRANSLATION_TAB_DELETE_BUTTON_XPATH = '//*[text()=" Translation "]/parent::nb-accordion-item//nb-accordion-item-body//*[@class="nb-trash"]'

    TRANSLATION_TAB_LANGUAGE_XPATH = '//*[@placeholder="Language *"]'
    TRANSLATION_TAB_LANGUAGE_FILTER_XPATH = '//*[@class="lang ng2-smart-th ng-star-inserted"]//input'
    TRANSLATION_TAB_NAME_XPATH = '//*[@placeholder="Name *"]'
    TRANSLATION_TAB_NAME_FILTER_XPATH = '//*[@class="langVenueName ng2-smart-th ng-star-inserted"]//input'
    TRANSLATION_TAB_DESCRIPTION_XPATH = '//*[@placeholder="Description"]'
    TRANSLATION_TAB_DESCRIPTION_FILTER_XPATH = '//*[@class="ng2-smart-th venueDescription ng-star-inserted"]//input'
    TRANSLATION_TAB_VENUE_SHORT_NAME_XPATH = '//*[@placeholder="Venue Short Name"]'
    TRANSLATION_TAB_VENUE_SHORT_NAME_FILTER_XPATH = '//*[@class="ng2-smart-th venueShortName ng-star-inserted"]//input'
    TRANSLATION_TAB_VENUE_VERY_SHORT_NAME_XPATH = '//*[@placeholder="Venue Short Name"]'
    TRANSLATION_TAB_VENUE_VERY_SHORT_NAME_FILTER_XPATH = '//*[@class="ng2-smart-th venueVeryShortName ng-star-inserted"]//input'

    # --Instructions tab--
    INSTRUCTIONS_TAB_INSTRUCTIONS_XPATH = '//*[@formcontrolname="venueExecInstType"]'
    INSTRUCTIONS_TAB_ORD_CAPACITY_XPATH = '//*[@id="venueOrdCapacity"]'

    # --Trading session tab--
    TRADING_SESSION_TAB_PLUS_BUTTON_XPATH = '//*[text()=" Trading Session "]/parent::nb-accordion-item//nb-accordion-item-body//*[@class="nb-plus"]'
    TRADING_SESSION_TAB_CHECKMARK_BUTTON_XPATH = '//*[text()=" Trading Session "]/parent::nb-accordion-item//nb-accordion-item-body//*[@class="nb-checkmark"]'
    TRADING_SESSION_TAB_CLOSE_BUTTON_XPATH = '//*[text()=" Trading Session "]/parent::nb-accordion-item//nb-accordion-item-body//*[@class="nb-close"]'
    TRADING_SESSION_TAB_EDIT_BUTTON_XPATH = '//*[text()=" Trading Session "]/parent::nb-accordion-item//nb-accordion-item-body//*[@class="nb-edit"]'
    TRADING_SESSION_TAB_DELETE_BUTTON_XPATH = '//*[text()=" Trading Session "]/parent::nb-accordion-item//nb-accordion-item-body//*[@class="nb-trash"]'

    TRADING_SESSION_TAB_VENUE_TRADING_SESSION_ID_XPATH = '//*[@placeholder="Venue Trading Session ID *"]'
    TRADING_SESSION_TAB_VENUE_TRADING_SESSION_ID_FILTER_XPATH = '//*[@class="ng2-smart-th venueTradingSessionID ng-star-inserted"]//input'
    TRADING_SESSION_TAB_TRADING_SESSION_DESCRIPTION_XPATH = '//*[@placeholder="Trading Session Description"]'
    TRADING_SESSION_TAB_TRADING_SESSION_DESCRIPTION_FILTER_XPATH = '//*[@class="ng2-smart-th tradingSessionDesc ng-star-inserted"]//input'

    # --Match type tab--
    MATCH_TYPE_TAB_PLUS_BUTTON_XPATH = '//*[text()=" Match Type "]/parent::nb-accordion-item//nb-accordion-item-body//*[@class="nb-plus"]'
    MATCH_TYPE_TAB_CHECKMARK_BUTTON_XPATH = '//*[text()=" Match Type "]/parent::nb-accordion-item//nb-accordion-item-body//*[@class="nb-checkmark"]'
    MATCH_TYPE_TAB_CLOSE_BUTTON_XPATH = '//*[text()=" Match Type "]/parent::nb-accordion-item//nb-accordion-item-body//*[@class="nb-close"]'
    MATCH_TYPE_TAB_EDIT_BUTTON_XPATH = '//*[text()=" Match Type "]/parent::nb-accordion-item//nb-accordion-item-body//*[@class="nb-edit"]'
    MATCH_TYPE_TAB_DELETE_BUTTON_XPATH = '//*[text()=" Match Type "]/parent::nb-accordion-item//nb-accordion-item-body//*[@class="nb-trash"]'

    MATCH_TYPE_TAB_NAME_XPATH = '//*[@placeholder="Name *"]'
    MATCH_TYPE_TAB_NAME_FILTER_XPATH = '//*[@class="matchTypeName ng2-smart-th ng-star-inserted"]//input'
    MATCH_TYPE_TAB_MATCH_TYPE_XPATH = '//*[@placeholder="Match Type *"]'
    MATCH_TYPE_TAB_MATCH_TYPE_FILTER_XPATH = '//*[@class="matchType ng2-smart-th ng-star-inserted"]//input'

    # --Phase session tab--
    PHASE_SESSION_TAB_PLUS_BUTTON_XPATH = '//*[text()=" Phase Session "]/parent::nb-accordion-item//nb-accordion-item-body//*[@class="nb-plus"]'
    PHASE_SESSION_TAB_CHECKMARK_BUTTON_XPATH = '//*[text()=" Phase Session "]/parent::nb-accordion-item//nb-accordion-item-body//*[@class="nb-checkmark"]'
    PHASE_SESSION_TAB_CLOSE_BUTTON_XPATH = '//*[text()=" Phase Session "]/parent::nb-accordion-item//nb-accordion-item-body//*[@class="nb-close"]'
    PHASE_SESSION_TAB_EDIT_BUTTON_XPATH = '//*[text()=" Phase Session "]/parent::nb-accordion-item//nb-accordion-item-body//*[@class="nb-edit"]'
    PHASE_SESSION_TAB_DELETE_BUTTON_XPATH = '//*[text()=" Phase Session "]/parent::nb-accordion-item//nb-accordion-item-body//*[@class="nb-trash"]'

    PHASE_SESSION_TAB_TRADING_PHASE_XPATH = '//*[@placeholder="Trading Phase *"]'
    PHASE_SESSION_TAB_TRADING_PHASE_FILTER_XPATH = '//*[@class="ng2-smart-th tradingPhase ng-star-inserted"]//input'
    PHASE_SESSION_TAB_TRADING_SESSION_XPATH = '//*[@placeholder="Trading Session *"]'
    PHASE_SESSION_TAB_TRADING_SESSION_FILTER_XPATH = '//*[@class="ng2-smart-th tradingSession ng-star-inserted"]//input'
    PHASE_SESSION_TAB_SUPPORT_MIN_QUANTITY_XPATH = '//*[@placeholder="Trading Session *"]'
    PHASE_SESSION_TAB_SUPPORT_MIN_QUANTITY_FILTER_XPATH = '//*[@class="status-basic ng-untouched ng-pristine ng-valid nb-transition"]//input'
    PHASE_SESSION_TAB_PEG_PRICE_TYPE_XPATH = '//*[@class="appearance-outline full-width size-medium status-basic shape-rectangle ng-untouched ng-pristine ng-valid nb-transition"]'
    PHASE_SESSION_TAB_PEG_PRICE_TYPE_FILTER_XPATH = '//*[@class="ng2-smart-th venuePhaseSessionPegPriceType ng-star-inserted"]//input'

    # --Type tif sub tab--
    TYPE_TIF_TAB_PLUS_BUTTON_XPATH = '//*[text()="Type TIF"]/following-sibling::ng2-smart-table//*[@class="nb-plus sub-table-action"]'
    TYPE_TIF_TAB_CHECKMARK_BUTTON_XPATH = '//*[text()="Type TIF"]/following-sibling::ng2-smart-table//*[@class="nb-checkmark"]'
    TYPE_TIF_TAB_CLOSE_BUTTON_XPATH = '//*[text()="Type TIF"]/following-sibling::ng2-smart-table//*[@class="nb-close"]'
    TYPE_TIF_TAB_EDIT_BUTTON_XPATH = '//*[text()="Type TIF"]/following-sibling::ng2-smart-table//*[@class="nb-edit sub-table-action"]'
    TYPE_TIF_TAB_DELETE_BUTTON_XPATH = '//*[text()="Type TIF"]/following-sibling::ng2-smart-table//*[@class="nb-trash sub-table-action"]'

    TYPE_TIF_TAB_TIME_IN_FORCE_XPATH = '//*[@placeholder="Time In Force *"]'
    TYPE_TIF_TAB_TIME_IN_FORCE_FILTER_XPATH = '//*[@class="ng2-smart-th timeInForce ng-star-inserted"]//input'
    TYPE_TIF_TAB_ORD_TYPE_XPATH = '//*[@placeholder="Ord Type *"]'
    TYPE_TIF_TAB_ORD_TYPE_FILTER_XPATH = '//*[@class="ng2-smart-th ordType ng-star-inserted"]//input'
    TYPE_TIF_TAB_SUPPORT_DISPLAY_QUANTITY_CHECKBOX_XPATH = '//*[@class="status-basic ng-untouched ng-pristine ng-valid nb-transition"]//input'
    TYPE_TIF_TAB_SUPPORT_DISPLAY_QUANTITY_CHECKBOX_FILTER_XPATH = '//*[@class="ng2-smart-th supportDisplayQty ng-star-inserted"]//input'

    # --Status metrics--
    STATUS_METRICS_TAB_WARNING_THRESHOLD_XPATH = '//*[@id="warnLast Update Elapsed Time (sec)"]'
    STATUS_METRICS_TAB_ERROR_THRESHOLD_XPATH = '//*[@id="errLast Update Elapsed Time (sec)"]'
    STATUS_METRICS_TAB_ENABLE_METRIC_CHECKBOX_XPATH = '//*[text()="Enable Metric"]/parent::label//input'
