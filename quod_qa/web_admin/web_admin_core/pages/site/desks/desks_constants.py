class DesksConstants:
    DESKS_PAGE_TITLE_XPATH = "//*[@class='menu-title ng-tns-c76-90'][text()='Desks']"
    NEW_BUTTON_XPATH = '//button[text()="New"]'
    REFRESH_BUTTON_XPATH = '//*[@data-name="refresh"]'
    MORE_ACTIONS_XPATH = '//*[@data-name="more-vertical"]'
    EDIT_AT_MORE_ACTIONS_XPATH = '//*[@data-name="edit"]'
    CLONE_AT_MORE_ACTIONS_XPATH = '//*[@data-name="copy"]'
    DELETE_AT_MORE_ACTIONS_XPATH = '//*[@data-name="trash-2"]'
    CANCEL_BUTTON_XPATH = '//*[text()="Cancel"]'
    OK_BUTTON_XPATH = '//*[text()="Ok"]'

    #Filters at main page
    NAME_FILTER_AT_MAIN_PAGE_XPATH = "//*[@class='ag-header-container']//div[2]//div[1]//div/input"
    MODE_FILTER_AT_MAIN_PAGE_XPATH = "//*[@class='ag-header-container']//div[2]//div[2]//div/input"
    LOCATION_FILTER_AT_MAIN_PAGE_XPATH = "//*[@class='ag-header-container']//div[2]//div[3]//div/input"

    #Wizard
    NAME_AT_DESCRIPTION_TAB_XPATH = '//*[text()="Name *"]/preceding-sibling::input'
    DESK_MODE_AT_DESCRIPTION_TAB_XPATH = '//*[text()="Desk mode *"]/preceding-sibling::input'
    LOCATION_AT_DESCRIPTION_TAB_XPATH = '//*[text()="Location"]/preceding-sibling::input'

    SAVE_CHANGES_BUTTON_XPATH = "//*[text()='Save Changes']"
    REVERT_CHANGES_BUTTON_XPATH  = "//*[text()='Revert Changes']"