import os


from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.RestApiMessages import RestApiMessages

from custom import basic_custom_actions as bca


def check_wash_book_status(response, response_name, tested_wash_book_name, case_id):
    wash_book_status = True
    for count in range(len(response.fields[response_name].list_value.values)):
        entity = response.fields[response_name].list_value.values[count].message_value.fields[
            "accountID"].simple_value
        if entity == tested_wash_book_name:
            bca.create_event(f'Fail test event, {tested_wash_book_name} is present on the Web Admin',
                             status='FAILED',
                             parent_id=case_id)
            wash_book_status = False
            break
    if wash_book_status:
        bca.create_event(f'Passed test event, {tested_wash_book_name} is not present on the Web Admin',
                         parent_id=case_id)


def execute(report_id):
    case_id = bca.create_event((os.path.basename(__file__)[:-3]), report_id)

    api_message = RestApiMessages()
    api_manager = RestApiManager(session_alias='rest_wa320kuiper', case_id=case_id)

    tested_wash_book_name = 'api_wash_book_6304'
    response_name = "WashBookResponse"

    # region Create new WashBookRule without required field - accountID and Verify response - step 1
    wash_book_params = {
        "accountGroupID": "1",
        "accountDesc": tested_wash_book_name,
        "clientAccountID": tested_wash_book_name,
        "clientAccountIDSource": "BIC",
        "clearingAccountType": "FIR",
        "isWashBook": "true",
        "counterpartID": 1,
        "institutionID": 1,
        "alive": "true"
    }

    api_message.create_security_account(wash_book_params)
    api_manager.send_post_request(api_message)

    api_message.find_all_security_account_washBook()
    response = api_manager.send_get_request(api_message)
    try:
        check_wash_book_status(response, response_name, tested_wash_book_name, case_id)
    except:
        bca.create_event(f'Fail test event. Response is empty',
                         status='FAILED',
                         parent_id=case_id)
    # endregion

    # region Create new WashBookRule without required field - clientAccountIDSource and Verify response - step 2
    wash_book_params = {
        "accountID": tested_wash_book_name,
        "accountGroupID": "1",
        "accountDesc": tested_wash_book_name,
        "clientAccountID": tested_wash_book_name,
        "clearingAccountType": "FIR",
        "isWashBook": "true",
        "counterpartID": 1,
        "institutionID": 1,
        "alive": "true"
    }

    api_message.create_security_account(wash_book_params)
    api_manager.send_post_request(api_message)

    api_message.find_all_security_account_washBook()
    response = api_manager.send_get_request(api_message)
    try:
        check_wash_book_status(response, response_name, tested_wash_book_name, case_id)
    except:
        bca.create_event(f'Fail test event. Response is empty',
                         status='FAILED',
                         parent_id=case_id)
    # endregion

        # region Create new WashBookRule without required field - clientAccountIDSource and Verify response - step 3
        wash_book_params = {
            "accountID": tested_wash_book_name,
            "accountGroupID": "1",
            "accountDesc": tested_wash_book_name,
            "clientAccountID": tested_wash_book_name,
            "clearingAccountType": "FIR",
            "isWashBook": "true",
            "counterpartID": 1,
            "institutionID": 1,
            "alive": "true"
        }

        api_message.create_security_account(wash_book_params)
        api_manager.send_post_request(api_message)

        api_message.find_all_security_account_washBook()
        response = api_manager.send_get_request(api_message)
        try:
            check_wash_book_status(response, response_name, tested_wash_book_name, case_id)
        except:
            bca.create_event(f'Fail test event. Response is empty',
                             status='FAILED',
                             parent_id=case_id)
        # endregion