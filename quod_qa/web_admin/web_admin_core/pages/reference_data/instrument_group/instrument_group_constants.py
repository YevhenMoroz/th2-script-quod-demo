class InstrumentGroupConstants:
    INSTRUMENT_GROUP_PAGE_TITLE_XPATH = "//span[@class='entity-title left'][text()='Instrument Group ']"
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

    # Main page
    MAIN_PAGE_INSTRUMENT_GROUP_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[1]//input'
    MAIN_PAGE_INSTRUMENT_GROUP_XPATH = '//*[@col-id="instrumentGroupName"]//span//span[4]'
    MAIN_PAGE_DESCRIPTION_FILTER_XPATH = '//*[@class="ag-header-container"]/div[2]/div[2]//input'
    MAIN_PAGE_DESCRIPTION_XPATH = '//*[@col-id="instrGroupDescription"]//span//span[4]'

    # Wizard
    WIZARD_INSTRUMENT_GROUP_NAME_XPATH = '//*[@formcontrolname="instrumentGroupName"]'
    WIZARD_INSTR_GROUP_DESCRIPTION_XPATH = '//*[@formcontrolname="instrGroupDescription"]'

    WIZARD_PLUS_BUTTON_XPATH = '//*[@class="nb-plus"]'
    WIZARD_CHECKMARK_XPATH = '//*[@class="nb-checkmark"]'
    WIZARD_CLOSE_XPATH = '//*[@class="nb-close"]'
    WIZARD_EDIT_XPATH = '//*[@class="nb-edit"]'
    WIZARD_DELETE_XPATH = '//*[@class="nb-trash"]'
    WIZARD_INSTRUMENT_FILTER_XPATH = '//*[@class="instrument ng2-smart-th ng-star-inserted"]//input'
    WIZARD_INSTRUMENT_XPATH = '//*[@placeholder="Instrument *"]'