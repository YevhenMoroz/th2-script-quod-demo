class PositionsConstants:
    # region Positions
    MAXIMIZE_BUTTON_CSS = 'return document.querySelector("*.doc-manager-geojit-window").querySelector("*.dockManagerContent.ng-star-inserted").querySelector("igc-dockmanager").shadowRoot.querySelector("igc-pane-header-component").shadowRoot.querySelector("*[name=\'maximize\']")'
    MINIMIZE_BUTTON_CSS = 'return document.querySelector("*[slot=\'tab_default_123456789\']").querySelector("igc-dockmanager").shadowRoot.querySelector("igc-pane-header-component").shadowRoot.querySelector("*[name=\'maximize\']")'
    CLOSE_BUTTON_CSS = 'return document.querySelector("*[slot=\'tab_default_123456789\']").querySelector("igc-dockmanager").shadowRoot.querySelector("igc-pane-header-component").shadowRoot.querySelector("*[title=\'Close\']")'
    COPY_PANEL_BUTTON_XPATH = '//*[@class="copy-workspace-icon"]/img'
    FIELD_CHOOSER_XPATH = '//*[@name="btnColumnHiding"]'
    ADVANCED_FILTERING_BUTTON_XPATH = '//*[@name="btnAdvancedFiltering"]'
    HORIZONTAL_SCROLL_XPATH = '//*[@class="igx-vhelper--horizontal ng-star-inserted"]/div[@class="igx-vhelper__placeholder-content"]'
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

    # region Columns Positions
    SYMBOL_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" Symbol "]'
    SORT_SYMBOL_COLUMN_XPATH = '//*[text()=" Symbol "]/../following-sibling::div/igx-icon'
    FILTER_SYMBOL_COLUMN_XPATH = '//*[text()=" Symbol "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

    INSTR_TYPE_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" InstrType "]'
    SORT_INSTR_TYPE_COLUMN_XPATH = '//*[text()=" InstrType "]/../following-sibling::div/igx-icon'
    FILTER_INSTR_TYPE_COLUMN_XPATH = '//*[text()=" InstrType "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

    EXCHANGE_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" Exchange "]'
    SORT_EXCHANGE_COLUMN_XPATH = '//*[text()=" Exchange "]/../following-sibling::div/igx-icon'
    FILTER_EXCHANGE_COLUMN_XPATH = '//*[text()=" Exchange "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

    TOTALY_QTY_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" Total Qty "]'
    SORT_TOTALY_QTY_COLUMN_XPATH = '//*[text()=" Total Qty "]/../following-sibling::div/igx-icon'
    FILTER_TOTALY_QTY_COLUMN_XPATH = '//*[text()=" Total Qty "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

    RESERVED_QTY_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" Reserved Qty "]'
    SORT_RESERVED_QTY_COLUMN_XPATH = '//*[text()=" Reserved Qty "]/../following-sibling::div/igx-icon'
    FILTER_RESERVED_QTY_COLUMN_XPATH = '//*[text()=" Reserved Qty "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

    COVERED_QTY_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" Covered Qty "]'
    SORT_COVERED_QTY_COLUMN_XPATH = '//*[text()=" Covered Qty "]/../following-sibling::div/igx-icon'
    FILTER_COVERED_QTY_COLUMN_XPATH = '//*[text()=" Covered Qty "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

    LEAVES_BUY_QTY_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" Leaves Buy Qty "]'
    SORT_LEAVES_BUY_QTY_COLUMN_XPATH = '//*[text()=" Leaves Buy Qty "]/../following-sibling::div/igx-icon'
    FILTER_LEAVES_BUY_QTY_COLUMN_XPATH = '//*[text()=" Leaves Buy Qty "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

    LEAVES_SELL_QTY_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" Leaves Sell Qty "]'
    SORT_LEAVES_SELL_QTY_COLUMN_XPATH = '//*[text()=" Leaves Sell Qty "]/../following-sibling::div/igx-icon'
    FILTER_LEAVES_SELL_QTY_COLUMN_XPATH = '//*[text()=" Leaves Sell Qty "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

    CUMULATIVE_BUY_AMT_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" Cumulative Buy Amt "]'
    SORT_CUMULATIVE_BUY_AMT_COLUMN_XPATH = '//*[text()=" Cumulative Buy Amt "]/../following-sibling::div/igx-icon'
    FILTER_CUMULATIVE_BUY_AMT_COLUMN_XPATH = '//*[text()=" Cumulative Buy Amt "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

    CUMULATIVE_SELL_AMT_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" Cumulative Sell Amt "]'
    SORT_CUMULATIVE_SELL_AMT_COLUMN_XPATH = '//*[text()=" Cumulative Sell Amt "]/../following-sibling::div/igx-icon'
    FILTER_CUMULATIVE_SELL_AMT_COLUMN_XPATH = '//*[text()=" Cumulative Sell Amt "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'
    # endregion

    # region Hover order buttons
    BUY_HOVER_BUTTON_XPATH = '//*[@class="buy-hover ng-star-inserted"]'
    SELL_HOVER_BUTTON_XPATH = '//*[@class="sell-hover ng-star-inserted"]'
    MARKET_DEPTH_HOVER_BUTTON_XPATH = '//*[@data-rowindex="0"]//*[contains(@src, "list-outline")]'
    TIMES_AND_SALES_HOVER_BUTTON_XPATH = '//*[@data-rowindex="0"]//*[contains(@src, "watchlist")]'
    # endregion

    # region Orders fields
    ORDER_SYMBOL_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_InstrSymbol")]//span'
    ORDER_INSTR_TYPE_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_InstrType")]//span'
    ORDER_EXCHANGE_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_SecurityExchange")]//span'
    ORDER_TOTAL_QTY_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_positionQtys_TotalTransactionQty")]//span'
    ORDER_RESERVED_QTY_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_positionQtys_ReservedQty")]//span'
    ORDER_COVERED_QTY_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_positionQtys_CoveredQty")]//span'
    ORDER_LEAVES_BUY_QTY_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_positionQtys_LeavesBuyQty")]//span'
    ORDER_LEAVES_SELL_QTY_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_positionQtys_LeavesSellQty")]//span'
    ORDER_CUMULATIVE_BUY_AMT_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_positionAmounts_CumBuyAmt")]//span'
    ORDER_CUMULATIVE_SELL_AMT_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_positionAmounts_CumSellAmt")]//span'
    # endregion
