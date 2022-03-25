class WashBookConstants:
    WASHBOOK_PAGE_TITLE_XPATH = "//span[@class='entity-title left'][text()='Wash Books ']"

    # region ~~~MAIN PAGE~~~
    NEW_BUTTON_XPATH = '//*[text()="New"]'
    EDIT_BUTTON_XPATH = '//*[@data-name="edit"]'
    ENABLE_DISABLE_BUTTON_XPATH = "//div[contains(@class, 'toggle')]"
    MORE_ACTIONS_XPATH = "//nb-icon[@title='More Actions']"
    EDIT_AT_MORE_ACTIONS_XPATH = '//*[@data-name="edit"]'
    CLONE_AT_MORE_ACTIONS_XPATH = '//*[@data-name="copy"]'
    DOWNLOAD_PDF_AT_MORE_ACTIONS_XPATH = "//nb-icon[@icon='download-outline']//*[@data-name='download']"
    PIN_TO_ROW_AT_MORE_ACTIONS_XPATH = '//*[@nbtooltip="Click to Pin Row"]'
    OK_BUTTON_XPATH = "//*[text()='Ok']"

    # -FIELDS WITH VALUES AT MAIN PAGE-
    ID_AT_MAIN_PAGE_XPATH = '//*[@class="ag-center-cols-container"]//div//div[1]//*[@class="ag-group-value"]'
    DESCRIPTION_AT_MAIN_PAGE_XPATH = '//*[@class="ag-center-cols-container"]//div//div[2]//*[@class="ag-group-value"]'
    CLIENT_AT_MAIN_PAGE_XPATH = '//*[@class="ag-center-cols-container"]//div//div[3]//*[@class="ag-group-value"]'
    EXT_ID_CLIENT_AT_MAIN_PAGE_XPATH = '//*[@class="ag-center-cols-container"]//div//div[4]//*[@class="ag-group-value"]'
    CLIENT_ID_SOURCE_AT_MAIN_PAGE_XPATH = '//*[@class="ag-center-cols-container"]//div//div[5]//*[@class="ag-group-value"]'
    CLEARING_ACCOUNT_TYPE_AT_MAIN_PAGE_XPATH = '//*[@class="ag-center-cols-container"]//div//div[6]//*[@class="ag-group-value"]'
    COUNTERPART_AT_MAIN_PAGE_XPATH = '//*[@class="ag-center-cols-container"]//div//div[7]//*[@class="ag-group-value"]'
    ENABLED_AT_MAIN_PAGE_XPATH = '//*[@class="custom-checkbox checked"]'

    # -FILTERS AT MAIN PAGE-
    ID_FILTER_AT_MAIN_PAGE_XPATH = "//*[@class='ag-header-container']/div[2]/div[1]//input"
    DESCRIPTION_FILTER_AT_MAIN_PAGE_XPATH = "//*[@class='ag-header-container']/div[2]/div[2]//input"
    CLIENT_FILTER_AT_MAIN_PAGE_XPATH = "//*[@class='ag-header-container']/div[2]/div[3]//input"
    EXT_ID_CLIENT_FILTER_AT_MAIN_PAGE_XPATH = "//*[@class='ag-header-container']/div[2]/div[4]//input"
    CLIENT_ID_SOURCE_FILTER_AT_MAIN_PAGE_XPATH = "//*[@class='ag-header-container']/div[2]/div[5]//input"
    CLEARING_ACCOUNT_TYPE_FILTER_AT_MAIN_PAGE_XPATH = "//*[@class='ag-header-container']/div[2]/div[6]//input"
    COUNTERPART_FILTER_AT_MAIN_PAGE_XPATH = "//*[@class='ag-header-container']/div[2]/div[7]//input"
    ENABLED_FILTER_AT_MAIN_PAGE_XPATH = "//select[@class='boolean-filter ng-untouched ng-pristine ng-valid']"
    ENABLED_FILTER_LIST_AT_MAIN_PAGE_XPATH = "//*[text()='{}']"

    # ~~~EDIT SUB WIZARD~~~
    SINCE_INCEPTION_PL = '//*[text()="Since Inception PL"]/preceding-sibling::input'
    MONTH_PL = '//*[text()="Month PL"]/preceding-sibling::input'
    WEEK_PL = '//*[text()="Week PL"]/preceding-sibling::input'
    QUARTER_PL = '//*[text()="Quarter PL"]/preceding-sibling::input'
    YEAR_PL = '//*[text()="Year PL"]/preceding-sibling::input'
    SAVE_CHANGES_AT_EDIT_SUB_WIZARD = '//*[text()="Save Changes"]'
    REVERT_CHANGES_AT_EDIT_SUB_WIZARD = '//*[text()="Revert Changes"]'
    CLOSE_AT_EDIT_SUB_WIZARD = '//*[@nbtooltip="Close"]'
    # endregion

    # region ~~~WIZARD~~~
    SAVE_CHANGES_AT_WIZARD = '//*[text()="Save Changes"]'
    CLEAR_CHANGES_AT_WIZARD = '//*[text()="Clear Changes"]'
    # -VALUES-
    ID_AT_VALUES_TAB = '//*[text()="ID *"]/preceding-sibling::input'
    EXT_ID_CLIENT_AT_VALUES_TAB = '//*[text()="Ext ID Client *"]/preceding-sibling::input'
    CLIENT_AT_VALUES_TAB = '//*[text()="Client"]/preceding-sibling::input'
    DESCRIPTION_AT_VALUES_TAB = '//*[text()="Description"]/preceding-sibling::input'
    CLEARING_ACCOUNT_TYPE_AT_VALUES_TAB = '//*[text()="Clearing Account Type"]/preceding-sibling::input'
    CLIENT_ID_SOURCE_AT_VALUES_TAB = '//*[text()="Client ID Source *"]/preceding-sibling::input'
    COUNTERPART_AT_VALUES_TAB = '//*[text()="Counterpart"]/preceding-sibling::input'
    MANAGE_COUNTERPART_AT_VALUES_TAB = '//*[text()="Manage"]'

    # -DIMENSIONS TAB-
    PLUS_AT_DIMENSIONS_TAB = '//*[@class="wash-book-security-account-detail-settings"]//nb-accordion-item[2]//*[@class="nb-plus"]'
    CHECKMARK_AT_DIMENSIONS_TAB = '//*[@class="wash-book-security-account-detail-settings"]//nb-accordion-item[2]//*[@class="nb-checkmark"]'
    CANCEL_AT_DIMENSIONS_TAB = '//*[@class="wash-book-security-account-detail-settings"]//nb-accordion-item[2]//*[@class="nb-close"]'
    EDIT_AT_DIMENSIONS_TAB = '//*[@class="wash-book-security-account-detail-settings"]//nb-accordion-item[2]//*[@class="nb-edit"]'
    DELETE_AT_DIMENSIONS_TAB = '//*[@class="wash-book-security-account-detail-settings"]//nb-accordion-item[2]//*[@class="nb-trash"]'
    # VALUES
    VENUE_ACCOUNT_AT_DIMENSIONS_TAB = "//*[@placeholder='Venue Account *']"
    VENUE_AT_AT_DIMENSIONS_TAB = "//*[@placeholder='Venue *']"
    ACCOUNT_ID_SOURCE_AT_DIMENSIONS_TAB = "//*[@placeholder='Account ID Source *']"
    DEFAULT_ROUTE_AT_DIMENSIONS_TAB = "//*[@placeholder='Default Route']"
    # FILTERS
    VENUE_ACCOUNT_FILTER_AT_DIMENSIONS_TAB = "//*[@class='ng2-smart-th venueAccountName ng-star-inserted']//*[@placeholder='Filter']"
    VENUE_FILTER_AT_DIMENSIONS_TAB = "//*[@class='ng2-smart-th venue ng-star-inserted']//*[@placeholder='Filter']"
    ACCOUNT_ID_SOURCE_FILTER_AT_DIMENSIONS_TAB = "//*[@class='ng2-smart-th venueAccountIDSource ng-star-inserted']//*[@placeholder='Filter']"
    DEFAULT_ROUTE_FILTER_AT_DIMENSIONS_TAB = "defaultRoute ng2-smart-th ng-star-inserted"

    # -ROUTES TAB-
    DEFAULT_ROUTE_AT_ROUTES_TAB = '//*[text()="Default Route"]/preceding-sibling::input'
    PLUS_AT_ROUTES_TAB = '//*[@class="wash-book-security-account-detail-settings"]//nb-accordion-item[3]//*[@class="nb-plus"]'
    CHECKMARK_AT_ROUTES_TAB = '//*[@class="wash-book-security-account-detail-settings"]//nb-accordion-item[3]//*[@class="nb-checkmark"]'
    CANCEL_AT_ROUTES_TAB = '//*[@class="wash-book-security-account-detail-settings"]//nb-accordion-item[3]//*[@class="nb-close"]'
    EDIT_AT_ROUTES_TAB = '//*[@class="wash-book-security-account-detail-settings"]//nb-accordion-item[3]//*[@class="nb-edit"]'
    DELETE_AT_ROUTES_TAB = '//*[@class="wash-book-security-account-detail-settings"]//nb-accordion-item[3]//*[@class="nb-trash"]'

    # VALUES
    ROUTE_ACCOUNT_NAME_AT_ROUTES_TAB = "//*[@placeholder='Route Account Name *']"
    ROUTE_AT_ROUTES_TAB = "//*[@placeholder='Route *']"
    # FILTERS
    ROUTE_ACCOUNT_NAME_FILTER_AT_ROUTES_TAB = "//*[@class='ng2-smart-th routeSecActName ng-star-inserted']//*[@placeholder='Filter']"
    ROUTE_FILTER_AT_ROUTES_TAB = "//*[@class='ng2-smart-th route ng-star-inserted']//*[@placeholder='Filter']"
    # endregion
