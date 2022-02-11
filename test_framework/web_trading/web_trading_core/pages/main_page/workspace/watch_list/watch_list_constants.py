class WatchListConstants:
    # region Watch List
    MAXIMIZE_BUTTON_XPATH = 'return document.querySelector("*[slot=\'tab_default_123456789\']").querySelector("igc-dockmanager").shadowRoot.querySelector("igc-pane-header-component").shadowRoot.querySelector("*[name=\'maximize\']")'
    MINIMIZE_BUTTON_XPATH = 'return document.querySelector("*[slot=\'tab_default_123456789\']").querySelector("igc-dockmanager").shadowRoot.querySelector("igc-pane-header-component").shadowRoot.querySelector("*[name=\'maximize\']")'
    CLOSE_BUTTON_XPATH = 'return document.querySelector("*[slot=\'tab_default_123456789\']").querySelector("igc-dockmanager").shadowRoot.querySelector("igc-pane-header-component").shadowRoot.querySelector("*[title=\'Close\']")'
    COPY_PANAL_BUTTON_XPATH = '//*[@class="copy-workspace-icon"]/img'
    FIELD_CHOOSER_XPATH = '//*[@name="btnColumnHiding"]'
    ADVANCED_FILTERING_BUTTON_XPATH = '//*[@name="btnAdvancedFiltering"]'
    HORIZONTAL_SCROLL_XPATH = '//*[@class="igx-vhelper--horizontal ng-star-inserted"]/div[@class="igx-vhelper__placeholder-content"]'
    SEARCH_SYMBOL_INPUT_XPATH = '//*[@id="style-3"]//igx-input-group'
    TRADED_LISTINGS_BUTTON_XPATH = '//*[@class="trading-listing"]/igx-switch'
    # endregion

    # region Field chooser
    FILTER_COLUMNS_LIST_FIELD_XPATH = '//*[@class="igx-column-actions__header"]//input'
    SYMBOL_CHECKBOX_XPATH = '//*[@class="igx-overlay__content"]//*[text()=" Symbol "]'
    HIDE_ALL_BUTTON_XPATH = '//*[text()="Hide All"]'
    SHOW_ALL_BUTTON_XPATH = '//*[text()="Show All"]'
    # endregion

    # region Advanced filtering
    DRAG_ADVANCED_FILTERING_WINDOW_XPATH = '//*[@class="igx-overlay__wrapper"]//header'
    AND_GROUP_BUTTON_XPATH = '//*[text()=\'"And" Group\']'
    OR_GROUP_BUTTON_XPATH = '//*[text()=\'"Or" Group\']'
    CLEAR_FILTER_BUTTON_XPATH = '//*[@class="igx-excel-filter__clear"]/button'
    CANCEL_BUTTON_XPATH = '//*[@class="igx-excel-filter__cancel"]/button'
    APPLY_BUTTON_XPATH = '//*[@class="igx-excel-filter__apply"]/button'
    BACK_LINE_BUTTON_XPATH = '//*[contains(@class,"igx-filter-tree__line")]'
    SELECT_COLUMN_FIELD_XPATH = '//*[@placeholder="Select column"]'
    SELECT_COLUMN_SYMBOL_XPATH = '//*[@class="igx-drop-down__list-scroll"]//*[text()=" Symbol "]'
    SELECT_FILTER_FIELD_XPATH = '//*[@placeholder="Select filter"]'
    SELECT_FILTER_CONTAINS_XPATH = '//*[text()="Contains"]'
    VALUE_FIELD_XPATH = '//*[@placeholder="Value"]'
    CHECK_AF_BUTTON_XPATH = '//*[contains(@class,"igx-filter-tree__inputs ng-star-inserted")]//button[1]'
    CLOSE_AF_BUTTON_XPATH = '//*[contains(@class,"igx-filter-tree__inputs ng-star-inserted")]//button[2]'
    CONDITION_BUTTON_XPATH = '//*[text()="Condition"]'
    AND_BUTTON_XPATH = '//*[text()=\'"And" Group\']'
    OR_BUTTON_XPATH = '//*[text()=\'"Or" Group\']'
    # endregion

    # region Columns Trades
    SYMBOL_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" Symbol "]'
    SORT_SYMBOL_COLUMN_XPATH = '//*[text()=" Symbol "]/../following-sibling::div/igx-icon'
    FILTER_SYMBOL_COLUMN_XPATH = '//*[text()=" Symbol "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

    LAST_TREND_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" LastTrend "]'
    SORT_LAST_TREND_COLUMN_XPATH = '//*[text()=" LastTrend "]/../following-sibling::div/igx-icon'
    FILTER_LAST_TREND_COLUMN_XPATH = '//*[text()=" LastTrend "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

    BID_QTY_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" BidQty "]'
    SORT_BID_QTY_COLUMN_XPATH = '//*[text()=" BidQty "]/../following-sibling::div/igx-icon'
    FILTER_BID_QTY_COLUMN_XPATH = '//*[text()=" BidQty "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

    BID_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" Bid "]'
    SORT_BID_COLUMN_XPATH = '//*[text()=" Bid "]/../following-sibling::div/igx-icon'
    FILTER_BID_COLUMN_XPATH = '//*[text()=" Bid "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

    ASK_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" Ask "]'
    SORT_ASK_COLUMN_XPATH = '//*[text()=" Ask "]/../following-sibling::div/igx-icon'
    FILTER_ASK_COLUMN_XPATH = '//*[text()=" Ask "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

    ASK_QTY_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" AskQty "]'
    SORT_ASK_QTY_COLUMN_XPATH = '//*[text()=" AskQty "]/../following-sibling::div/igx-icon'
    FILTER_ASK_QTY_COLUMN_XPATH = '//*[text()=" AskQty "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

    TRADE_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" Trade "]'
    SORT_TRADE_COLUMN_XPATH = '//*[text()=" Trade "]/../following-sibling::div/igx-icon'
    FILTER_TRADE_COLUMN_XPATH = '//*[text()=" Trade "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

    OPENPX_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" OpenPx "]'
    SORT_OPENPX_COLUMN_XPATH = '//*[text()=" OpenPx "]/../following-sibling::div/igx-icon'
    FILTER_OPENPX_COLUMN_XPATH = '//*[text()=" OpenPx "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

    CLOSINGPX_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" ClosingPx "]'
    SORT_CLOSINGPX_COLUMN_XPATH = '//*[text()=" ClosingPx "]/../following-sibling::div/igx-icon'
    FILTER_CLOSINGPX_COLUMN_XPATH = '//*[text()=" ClosingPx "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

    HIGHPX_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" HighPx "]'
    SORT_HIGHPX_COLUMN_XPATH = '//*[text()=" HighPx "]/../following-sibling::div/igx-icon'
    FILTER_HIGHPX_COLUMN_XPATH = '//*[text()=" HighPx "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

    LOWPX_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" LowPx "]'
    SORT_LOWPX_COLUMN_XPATH = '//*[text()=" LowPx "]/../following-sibling::div/igx-icon'
    FILTER_LOWPX_COLUMN_XPATH = '//*[text()=" LowPx "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

    TRADE_VOLUME_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" TradeVolume "]'
    SORT_TRADE_VOLUME_COLUMN_XPATH = '//*[text()=" TradeVolume "]/../following-sibling::div/igx-icon'
    FILTER_TRADE_VOLUME_COLUMN_XPATH = '//*[text()=" TradeVolume "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

    OPEN_INTEREST_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" OpenInterest "]'
    SORT_OPEN_INTEREST_COLUMN_XPATH = '//*[text()=" OpenInterest "]/../following-sibling::div/igx-icon'
    FILTER_OPEN_INTEREST_COLUMN_XPATH = '//*[text()=" OpenInterest "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

    SIMULATED_SELL_PRICE_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" SimulatedSellPrice "]'
    SORT_SIMULATED_SELL_PRICE_COLUMN_XPATH = '//*[text()=" SimulatedSellPrice "]/../following-sibling::div/igx-icon'
    FILTER_SIMULATED_SELL_PRICE_COLUMN_XPATH = '//*[text()=" SimulatedSellPrice "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

    SIMULATED_BUY_PRICE_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" SimulatedBuyPrice "]'
    SORT_SIMULATED_BUY_PRICE_COLUMN_XPATH = '//*[text()=" SimulatedBuyPrice "]/../following-sibling::div/igx-icon'
    FILTER_SIMULATED_BUY_PRICE_COLUMN_XPATH = '//*[text()=" SimulatedBuyPrice "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

    MARGIN_RATE_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" MarginRate "]'
    SORT_MARGIN_RATE_COLUMN_XPATH = '//*[text()=" MarginRate "]/../following-sibling::div/igx-icon'
    FILTER_MARGIN_RATE_COLUMN_XPATH = '//*[text()=" MarginRate "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

    MID_PRICE_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" MidPrice "]'
    SORT_MID_PRICE_COLUMN_XPATH = '//*[text()=" MidPrice "]/../following-sibling::div/igx-icon'
    FILTER_MID_PRICE_COLUMN_XPATH = '//*[text()=" MidPrice "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

    SETTLE_HIGH_PRICE_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" SettleHighPrice "]'
    SORT_SETTLE_HIGH_PRICE_COLUMN_XPATH = '//*[text()=" SettleHighPrice "]/../following-sibling::div/igx-icon'
    FILTER_SETTLE_HIGH_PRICE_COLUMN_XPATH = '//*[text()=" SettleHighPrice "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

    PRIOR_SETTLE_PRICE_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" PriorSettlePrice "]'
    SORT_PRIOR_SETTLE_PRICE_COLUMN_XPATH = '//*[text()=" PriorSettlePrice "]/../following-sibling::div/igx-icon'
    FILTER_PRIOR_SETTLE_PRICE_COLUMN_XPATH = '//*[text()=" PriorSettlePrice "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

    PRIOR_SETTLE_PRICEPRICE_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" PriorSettlePriceprice "]'
    SORT_PRIOR_SETTLE_PRICEPRICE_COLUMN_XPATH = '//*[text()=" PriorSettlePriceprice "]/../following-sibling::div/igx-icon'
    FILTER_PRIOR_SETTLE_PRICEPRICE_COLUMN_XPATH = '//*[text()=" PriorSettlePriceprice "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

    SESSION_HIGH_BID_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" SessionHighBid "]'
    SORT_SESSION_HIGH_BID_COLUMN_XPATH = '//*[text()=" SessionHighBid "]/../following-sibling::div/igx-icon'
    FILTER_SESSION_HIGH_BID_COLUMN_XPATH = '//*[text()=" SessionHighBid "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

    SESSION_LOW_OFFER_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" SessionLowOffer "]'
    SORT_SESSION_LOW_OFFER_COLUMN_XPATH = '//*[text()=" SessionLowOffer "]/../following-sibling::div/igx-icon'
    FILTER_SESSION_LOW_OFFER_COLUMN_XPATH = '//*[text()=" SessionLowOffer "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

    AUCTION_PRICE_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" AuctionPrice "]'
    SORT_AUCTION_PRICE_COLUMN_XPATH = '//*[text()=" AuctionPrice "]/../following-sibling::div/igx-icon'
    FILTER_AUCTION_PRICE_COLUMN_XPATH = '//*[text()=" AuctionPrice "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

    FIXING_PRICE_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" FixingPrice "]'
    SORT_FIXING_PRICE_COLUMN_XPATH = '//*[text()=" FixingPrice "]/../following-sibling::div/igx-icon'
    FILTER_FIXING_PRICE_COLUMN_XPATH = '//*[text()=" FixingPrice "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

    CASH_RATE_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" CashRate "]'
    SORT_CASH_RATE_COLUMN_XPATH = '//*[text()=" CashRate "]/../following-sibling::div/igx-icon'
    FILTER_CASH_RATE_COLUMN_XPATH = '//*[text()=" CashRate "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

    RECOVERY_RATE_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" RecoveryRate "]'
    SORT_RECOVERY_RATE_COLUMN_XPATH = '//*[text()=" RecoveryRate "]/../following-sibling::div/igx-icon'
    FILTER_RECOVERY_RATE_COLUMN_XPATH = '//*[text()=" RecoveryRate "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'
    # endregion

    # region Hover order buttons
    BUY_HOVER_BUTTON_XPATH = '//*[@class="buy-hover ng-star-inserted"]'
    SELL_HOVER_BUTTON_XPATH = '//*[@class="sell-hover ng-star-inserted"]'
    MARKET_DEPTH_HOVER_BUTTON_XPATH = '//*[@data-rowindex="0"]//*[contains(@src, "list-outline")]'
    TIMES_AND_SALES_HOVER_BUTTON_XPATH = '//*[@data-rowindex="0"]//*[contains(@src, "watchlist")]'
    # endregion

    # region Orders fields
    ORDER_SYMBOL_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_InstrSymbol")]'
    ORDER_LAST_TREND_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_Indicator")]'
    ORDER_BID_QTY_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_Bidquantity")]'
    ORDER_BID_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_Bidprice")]'
    ORDER_ASK_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_Offerprice")]'
    ORDER_ASK_QTY_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_Offerquantity")]'
    ORDER_TRADE_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_Tradeprice")]'
    ORDER_OPENPX_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_OpeningPriceprice")]'
    ORDER_CLOSINGPX_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_ClosingPriceprice")]'
    ORDER_HIGHPX_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_TradingSessionHighPriceprice")]'
    ORDER_LOWPX_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_TradingSessionLowPriceprice")]'
    ORDER_TRADE_VOLUME_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_TradeVolumequantity")]'
    ORDER_OPEN_INTEREST_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_OpenInterestquantity")]'
    ORDER_SIMULATED_SELL_PRICE_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_SimulatedSellPriceprice")]'
    ORDER_SIMULATED_BUY_PRICE_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_SimulatedBuyPriceprice")]'
    ORDER_MARGIN_RATE_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_MarginRateprice")]'
    ORDER_MID_PRICE_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_MidPriceprice")]'
    ORDER_SETTLE_HIGH_PRICE_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_SettleHighPriceprice")]'
    ORDER_PRIOR_SETTLE_PRICE_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_SettleLowPriceprice")]'
    ORDER_PRIOR_SETTLE_PRICEPRICE_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_PriorSettlePriceprice")]'
    ORDER_SESSION_HIGH_BID_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_SessionHighBidprice")]'
    ORDER_SESSION_LOW_OFFER_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_SessionLowOfferprice")]'
    ORDER_AUCTION_PRICE_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_AuctionClearingPriceprice")]'
    ORDER_FIXING_PRICE_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_FixingPriceprice")]'
    ORDER_CASH_RATE_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_CashRateprice")]'
    ORDER_RECOVERY_RATE_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_RecoveryRateprice")]'
    # endregion
