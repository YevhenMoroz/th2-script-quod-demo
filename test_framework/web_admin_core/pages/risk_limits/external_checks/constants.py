class ExternalChecksConstants:
    EXTERNAL_CHECKS_PAGE_TITLE_XPATH = "//span[@class='entity-title left'][normalize-space()='External Checks']"

    REFRESH_PAGE_BUTTON_XPATH = "//*[@data-name='refresh']"
    DOWNLOAD_PDF_BUTTON_XPATH = "//*[@data-name='download']"
    SAVE_CHANGES_BUTTON_XPATH = "//*[normalize-space()='Save Changes']"
    CLEAR_CHANGES_BUTTON_XPATH = "//*[normalize-space()='Clear Changes']"
    CLOSE_WIZARD_XPATH = "//*[@data-name='close']"
    OK_BUTTON_XPATH = '//*[normalize-space()="Ok"]'
    CANCEL_BUTTON_XPATH = '//*[normalize-space()="Cancel"]'
    REVERT_CHANGES_XPATH = "//*[text()='Revert Changes']"
    MORE_ACTIONS_XPATH = "//*[@data-name = 'more-vertical']"
    EDIT_XPATH = "//*[@data-name = 'edit']"
    CLONE_XPATH = "//*[@data-name = 'copy']"
    DELETE_XPATH = "//*[@data-name = 'trash-2']"
    PIN_ROW_XPATH = "//*[@nbtooltip ='Click to Pin Row']"
    NEW_BUTTON_XPATH = '//*[normalize-space()="New"]'
    USER_ICON_AT_RIGHT_CORNER = "//*[@class='control-item icon-btn context-menu-host']"
    LOGOUT_BUTTON_XPATH = "//*[text()='Logout']"
    GO_BACK_BUTTON_XPATH = "//*[text()='Go Back']"

    # main page

    MAIN_PAGE_NAME_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[1]//input'
    MAIN_PAGE_CLIENT_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[2]//input'
    MAIN_PAGE_INSTR_TYPE_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[3]//input'
    MAIN_PAGE_VENUE_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[4]//input'
    MAIN_PAGE_CLIENT_GROUP_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[5]//input'
    MAIN_PAGE_NAME_XPATH = '//*[@col-id="externalOrderValidationName"]//span[@ref="eValue"]'
    MAIN_PAGE_CLIENT_XPATH = '//*[@col-id="accountGroupID"]//span[@ref="eValue"]'
    MAIN_PAGE_INSTR_TYPE_XPATH = '//*[@col-id="instrType"]//span[@ref="eValue"]'
    MAIN_PAGE_VENUE_XPATH = '//*[@col-id="venue.venueID"]//span[@ref="eValue"]'
    MAIN_PAGE_CLIENT_GROUP_XPATH = '//*[@col-id="clientGroup.clientGroupName"]//span[@ref="eValue"]'




    # Values tab

    VALUES_TAB_NAME_XPATH = '//*[@formcontrolname="externalOrderValidationName"]'

    # Dimensions tab
    DIMENSIONS_VENUE_XPATH = '//*[@id="venue"]'
    DIMENSIONS_CLIENT_XPATH = '//*[@id="accountGroup"]'
    DIMENSIONS_INSTR_TYPE_XPATH = '//*[@id="instrType"]'
    DIMENSIONS_CLIENT_GROUP_XPATH = '//*[@id="clientGroup"]'
