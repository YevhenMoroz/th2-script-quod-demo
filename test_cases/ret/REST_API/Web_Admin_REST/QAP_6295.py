import os

from custom import basic_custom_actions as bca
from test_cases.wrapper.ret_wrappers import verifier
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.RestApiMessages import RestApiMessages


def execute(report_id):
    case_id = bca.create_event((os.path.basename(__file__)[:-3]), report_id)

    api_message = RestApiMessages()
    api_manager = RestApiManager(session_alias='rest_wa320kuiper', case_id=case_id)
    tested_wash_book_name = "api_wash_book_rule_123"
    response_name = "WashBookRuleResponse"

    # region Create new WashBookRule and Verify response - step 1
    wash_book_rule_params = {
        "washBookRuleName": tested_wash_book_name,
        "institutionID": 1,
        "washBookAccountID": "HAKKIM3",
    }
    api_message.create_wash_book_rule(wash_book_rule_params)
    api_manager.send_post_request(api_message)

    api_message.find_all_wash_book_rule()

    rule_params = api_manager.get_response_details(
        response=api_manager.send_get_request(api_message),
        response_name=response_name,
        expected_entity_name=tested_wash_book_name,
        entity_field_id="washBookRuleName")
    rule_id = ""
    try:
        verifier(case_id=case_id,
                 event_name="Check WashBookRule status",
                 expected_value="true",
                 actual_value=rule_params['alive'].simple_value)
        print(rule_params)
        rule_id = rule_params["washBookRuleID"].simple_value
    except:
        bca.create_event(f'Fail test event. Response is empty',
                         status='FAILED',
                         parent_id=case_id)
    # endregion
    print(rule_id)
    # region Modify created WashBookRule and Verify response - step 2
    modify_wash_book_rule_params = {
        'washBookRuleID': rule_id,
        "washBookRuleName": tested_wash_book_name,
        "instrType": "EQU",
        "washBookAccountID": "HAKKIM3",
        "institutionID": 1
    }

    print(modify_wash_book_rule_params['washBookRuleID'])
    api_message.modify_wash_book_rule(modify_wash_book_rule_params)
    api_manager.send_post_request(api_message)

    api_message.find_all_wash_book_rule()
    modified_rule_params = api_manager.get_response_details(
        response=api_manager.send_get_request(api_message),
        response_name=response_name,
        expected_entity_name=modify_wash_book_rule_params['washBookRuleID'],
        entity_field_id="washBookRuleID")
    print(modified_rule_params)
    try:
        verifier(case_id=case_id,
                 event_name="Check new field for WashBookRule ",
                 expected_value="EQU",
                 actual_value=modified_rule_params['instrType'].simple_value)
    except:
        bca.create_event(f'Fail test event. Response is empty',
                         status='FAILED',
                         parent_id=case_id)
    # endregion

    # region Delete WashBookRule - step 3
    api_message.delete_wash_book_rule(wash_book_rule_id=rule_id)
    api_manager.send_post_request(api_message)

    api_message.find_all_wash_book_rule()
    try:
        response = api_manager.send_get_request(api_message)
        for count in range(len(response.fields[response_name].list_value.values)):
            entity = response.fields[response_name].list_value.values[count].message_value.fields[
                "washBookRuleName"].simple_value
            if entity == tested_wash_book_name:
                bca.create_event(f'Fail test event, {tested_wash_book_name} not deleted on the Web Admin',
                                 status='FAILED',
                                 parent_id=case_id)
                break
    except:
        bca.create_event(f'Fail test event. Response is empty',
                         status='FAILED',
                         parent_id=case_id)
    # endregion
