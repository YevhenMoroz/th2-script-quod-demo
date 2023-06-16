class UsersConstants:
    USERS_PAGE_TITLE_XPATH = '//*[@class="entity-title left"][normalize-space(text())="Users"]'
    USER_ICON_AT_RIGHT_CORNER = "//*[@class='control-item icon-btn context-menu-host']"
    USER_WIZARD_HEADER_LINK = '//div[@class="breadcrumbs entity-title user-breadcrumbs"]//span[normalize-space()="Users"]'
    LOGOUT_BUTTON_XPATH = "//*[text()='Logout']"
    DISABLED_ENABLED_SUCCESSFUL_MESSAGE = "//*[@class='title subtitle']"
    RECORD_EXIST_EXCEPTION = "//*[text()='Such a record already exists']"
    INCORRECT_OR_MISSING_VALUES_EXCEPTION = "//*[text()='Incorrect or missing values']"
    NEW_BUTTON_XPATH = '//*[normalize-space()="New"]'
    ENABLE_DISABLE_BUTTON_XPATH = "//div[contains(@class, 'toggle')]"
    MORE_ACTIONS_XPATH = "//nb-icon[@title='More Actions']"
    EDIT_AT_MORE_ACTIONS_XPATH = '//*[@data-name="edit"]'
    CLONE_AT_MORE_ACTIONS_XPATH = '//*[@data-name="copy"]'
    DOWNLOAD_PDF_AT_MORE_ACTIONS_XPATH = "//nb-icon[@icon='download-outline']//*[@data-name='download']"
    DOWNLOAD_PDF_AT_WIZARD_XPATH = "//*[@data-name='download']"
    PIN_TO_ROW_AT_MORE_ACTIONS_XPATH = '//*[@nbtooltip="Click to Pin Row"]'
    UNPIN_TO_ROW_AT_MORE_ACTIONS_XPATH = '//*[@nbtooltip="Click to Unpin Row"]'
    OK_BUTTON_XPATH = '//*[text()="OK" or text()="Ok"]'
    CANCEL_BUTTON_XPATH = '//*[normalize-space()="Cancel"]'
    LOCK_UNLOCK_BUTTON_XPATH = "//*[@data-name='lock' or @data-name='unlock']"
    REQUEST_FAILED_MESSAGE_XPATH = "//nb-toast[contains(@class, 'danger')]"
    DISPLAYED_USER_XPATH = "//*[text()='{}']"
    ONLINE_STATUS_XPATH = '//*[@icon="circle-fill"]'
    ALL_DISPLAYED_USERS_XPATH = '//*[@ref="eCenterContainer"]//div[@role="row"]'
    NOT_FOUND_OPTION_XPATH = '//*[normalize-space(text())="Not found"]'
    WARNING_MESSAGE = '//*[@outline="danger"]'
    DROP_DOWN_MENU_XPATH = '//*[@class="option-list"]//span'
    USERS_LOOK_UP_INPUT = '//nb-card-header//form//input[contains(@class, "lookup-input")]'
    LOAD_BUTTON = '//nb-card-header//form//button'

    # filters
    USER_ID_FILTER_AT_MAIN_PAGE = "//ag-grid-angular/div/div[1]/div/div[1]/div[2]/div/div[2]/div[1]/div[1]/div/input"
    FIRST_NAME_FILTER_AT_MAIN_PAGE = "//ag-grid-angular/div/div[1]/div/div[1]/div[2]/div/div[2]/div[2]/div[1]/div/input"
    LAST_NAME_FILTER_AT_MAIN_PAGE = "//ag-grid-angular/div/div[1]/div/div[1]/div[2]/div/div[2]/div[3]/div[1]/div/input"
    EXT_ID_CLIENT_FILTER_AT_MAIN_PAGE = "//ag-grid-angular/div/div[1]/div/div[1]/div[2]/div/div[2]/div[4]/div[1]/div/input"
    EXT_ID_VENUE_FILTER_AT_MAIN_PAGE = "//ag-grid-angular/div/div[1]/div/div[1]/div[2]/div/div[2]/div[5]/div[1]/div/input"
    PASSWORD_EXPIRY_DATE_FILTER_AT_MAIN_PAGE = "//ag-grid-angular/div/div[1]/div/div[1]/div[2]/div/div[2]/div[6]/div[1]/div/div/div/input"
    FIRST_LOGIN_FILTER_AT_MAIN_PAGE = "//ag-grid-angular/div/div[1]/div/div[1]/div[2]/div/div[2]/div[7]/div[1]/ng-component/select"
    PING_FILTER_AT_MAIN_PAGE = "//ag-grid-angular/div/div[1]/div/div[1]/div[2]/div/div[2]/div[2]/div[1]/ng-component/select"
    ADDRESS_FILTER_AT_MAIN_PAGE = "//ag-grid-angular/div/div[1]/div/div[1]/div[2]/div/div[2]/div[3]/div[1]/div/input"
    COUNTRY_FILTER_AT_MAIN_PAGE = "//ag-grid-angular/div/div[1]/div/div[1]/div[2]/div/div[2]/div[4]/div[1]/div/input"
    BIRTH_DATE_FILTER_AT_MAIN_PAGE = "//ag-grid-angular/div/div[1]/div/div[1]/div[2]/div/div[2]/div[5]/div[1]/div/div/div/input"
    EXTENSION_FILTER_AT_MAIN_PAGE = '//ag-grid-angular/div/div[1]/div/div[1]/div[2]/div/div[2]/div[6]/div[1]/div/input'
    MOBILE_FILTER_AT_MAIN_PAGE = '//ag-grid-angular/div/div[1]/div/div[1]/div[2]/div/div[2]/div[6]/div[1]/div/input'
    EMAIL_FILTER_AT_MAIN_PAGE = '//ag-grid-angular/div/div[1]/div/div[1]/div[2]/div/div[2]/div[8]/div[1]/div/input'
    ENABLED_FILTER_AT_MAIN_PAGE = '//ag-grid-angular/div/div[1]/div/div[1]/div[2]/div/div[2]/div[7]/div[1]/ng-component/select'
    LOCKED_FILTER_AT_MAIN_PAGE = '//ag-grid-angular/div/div[1]/div/div[1]/div[2]/div/div[2]/div[8]/div[1]/ng-component/select'
    CONNECTED_FILTER_AT_MAIN_PAGE = '(//*[@style="width: 200px; left: 3600px;"])[2]//ng-component'
    HORIZONTAL_SCROLL = "//*[@class='ag-body-horizontal-scroll']"

    # values for getters
    USER_ID_AT_MAIN_PAGE = "//*[@col-id='userID']//*[@class='ag-group-value']"
    FIRST_NAME_AT_MAIN_PAGE = "//*[@col-id='firstName']//*[@class='ag-group-value']"
    LAST_NAME_AT_MAIN_PAGE = "//*[@col-id='lastName']//*[@class='ag-group-value']"
    EXT_ID_CLIENT_AT_MAIN_PAGE = "//*[@col-id='clientUserID']//*[@class='ag-group-value']"
    EXT_ID_VENUE_AT_MAIN_PAGE = "//*[@col-id='venueUserID']//*[@class='ag-group-value']"
    PASSWORD_EXPIRY_DATE_AT_MAIN_PAGE = "//div[@col-id='passwdExpiryDate_ext'][span]/span"
    FIRST_LOGIN_AT_MAIN_PAGE = "//*[@col-id='firstTimeLogin']//*[@class='custom-checkbox']"
    PING_AT_MAIN_PAGE = "//*[@col-id='pingRequired']//*[@class='custom-checkbox']"
    ADDRESS_AT_MAIN_PAGE = "//*[@col-id='address']//*[@class='ag-group-value']"
    COUNTRY_AT_MAIN_PAGE = "//*[@col-id='country']//*[@class='ag-group-value']"
    BIRTH_AT_MAIN_PAGE = "//*[@col-id='dateOfBirth_ext']/span"
    EXTENSION_AT_MAIN_PAGE = "//*[@col-id='userExtension']//*[@class='ag-group-value']"
    MOBILE_AT_MAIN_PAGE = "//*[@col-id='userMobile']//*[@class='ag-group-value']"
    EMAIL_AT_MAIN_PAGE = "//*[@col-id='userEmail']//*[@class='ag-group-value']"
    ENABLED_AT_MAIN_PAGE = "//*[@col-id='alive_ext']//*[@class='custom-checkbox']"
    LOCKED_AT_MAIN_PAGE = "//*[@col-id='loginLocked']//*[@class='custom-checkbox']"
    CONNECTED_AT_MAIN_PAGE = "//*[@col-id='1']//*[@class='custom-checkbox']"

    # Wizard
    SAVE_CHANGES_BUTTON = "//*[normalize-space()='Save Changes']"
    REVERT_CHANGES_BUTTON = '//button[normalize-space()="Revert Changes"]'
    ERROR_MESSAGE_IN_FOOTER = "//*[@outline='danger']"
    CONFIRM_POP_UP = '(//nb-card)[2]'

    # Values sub wizard

    USER_ID_AT_LOGIN_SUB_WIZARD = '//*[text()="User ID *"]/preceding-sibling::input'
    EXT_ID_CLIENT_AT_LOGIN_SUB_WIZARD = '//*[text()="Ext ID Client *"]/preceding-sibling::input'
    EXT_ID_VENUE_AT_LOGIN_SUB_WIZARD = '//*[text()="Ext ID Venue"]/preceding-sibling::input'
    EXT_ENTITLEMENT_AT_LOGIN_SUB_WIZARD = '//*[text()="Ext Entitlement Key"]/preceding-sibling::input'
    PIN_CODE_AT_LOGIN_SUB_WIZARD = '//*[text()="PIN Code *"]/preceding-sibling::input'
    PASSWORD_AT_LOGIN_SUB_WIZARD = '//*[text()="Password *"]/preceding-sibling::input'
    PASSWORD_EXPIRATION_AT_LOGIN_SUB_WIZARD = '//*[text()="Password Expiration"]/preceding-sibling::input'
    COUNTERPART_AT_LOGIN_SUB_WIZARD = '//*[text()="Counterpart"]/preceding-sibling::input'
    MANAGE_AT_LOGIN_SUB_WIZARD = '//*[text()="Manage"]'
    NON_VISIBLE_POSITION_FLATTENING_PERIODS = '//*[@id="Non-Visible Position Flattening Periods"]//p-multiselect//div'
    CHANGE_PASSWORD_BUTTON_AT_LOGIN_SUB_WIZARD = '//button[normalize-space()="Change Password"]'
    NEW_PASSWORD_AT_LOGIN_SUB_WIZARD = '//*[@formcontrolname="newPassword"]'
    CONFIRM_NEW_PASSWORD_AT_LOGIN_SUB_WIZARD = '//*[@formcontrolname="confirmNewPassword"]'
    CHANGE_PASSWORD_BUTTON_AT_POP_UP_LOGIN_SUB_WIZARD = '//div[@class="change-password"]//button[@status="primary"]'
    CHANGE_PASSWORD_POP_UP = '//div[@class="change-password"]'
    CHANGE_PASSWORD_POP_UP_ERROR_TEXT = '//div[@class="change-password"]//*[@class="alert-message ng-star-inserted"]'

    GENERATE_PIN_CODE_CHECKBOX_AT_LOGIN_SUB_WIZARD = '//*[text()="Generate PIN Code"]/preceding-sibling::span'
    GENERATE_PASSWORD_CHECKBOX_AT_LOGIN_SUB_WIZARD = '//*[text()="Generate Password"]/preceding-sibling::span'
    CONFIRM_FOLLOW_UP_CHECKBOX_AT_LOGIN_SUB_WIZARD = '//*[text()="Confirm Follow Up"]/preceding-sibling::span'
    FIRST_TIME_LOGIN_CHECKBOX_AT_LOGIN_SUB_WIZARD = '//*[@formcontrolname="firstTimeLogin"]//span[contains(@class,"custom-checkbox")]'
    PING_REQUIRED_CHECKBOX_AT_LOGIN_SUB_WIZARD = '//*[text()="Ping Required *"]/preceding-sibling::span'

    # User details
    FIRST_NAME_AT_USER_DETAILS_SUB_WIZARD = '//*[text()="First Name"]/preceding-sibling::input'
    LAST_NAME_AT_USER_DETAILS_SUB_WIZARD = '//*[text()="Last Name"]/preceding-sibling::input'
    ADDRESS_AT_USER_DETAILS_SUB_WIZARD = '//*[text()="Address"]/preceding-sibling::input'
    MAIL_AT_USER_DETAILS_SUB_WIZARD = '//*[@formcontrolname="userEmail"]'
    EXTENSION_AT_USER_DETAILS_SUB_WIZARD = '//*[text()="Extension"]/preceding-sibling::input'
    MOBILE_AT_USER_DETAILS_SUB_WIZARD = '//*[text()="Mobile"]/preceding-sibling::input'
    COUNTRY_AT_USER_DETAILS_SUB_WIZARD = '//*[text()="Country"]/preceding-sibling::input'
    DATE_OF_BIRTH = '//*[text()="Date of Birth"]/preceding-sibling::input'

    # Assignments
    DESKS_AT_ASSIGNMENTS_SUB_WIZARD = '//*[@id="Desks"]'
    DESKS_CHECKBOX_LIST_AT_ASSIGNMENTS_SUB_WIZARD = '//*[@class="cdk-overlay-container"]//*[text()="{}"]'
    LOCATION_AT_ASSIGNMENTS_SUB_WIZARD = '//*[text()="Location"]/preceding-sibling::input'
    ZONE_AT_ASSIGNMENTS_SUB_WIZARD = "//*[text()='Zone']/preceding-sibling::input"
    SELECTED_ZONE_URL_AT_ASSIGNMENTS_SUB_WIZARD = '//*[@form-control-name="zone"]//a'
    INSTITUTION = "//*[text()='Institution']/preceding-sibling::input"
    TECHNICAL_USER_CHECKBOX_AT_ASSIGNMENTS_SUB_WIZARD = '//*[@formcontrolname="technicalUser"]//span[1]'
    HEAD_OF_DESK_AT_ASSIGNMENTS_SUB_WIZARD = '//*[@formcontrolname="headOfDesk"]//span[1]'
    HEAD_OF_DESK_AT_ASSIGNMENTS_SUB_WIZARD_INPUT = '//*[@formcontrolname="headOfDesk"]//input'

    # Role
    PERM_ROLE_AT_ROLE_SUB_WIZARD = '//*[text()="Perm Role"]/preceding-sibling::input'
    GROUP_AT_ROLE_SUB_WIZARD = '//*[text()="Group"]/preceding-sibling::input'
    PERM_OP_AT_ROLE_SUB_WIZARD = '//*[@id="permOp"]'
    PERMISSION_PROFILES = '//*[@id="Permission Profiles"]'

    # Must not be visible
    ROLE_ID_AT_ROLE_SUB_WIZARD = '//*[text()="Role Id"]/preceding-sibling::input'

    # Client
    PLUS_BUTTON_AT_CLIENT_SUB_WIZARD = '//*[text()=" Client "]/ancestor::*[@class="expanded"]//*[@data-name="plus"]'
    CHECKMARK_AT_CLIENT_WIZARD = '//*[text()=" Client "]/ancestor::*[@class="expanded"]//*[@data-name="checkmark"]'
    CANCEL_AT_CLIENT_SUB_WIZARD = '//*[text()=" Client "]/ancestor::*[@class="expanded"]//*[@data-name="close"]'
    EDIT_AT_CLIENT_SUB_WIZARD = '//*[text()=" Client "]/ancestor::*[@class="expanded"]//*[@data-name="edit"]'
    DELETE_AT_CLIENT_SUB_WIZARD = '//*[text()=" Client "]/ancestor::*[@class="expanded"]//*[@data-name="trash-2"]'
    CLIENT_AT_CLIENT_SUB_WIZARD = '//*[@placeholder = "Client *"]'
    TYPE_AT_CLIENT_SUB_WIZARD = '//nb-accordion-item-header[normalize-space()="Clients"]//..//nb-select'
    CLIENT_FILTER_AT_CLIENT_SUB_WIZARD = '(//*[text()=" Client "]//following-sibling::nb-accordion-item-body//thead//input)[1]'
    TYPE_FILTER_AT_CLIENT_SUB_WIZARD = '//*[text()=" Client "]//following-sibling::nb-accordion-item-body//thead//input)[2]'
    CLIENT_IN_TABLE_AT_CLIENT_SUB_WIZARD = '//*[normalize-space()="Clients"]//..//tbody//td[2]//span'

    # Venue trader
    PLUS_BUTTON_AT_VENUE_TRADER_SUB_WIZARD = '//*[text()="Manage Trader Groups"]/ancestor::*[@class="expanded"]//*[@data-name="plus"]'
    CHECKMARK_AT_VENUE_TRADER_SUB_WIZARD = '//*[text()="Manage Trader Groups"]/ancestor::*[@class="expanded"]//*[@data-name="checkmark"]'
    CANCEL_AT_VENUE_TRADER_SUB_WIZARD = '//*[text()="Manage Trader Groups"]/ancestor::*[@class="expanded"]//*[@data-name="close"]'
    EDIT_AT_VENUE_TRADER_SUB_WIZARD = '//*[text()="Manage Trader Groups"]/ancestor::*[@class="expanded"]//*[@data-name="edit"]'
    DELETE_AT_VENUE_TRADER_SUB_WIZARD = '//*[text()="Manage Trader Groups"]/ancestor::*[@class="expanded"]//*[@data-name="trash-2"]'
    GO_BACK_BUTTON = '//*[text()="Go Back"]'
    VENUE_AT_VENUE_TRADER_SUB_WIZARD = '//*[@placeholder="Venue *"]'
    VENUE_TRADER_NAME_AT_VENUE_TRADER_SUB_WIZARD = '//*[@placeholder="Venue Trader Name *"]'
    TRADER_GROUP_AT_VENUE_TRADER_SUB_WIZARD = "//*[@placeholder='Trader Group']"
    VENUE_FILTER_AT_VENUE_TRADER_SUB_WIZARD = '//*[text()=" Venue Trader "]/following-sibling::nb-accordion-item-body//th[@class="add-button-cell"]/following-sibling::th[1]'
    VENUE_TRADER_NAME_FILTER_AT_VENUE_TRADER_SUB_WIZARD = '//*[text()=" Venue Trader "]/following-sibling::nb-accordion-item-body//th[@class="add-button-cell"]/following-sibling::th[2]'
    TRADER_GROUP_FILTER_AT_VENUE_TRADER_SUB_WIZARD = '//*[text()=" Venue Trader "]/following-sibling::nb-accordion-item-body//th[@class="add-button-cell"]/following-sibling::th[3]'
    MANAGE_TRADER_GROUPS_AT_VENUE_TRADER_SUB_WIZARD = '//*[text()="Manage Trader Groups"]'
    CREATED_VENUE_AT_VENUE_TRADER_TAB = "//*[text()=' Venue Trader ']/following-sibling::nb-accordion-item-body//*[@class='ui-table-scrollable-body ng-star-inserted']//td[2]//span"
    CREATED_VENUE_TRADE_NAME_AT_VENUE_TRADER_TAB = "//*[text()=' Venue Trader ']/following-sibling::nb-accordion-item-body//*[@class='ui-table-scrollable-body ng-star-inserted']//td[3]//span"
    CREATED_TRADER_GROUP_AT_VENUE_TRADER_TAB = "//*[text()=' Venue Trader ']/following-sibling::nb-accordion-item-body//*[@class='ui-table-scrollable-body ng-star-inserted']//td[4]//span"

    # Manage Trader Groups
    PLUS_BUTTON_AT_TRADER_GROUPS_SUB_WIZARD = '//*[@class="nb-plus"]'
    CHECKMARK_AT_TRADER_GROUPS_SUB_WIZARD = '//*[@class="nb-checkmark"]'
    CANCEL_AT_TRADER_GROUPS_SUB_WIZARD = '//*[@class="nb-close"]'
    NAME_AT_TRADER_GROUPS_SUB_WIZARD = '//*[@placeholder="Name *"]'
    VENUE_TRADER_GROUP_ID_AT_TRADER_GROUPS = '//*[@placeholder="Venue Trader Group ID *"]'
    NAME_FILTER_AT_TRADER_GROUPS_SUB_WIZARD = '//*[@class="ng2-smart-th traderGroupName ng-star-inserted"]//*[@placeholder="Filter"]'
    VENUE_TRADER_GROUP_ID_FILTER_AT_TRADER_GROUPS_SUB_WIZARD = '//*[@class="form-control ng-untouched ng-pristine ng-valid"]//*[@placeholder="Filter"]'

    # Roustes
    PLUS_BUTTON_AT_ROUTES_SUB_WIZARD = '//*[normalize-space()="Routes"]//..//*[@nbtooltip="Add"]'
    CHECKMARK_AT_ROUTES_SUB_WIZARD = '//*[normalize-space()="Routes"]//..//*[@data-name="checkmark"]'
    CANCEL_AT_ROUTES_SUB_WIZARD = '//*[normalize-space()="Routes"]//..//*[@data-name="close"]'
    EDIT_AT_ROUTES_SUB_WIZARD = '//*[normalize-space()="Routes"]//..//*[@data-name="edit"]'
    DELETE_AT_ROUTES_WIZARD = '//*[normalize-space()="Routes"]//..//*[@data-name="trash-2"]'
    DELETE_LAST_ENTRY_AT_ROUTE_WIZARD = '(//*[normalize-space()="Routes"]//..//*[@data-name="trash-2"])[last()]'

    ROUTE_AT_ROUTES_SUB_WIZARD = '//*[@placeholder="Route *"]'
    ROUTE_USER_NAME_AT_ROUTES_SUB_WIZARD = '//*[@placeholder="Route User Name *"]'
    ROUTE_FILTER_AT_ROUTES_SUB_WIZARD = '(//*[normalize-space()="Routes"]//..//*[@placeholder="Filter"])[1]'
    ROUTE_USER_NAME_FILTER_AT_ROUTES_SUB_WIZARD = '(//*[normalize-space()="Routes"]//..//*[@placeholder="Filter"])[2]'
    ROUTE_IN_ROUTE_TABLE_SUB_WIZARD = '//*[normalize-space()="Routes"]//..//p-table//tbody//td[2]//span'
