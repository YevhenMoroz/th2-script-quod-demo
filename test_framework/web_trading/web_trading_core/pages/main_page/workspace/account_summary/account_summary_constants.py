#region Account Summary
ACCOUNT_SUMMARY_BUTTON = '//*[@class="container"]//button[8]'
MAXIMIZE_BUTTON_XPATH = ''
MINIMIZE_BUTTON_XPATH = ''
CLOSE_BUTTON_XPATH = ''
COPY_PANAL_BUTTON_XPATH = '//*[@class="copy-workspace-icon"]/img'
FIELD_CHOOSER_XPATH = '//*[@name="btnColumnHiding"]'
ADVANCED_FILTERING_BUTTON_XPATH = '//*[@name="btnAdvancedFiltering"]'
CASH_ACCOUNT_COLUMN_XPATH = '//*[@id="igx-grid-0_-1_0_0"]//span[text()=" Cash Account "]'
SORT_ACCOUNT_COLUMN_XPATH = '//*[@data-sortindex="1"]'
FILTER_ACCOUNT_COLUMN_XPATH = '//*[@data-sortindex="1"]/following-sibling::div'
CURRENCY_COLUMN_XPATH = '//*[@id="igx-grid-0_-1_0_1"]//span[text()=" Currency "]'
SORT_CURRENCY_COLUMN_XPATH = '//*[@id="igx-grid-0_-1_0_1"]//igx-icon[contains(@class, "sort-icon")]'
FILTER_CURRENCY_COLUMN_XPATH = '//*[@id="igx-grid-0_-1_0_1"]//div[contains(@class, "igx-excel-filter__icon")]'
AVAILABLE_CASH_COLUMN_XPATH = '//*[@id="igx-grid-0_-1_0_2"]//span[text()=" Available Cash "]'
SORT_AVAILABLE_CASH_COLUMN_XPATH = '//*[@id="igx-grid-0_-1_0_2"]//igx-icon[contains(@class, "sort-icon")]'
FILTER_AVAILABLE_CASH_COLUMN_XPATH = '//*[@id="igx-grid-0_-1_0_2"]//div[contains(@class, "igx-excel-filter__icon")]'
TRANSACTION_HOLDING_AMOUNT_COLUMN_XPATH = '//*[@id="igx-grid-0_-1_0_3"]//span[text()=" Transaction Holding Amount "]'
SORT_TRANSACTION_HOLDING_AMOUNT_COLUMN_XPATH = '//*[@id="igx-grid-0_-1_0_3"]//igx-icon[contains(@class, "sort-icon")]'
FILTER_TRANSACTION_HOLDING_AMOUNT_COLUMN_XPATH = '//*[@id="igx-grid-0_-1_0_3"]//div[contains(@class, "igx-excel-filter__icon")]'
RESERVED_AMOUNT_COLUMN_XPATH = '//*[@id="igx-grid-0_-1_0_4"]//span[text()=" Reserved Amount "]'
SORT_RESERVED_AMOUNT_COLUMN_XPATH = '//*[@id="igx-grid-0_-1_0_4"]//igx-icon[contains(@class, "sort-icon")]'
FILTER_RESERVED_AMOUNT_COLUMN_XPATH = '//*[@id="igx-grid-0_-1_0_4"]//div[contains(@class, "igx-excel-filter__icon")]'
BUYING_POWER_COLUMN_XPATH = '//*[@id="igx-grid-0_-1_0_5"]//span[text()=" Buying Power "]'
SORT_BUYING_POWER_COLUMN_XPATH = '//*[@id="igx-grid-0_-1_0_5"]//igx-icon[contains(@class, "sort-icon")]'
FILTER_BUYING_POWER_COLUMN_XPATH = '//*[@id="igx-grid-0_-1_0_5"]//div[contains(@class, "igx-excel-filter__icon")]'
USER_CASH_ACCOUNT_COLUMN_XPATH = '//*[@id="igx-grid-2_0_0"]'
USER_CURRENCY_COLUMN_XPATH = '//*[@id="igx-grid-2_0_1"]'
USER_AVAILABLE_CASH_COLUMN_XPATH = '///*[@id="igx-grid-2_0_2"]'
USER_TRANSACTION_HOLDING_AMOUNT_COLUMN_XPATH = '//*[@id="igx-grid-2_0_3"]'
USER_RESERVED_AMOUNT_COLUMN_XPATH = '//*[@id="igx-grid-2_0_4"]'
USER_BUYING_POWER_COLUMN_XPATH = '//*[@id="igx-grid-2_0_5"]'
HORIZONTAL_SCROLL_XPATH = '//*[@class="igx-vhelper--horizontal ng-star-inserted"]/div[@class="igx-vhelper__placeholder-content"]'
#endregion

#region Field chooser
FILTER_COLUMNS_LIST_FIELD_XPATH = '//*[@id="igx-column-actions-0"]//input'
CASH_ACCOUNT_CHECKBOX_XPATH = '//*[@id="igx-checkbox-0-label"]'
HIDE_ALL_BUTTON_XPATH = '//*[text()="Hide All"]'
SHOW_ALL_BUTTON_XPATH = '//*[text()="Show All"]'
#endregion

#region Advanced filtering
DRAG_ADVANCED_FILTERING_WINDOW_XPATH = '//*[@class="igx-overlay__wrapper"]//header'
AND_GROUP_BUTTON_XPATH = '//*[@class="igx-advanced-filter__main"]/button[1]'
OR_GROUP_BUTTON_XPATH = '//*[@class="igx-advanced-filter__main"]/button[2]'
CLEAR_FILTER_BUTTON_XPATH = '//*[@class="igx-excel-filter__clear"]/button'
CANCEL_BUTTON_XPATH = '//*[@class="igx-excel-filter__cancel"]/button'
APPLY_BUTTON_XPATH = '//*[@class="igx-excel-filter__apply"]/button'
BACK_LINE_BUTTON_XPATH = '//*[contains(@class,"igx-filter-tree__line")]'
SELECT_COLUMN_FIELD_XPATH = '//*[contains(@class,"igx-filter-tree__inputs ng-star-inserted")]/igx-select[1]'
SELECT_COLUMN_CASH_ACCOUNT_XPATH = '//*[@id="igx-drop-down-item-54"]'
SELECT_FILTER_FIELD_XPATH = '//*[contains(@class,"igx-filter-tree__inputs ng-star-inserted")]/igx-select[2]'
SELECT_FILTER_CONTAINS_XPATH = '//*[@id="igx-drop-down-item-60"]'
VALUE_FIELD_XPATH = '//*[contains(@class,"igx-filter-tree__inputs ng-star-inserted")]/igx-input-group'
CHECK_AF_BUTTON_XPATH = '//*[contains(@class,"igx-filter-tree__inputs ng-star-inserted")]//button[1]'
CLOSE_AF_BUTTON_XPATH = '//*[contains(@class,"igx-filter-tree__inputs ng-star-inserted")]//button[2]'
CONDITION_BUTTON_XPATH = '//*[contains(@class,"igx-filter-tree__buttons ng-star-inserted")]//button[1]'
AND_BUTTON_XPATH = '//*[contains(@class,"igx-filter-tree__buttons ng-star-inserted")]//button[2]'
OR_BUTTON_XPATH = '//*[contains(@class,"igx-filter-tree__buttons ng-star-inserted")]//button[3]'
#endregion

#region Filter
PIN_BUTTON_XPATH = '//*[@aria-label="Pin column"]'
HIDE_BUTTON_XPATH = '//*[@aria-label="Hide column"]'
SEARCH_FIELD_XPATH = '//*[@class="igx-excel-filter__menu-main"]/igx-input-group'
SELECT_ALL_CHECKBOX_XPATH = '//*[@id="igx-checkbox-155-input"]'
CANCEL_XPATH = '//*[@class="igx-excel-filter__cancel"]'
APPLY_XPATH = '//*[@class="igx-excel-filter__apply"]'
#endregion