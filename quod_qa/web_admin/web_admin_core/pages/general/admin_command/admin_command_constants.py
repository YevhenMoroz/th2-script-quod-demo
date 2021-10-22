class AdminCommandConstants:
    ADMIN_COMMAND_PAGE_TITLE_XPATH = "//span[text()='Admin Command']"

    ADMIN_COMMAND_XPATH = '//*[@id="adminCommand"]'
    COMPONENT_ID_XPATH = '//*[@formcontrolname="componentID"]'

    PLUS_BUTTON_XPATH = '//*[@class="nb-plus"]'
    CHECKMARK_BUTTON_XPATH = '//*[@class="nb-checkmark"]'
    CLOSE_BUTTON_XPATH = '//*[@class="nb-close"]'
    EDIT_BUTTON_XPATH = '//*[@class="nb-edit"]'
    DELETE_BUTTON_XPATH = '//*[@class="nb-trash"]'

    NAME_FILTER_XPATH = '//*[@class="adminCommandParamName ng2-smart-th ng-star-inserted"]//input'
    NAME_XPATH = '//*[@placeholder="Name *"]'
    VALUE_FILTER_XPATH = '//*[@class="adminCommandParamValue ng2-smart-th ng-star-inserted"]//input'
    VALUE_XPATH = '//*[@placeholder="Value *"]'

    SEND_BUTTON_XPATH = '//*[text()="Send"]'
    ERROR_XPATH = '//*[text()="Request failed, verify the input data. If the problem persists, please contact the administrator for full details"]'