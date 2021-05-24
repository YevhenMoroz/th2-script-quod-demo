""" This modules contains constants for locators which are used in web test cases
    For more usability must import as get_xpath """


def sidebar_menu_tab_by_title(tab_title: str) -> str:
    """ Returns sidebar menu tab xpath by tab title
        Parameters:
            tab_title (str): tab title.
        Returns:
            str """
    return f'//*[@tag="menu-sidebar"]//a[@title="{tab_title}"]'


def sidebar_menu_sub_tab_by_title(sub_tab_title: str) -> str:
    """ Returns sidebar menu sub tab xpath by sub tab title. Uses WebElement for search
        Parameters:
            sub_tab_title (str): sub tab title.
        Returns:
            str """
    return f'./..//a[@title="{sub_tab_title}"]'


def card_header_by_text(header_text: str) -> str:
    """ Returns card header xpath by header text
        Parameters:
            header_text (str): header text.
        Returns:
            str """
    return f'//nb-card-header/*[contains(text(), "{header_text}")]/..'


# TODO: add Download and Refresh buttons xpath inside card header

def input_by_text(label_text: str, by_header_text=None) -> str:
    """ Returns input field xpath by label text inside or by header with placeholder tag
        Parameters:
            label_text (str): label text;
            by_header_text(str, default=None): text of header which contains input.
        Returns:
            str """
    if by_header_text:
        return f'//*[contains(text(), "{by_header_text}")]//following-sibling::nb-accordion-item-body' \
               f'//input[@placeholder="{label_text}"]'
    else:
        return f'//label[text()="{label_text}"]/preceding-sibling::input'


def button_by_text(btn_text: str) -> str:
    """ Returns button xpath by text inside
        Parameters:
            btn_text (str): text inside button.
        Returns:
            str """
    return f'//button[text()="{btn_text}"]'


def container_event_by_text(event_text: str) -> str:
    """ Returns event xpath by text inside
        Parameters:
            event_text (str): text inside event.
        Returns:
            str """
    return f'//nb-toast//*[text()="{event_text}"]'


# todo: rename?
def table_filter_name_by_text(filter_text: str) -> str:
    """ Returns filter xpath by text inside
        Parameters:
            filter_text (str): filter text.
        Returns:
            str """
    return f'//*[text()="{filter_text}"]/ancestor::*[@col-id]'


def action_by_tooltip(tooltip: str) -> str:
    """ Returns table action xpath by text inside
        Parameters:
            tooltip (str): action tooltip.
        Returns:
            str """
    return f'//*[@nbtooltip="{tooltip}"]/*'


login_logo = '//*[@class="login-logo"]'
person_btn = '//*[@data-name="person"]'
logout_btn = '//*[@href="#/auth/logout"]'

table_headers = '//*[@ref="eHeaderContainer"]/*[@class="ag-header-row"]'
table_filter_names = f'{table_headers}[1]/*'
table_filter_inputs = f'{table_headers}[2]/*'
table_row_container = '//*[@ref="eCenterContainer"]'
table_row = './*[@role="row"]'
filter_input = '//input[@ref="eFloatingFilterText"]'

actions_btn = '//*[@data-name="more-vertical"]'

plus_btn = '//*[@class="nb-plus"]'
