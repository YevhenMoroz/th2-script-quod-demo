import os

from custom import basic_custom_actions as bca
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.RestApiMessages import RestApiMessages


def check_wash_book_rule(response, response_name, tested_wash_book_rule_name, case_id):
    wash_book_rule_status = True
    for count in range(len(response.fields[response_name].list_value.values)):
        entity = response.fields[response_name].list_value.values[count].message_value.fields[
            "washBookRuleName"].simple_value
        if entity == tested_wash_book_rule_name:
            bca.create_event(f'Fail test event, {tested_wash_book_rule_name} is present on the Web Admin',
                             status='FAILED',
                             parent_id=case_id)
            wash_book_rule_status = False
            break
    if wash_book_rule_status:
        bca.create_event(f'Passed test event, {tested_wash_book_rule_name} is not present on the Web Admin',
                         parent_id=case_id)


def execute(report_id):
    case_id = bca.create_event((os.path.basename(__file__)[:-3]), report_id)

    api_message = RestApiMessages()
    api_manager = RestApiManager(session_alias='rest_wa320kuiper', case_id=case_id)
    tested_wash_book_rule_name = "api_wash_book_rule_6302"
    response_name = "WashBookRuleResponse"

    # region Create new WashBookRule without required field - institutionID and Verify response - step 1
    wash_book_rule_params = {
        "washBookRuleName": tested_wash_book_rule_name,
        "washBookAccountID": "HAKKIM3",
    }
    api_message.create_wash_book_rule(wash_book_rule_params)
    api_manager.send_post_request(api_message)

    api_message.find_all_wash_book_rule()

    try:
        response = api_manager.send_get_request(api_message)
        check_wash_book_rule(response, response_name, tested_wash_book_rule_name, case_id)
    except:
        bca.create_event(f'Fail test event. Response is empty',
                         status='FAILED',
                         parent_id=case_id)
    # endregion

    # region Create new WashBookRule without required field - washBookAccountID and Verify response - step 2
    wash_book_rule_params = {
        "washBookRuleName": tested_wash_book_rule_name,
        "institutionID": 1,
    }

    api_message.create_wash_book_rule(wash_book_rule_params)
    api_manager.send_post_request(api_message)

    api_message.find_all_wash_book_rule()

    try:
        response = api_manager.send_get_request(api_message)
        check_wash_book_rule(response, response_name, tested_wash_book_rule_name, case_id)
    except:
        bca.create_event(f'Fail test event. Response is empty',
                         status='FAILED',
                         parent_id=case_id)
    # endregion

    # region Create new WashBookRule without required field - washBookRuleName and Verify response - step 3
    wash_book_rule_params = {
        "washBookAccountID": "HAKKIM3",
        "institutionID": 1,
    }

    api_message.create_wash_book_rule(wash_book_rule_params)
    api_manager.send_post_request(api_message)

    api_message.find_all_wash_book_rule()

    try:
        response = api_manager.send_get_request(api_message)
        check_wash_book_rule(response, response_name, tested_wash_book_rule_name, case_id)
    except:
        bca.create_event(f'Fail test event. Response is empty',
                         status='FAILED',
                         parent_id=case_id)
    # endregion
