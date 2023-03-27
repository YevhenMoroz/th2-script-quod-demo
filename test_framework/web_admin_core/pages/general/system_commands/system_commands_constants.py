class SystemCommandsConstants:
    SYSTEM_COMMANDS_PAGE_TITLE_XPATH = "//span[text()='System Commands']"

    SYSTEM_COMMANDS_XPATH = '//*[@id="adminCommand"]'
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

    SEND_BUTTON_XPATH = '//button[normalize-space()="Save Changes"]'
    ERROR_XPATH = '//nb-toast[contains(@class, "danger")]'