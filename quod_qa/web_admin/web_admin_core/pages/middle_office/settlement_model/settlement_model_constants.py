class SettlementModelConstants:
    SETTLEMENT_MODEL_PAGE_TITLE_XPATH = "//span[@class='entity-title left'][text()='Settlement Model ']"
    REFRESH_PAGE_BUTTON_XPATH = "//*[@data-name='refresh']"
    DOWNLOAD_PDF_BUTTON_XPATH = "//*[@nbtooltip = 'Download PDF']//*[@data-name='download']"
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

    # Main page
    MAIN_PAGE_DESCRIPTION_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[1]//input'
    MAIN_PAGE_DESCRIPTION_XPATH = '//*[@col-id="settlementModelDescription"]//span//span[4]'
    MAIN_PAGE_NAME_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[2]//input'
    MAIN_PAGE_NAME_XPATH = '//*[@col-id="settlementModelName"]//span//span[4]'
    MAIN_PAGE_COUNTRY_CODE_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[3]//input'
    MAIN_PAGE_COUNTRY_CODE_XPATH = '//*[@col-id="countryCode"]//span//span[4]'
    MAIN_PAGE_INSTR_TYPE_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[4]//input'
    MAIN_PAGE_INSTR_TYPE_XPATH = '//*[@col-id="instrType"]//span//span[4]'
    MAIN_PAGE_SETTL_LOCATION_BIC_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[5]//input'
    MAIN_PAGE_SETTL_LOCATION_BIC_XPATH = '//*[@col-id="settlLocationBIC"]//span//span[4]'

    # Values tab
    VALUES_TAB_NAME_XPATH = '//*[@formcontrolname="settlementModelName"]'
    VALUES_TAB_DESCRIPTION_XPATH = '//*[@formcontrolname="settlementModelDescription"]'
    VALUES_TAB_SETTL_LOCATION_XPATH = '//*[@id="settlLocation"]'
    VALUES_TAB_SETTL_LOCATION_BIC_XPATH = '//*[@formcontrolname="settlLocationBIC"]'
    VALUES_TAB_INSTR_TYPE_XPATH = '//*[@id="instrType"]'
    VALUES_TAB_COUNTRY_CODE_XPATH = '//*[@id="countryCodeEnumTable"]'
    VALUES_TAB_SETTL_LOCATION_MANAGE_BUTTON_XPATH = '//*[text()="Manage"]'

    # Dimensions tab
    DIMENSIONS_TAB_CLIENT_GROUP_XPATH = '//*[@id="clientGroup"]'
    DIMENSIONS_TAB_ACCOUNT_XPATH = '//*[@id="account"]'
    DIMENSIONS_TAB_CLIENT_XPATH = '//*[@id="accountGroup"]'
    DIMENSIONS_TAB_VENUE_XPATH = '//*[@id="venue"]'
    DIMENSIONS_TAB_INSTRUMENT_XPATH = '//*[@id="instrument"]'
    DIMENSIONS_TAB_INSTRUMENT_GROUP_XPATH = '//*[@id="instrumentGroup"]'