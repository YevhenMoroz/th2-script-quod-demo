import logging
import time
from datetime import datetime
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from custom import basic_custom_actions as bca
from quod_qa.web_admin import QAP_758, login_logout_example
from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.pages.others.counterparts.counterparts_page import CounterpartsPage
from quod_qa.web_admin.web_admin_core.pages.others.counterparts.counterparts_wizard import CounterpartsWizard

from stubs import Stubs

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False

channels = dict()

test_cases = {
    '303': [login_logout_example,
            QAP_758,
            ],
    '305': [login_logout_example,
            ]
}


# NOTE: for now the following code is using only to check implementation of pages. It will be updated in the future
def test_run():
    # Generation ID and time for test run
    report_id = bca.create_event(f'{Stubs.custom_config["web_admin_login"]} tests '
                                 + datetime.now().strftime('%Y%m%d-%H:%M:%S'))
    logger.info(f"Root event was created (id = {report_id.id})")
    # Start session
    # driver.maximize_window()
    web_driver = WebDriverContainer()
    web_driver.start_driver(web_driver.INITIAL_URL)
    login_page = LoginPage(web_driver)
    login_page.set_login("adm08")
    login_page.set_password("adm08")
    login_page.click_login_button()
    # content
    counterparts_page = CounterpartsPage(web_driver)
    edit_wizard = CounterpartsWizard(web_driver)

    ###Worked with main page##

    counterparts_page.click_on_others()
    time.sleep(2)
    counterparts_page.click_on_counterparts()
    time.sleep(1)
    counterparts_page.click_on_new()
    # time.sleep(2)
    # counterparts_page.set_name_filter_value("new")
    # print(counterparts_page.get_name_value())
    # counterparts_page.click_on_more_actions()
    # counterparts_page.click_on_edit()
    # time.sleep(2)
    edit_wizard.set_name_value_at_values_tab("otherNew")
    time.sleep(3)
    edit_wizard.click_on_clear_changes()
    # time.sleep(3)
    # print(edit_wizard.get_name_at_values_tab())
    # edit_wizard.click_on_plus_sub_counterparts()
    # edit_wizard.set_name_at_sub_counterparts_tab("something")
    # edit_wizard.set_party_id_at_sub_counterparts_tab("12")
    # edit_wizard.set_ext_id_client_at_sub_counterparts_tab("1")
    # edit_wizard.set_party_sub_id_at_sub_counterparts_tab("BIC")
    # edit_wizard.click_on_check_mark()
    # print(edit_wizard.get_name_value_at_sub_counterparts_tab())
    # print(edit_wizard.get_party_id_value_at_sub_counterparts_tab())
    # print(edit_wizard.get_ext_id_client_value_at_sub_counterparts_tab())
    # print(edit_wizard.get_party_sub_id_type_value_at_sub_counterparts_tab())
    # edit_wizard.set_name_filter_at_sub_counterparts_tab("something")
    # edit_wizard.set_party_id_filter_at_sub_counterparts_tab("12")
    # edit_wizard.set_ext_id_client_filter_at_sub_counterparts_tab("1")
    # edit_wizard.set_party_sub_id_type_filter_at_sub_counterparts_tab("BIC")
    # edit_wizard.click_on_edit()
    # edit_wizard.click_on_close_changes()
    # edit_wizard.click_on_delete()
    # edit_wizard.click_on_revert_changes()
    # edit_wizard.click_on_close()
    # edit_wizard.click_on_save_changes()

    #--party roles--
    # edit_wizard.click_on_plus_party_roles()
    # edit_wizard.set_party_id_source_at_party_roles_tab("BIC")
    # edit_wizard.set_venue_counterpart_id_at_party_roles_tab("333")
    # edit_wizard.set_party_role_at_party_roles_tab("DeskID")
    # edit_wizard.set_ext_id_client_at_party_roles_tab("41")
    # edit_wizard.set_party_role_qualifier_at_party_roles_tab("Bank")
    # edit_wizard.set_venue_at_party_roles_tab("AMEX")
    #
    # edit_wizard.set_party_id_source_filter_at_party_roles_tab("BIC")
    # edit_wizard.set_venue_counterpart_id_filter_at_party_roles_tab("333")
    # edit_wizard.set_party_role_filter_at_party_roles_tab("DeskID")
    # edit_wizard.set_ext_id_client_filter_at_party_roles_tab("41")
    # edit_wizard.set_party_role_qualifier_filter_at_party_roles_tab("Bank")
    # edit_wizard.set_venue_filter_at_party_roles_tab("AMEX")







    # edit_wizard.click_on_check_mark()
    # print(edit_wizard.get_party_id_source_value_at_party_roles_tab())
    # print(edit_wizard.get_venue_counterpart_id_value_at_party_roles_tab())
    # print(edit_wizard.get_party_role_value_at_party_roles_tab())
    # print(edit_wizard.get_ext_id_client_value_at_party_roles_tab())
    # print(edit_wizard.get_party_role_qualifier_value_at_party_roles_tab())
    # print(edit_wizard.get_venue_value_at_party_roles_tab())


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    # Stubs.factory.close()
