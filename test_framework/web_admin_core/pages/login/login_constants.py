class LoginConstants:
    LOGIN_INPUT_CSS_SELECTOR = "input[id='input-email']"
    PASSWORD_INPUT_CSS_SELECTOR = "input[id='input-password']"
    LOGIN_BUTTON_XPATH = "//button[text()=' Login ']"
    LOGIN_ERROR_MESSAGE_XPATH = "//li[contains(@class, 'alert-message')]"
    LOGIN_PAGE_ADMIN_XPATH = "//*[text()='System Administration']"
    CHANGE_PASSWORD_PAGE_XPATH = '//*[text()="Change password"]'
    FORGOT_PASSWORD_LINK_XPATH = '//a[normalize-space()="Forgot password?"]'
    BACK_LINK_XPATH = '//a[normalize-space()="Back"]'
    EMAIL_INPUT_XPATH = '//input[@id="input-emailUser"]'
    RESET_PASSWORD_BUTTON_XPATH = '//button[normalize-space()="Reset Password"]'
    CHANGE_PASSWORD_INFO_MESSAGE_XPATH = '//span[@class="title subtitle"]'
    LOGIN_PAGE_TITLE_TEXT_XPATH = '//h2'
