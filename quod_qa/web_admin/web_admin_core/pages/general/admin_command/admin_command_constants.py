class AdminCommandConstants:
    ADMIN_COMMAND_PAGE_TITLE_XPATH = "//span[text()='Admin Command']"

    ADMIN_COMMAND_XPATH = '//*[@id="adminCommand"]'
    COMPONENT_ID_XPATH = '//*[@formcontrolname="componentID"]'

    PLUS_BUTTON_XPATH = '//*[@data-name="plus"]'
    CHECKMARK_BUTTON_XPATH = '//*[@data-name="checkmark"]'
    CLOSE_BUTTON_XPATH = '//*[@data-name="close"]'
    EDIT_BUTTON_XPATH = '//*[@data-name="edit"]'
    DELETE_BUTTON_XPATH = '//*[@data-name="trash-2"]'

    NAME_FILTER_XPATH = '//*[@class="adminCommandParamName ng2-smart-th ng-star-inserted"]//input'
    NAME_XPATH = '//*[@placeholder="Name *"]'
    VALUE_FILTER_XPATH = '//*[@class="adminCommandParamValue ng2-smart-th ng-star-inserted"]//input'
    VALUE_XPATH = '//*[@placeholder="Value *"]'

    SEND_BUTTON_XPATH = '//*[text()="Send"]'
    ERROR_XPATH = '//*[text()="Request failed, verify the input data. If the problem persists, please contact the administrator for full details"]'