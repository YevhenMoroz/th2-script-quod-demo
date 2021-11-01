import os

from th2_grpc_act_rest_quod.act_rest_quod_pb2 import SubmitMessageRequest

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import convert_to_get_request, wrap_message, create_check_rule, wrap_filter
from quod_qa.wrapper.ret_wrappers import verifier
from stubs import Stubs
from quod_qa.wrapper.RestApiManager import RestApiManager
from quod_qa.wrapper.RestApiMessages import RestApiMessages


def execute(report_id):

    case_id = bca.create_event((os.path.basename(__file__)[:-3]), report_id)

    api_message = RestApiMessages()
    api_manager = RestApiManager(session_alias='rest_wa315luna', case_id=case_id)

    institution_params = {
        "BIC": "RIN",
        "alive": "true",
        "crossCurrencySettlement": "true",
        "institutionID": 1,
        "institutionName": "REFINITIV INDIA",
        "posFlatteningTime": "1635508800000"
    }

    api_message.modify_institution(institution_params)
    api_manager.send_post_request(api_message)
    api_message.find_all_institution()
    cross_currency_settlement = api_manager.get_response_details(response=api_manager.send_get_request(api_message),
                                                                 response_name="InstitutionResponse",
                                                                 expected_entity_name="REFINITIV INDIA",
                                                                 entity_field_id="institutionName")
    print(type(cross_currency_settlement))
    verifier(case_id=case_id, event_name="Verify bla-bla", expected_value="true",
             actual_value=cross_currency_settlement["crossCurrencySettlement"].simple_value)


    # endregion