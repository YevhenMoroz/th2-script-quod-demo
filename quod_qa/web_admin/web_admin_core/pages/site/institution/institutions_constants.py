class InstitutionsConstants:
    INSTITUTIONS_PAGE_TITLE_XPATH = "//span[@class= 'entity-title left']//*[text()='Institutions']"

    REFRESH_PAGE_BUTTON_XPATH = "//*[@data-name='refresh']"
    DOWNLOAD_PDF_BUTTON_XPATH = "//*[@data-name='download']"
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
    ENABLE_DISABLE_TOGGLE_BUTTON_XPATH = "//div[contains(@class, 'toggle')]"
    ENABLE_DISABLE_TOGGLE_INPUT_XPATH = "//*[contains(@role, 'switch')]"
    SUCH_RECORD_ALREADY_EXISTS_MASSEGE_XPATH = "//*[text()='Such a record already exists']"


    # Main page

    MAIN_PAGE_INSTITUTION_NAME_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[1]//input'
    MAIN_PAGE_LEI_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[2]//input'
    MAIN_PAGE_CTM_BIC_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[3]//input'
    MAIN_PAGE_COUNTERPART_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[4]//input'
    MAIN_PAGE_ENABLED_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[5]//select'

    MAIN_PAGE_INSTITUTION_NAME_XPATH = '//*[@col-id="institutionName"]//span/span[4]'
    MAIN_PAGE_LEI_XPATH = '//*[@col-id="institutionLEI"]//span/span[4]'
    MAIN_PAGE_CTM_BIC_XPATH = '//*[@col-id="BIC"]//span/span[4]'
    MAIN_PAGE_COUNTERPART_XPATH = '//*[@col-id="counterpart.counterpartName"]//span/span[4]'
    MAIN_PAGE_ENABLED_XPATH = '//*[@col-id="alive"]//span'

    # Values tab
    VALUES_TAB_INSTITUTION_NAME = '//*[@formcontrolname="institutionName"]'
    VALUES_TAB_LEI_NAME = '//*[@formcontrolname="institutionLEI"]'
    VALUES_TAB_CTM_BIC_NAME = '//*[@formcontrolname="BIC"]'
    VALUES_TAB_COUNTERPART_NAME = '//*[@id="counterpart"]'
    VALUES_TAB_MANAGE_COUNTERPART_BUTTON_XPATH = '//*[@class="col-sm"]//button'

    # Assignments tab
    ASSIGNMENTS_TAB_ZONES_LINK_XPATH = '//a[text()=" {} "]'
    ASSIGNMENTS_TAB_USERS_LINK_XPATH = '//a[text()=" {} "]'
