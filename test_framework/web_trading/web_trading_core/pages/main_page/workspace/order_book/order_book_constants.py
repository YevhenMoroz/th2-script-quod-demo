class OrderBookConstants:

    # region Order Book
    SWITCH_BUTTON_XPATH = '//*[@class="igx-switch__composite"]'
    MAXIMIZE_BUTTON_CSS = 'return document.querySelector("*[slot=\'tab_default_123456789\']").querySelector("igc-dockmanager").shadowRoot.querySelector("igc-pane-header-component").shadowRoot.querySelector("*[name=\'maximize\']")'
    MINIMIZE_BUTTON_CSS = 'return document.querySelector("*[slot=\'tab_default_123456789\']").querySelector("igc-dockmanager").shadowRoot.querySelector("igc-pane-header-component").shadowRoot.querySelector("*[name=\'maximize\']")'
    CLOSE_BUTTON_CSS = 'return document.querySelector("*[slot=\'tab_default_123456789\']").querySelector("igc-dockmanager").shadowRoot.querySelector("igc-pane-header-component").shadowRoot.querySelector("*[title=\'Close\']")'
    COPY_PANEL_BUTTON_XPATH = '//*[@class="copy-workspace-icon"]/img'
    FIELD_CHOOSER_XPATH = '//*[@name="btnColumnHiding"]'
    ADVANCED_FILTERING_BUTTON_XPATH = '//*[@name="btnAdvancedFiltering"]'
    HORIZONTAL_SCROLL_XPATH = '//*[@class="igx-vhelper--horizontal ng-star-inserted"]/div[@class="igx-vhelper__placeholder-content"]'
    # endregion

    # region Orders fields
    ORDER_SYMBOL_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_Instrument_InstrSymbol")]//span'
    ORDER_INSTR_TYPE_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_Instrument_InstrType")]//span'
    ORDER_ORDER_ID_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_OrdID")]//span'
    ORDER_ACCOUNT_CODE_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_ClientAccountGroupID")]//span'
    ORDER_SIDE_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_Side")]//span'
    ORDER_ORDER_QTY_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_OrdQty")]//span'
    ORDER_PRICE_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_Price")]//span'
    ORDER_AVG_PRICE_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_AvgPrice")]//span'
    ORDER_LEAVES_QTY_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_LeavesQty")]//span'
    ORDER_ORDER_TYPE_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_OrdType")]//span'
    ORDER_CUM_QTY_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_CumQty")]//span'
    ORDER_ORDER_STATUS_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_OrderStatus")]//span'
    ORDER_EXPIRE_DATE_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_ExpireDate")]//span'
    ORDER_SETTLE_DATE_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_SettlDate")]//span'
    ORDER_SETTLE_TYPE_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_SettlType")]//span'
    ORDER_TIME_IN_FORCE_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_TimeInForce")]//span'
    ORDER_FREE_NOTES_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_FreeNotes")]//span'
    ORDER_ACCOUNT_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_Account")]//span'
    ORDER_TRANSACTION_TIME_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_TransactTime")]//span'
    ORDER_CIORDID_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_ClOrdID")]//span'
    # endregion

    # region Switch
    FROM_FIELD_XPATH = '//*[@formcontrolname="dateFrom"]//div[@class="igx-input-group__bundle-main"]'
    TO_FIELD_XPATH = '//*[@formcontrolname="dateTo"]//div[@class="igx-input-group__bundle-main"]'
    CANSEL_FROM_BUTTON_XPATH = '//*[@formcontrolname="dateFrom"]//igx-suffix'
    CANSEL_TO_BUTTON_XPATH = '//*[@formcontrolname="dateTo"]//igx-suffix'
    SEARCH_XPATH = '//*[text()="Search"]'
    # endregion

    # region Field chooser
    FILTER_COLUMNS_LIST_FIELD_XPATH = '//*[@class="igx-column-actions__header"]//input'
    LIST_CHECKBOX_XPATH = '//*[@class="igx-overlay__content"]//*[text()="{}"]'
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
    SELECT_COLUMN_LIST_XPATH = '//*[@class="igx-drop-down__list-scroll"]//*[text()="{}"]'
    SELECT_FILTER_FIELD_XPATH = '//*[@placeholder="Select filter"]'
    SELECT_FILTER_LIST_XPATH = '//*[text()="{}"]'
    VALUE_FIELD_XPATH = '//*[@placeholder="Value"]'
    CHECK_AF_BUTTON_XPATH = '//*[contains(@class,"igx-filter-tree__inputs ng-star-inserted")]//button[1]'
    CLOSE_AF_BUTTON_XPATH = '//*[contains(@class,"igx-filter-tree__inputs ng-star-inserted")]//button[2]'
    CONDITION_BUTTON_XPATH = '//*[text()="Condition"]'
    AND_BUTTON_XPATH = '//*[text()=\'"And" Group\']'
    OR_BUTTON_XPATH = '//*[text()=\'"Or" Group\']'
    # endregion

    # region Columns Filter
    PIN_BUTTON_XPATH = '//*[@aria-label="Pin column"]'
    HIDE_BUTTON_XPATH = '//*[@aria-label="Hide column"]'
    SEARCH_FIELD_XPATH = '//*[@placeholder="Search"]'
    SELECT_ALL_CHECKBOX_XPATH = '//*[text()=" Select All "]'
    CANCEL_XPATH = '//*[@class="igx-excel-filter__cancel"]'
    APPLY_XPATH = '//*[@class="igx-excel-filter__apply"]'
    # endregion

    # region Hover order buttons
    BUY_HOVER_BUTTON_XPATH = '//*[@class="buy-hover ng-star-inserted"]'
    SELL_HOVER_BUTTON_XPATH = '//*[@class="sell-hover ng-star-inserted"]'
    MODIFY_HOVER_BUTTON_XPATH = '//*[@data-rowindex="0"]//*[contains(@src, "edit")]'
    MARKET_DEPTH_HOVER_BUTTON_XPATH = '//*[@data-rowindex="0"]//*[contains(@src, "list-outline")]'
    TIMES_AND_SALES_HOVER_BUTTON_XPATH = '//*[@data-rowindex="0"]//*[contains(@src, "watchlist")]'
    CANCEL_HOVER_BUTTON_XPATH = '//*[@data-rowindex="0"]//*[contains(@src, "button-close")]'
    REORDER_HOVER_BUTTON_XPATH = '//*[@data-rowindex="0"]//*[contains(@src, "reorder")]'
    # endregion

    # region Columns Order Book
    SYMBOL_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" Symbol "]'
    SORT_SYMBOL_COLUMN_XPATH = '//*[text()=" Symbol "]/../following-sibling::div/igx-icon'
    FILTER_SYMBOL_COLUMN_XPATH = '//*[text()=" Symbol "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

    INSTR_TYPE_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" Instr Type "]'
    SORT_INSTR_TYPE_COLUMN_XPATH = '//*[text()=" Instr Type "]/../following-sibling::div/igx-icon'
    FILTER_INSTR_TYPE_COLUMN_XPATH = '//*[text()=" Instr Type "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

    ORDER_ID_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" Order ID "]'
    SORT_ORDER_ID_COLUMN_XPATH = '//*[text()=" Order ID "]/../following-sibling::div/igx-icon'
    FILTER_ORDER_ID_COLUMN_XPATH = '//*[text()=" Order ID "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

    ACCOUNT_CODE_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" Account Code "]'
    SORT_ACCOUNT_CODE_COLUMN_XPATH = '//*[text()=" Account Code "]/../following-sibling::div/igx-icon'
    FILTER_ACCOUNT_CODE_COLUMN_XPATH = '//*[text()=" Account Code "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

    SIDE_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" Side "]'
    SORT_SIDE_COLUMN_XPATH = '//*[text()=" Side "]/../following-sibling::div/igx-icon'
    FILTER_SIDE_COLUMN_XPATH = '//*[text()=" Side "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

    ORDER_QTY_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" Order Qty "]'
    SORT_ORDER_QTY_COLUMN_XPATH = '//*[text()=" Order Qty "]/../following-sibling::div/igx-icon'
    FILTER_ORDER_QTY_COLUMN_XPATH = '//*[text()=" Order Qty "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

    PRICE_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" Price "]'
    SORT_PRICE_COLUMN_XPATH = '//*[text()=" Price "]/../following-sibling::div/igx-icon'
    FILTER_PRICE_COLUMN_XPATH = '//*[text()=" Price "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

    AVG_PRICE_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" Avg Price "]'
    SORT_AVG_PRICE_COLUMN_XPATH = '//*[text()=" Avg Price "]/../following-sibling::div/igx-icon'
    FILTER_AVG_PRICE_COLUMN_XPATH = '//*[text()=" Avg Price "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

    LEAVES_QTY_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" Leaves Qty "]'
    SORT_LEAVES_QTY_COLUMN_XPATH = '//*[text()=" Leaves Qty "]/../following-sibling::div/igx-icon'
    FILTER_LEAVES_QTY_COLUMN_XPATH = '//*[text()=" Leaves Qty "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

    ORDER_TYPE_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" Order Type "]'
    SORT_ORDER_TYPE_COLUMN_XPATH = '//*[text()=" Order Type "]/../following-sibling::div/igx-icon'
    FILTER_ORDER_TYPE_COLUMN_XPATH = '//*[text()=" Order Type "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

    CUM_QTY_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" Cum Qty "]'
    SORT_CUM_QTY_COLUMN_XPATH = '//*[text()=" Cum Qty "]/../following-sibling::div/igx-icon'
    FILTER_CUM_QTY_COLUMN_XPATH = '//*[text()=" Cum Qty "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

    ORDER_STATUS_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" Order Status "]'
    SORT_ORDER_STATUS_COLUMN_XPATH = '//*[text()=" Order Status "]/../following-sibling::div/igx-icon'
    FILTER_ORDER_STATUS_COLUMN_XPATH = '//*[text()=" Order Status "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

    EXPIRE_DATE_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" Expire Date "]'
    SORT_EXPIRE_DATE_COLUMN_XPATH = '//*[text()=" Expire Date "]/../following-sibling::div/igx-icon'
    FILTER_EXPIRE_DATE_COLUMN_XPATH = '//*[text()=" Expire Date "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

    SETTLE_DATE_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" Settle Date "]'
    SORT_SETTLE_DATE_COLUMN_XPATH = '//*[text()=" Settle Date "]/../following-sibling::div/igx-icon'
    FILTER_SETTLE_DATE_COLUMN_XPATH = '//*[text()=" Settle Date "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

    SETTLE_TYPE_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" Settle Type "]'
    SORT_SETTLE_TYPE_COLUMN_XPATH = '//*[text()=" Settle Type "]/../following-sibling::div/igx-icon'
    FILTER_SETTLE_TYPE_COLUMN_XPATH = '//*[text()=" Settle Type "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

    TIME_IN_FORCE_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" Time In Force "]'
    SORT_TIME_IN_FORCE_COLUMN_XPATH = '//*[text()=" Time In Force "]/../following-sibling::div/igx-icon'
    FILTER_TIME_IN_FORCE_COLUMN_XPATH = '//*[text()=" Time In Force "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

    FREE_NOTES_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" FreeNotes "]'
    SORT_FREE_NOTES_COLUMN_XPATH = '//*[text()=" FreeNotes "]/../following-sibling::div/igx-icon'
    FILTER_FREE_NOTES_COLUMN_XPATH = '//*[text()=" FreeNotes "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

    ACCOUNT_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" Account "]'
    SORT_ACCOUNT_COLUMN_XPATH = '//*[text()=" Account "]/../following-sibling::div/igx-icon'
    FILTER_ACCOUNT_COLUMN_XPATH = '//*[text()=" Account "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

    TRANSACTION_TIME_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" Transaction Time "]'
    SORT_TRANSACTION_TIME_COLUMN_XPATH = '//*[text()=" Transaction Time "]/../following-sibling::div/igx-icon'
    FILTER_TRANSACTION_TIME_COLUMN_XPATH = '//*[text()=" Transaction Time "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

    CIORDID_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" ClOrdID "]'
    SORT_CIORDID_COLUMN_XPATH = '//*[text()=" ClOrdID "]/../following-sibling::div/igx-icon'
    FILTER_CIORDID_COLUMN_XPATH = '//*[text()=" ClOrdID "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'
    # endregion
