class UsersConstants:
    USERS_PAGE_TITLE_XPATH = "//*[@href='#/pages/users/view']//*[text()='Users']"
    USER_ICON_AT_RIGHT_CORNER = "//*[@class='control-item icon-btn context-menu-host']"
    LOGOUT_BUTTON_XPATH = "//*[text()='Logout']"
    DISABLED_ENABLED_SUCCESSFUL_MESSAGE = "//*[@class='title subtitle']"
    RECORD_EXIST_EXCEPTION = "//*[text()='Such a record already exists']"
    INCORRECT_OR_MISSING_VALUES_EXCEPTION = "//*[text()='Incorrect or missing values']"
    NEW_BUTTON_XPATH = '//*[text()="New"]'
    ENABLE_DISABLE_BUTTON_XPATH = "//div[contains(@class, 'toggle')]"
    MORE_ACTIONS_XPATH = "//nb-icon[@title='More Actions']"
    EDIT_AT_MORE_ACTIONS_XPATH = '//*[@data-name="edit"]'
    CLONE_AT_MORE_ACTIONS_XPATH = '//*[@data-name="copy"]'
    DOWNLOAD_PDF_AT_MORE_ACTIONS_XPATH = "//nb-icon[@icon='download-outline']//*[@data-name='download']"
    DOWNLOAD_PDF_AT_WIZARD_XPATH = "//*[@data-name='download']"
    PIN_TO_ROW_AT_MORE_ACTIONS_XPATH = '//*[@nbtooltip="Click to Pin Row"]'
    OK_BUTTON_XPATH = "//*[text()='Ok']"

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
    CONNECTED_FILTER_AT_MAIN_PAGE = '//ag-grid-angular/div/div[1]/div/div[1]/div[2]/div/div[2]/div[9]/div[1]/ng-component/select'
    HORIZONTAL_SCROLL = "//*[@class='ag-body-horizontal-scroll']"

    # values for getters
    USER_ID_AT_MAIN_PAGE = "//*[@col-id='userID']//*[@class='ag-group-value']"
    FIRST_NAME_AT_MAIN_PAGE = "//*[@col-id='firstName']//*[@class='ag-group-value']"
    LAST_NAME_AT_MAIN_PAGE = "//*[@col-id='lastName']//*[@class='ag-group-value']"
    EXT_ID_CLIENT_AT_MAIN_PAGE = "//*[@col-id='clientUserID']//*[@class='ag-group-value']"
    EXT_ID_VENUE_AT_MAIN_PAGE = "//*[@col-id='venueUserID']//*[@class='ag-group-value']"
    PASSWORD_EXPIRY_DATE_AT_MAIN_PAGE = "//*[@col-id='passwdExpiryDate_ext'][@class='ag-cell ag-cell-not-inline-editing ag-cell-with-height ag-cell-value']"
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
    SAVE_CHANGES_BUTTON = "//*[text()='Save Changes']"
    CLEAR_CHANGES_BUTTON = "//*[text()='First Login']"

    # Login sub wizard

    USER_ID_AT_LOGIN_SUB_WIZARD = '//*[text()="User ID *"]/preceding-sibling::input'
    EXT_ID_CLIENT_AT_LOGIN_SUB_WIZARD = '//*[text()="Ext ID Client"]/preceding-sibling::input'
    EXT_ID_VENUE_AT_LOGIN_SUB_WIZARD = '//*[text()="Ext ID Venue"]/preceding-sibling::input'
    EXT_ENTITLEMENT_AT_LOGIN_SUB_WIZARD = '//*[text()="Ext Entitlement Key"]/preceding-sibling::input'
    PIN_CODE_AT_LOGIN_SUB_WIZARD = '//*[text()="PIN Code *"]/preceding-sibling::input'
    PASSWORD_AT_LOGIN_SUB_WIZARD = '//*[text()="Password *"]/preceding-sibling::input'
    PASSWORD_EXPIRATION_AT_LOGIN_SUB_WIZARD = '//*[text()="Password Expiration"]/preceding-sibling::input'
    COUNTERPART_AT_LOGIN_SUB_WIZARD = '//*[text()="Counterpart"]/preceding-sibling::input'
    MANAGE_AT_LOGIN_SUB_WIZARD = '//*[text()="Manage"]'

    GENERATE_PIN_CODE_CHECKBOX_AT_LOGIN_SUB_WIZARD = '//*[text()="Generate PIN Code"]/preceding-sibling::span'
    GENERATE_PASSWORD_CHECKBOX_AT_LOGIN_SUB_WIZARD = '//*[text()="Generate Password"]/preceding-sibling::span'
    CONFIRM_FOLLOW_UP_CHECKBOX_AT_LOGIN_SUB_WIZARD = '//*[text()="Confirm Follow Up"]/preceding-sibling::span'
    FIRST_TIME_LOGIN_CHECKBOX_AT_LOGIN_SUB_WIZARD = '//*[@formcontrolname="firstTimeLogin"]//span[contains(@class,"custom-checkbox")]'
    PING_REQUIRED_CHECKBOX_AT_LOGIN_SUB_WIZARD = '//*[text()="Ping Required"]/preceding-sibling::span'

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
    DESKS_AT_ASSIGNMENTS_SUB_WIZARD = "//*[text()='Desks']/parent::div//button"
    DESKS_CHECKBOX_LIST_AT_ASSIGNMENTS_SUB_WIZARD = '//*[@class="cdk-overlay-container"]//*[text()="{}"]'
    LOCATION_AT_ASSIGNMENTS_SUB_WIZARD = '//*[text()="Location"]/preceding-sibling::input'
    ZONE_AT_ASSIGNMENTS_SUB_WIZARD = "//*[text()='Zone']/preceding-sibling::input"
    INSTITUTION = "//*[text()='Institution']/preceding-sibling::input"

    # Role
    PERM_ROLE_AT_ROLE_SUB_WIZARD = '//*[text()="Perm Role"]/preceding-sibling::input'
    GROUP_AT_ROLE_SUB_WIZARD = '//*[text()="Group"]/preceding-sibling::input'
    PERM_OP_AT_ROLE_SUB_WIZARD = '//*[text()="Perm Op"]/preceding-sibling::input'

    # Must not be visible
    ROLE_ID_AT_ROLE_SUB_WIZARD = '//*[text()="Role Id"]/preceding-sibling::input'

    # Client
    PLUS_BUTTON_AT_CLIENT_SUB_WIZARD = '//*[text()=" Client "]/ancestor::*[@class="expanded"]//*[@class="nb-plus"]'
    CHECKMARK_AT_CLIENT_WIZARD = '//*[text()=" Client "]/ancestor::*[@class="expanded"]//*[@class="nb-checkmark"]'
    CANCEL_AT_CLIENT_SUB_WIZARD = '//*[text()=" Client "]/ancestor::*[@class="expanded"]//*[@class="nb-close"]'
    EDIT_AT_CLIENT_SUB_WIZARD = '//*[text()=" Client "]/ancestor::*[@class="expanded"]//*[@class="nb-edit"]'
    DELETE_AT_CLIENT_SUB_WIZARD = '//*[text()=" Client "]/ancestor::*[@class="expanded"]//*[@class="nb-trash"]'
    CLIENT_AT_CLIENT_SUB_WIZARD = '//*[@placeholder = "Client *"]'
    TYPE_AT_CLIENT_SUB_WIZARD = '//*[@placeholder = "Type *"]'
    CLIENT_FILTER_AT_CLIENT_SUB_WIZARD = '//*[@class= "accountGroup ng2-smart-th ng-star-inserted"]//*[@placeholder="Filter"]'
    TYPE_FILTER_AT_CLIENT_SUB_WIZARD = "//*[@class= 'ng2-smart-th userRoleAccountGroupType ng-star-inserted']//*[@placeholder='Filter']"

    # Venue trader
    PLUS_BUTTON_AT_VENUE_TRADER_SUB_WIZARD = '//*[text()="Manage Trader Groups"]/ancestor::*[@class="expanded"]//*[@class="nb-plus"]'
    CHECKMARK_AT_VENUE_TRADER_SUB_WIZARD = '//*[text()="Manage Trader Groups"]/ancestor::*[@class="expanded"]//*[@class="nb-checkmark"]'
    CANCEL_AT_VENUE_TRADER_SUB_WIZARD = '//*[text()="Manage Trader Groups"]/ancestor::*[@class="expanded"]//*[@class="nb-close"]'
    EDIT_AT_VENUE_TRADER_SUB_WIZARD = '//*[text()="Manage Trader Groups"]/ancestor::*[@class="expanded"]//*[@class="nb-edit"]'
    DELETE_AT_VENUE_TRADER_SUB_WIZARD = '//*[text()="Manage Trader Groups"]/ancestor::*[@class="expanded"]//*[@class="nb-trash"]'
    GO_BACK_BUTTON = '//*[text()="Go Back"]'
    VENUE_AT_VENUE_TRADER_SUB_WIZARD = '//*[@placeholder="Venue *"]'
    VENUE_TRADER_NAME_AT_VENUE_TRADER_SUB_WIZARD = '//*[@placeholder="Venue Trader Name *"]'
    TRADER_GROUP_AT_VENUE_TRADER_SUB_WIZARD = "//*[@placeholder='Trader Group']"
    VENUE_FILTER_AT_VENUE_TRADER_SUB_WIZARD = '//*[@class= "ng2-smart-th venue ng-star-inserted"]//*[@placeholder="Filter"]'
    VENUE_TRADER_NAME_FILTER_AT_VENUE_TRADER_SUB_WIZARD = '//*[@class= "ng2-smart-th venueTraderName ng-star-inserted"]//*[@placeholder="Filter"]'
    TRADER_GROUP_AT_VENUE_TRADER_SUB_WIZARD = '//*[@placeholder="Trader Group"]'
    TRADER_GROUP_FILTER_AT_VENUE_TRADER_SUB_WIZARD = '//*[@class= "ng2-smart-th traderGroup ng-star-inserted"]//*[@placeholder="Filter"]'
    MANAGE_TRADER_GROUPS_AT_VENUE_TRADER_SUB_WIZARD = '//*[text()="Manage Trader Groups"]'

    # Manage Trader Groups
    PLUS_BUTTON_AT_TRADER_GROUPS_SUB_WIZARD = '//*[@class="nb-plus"]'
    CHECKMARK_AT_TRADER_GROUPS_SUB_WIZARD = '//*[@class="nb-checkmark"]'
    CANCEL_AT_TRADER_GROUPS_SUB_WIZARD = '//*[@class="nb-close"]'
    NAME_AT_TRADER_GROUPS_SUB_WIZARD = '//*[@placeholder="Name *"]'
    VENUE_TRADER_GROUP_ID_AT_TRADER_GROUPS = '//*[@placeholder="Venue Trader Group ID *"]'
    NAME_FILTER_AT_TRADER_GROUPS_SUB_WIZARD = '//*[@class="ng2-smart-th traderGroupName ng-star-inserted"]//*[@placeholder="Filter"]'
    VENUE_TRADER_GROUP_ID_FILTER_AT_TRADER_GROUPS_SUB_WIZARD = '//*[@class="form-control ng-untouched ng-pristine ng-valid"]//*[@placeholder="Filter"]'

    # Roustes
    PLUS_BUTTON_AT_ROUTES_SUB_WIZARD = '//*[text()=" Routes "]/ancestor::*[@class="expanded"]//*[@class="nb-plus"]'
    CHECKMARK_AT_ROUTES_SUB_WIZARD = '//*[text()=" Routes "]/ancestor::*[@class="expanded"]//*[@class="nb-checkmark"]'
    CANCEL_AT_ROUTES_SUB_WIZARD = '//*[text()=" Routes "]/ancestor::*[@class="expanded"]//*[@class="nb-close"]'
    EDIT_AT_ROUTES_SUB_WIZARD = '//*[text()=" Routes "]/ancestor::*[@class="expanded"]//*[@class="nb-edit"]'
    DELETE_AT_ROUTES_WIZARD = '//*[text()=" Routes "]/ancestor::*[@class="expanded"]//*[@class="nb-trash"]'

    ROUTE_AT_ROUTES_SUB_WIZARD = '//*[@placeholder="Route *"]'
    ROUTE_USER_NAME_AT_ROUTES_SUB_WIZARD = '//*[@placeholder="Route User Name *"]'
    ROUTE_FILTER_AT_ROUTES_SUB_WIZARD = '//*[@class="ng2-smart-th route ng-star-inserted"]//*[@placeholder="Filter"]'
    ROUTE_USER_NAME_FILTER_AT_ROUTES_SUB_WIZARD = '//*[@class="ng2-smart-th routeUserName ng-star-inserted"]//*[@placeholder="Filter"]'
