class CommonConstants:
    COMBOBOX_OPTION_PATTERN_XPATH = '//*[@class="option-list"]//*[normalize-space()="{}"]'
    COMBOBOX_DROP_DOWN_XPATH = '//*[@class="option-list"]'
    COMMON_CHECKBOX_STATE_SPAN_CSS_SELECTOR = "span[class*='custom-checkbox']"
    MULTISELECT_FORM_LOOK_UP = '//input[@role="textbox"]'
    MULTISELECT_ITEM_XPATH = '//p-multiselectitem//li//span[@id][text()="{}"]'
    MULTISELECT_ENTITIES = '//div[contains(@class, "multiselect-values")]'
    CHECKED_ATTRIBUTE = "checked"
    HORIZONTAL_SCROLL_ELEMENT_XPATH = '//*[@ref="eBodyHorizontalScrollViewport"]'
    HORIZONTAL_SCROLL_WHEEL = '//*[@ref="eBottomContainer"]'
    DROP_MENU_OPTION_PATTERN_XPATH = '//option[normalize-space()="{}"] | //nb-option[normalize-space()="{}"] '
    HELP_ICON = '//nb-card-header//*[@nbtooltip="Help"]'
    USER_ICON = '//*[@data-name="person"]'
    PAGE_BODY = '//body'
    NGX_APP_LOADED = '//ngx-app//*'
