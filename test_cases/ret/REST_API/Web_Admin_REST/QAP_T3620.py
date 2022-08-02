import os

from custom import basic_custom_actions as bca
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.RestApiMessages import RestApiMessages


def execute(report_id):
    case_id = bca.create_event((os.path.basename(__file__)[:-3]), report_id)

    api_message = RestApiMessages()
    api_manager = RestApiManager(session_alias='rest_wa315luna_site_admin', case_id=case_id)
    tested_user = "QA2"
    response_name = "UserSessionResponse"

    # region receive user session_key and send POST request - DropSession - step 2
    api_message.find_all_user_session()
    user_session_params = api_manager.get_response_details(response=api_manager.send_get_request(api_message),
                                                           response_name=response_name,
                                                           expected_entity_name=tested_user,
                                                           entity_field_id="userID")
    print(user_session_params)
    try:
        user_session_key = user_session_params["sessionKey"].simple_value
        api_message.drop_session(user_id=tested_user, role_id="HSD", session_key=user_session_key)
        api_manager.send_post_request(api_message)
    except:
        bca.create_event(f'Fail test event, {tested_user} user session key is not defined',
                         status='FAILED',
                         parent_id=case_id)
    # endregion

    # region Send Get request and verify result - step 2
    api_message.find_all_user_session()
    # Gets user session params after sending DropSession request
    response = api_manager.send_get_request(api_message)
    for count in range(len(response.fields[response_name].list_value.values)):
        entity = response.fields[response_name].list_value.values[count].message_value.fields["userID"].simple_value
        if entity == tested_user:
            bca.create_event(f'Fail test event, {tested_user} user have session after send DropSession request',
                             status='FAILED',
                             parent_id=case_id)
            break
    # endregion
