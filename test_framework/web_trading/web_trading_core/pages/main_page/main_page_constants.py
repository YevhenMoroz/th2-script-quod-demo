class MainPageConstants:
    # region Navbar
    PLUS_BUTTON_XPATH = '//span[text()="B"]/../preceding-sibling::button'
    BUY_BUTTON_XPATH = '//span[text()="B"]'
    SELL_BUTTON_XPATH = '//span[text()="S"]'
    WATCH_LIST_BUTTON_XPATH = '//*[contains(@src, "dashboard/watchlist")]'
    ORDER_BOOK_BUTTON_XPATH = '//*[contains(@src, "dashboard/orderbook")]'
    TRADES_BUTTON_XPATH = '//*[contains(@src, "dashboard/tradebook")]'
    POSITION_BUTTON_XPATH = '//*[contains(@src, "dashboard/positions")]'
    ACCOUNT_SUMMARY_BUTTON_XPATH = '//*[contains(@src, "dashboard/pie-chart-outline")]'
    SYMBOL_DETAILS_BUTTON_XPATH = '//*[contains(@src, "dashboard/grid-outline")]'
    NOTIFICATION_BUTTON_XPATH = '//*[contains(@src, "dashboard/bell-outline")]'
    USER_NAME_XPATH = '//*[@class="user-name-geojit-landing"]'
    MENU_BUTTON_XPATH = '//*[@class="button-icons-more"]'
    # endregion

    # region Tabs
    DASHBOARD_CSS = '*[aria-label="Dashboard"]'
    DASHBOARD_CLOSE_BUTTON_CSS = '*[title="Close"]'
    NEW_WORKSPACE_CSS = '*[aria-label="New Workspace"]'
    NEW_WORKSPACE_CLOSE_BUTTON_CSS = 'return document.querySelector("igc-dockmanager").shadowRoot.querySelector("*[aria-controls=\'tab-panel-2\']").shadowRoot.querySelector("*[title=\'Close\']")'
    # endregion