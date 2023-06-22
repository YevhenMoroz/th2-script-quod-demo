class ClientListsConstants:
    CLIENT_LIST_PAGE_TITLE_XPATH = "//span[@class='entity-title left'][normalize-space()='Client Lists']"
    REFRESH_PAGE_BUTTON_XPATH = "//*[@data-name='refresh']"
    DOWNLOAD_PDF_BUTTON_XPATH = "//nb-icon[@icon='download-outline']//*[@data-name='download']"
    DOWNLOAD_CSV_BUTTON = '//nb-card-header//*[@data-name="download"]'
    SAVE_CHANGES_BUTTON_XPATH = "//*[normalize-space()='Save Changes']"
    CLEAR_CHANGES_BUTTON_XPATH = "//*[normalize-space()='Clear Changes']"
    CLOSE_WIZARD_XPATH = "//*[@data-name='close']"
    OK_BUTTON_XPATH = '//*[normalize-space()="Ok" or normalize-space()="OK"]'
    CANCEL_BUTTON_XPATH = '//*[normalize-space()="Cancel"]'
    NO_BUTTON_XPATH = '//button[normalize-space()="No"]'
    REVERT_CHANGES_XPATH = "//*[normalize-space()='Revert Changes']"
    MORE_ACTIONS_XPATH = "//*[@data-name = 'more-vertical']"
    EDIT_XPATH = "//*[@data-name = 'edit']"
    CLONE_XPATH = "//*[@data-name = 'copy']"
    DELETE_XPATH = "//*[@data-name = 'trash-2']"
    PIN_ROW_XPATH = "//*[@nbtooltip ='Click to Pin Row']"
    NEW_BUTTON_XPATH = '//*[normalize-space()="Client Lists"]//..//*[normalize-space()="New"]'
    USER_ICON_AT_RIGHT_CORNER = "//*[@class='control-item icon-btn context-menu-host']"
    LOGOUT_BUTTON_XPATH = "//*[text()='Logout']"
    GO_BACK_BUTTON_XPATH = "//*[text()='Go Back']"
    DISPLAYED_CLIENT_LIST_XPATH = '//*[text()="{}"]'

    # Main page

    MAIN_PAGE_NAME_FILTER_XPATH = '//*[@col-id="clientListName"]//following::input[@ref="eFloatingFilterText"][1]'
    MAIN_PAGE_NAME_XPATH = '//*[@col-id="clientListName"]//span//span[4]'
    MAIN_PAGE_DESCRIPTION_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[2]//input'
    MAIN_PAGE_DESCRIPTION_XPATH = '//*[@col-id="clientListDescription"]//span//span[4]'

    # Wizard

    WIZARD_CLIENT_LIST_NAME_XPATH = '//*[@formcontrolname="clientListName"]'
    WIZARD_CLIENT_LIST_DESCRIPTION_XPATH = '//*[@formcontrolname="clientListDescription"]'
    WIZARD_PLUS_BUTTON_XPATH = '//*[@data-name="plus"]'
    WIZARD_CHECKMARK_BUTTON_XPATH = '//*[@data-name="checkmark"]'
    WIZARD_CLOSE_BUTTON_XPATH = '//*[@data-name="close"]'
    WIZARD_EDIT_BUTTON_XPATH = '//*[@data-name="edit"]'
    WIZARD_DELETE_BUTTON_XPATH = '//*[@data-name="trash-2"]'
    WIZARD_CLIENT_FILTER_XPATH = '//app-inline-table//input[@placeholder="Filter"]'
    WIZARD_CLIENT_XPATH = '//*[@placeholder="Client *"]'
    WIZARD_DISPLAYED_CLIENTS_AT_TABLE = '//tbody//div//span'
    WIZARD_WARNING_MESSAGE_TEXT_XPATH = '//nb-alert//span'
    WIZARD_TITLE_CLIENT_LIST_XPATH = '//nb-card-header//span[text()="Client Lists"]'
    WIZARD_CLIENT_LINK_NAME_XPATH = '//*[normalize-space()="Client"]//..//a'






















