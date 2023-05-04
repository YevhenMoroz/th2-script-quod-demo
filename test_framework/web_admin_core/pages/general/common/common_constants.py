class CommonConstants:
    DOWNLOAD_CSV_XPATH = '//*[@class="right size-small"]//a//*[@data-name="download"]'
    REFRESH_PAGE_XPATH = '//*[@class="right size-small"]//a//*[@data-name="refresh"]'
    SEND_FEEDBACK_BUTTON_XPATH = '//*[@nbtooltip="Send Feedback to Quod Financial"]'
    SEND_FEEDBACK_TEXT_AREA_XPATH = '//*[@placeholder="Please share your feedback..."]'
    SEND_FEEDBACK_SEND_BUTTON_XPATH = '//*[text()="Send"]'
    LOGOUT_BUTTON_XPATH = '//*[@title="Logout"]'
    USER_ICON_AT_RIGHT_CORNER = "//*[@class='control-item icon-btn context-menu-host']"
    OLD_PASSWORD_FIELD_AT_LOGIN_PAGE_XPATH = "//*[@formcontrolname='currentPassword']"
    NEW_PASSWORD_FIELD_AT_LOGIN_PAGE_XPATH = "//*[@formcontrolname='newPassword']"
    CONFIRM_PASSWORD_FIELD_AT_LOGIN_PAGE_XPATH = "//*[@formcontrolname='confirmNewPassword']"
    CHANGE_PASSWORD_BUTTON_AT_LOGIN_PAGE_XPATH = '//button[normalize-space()="Change password"]'
    BACK_BUTTON_AT_LOGIN_PAGE_XPATH = '//a[text()="Back"]'
    HELP_ICON_XPATH = '//*[@nbtooltip="Help"]'
    HELP_ICON_AT_LOGIN_PAGE_XPATH = '//*[@icon="question-mark-circle-outline"]'
    REFRESH_PAGE_BUTTON_XPATH = "//*[@data-name='refresh']"
    USER_NAME_XPATH = '//*[@class="logged-in-user ng-star-inserted"]'
    SITE_NAME_XPATH = '//span[@class="site-name"]'
    FULL_SCREEN_BUTTON_XPATH = '//*[@nbtooltip="Full Screen"]'
    EXIT_FULL_SCREEN_BUTTON_XPATH = '//*[@nbtooltip="Exit Full Screen"]'
    DARK_THEME_XPATH = '//a[@title="Dark Theme"]'
    COPY_VERSION_BUTTON = '//*[@nbtooltip="Copy version"]'
    ABOUT_BUTTON_XPATH = '//*[@title="About"]'
    ADMIN_VERSION_XPATH = '//*[@id="admVersionInput"]'
    APPLICATION_INFORMATION_AT_SEND_FEEDBACK_XPATH = '//*[text()="application information"]'
    ARROW_BACK_BUTTON_XPATH = '//*[@data-name="arrow-back"]'
    HEADER_XPATH = '//*[@class="fixed"]'
    USER_ID_AT_SEND_FEEDBACK_ADDITION_INFORMATION = '//*[@id="userFeedback"]//*[text()="User ID"]/following-sibling::td'
    INFO_MESSAGE_POP_UP = '//nb-toast'
    ERROR_MESSAGE_POP_UP = '//nb-toast[contains(@class, "danger")]'
    ERROR_POP_UP_TEXT = '//nb-toast//*[@class="message"]'
    INFO_POP_UP_TEXT = '//nb-toast//*[@class="title subtitle"]'
    LOADING_OVERLAY = '//*[@ref="eOverlayWrapper"]/span'
