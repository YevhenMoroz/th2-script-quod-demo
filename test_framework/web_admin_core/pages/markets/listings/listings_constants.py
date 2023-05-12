class ListingsConstants:
    LISTINGS_PAGE_TITLE_XPATH = "//span[@class='entity-title left'][normalize-space()='Listings']"
    REFRESH_PAGE_BUTTON_XPATH = "//*[@data-name='refresh']"
    DOWNLOAD_PDF_BUTTON_XPATH = "//nb-icon[@icon='download-outline']//*[@data-name='download']"
    DOWNLOAD_PDF_AT_WIZARD_XPATH = '//*[@data-name="download"]'
    SAVE_CHANGES_BUTTON_XPATH = "//*[contains(text(), 'Save Changes')]"
    CLEAR_CHANGES_BUTTON_XPATH = "//*[text()='Clear Changes']"
    CLOSE_WIZARD_XPATH = "//*[@data-name='close']"
    OK_BUTTON_XPATH = '//*[text()="Ok" or text()="OK"]'
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
    ENABLE_DISABLE_BUTTON_XPATH = "//div[contains(@class, 'toggle')]"
    ERROR_MESSAGE_WIZARD_XPATH = "//*[@outline='danger']"
    REQUEST_FAILED_MESSAGE_XPATH = "//nb-toast[contains(@class, 'danger')]"
    DISPLAYED_LISTING_XPATH = "//*[text()='{}']"
    DROP_DOWN = '//*[@class="option-list"]//nb-option | span'

    # Main page
    MAIN_PAGE_LISTING_GLOBAL_FILTER_XPATH = '//*[text()="Listing"]/preceding-sibling::input'
    MAIN_PAGE_LOAD_BUTTON_XPATH = '//*[text()="Listing"]/following-sibling::button'
    MAIN_PAGE_VENUE_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[1]//input'
    MAIN_PAGE_VENUE_XPATH = '//*[@col-id="venue.venueName"]//span//span[4]'
    MAIN_PAGE_SUB_VENUE_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[2]//input'
    MAIN_PAGE_SUB_VENUE_XPATH = '//*[@col-id="subVenue.subVenueName"]//span//span[4]'
    MAIN_PAGE_SYMBOL_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[3]//input'
    MAIN_PAGE_SYMBOL_XPATH = '//*[@col-id="symbol"]//span//span[4]'
    MAIN_PAGE_INSTRUMENT_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[4]//input'
    MAIN_PAGE_INSTRUMENT_XPATH = '//*[@col-id="instrSymbol"]//span//span[4]'
    MAIN_PAGE_CURRENCY_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[5]//input'
    MAIN_PAGE_CURRENCY_XPATH = '//*[@col-id="currency"]//span//span[4]'
    MAIN_PAGE_INSTR_TYPE_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[6]//input'
    MAIN_PAGE_INSTR_TYPE_XPATH = '//*[@col-id="instrType"]//span//span[4]'
    MAIN_PAGE_TENOR_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[7]//input'
    MAIN_PAGE_TENOR_XPATH = '//*[@col-id="tenor"]//span//span[4]'

    # Values tab
    VALUES_TAB_SYMBOL_XPATH = '//*[@formcontrolname="symbol"]'
    VALUES_TAB_INSTR_TYPE_XPATH = '//*[@id="instrType"]'
    VALUES_TAB_SECURITY_EXCHANGE_XPATH = '//*[@formcontrolname="securityExchange"]'
    VALUES_TAB_STRIKE_PRICE_XPATH = '//*[@formcontrolname="strikePrice"]'
    VALUES_TAB_MATURITY_DATE_XPATH = '//*[@formcontrolname="maturityDate_ext"]'
    VALUES_TAB_SETTL_TYPE_XPATH = '//*[@id="settlType"]'
    VALUES_TAB_LOOKUP_SYMBOL_XPATH = '//*[@formcontrolname="lookupSymbol"]'
    VALUES_TAB_INSTR_SUB_TYPE_XPATH = '//*[@id="instrSubType"]'
    VALUES_TAB_PREFERRED_SECURITY_EXCHANGE_XPATH = '//*[@formcontrolname="preferredSecurityExchange"]'
    VALUES_TAB_TENOR_XPATH = '//*[@id="tenor"]'
    VALUES_TAB_MATURITY_MONTH_YEAR_XPATH = '//*[@formcontrolname="maturityMonthYear"]'
    VALUES_TAB_DUMMY_CHECKBOX_XPATH = '//*[text()="Dummy"]/preceding-sibling::span'
    VALUES_TAB_INSTR_SYMBOL_XPATH = '//*[@formcontrolname="instrSymbol"]'
    VALUES_TAB_CFI_XPATH = '//*[@formcontrolname="CFI"]'
    VALUES_TAB_MIC_XPATH = '//*[@formcontrolname="MIC"]'
    VALUES_TAB_CALL_PUT_XPATH = '//*[@id="callPut"]'
    VALUES_TAB_INDUSTRY_XPATH = '//*[@id="industry"]'
    VALUES_TAB_SUB_INDUSTRY_XPATH = '//*[@id="subIndustry"]'
    VALUES_TAB_INDUSTRY_GROUP_XPATH = '//*[@id="industryGroup"]'
    VALUES_TAB_SECTOR_XPATH = '//*[@id="sector"]'
    VALUES_TAB_INSTR_SETTL_DATE_XPATH = '//*[@formcontrolname="instrSettlDate"]'
    VALUES_TAB_OPT_ATTR_XPATH = '//*[@formcontrolname="optAttr"]'

    # Translation tab
    # Listing
    TRANSLATION_TAB_LISTING_PLUS_BUTTON_XPATH = '//*[normalize-space()="Translation"]//..//*[normalize-space()="Listing"]//..//*[@nbtooltip="Add"]'
    TRANSLATION_TAB_LISTING_CHECKMARK_BUTTON_XPATH = '//*[normalize-space()="Translation"]//..//*[normalize-space()="Listing"]//..//*[@data-name="checkmark"]'
    TRANSLATION_TAB_LISTING_CLOSE_BUTTON_XPATH = '//*[normalize-space()="Translation"]//..//*[normalize-space()="Listing"]//..//*[@data-name="close"]'
    TRANSLATION_TAB_LISTING_EDIT_BUTTON_XPATH = '//*[normalize-space()="Translation"]//..//*[normalize-space()="Listing"]//..//*[@data-name="edit"]'
    TRANSLATION_TAB_LISTING_DELETE_BUTTON_XPATH = '//*[normalize-space()="Translation"]//..//*[normalize-space()="Listing"]//..//*[@data-name="trash-2"]'

    TRANSLATION_TAB_LISTING_LANGUAGE_FILTER_XPATH = '(//*[normalize-space()="Translation"]//..//*[normalize-space()="Listing"]//..//*[@placeholder="Filter"])[1]'
    TRANSLATION_TAB_LISTING_LANGUAGE_XPATH = '//*[normalize-space()="Translation"]//..//*[normalize-space()="Listing"]//..//*[@placeholder="Language *"]'
    TRANSLATION_TAB_LISTING_DESCRIPTION_FILTER_XPATH = '(//*[normalize-space()="Translation"]//..//*[normalize-space()="Listing"]//..//*[@placeholder="Filter"])[2]'
    TRANSLATION_TAB_LISTING_DESCRIPTION_XPATH = '//*[normalize-space()="Translation"]//..//*[normalize-space()="Listing"]//..//*[@placeholder="Description *"]'
    TRANSLATION_TAB_LISTING_SEARCHED_ENTITY_XPATH = '//*[normalize-space()="Translation"]//..//*[normalize-space()="Listing"]//..//span[normalize-space()="{}"]'

    # Instrument
    TRANSLATION_TAB_INSTRUMENT_PLUS_BUTTON_XPATH = '//*[normalize-space()="Translation"]//..//*[normalize-space()="Instrument"]//..//*[@nbtooltip="Add"]'
    TRANSLATION_TAB_INSTRUMENT_CHECKMARK_BUTTON_XPATH = '//*[normalize-space()="Translation"]//..//*[normalize-space()="Instrument"]//..//*[@data-name="checkmark"]'
    TRANSLATION_TAB_INSTRUMENT_CLOSE_BUTTON_XPATH = '//*[normalize-space()="Translation"]//..//*[normalize-space()="Instrument"]//..//*[@data-name="close"]'
    TRANSLATION_TAB_INSTRUMENT_EDIT_BUTTON_XPATH = '//*[normalize-space()="Translation"]//..//*[normalize-space()="Instrument"]//..//*[@data-name="edit"]'
    TRANSLATION_TAB_INSTRUMENT_DELETE_BUTTON_XPATH = '//*[normalize-space()="Translation"]//..//*[normalize-space()="Instrument"]//..//*[@data-name="trash-2"]'

    TRANSLATION_TAB_INSTRUMENT_LANGUAGE_FILTER_XPATH = '(//*[normalize-space()="Translation"]//..//*[normalize-space()="Instrument"]//..//*[@placeholder="Filter"])[1]'
    TRANSLATION_TAB_INSTRUMENT_LANGUAGE_XPATH = '//*[normalize-space()="Translation"]//..//*[normalize-space()="Instrument"]//..//*[@placeholder="Language *"]'
    TRANSLATION_TAB_INSTRUMENT_DESCRIPTION_FILTER_XPATH = '(//*[normalize-space()="Translation"]//..//*[normalize-space()="Instrument"]//..//*[@placeholder="Filter"])[2]'
    TRANSLATION_TAB_INSTRUMENT_DESCRIPTION_XPATH = '//*[normalize-space()="Translation"]//..//*[normalize-space()="Instrument"]//..//*[@placeholder="Description *"]'
    TRANSLATION_TAB_INSTRUMENT_SEARCHED_ENTITY_XPATH = '//*[normalize-space()="Translation"]//..//*[normalize-space()="Instrument"]//..//span[normalize-space()="{}"]'

    # Attachment tab
    ATTACHMENT_TAB_VENUE_XPATH = '//*[@id="venue"]'
    ATTACHMENT_TAB_PREFERRED_VENUE_XPATH = '//*[@id="preferredVenue"]'
    ATTACHMENT_TAB_SUB_VENUE_XPATH = '//*[@id="subVenue"]'
    ATTACHMENT_TAB_LISTING_GROUP_XPATH = '//*[@id="listingGroup"]'

    # Currency
    CURRENCY_TAB_CURRENCY_XPATH = '//*[@id="currency"]'
    CURRENCY_TAB_INSTR_CURRENCY_XPATH = '//*[@id="instrCurrency"]'
    CURRENCY_TAB_BASE_CURRENCY_XPATH = '//*[@id="baseCurrency"]'
    CURRENCY_TAB_STRIKE_CURRENCY_XPATH = '//*[@id="strikeCurrency"]'
    CURRENCY_TAB_QUOTE_CURRENCY_XPATH = '//*[@id="quoteCurrency"]'

    # Dark Algo Commissions
    DARK_ALGO_COM_COST_PER_TRADE_XPATH = '//*[@id="darkAlgoCostPerTrade"]'
    DARK_ALGO_COM_PER_UNIT_COMM_AMT_XPATH = '//*[@id="darkAlgoPerUnitCommAmt"]'
    DARK_ALGO_COM_COMM_BASIS_POINT_XPATH = '//*[@id="darkAlgoCommBasisPoints"]'
    DARK_ALGO_COM_SPREAD_DISCOUNT_PROPORTION_XPATH = '//*[@id="darkAlgoSpreadDiscount"]'
    DARK_ALGO_COM_IS_COMM_PER_UNIT_XPATH = '//*[@formcontrolname = "darkAlgoIsCommPerUnit"]//span[1]'

    # Market Data
    MARKET_DATA_TAB_SOURCE_XPATH = '//*[@formcontrolname="MDSource"]'
    MARKET_DATA_TAB_NEWS_SYMBOL_XPATH = '//*[@formcontrolname="newsMDSymbol"]'
    MARKET_DATA_TAB_QUOTE_SYMBOL_XPATH = '//*[@formcontrolname="quoteMDSymbol"]'
    MARKET_DATA_TAB_MARKET_DEPTH_SYMBOL_XPATH = '//*[@formcontrolname="marketDepthMDSymbol"]'
    MARKET_DATA_TAB_DEFAULT_MD_SYMBOL_XPATH = '//*[@formcontrolname="defaultMDSymbol"]'
    MARKET_DATA_TAB_TRADE_SYMBOL_XPATH = '//*[@formcontrolname="tradeMDSymbol"]'
    MARKET_DATA_TAB_QUOTE_BOOK_SYMBOL_XPATH = '//*[@formcontrolname="quoteBookMDSymbol"]'
    MARKET_DATA_TAB_ORDER_BOOK_SYMBOL_XPATH = '//*[@formcontrolname="orderBookMDSymbol"]'
    MARKET_DATA_TAB_STANDARD_MARKET_SIZE_XPATH = '//*[@formcontrolname="standardMarketSize"]'
    MARKET_DATA_TAB_STATUS_SYMBOL_XPATH = '//*[@formcontrolname="statusMDSymbol"]'
    MARKET_DATA_TAB_INTRADAY_SYMBOL_XPATH = '//*[@formcontrolname="intradayDataMDSymbol"]'
    MARKET_DATA_TAB_NATIVE_QUOTES_CHECKBOX_XPATH = '//*[text()="Native Quotes"]/preceding-sibling::span'

    # Market Identifiers tab
    MARKET_IDENTIFIERS_TAB_SECURITY_ID_XPATH = '//*[@formcontrolname="securityID"]'
    MARKET_IDENTIFIERS_TAB_SEDOL_ID_XPATH = '//*[@formcontrolname="SEDOLSecurityAltID"]'
    MARKET_IDENTIFIERS_TAB_RIC_ID_XPATH = '//*[@formcontrolname="RICSecurityAltID"]'
    MARKET_IDENTIFIERS_TAB_CTA_ID_XPATH = '//*[@formcontrolname="CTASecurityAltID"]'
    MARKET_IDENTIFIERS_TAB_DUTCH_ID_XPATH = '//*[@formcontrolname="dutchSecurityAltID"]'
    MARKET_IDENTIFIERS_TAB_BELGIAN_ID_XPATH = '//*[@formcontrolname="belgianSecurityAltID"]'
    MARKET_IDENTIFIERS_TAB_ISDA_ID_XPATH = '//*[@formcontrolname="ISDASecurityAltID"]'
    MARKET_IDENTIFIERS_TAB_INTERACTIVE_DATA_ID_XPATH = '//*[@formcontrolname="interactiveDataSecurityAltID"]'
    MARKET_IDENTIFIERS_TAB_SECURITY_ID_SOURCE_XPATH = '//*[@id="securityIDSource"]'
    MARKET_IDENTIFIERS_TAB_QUIK_ID_XPATH = '//*[@formcontrolname="QUIKSecurityAltID"]'
    MARKET_IDENTIFIERS_TAB_ISO_ID_XPATH = '//*[@formcontrolname="ISOSecurityAltID"]'
    MARKET_IDENTIFIERS_TAB_BLOOMBERG_ID_XPATH = '//*[@formcontrolname="blmbrgSecurityAltID"]'
    MARKET_IDENTIFIERS_TAB_VALOREN_ID_XPATH = '//*[@formcontrolname="valorenSecurityAltID"]'
    MARKET_IDENTIFIERS_TAB_COMMON_ID_XPATH = '//*[@formcontrolname="commonSecurityAltID"]'
    MARKET_IDENTIFIERS_TAB_OPTION_PRC_REPORTING_AUTH__ID_XPATH = '//*[@formcontrolname="optionPrcReportingAuthSecurityAltID"]'
    MARKET_IDENTIFIERS_TAB_MARKET_DATA_KEY_ID_XPATH = '//*[@formcontrolname="marketDataKeySecurityAltID"]'
    MARKET_IDENTIFIERS_TAB_CUSIP_ID_XPATH = '//*[@formcontrolname="CUSIPSecurityAltID"]'
    MARKET_IDENTIFIERS_TAB_ISIN_ID_XPATH = '//*[@formcontrolname="ISINSecurityAltID"]'
    MARKET_IDENTIFIERS_TAB_EXCHANGE_SYMBOL_ID_XPATH = '//*[@formcontrolname="exchSymbSecurityAltID"]'
    MARKET_IDENTIFIERS_TAB_WERTPAPIER_ID_XPATH = '//*[@formcontrolname="wertpapierSecurityAltID"]'
    MARKET_IDENTIFIERS_TAB_SICOVAM_ID_XPATH = '//*[@formcontrolname="sicovamSecurityAltID"]'
    MARKET_IDENTIFIERS_TAB_CLEARING_ID_XPATH = '//*[@formcontrolname="clearingSecurityAltID"]'
    MARKET_IDENTIFIERS_TAB_GL_TRADE_ID_XPATH = '//*[@formcontrolname="GLTradeSecurityAltID"]'
    MARKET_IDENTIFIERS_TAB_PRODUCT_COMPLEX = '//*[text()="Product Complex"]/preceding-sibling::input'

    # Format tab
    FORMAT_TAB_PRICE_FORMAT_XPATH = '//*[@formcontrolname="priceFormat"]'
    FORMAT_TAB_STRIKE_DECIMAL_PLACES_XPATH = '//*[@formcontrolname="strikeDecimalPlaces"]'
    FORMAT_TAB_STRIKE_TICK_DENOMINATOR_XPATH = '//*[@formcontrolname="strikeTickDenominator"]'
    FORMAT_TAB_PRICE_PRECISION_XPATH = '//*[@formcontrolname="pxPrecision"]'
    FORMAT_TAB_TICK_VALUE_XPATH = '//*[@formcontrolname="tickValue"]'
    FORMAT_TAB_LARGE_NUMBERS_PRECISION_XPATH = '//*[@formcontrolname="largeNumberPxPrecision"]'
    FORMAT_TAB_TICK_DENOMINATOR_XPATH = '//*[@formcontrolname="tickDenominator"]'

    # Feature tab
    FEATURE_TAB_ORDER_BOOK_VISIBILITY_XPATH = '//*[@id="orderBookVisibility"]'
    FEATURE_TAB_FORWARD_POINT_DIVISOR_XPATH = '//*[@formcontrolname="forwardPointDivisor"]'
    FEATURE_TAB_COMPOSITE_LISTING_ID_XPATH = '//*[@id="compositeListingID"]'
    FEATURE_TAB_COMPOSITE_VENUE_NAME_XPATH = '//*[@id="compositeVenueName"]'
    FEATURE_TAB_DEFAULT_TRADING_SESSION_XPATH = '//*[@id="defaultVenueTradingSessionID"]'
    FEATURE_TAB_CONTRACT_MULTIPLIER_XPATH = '//*[@formcontrolname="contractMultiplier"]'

    FEATURE_TAB_ASYNC_INDICATOR_CHECKBOX_XPATH = '//*[text()=" Async Indicator "]/preceding-sibling::span'
    FEATURE_TAB_CROSS_THROUGH_USD_CHECKBOX_XPATH = '//*[text()=" Cross Through USD "]/preceding-sibling::span'
    FEATURE_TAB_CROSS_THROUGH_EUR_TO_USD_CHECKBOX_XPATH = '//*[text()=" Cross Through EUR To USD "]/preceding-sibling::span'
    FEATURE_TAB_IS_REFINITIV_COMPOSITE_XPATH = '//*[text()=" Is Refinitiv Composite "]/preceding-sibling::span'

    FEATURE_TAB_IMPLIED_IN_SUPPORT_CHECKBOX_XPATH = '//*[text()=" Implied In Support "]/preceding-sibling::span'
    FEATURE_TAB_CROSS_THROUGH_EUR_CHECKBOX_XPATH = '//*[text()=" Cross Through EUR "]/preceding-sibling::span'
    FEATURE_TAB_CROSS_THROUGH_USD_TO_EUR_CHECKBOX_XPATH = '//*[text()=" Cross Through USD To EUR "]/preceding-sibling::span'

    FEATURE_TAB_ALGO_INCLUDED_CHECKBOX_XPATH = '//*[text()=" Algo Included "]/preceding-sibling::span'
    FEATURE_TAB_PERSIST_HISTORIC_TIME_SALES_XPATH = '//*[text()=" Persist Historic Time & Sales "]/preceding-sibling::span'
    FEATURE_TAB_IS_BLOOMBERG_COMPOSITE_XPATH = '//*[text()=" Is Bloomberg Composite "]/preceding-sibling::span'

    # Validations tab
    VALIDATIONS_TAB_PRICE_LIMIT_XPATH = '//*[@id="priceLimitProfile"]'
    VALIDATIONS_TAB_MIN_TRADE_VOL_XPATH = '//*[@formcontrolname="minTradeVolume"]'
    VALIDATIONS_TAB_PREVIOUS_TOTAL_TRADED_QTY_XPATH = '//*[@formcontrolname="prevTotalTradedQty"]'
    VALIDATIONS_TAB_PRE_TRADE_LIS_QTY_XPATH = '//*[@formcontrolname="preTradeLISQty"]'
    VALIDATIONS_TAB_MAX_TRADE_VOL_XPATH = '//*[@formcontrolname="maxTradeVolume"]'
    VALIDATIONS_TAB_MAX_SPREAD_XPATH = '//*[@formcontrolname="maxSpread"]'
    VALIDATIONS_TAB_TICK_SIZE_PROFILE_XPATH = '//*[@id="tickSizeProfile"]//following::button[1]'
    VALIDATIONS_TAB_PREVIOUS_CLOSE_PRICE_XPATH = '//*[@formcontrolname="prevClosePx"]'
    VALIDATIONS_TAB_ROUND_LOT_XPATH = '//*[@formcontrolname="roundLot"]'
    VALIDATIONS_TAB_MANAGE_PRICE_LIMIT_PROFILE_XPATH = '//*[@form-control-name="priceLimitProfile"]/parent::div/following-sibling::div//button'
    VALIDATIONS_TAB_MANAGE_TICK_SIZE_PROFILE_XPATH = '//*[@form-control-name="tickSizeProfile"]/parent::div/following-sibling::div//button'

    # Status tab
    STATUS_TAB_TRADING_PHASE_XPATH = '//*[@id="tradingPhase"]'
    STATUS_TAB_TRADING_SESSION_XPATH = '//*[@id="tradingSession"]'
    STATUS_TAB_TRADING_STATUS_XPATH = '//*[@id="tradingStatus"]'
    STATUS_TAB_EXTERNAL_TRADING_STATUS_PHASE_XPATH = '//*[@id="externalTradingStatus"]'

    # Short Sell
    SHORT_SELL_TAB_ALLOW_SHORT_SELL_CHECKBOX_XPATH = '//*[text()="Allow Short Sell"]/preceding-sibling::span'
    SHORT_SELL_TAB_DISABLE_UPDATE_TIME_XPATH = '//*[@id="disableShortSellUpdateTime_ext"]'
    SHORT_SELL_TAB_DISABLE_PERCENT_XPATH = '//*[@id="disableShortSellPrcFallPct"]'
    SHORT_SELL_TAB_DISABLE_UNTIL_DATE_XPATH = '//*[@formcontrolname="disableShortSellUntilDate_ext"]'

    # Misc tab
    MISC_TAB_MISC_0 = '//*[@formcontrolname="listingMisc0"]'
    MISC_TAB_MISC_1 = '//*[@formcontrolname="listingMisc1"]'
    MISC_TAB_MISC_2 = '//*[@formcontrolname="listingMisc2"]'
    MISC_TAB_MISC_3 = '//*[@formcontrolname="listingMisc3"]'
    MISC_TAB_MISC_4 = '//*[@formcontrolname="listingMisc4"]'
    MISC_TAB_MISC_5 = '//*[@formcontrolname="listingMisc5"]'
    MISC_TAB_MISC_6 = '//*[@formcontrolname="listingMisc6"]'
    MISC_TAB_MISC_7 = '//*[@formcontrolname="listingMisc7"]'
    MISC_TAB_MISC_8 = '//*[@formcontrolname="listingMisc8"]'
    MISC_TAB_MISC_9 = '//*[@formcontrolname="listingMisc9"]'

    # Counterpart tab
    COUNTERPART_TAB_COUNTERPART_XPATH = '//*[@id="counterpartPrimeBrokerGeneralTradeServices"]'

    # Fee Type Exemption
    FEE_TYPE_EXEMPTION_TAB_STAMP_FEE_EXEMPTION_CHECKBOX_XPATH = '//*[text()="Stamp Fee Exemption"]/preceding-sibling::span'
    FEE_TYPE_EXEMPTION_TAB_LEVY_FEE_EXEMPTION_CHECKBOX_XPATH = '//*[text()="Levy Fee Exemption"]/preceding-sibling::span'
    FEE_TYPE_EXEMPTION_TAB_PER_TRANSAC_FEE_EXEMPTION_CHECKBOX_XPATH = '//*[text()="Per Transac Fee Exemption"]/preceding-sibling::span'

    # Instrument list
    INSTRUMENT_LIST_TAB_PLUS_BUTTON_XPATH = '//*[text()=" Instrument List "]/parent::nb-accordion-item//nb-accordion-item-body//*[@class="nb-plus"]'
    INSTRUMENT_LIST_TAB_CHECKMARK_BUTTON_XPATH = '//*[text()=" Instrument List "]/parent::nb-accordion-item//nb-accordion-item-body//*[@class="nb-checkmark"]'
    INSTRUMENT_LIST_TAB_CLOSE_BUTTON_XPATH = '//*[text()=" Instrument List "]/parent::nb-accordion-item//nb-accordion-item-body//*[@class="nb-close"]'
    INSTRUMENT_LIST_TAB_EDIT_BUTTON_XPATH = '//*[text()=" Instrument List "]/parent::nb-accordion-item//nb-accordion-item-body//*[@class="nb-edit"]'
    INSTRUMENT_LIST_TAB_DELETE_BUTTON_XPATH = '//*[text()=" Instrument List "]/parent::nb-accordion-item//nb-accordion-item-body//*[@class="nb-trash"]'

    INSTRUMENT_LIST_TAB_INSTRUMENT_LIST_FILTER_XPATH = '//*[@class="instrumentList ng2-smart-th ng-star-inserted"]//input'
    INSTRUMENT_LIST_TAB_INSTRUMENT_LIST_XPATH = '//*[@placeholder="Instrument List *"]'

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
    TICK_SIZE_PROFILES_TAB_PLUS_BUTTON_XPATH = '//*[normalize-space()="External ID"]//ancestor::p-table//*[@nbtooltip="Add"]'
    TICK_SIZE_PROFILES_TAB_CHECKMARK_BUTTON_XPATH = '//*[normalize-space()="External ID"]//ancestor::p-table//*[@data-name="checkmark"]'
    TICK_SIZE_PROFILES_TAB_CLOSE_BUTTON_XPATH = '//*[normalize-space()="External ID"]//ancestor::p-table//*[@data-name="close"]'
    TICK_SIZE_PROFILES_TAB_EDIT_BUTTON_XPATH = '//*[normalize-space()="External ID"]//ancestor::p-table//*[@data-name="edit"]'
    TICK_SIZE_PROFILES_TAB_DELETE_BUTTON_XPATH = '//*[normalize-space()="External ID"]//ancestor::p-table//*[@data-name="trash-2"]'

    TICK_SIZE_PROFILES_TAB_EXTERNAL_ID_XPATH = '//*[@placeholder="External ID *"]'
    TICK_SIZE_PROFILES_TAB_EXTERNAL_ID_FILTER_XPATH = '(//*[normalize-space()="External ID"]//ancestor::p-table//*[@placeholder="Filter"])[1]'
    TICK_SIZE_PROFILES_TAB_TICK_SIZE_XAXIS_TYPE_XPATH = '//*[@placeholder="Tick Size XAxis Type"]'
    TICK_SIZE_PROFILES_TAB_TICK_SIZE_XAXIS_TYPE_FILTER_XPATH = '(//*[normalize-space()="External ID"]//ancestor::p-table//*[@placeholder="Filter"])[2]'
    TICK_SIZE_PROFILES_TAB_TICK_SIZE_REFPRICE_TYPE_XPATH = '//*[@placeholder="Tick Size RefPrice Type"]'
    TICK_SIZE_PROFILES_TAB_TICK_SIZE_REFPRICE_TYPE_FILTER_XPATH = '(//*[normalize-space()="External ID"]//ancestor::p-table//*[@placeholder="Filter"])[3]'
    TICK_SIZE_PROFILES_LOOKUP_FIELD_XPATH = '//input[contains(@class, "lookup-in")]'
    TICK_SIZE_PROFILES_LOAD_BUTTON_XPATH = '//button[contains(@class, "lookup-btn")]'

    # --Tick size points sub tab--
    TICK_SIZE_POINTS_TAB_PLUS_BUTTON_XPATH = '//*[normalize-space()="Tick"]//ancestor::p-table//*[@nbtooltip="Add"]'
    TICK_SIZE_POINTS_TAB_CHECKMARK_BUTTON_XPATH = '//*[normalize-space()="Tick"]//ancestor::p-table//*[@data-name="checkmark"]'
    TICK_SIZE_POINTS_TAB_CLOSE_BUTTON_XPATH = '//*[normalize-space()="Tick"]//ancestor::p-table//*[@data-name="close"]'
    TICK_SIZE_POINTS_TAB_EDIT_BUTTON_XPATH = '//*[normalize-space()="Tick"]//ancestor::p-table//*[@data-name="edit"]'
    TICK_SIZE_POINTS_TAB_DELETE_BUTTON_XPATH = '//*[normalize-space()="Tick"]//ancestor::p-table//*[@data-name="trash-2"]'

    TICK_SIZE_POINTS_TAB_TICK_XPATH = '//*[@placeholder="Tick *"]'
    TICK_SIZE_POINTS_TAB_TICK_FILTER_XPATH = '(//*[normalize-space()="Tick"]//ancestor::p-table//*[@placeholder="Filter"])[1]'
    TICK_SIZE_POINTS_TAB_UPPER_LIMIT_XPATH = '//*[@placeholder="Upper Limit"]'
    TICK_SIZE_POINTS_TAB_UPPER_LIMIT_FILTER_XPATH = '(//*[normalize-space()="Tick"]//ancestor::p-table//*[@placeholder="Filter"])[2]'
