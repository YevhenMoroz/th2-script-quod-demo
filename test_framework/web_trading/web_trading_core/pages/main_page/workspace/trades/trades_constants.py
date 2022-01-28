#region Trades
MAXIMIZE_BUTTON_XPATH = ''
MINIMIZE_BUTTON_XPATH = ''
CLOSE_BUTTON_XPATH = ''
COPY_PANAL_BUTTON_XPATH = '//*[@class="copy-workspace-icon"]/img'
FIELD_CHOOSER_XPATH = '//*[@name="btnColumnHiding"]'
ADVANCED_FILTERING_BUTTON_XPATH = '//*[@name="btnAdvancedFiltering"]'
HORIZONTAL_SCROLL_XPATH = '//*[@class="igx-vhelper--horizontal ng-star-inserted"]/div[@class="igx-vhelper__placeholder-content"]'
#endregion

#region Field chooser
FILTER_COLUMNS_LIST_FIELD_XPATH = '//*[@class="igx-column-actions__header"]//input'
SYMBOL_CHECKBOX_XPATH = '//*[@class="igx-overlay__content"]//*[text()=" Symbol "]'
HIDE_ALL_BUTTON_XPATH = '//*[text()="Hide All"]'
SHOW_ALL_BUTTON_XPATH = '//*[text()="Show All"]'
#endregion

#region Advanced filtering
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
#endregion

#region Columns Trades
SYMBOL_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" Symbol "]'
SORT_SYMBOL_COLUMN_XPATH = '//*[text()=" Symbol "]/../following-sibling::div/igx-icon'
FILTER_SYMBOL_COLUMN_XPATH = '//*[text()=" Symbol "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

INSTR_TYPE_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" InstrType "]'
SORT_INSTR_TYPE_COLUMN_XPATH = '//*[text()=" InstrType "]/../following-sibling::div/igx-icon'
FILTER_INSTR_TYPE_COLUMN_XPATH = '//*[text()=" InstrType "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

ORDER_ID_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" Order ID "]'
SORT_ORDER_ID_COLUMN_XPATH = '//*[text()=" Order ID "]/../following-sibling::div/igx-icon'
FILTER_ORDER_ID_COLUMN_XPATH = '//*[text()=" Order ID "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

EXCEL_ID_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" ExceID "]'
SORT_EXCEL_ID_COLUMN_XPATH = '//*[text()=" ExceID "]/../following-sibling::div/igx-icon'
FILTER_EXCEL_ID_COLUMN_XPATH = '//*[text()=" ExceID "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

SIDE_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" Side "]'
SORT_SIDE_COLUMN_XPATH = '//*[text()=" Side "]/../following-sibling::div/igx-icon'
FILTER_SIDE_COLUMN_XPATH = '//*[text()=" Side "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

QTY_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" Qty "]'
SORT_QTY_COLUMN_XPATH = '//*[text()=" Qty "]/../following-sibling::div/igx-icon'
FILTER_QTY_COLUMN_XPATH = '//*[text()=" Qty "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

EXECUTION_PRICE_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" Execution Price "]'
SORT_EXECUTION_PRICE_COLUMN_XPATH = '//*[text()=" Execution Price "]/../following-sibling::div/igx-icon'
FILTER_EXECUTION_PRICE_COLUMN_XPATH = '//*[text()=" Execution Price "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

EXECUTION_TYPE_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" Execution Type "]'
SORT_EXECUTION_TYPE_COLUMN_XPATH = '//*[text()=" Execution Type "]/../following-sibling::div/igx-icon'
FILTER_EXECUTION_TYPE_COLUMN_XPATH = '//*[text()=" Execution Type "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

AVG_PRICE_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" Avg Price "]'
SORT_AVG_PRICE_COLUMN_XPATH = '//*[text()=" Avg Price "]/../following-sibling::div/igx-icon'
FILTER_AVG_PRICE_COLUMN_XPATH = '//*[text()=" Avg Price "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

CUMULATIVE_QTY_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" Cumulative Qty "]'
SORT_CUMULATIVE_QTY_COLUMN_XPATH = '//*[text()=" Cumulative Qty "]/../following-sibling::div/igx-icon'
FILTER_CUMULATIVE_QTY_COLUMN_XPATH = '//*[text()=" Cumulative Qty "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

LEAVES_QTY_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" Leaves Qty "]'
SORT_LEAVES_QTY_COLUMN_XPATH = '//*[text()=" Leaves Qty "]/../following-sibling::div/igx-icon'
FILTER_LEAVES_QTY_COLUMN_XPATH = '//*[text()=" Leaves Qty "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

ORDER_STATUS_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" Order Status "]'
SORT_ORDER_STATUS_COLUMN_XPATH = '//*[text()=" Order Status "]/../following-sibling::div/igx-icon'
FILTER_ORDER_STATUS_COLUMN_XPATH = '//*[text()=" Order Status "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

TRANSACTION_TIME_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" Transaction Time "]'
SORT_TRANSACTION_TIME_COLUMN_XPATH = '//*[text()=" Transaction Time "]/../following-sibling::div/igx-icon'
FILTER_TRANSACTION_TIME_COLUMN_XPATH = '//*[text()=" Transaction Time "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'
#endregion

#region Hover order buttons
BUY_HOVER_BUTTON_XPATH = '//*[@class="buy-hover ng-star-inserted"]'
SELL_HOVER_BUTTON_XPATH = '//*[@class="sell-hover ng-star-inserted"]'
MARKET_DEPTH_HOVER_BUTTON_XPATH = '//*[@data-rowindex="0"]//*[contains(@src, "list-outline")]'
TIMES_AND_SALES_HOVER_BUTTON_XPATH = '//*[@data-rowindex="0"]//*[contains(@src, "watchlist")]'
#endregion

#region Orders fields
ORDER_SYMBOL_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_InstrSymbol")]'
ORDER_INSTR_TYPE_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_InstrType")]'
ORDER_ORDER_ID_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_OrdID")]'
ORDER_EXCEL_ID_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_ExecID")]'
ORDER_SIDE_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_Side")]'
ORDER_QTY_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_ExecQty")]'
ORDER_EXECUTION_PRICE_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_ExecPrice")]'
ORDER_EXECUTION_TYPE_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_ExecType")]'
ORDER_AVG_PRICE_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_AvgPrice")]'
ORDER_CUMULATIVE_QTY_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_CumQty")]'
ORDER_LEAVES_QTY_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_LeavesQty")]'
ORDER_ORDER_STATUS_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_OrderStatus")]'
ORDER_TRANSACTION_TIME_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_TransactTime")]'
#endregion