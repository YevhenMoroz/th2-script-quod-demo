class AccountSummaryConstants:
    # region Account Summary
    MAXIMIZE_BUTTON_CSS = 'return document.querySelector("*.doc-manager-geojit-window").querySelector("*.dockManagerContent.ng-star-inserted").querySelector("igc-dockmanager").shadowRoot.querySelector("igc-pane-header-component").shadowRoot.querySelector("*[name=\'maximize\']")'
    MINIMIZE_BUTTON_CSS = 'return document.querySelector("*[slot=\'tab_default_123456789\']").querySelector("igc-dockmanager").shadowRoot.querySelector("igc-pane-header-component").shadowRoot.querySelector("*[name=\'maximize\']")'
    CLOSE_BUTTON_CSS = 'return document.querySelector("*[slot=\'tab_default_123456789\']").querySelector("igc-dockmanager").shadowRoot.querySelector("igc-pane-header-component").shadowRoot.querySelector("*[title=\'Close\']")'
    COPY_PANEL_BUTTON_XPATH = '//*[@class="copy-workspace-icon"]/img'
    FIELD_CHOOSER_XPATH = '//*[@name="btnColumnHiding"]'
    ADVANCED_FILTERING_BUTTON_XPATH = '//*[@name="btnAdvancedFiltering"]'
    HORIZONTAL_SCROLL_XPATH = '//*[@class="igx-vhelper--horizontal ng-star-inserted"]/div[@class="igx-vhelper__placeholder-content"]'
    # endregion

    # region Field chooser
    SEARCH_FILTER_COLUMNS_LIST_FIELD_XPATH = '//*[@class="igx-column-actions__header"]//input'
    COLUMNS_LIST_CHECKBOX_XPATH = '//*[@class="igx-overlay__content"]//*[text()="{}"]'
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

    # region Filter
    PIN_BUTTON_XPATH = '//*[@aria-label="Pin column"]'
    HIDE_BUTTON_XPATH = '//*[@aria-label="Hide column"]'
    SEARCH_FIELD_XPATH = '//*[@placeholder="Search"]'
    SELECT_ALL_CHECKBOX_XPATH = '//*[text()=" Select All "]'
    CANCEL_XPATH = '//*[@class="igx-excel-filter__cancel"]'
    APPLY_XPATH = '//*[@class="igx-excel-filter__apply"]'
    # endregion

    # region Columns
    CASH_ACCOUNT_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" Cash Account "]'
    SORT_ACCOUNT_COLUMN_XPATH = '//*[text()=" Cash Account "]/../following-sibling::div/igx-icon'
    FILTER_ACCOUNT_COLUMN_XPATH = '//*[text()=" Cash Account "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

    CURRENCY_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" Currency "]'
    SORT_CURRENCY_COLUMN_XPATH = '//*[text()=" Currency "]/../following-sibling::div/igx-icon'
    FILTER_CURRENCY_COLUMN_XPATH = '//*[text()=" Currency "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

    AVAILABLE_CASH_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" Available Cash "]'
    SORT_AVAILABLE_CASH_COLUMN_XPATH = '//*[text()=" Available Cash "]/../following-sibling::div/igx-icon'
    FILTER_AVAILABLE_CASH_COLUMN_XPATH = '//*[text()=" Available Cash "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

    TRANSACTION_HOLDING_AMOUNT_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" Transaction Holding Amount "]'
    SORT_TRANSACTION_HOLDING_AMOUNT_COLUMN_XPATH = '//*[text()=" Transaction Holding Amount "]/../following-sibling::div/igx-icon'
    FILTER_TRANSACTION_HOLDING_AMOUNT_COLUMN_XPATH = '//*[text()=" Transaction Holding Amount "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

    RESERVED_AMOUNT_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" Reserved Amount "]'
    SORT_RESERVED_AMOUNT_COLUMN_XPATH = '//*[text()=" Reserved Amount "]/../following-sibling::div/igx-icon'
    FILTER_RESERVED_AMOUNT_COLUMN_XPATH = '//*[text()=" Reserved Amount "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'

    BUYING_POWER_COLUMN_XPATH = '//*[@role="columnheader"]//*[text()=" Buying Power "]'
    SORT_BUYING_POWER_COLUMN_XPATH = '//*[text()=" Buying Power "]/../following-sibling::div/igx-icon'
    FILTER_BUYING_POWER_COLUMN_XPATH = '//*[text()=" Buying Power "]/../following-sibling::div/*[contains(@class, "igx-excel-filter__icon")]'
    # endregion

    # region Orders fields
    USER_CASH_ACCOUNT_COLUMN_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_cashAccount")]//span'
    USER_CURRENCY_COLUMN_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_currency")]//span'
    USER_CURRENCY_CASH_BALANCE_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_cashAccountBalance")]//span'
    USER_AVAILABLE_CASH_COLUMN_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_availableCash")]//span'
    USER_TRANSACTION_HOLDING_AMOUNT_COLUMN_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_holdingAmount")]//span'
    USER_RESERVED_AMOUNT_COLUMN_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_reservedAmount")]//span'
    USER_BUYING_POWER_COLUMN_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_buyingPower")]//span'
    USER_SECURITY_ACCOUNT_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_Account")]//span'
    USER_TOTAL_SECURITY_VALUE_XPATH = '//*[@data-rowindex="0"]//*[contains(@aria-describedby,"_positionAmounts_IncrementalMarkToMarketAmount")]//span'
    # endregion
