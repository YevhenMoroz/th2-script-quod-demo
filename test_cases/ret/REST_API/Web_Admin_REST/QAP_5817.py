import os
import logging
from datetime import datetime
from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from test_framework.rest_api_wrappers.RestApiMessages import RestApiMessages
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.old_wrappers.ret_wrappers import verifier

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id):
    case_name = os.path.basename(__file__)

    seconds, nanos = timestamps()

    case_id = bca.create_event((os.path.basename(__file__)[:-3]), report_id)

    api_message = RestApiMessages()
    api_manager = RestApiManager(session_alias='rest_wa315luna', case_id=case_id)

    # region Modify Institution with 'CrossCurrencySettlement" checked according to 3rd step
    institution_parameters = {
        "BIC": "RIN",
        "alive": "true",
        "crossCurrencySettlement": "true",
        "institutionID": 1,
        "institutionName": "REFINITIV INDIA",
        "posFlatteningTime": "1635508800000"
    }

    api_message.modify_institution(institution_parameters)
    api_manager.send_post_request(api_message)

    api_message.find_all_institution()
    institution_condition = api_manager.get_response_details(response=api_manager.send_get_request(api_message),
                                                             response_name="InstitutionResponse",
                                                             expected_entity_name="REFINITIV INDIA",
                                                             entity_field_id="institutionName")

    verifier(case_id=case_id, event_name="Check Institution condition", expected_value="true",
             actual_value=institution_condition["crossCurrencySettlement"].simple_value)
    # endregion

    # region Modify Institution with 'CrossCurrencySettlement" unchecked according to 4th step
    institution_parameters_2 = {
        "BIC": "RIN",
        "alive": "true",
        "crossCurrencySettlement": "false",
        "institutionID": 1,
        "institutionName": "REFINITIV INDIA",
        "posFlatteningTime": "1635508800000"
    }

    api_message.modify_institution(institution_parameters_2)
    api_manager.send_post_request(api_message)

    api_message.find_all_institution()
    institution_condition_2 = api_manager.get_response_details(response=api_manager.send_get_request(api_message),
                                                               response_name="InstitutionResponse",
                                                               expected_entity_name="REFINITIV INDIA",
                                                               entity_field_id="institutionName")

    verifier(case_id=case_id, event_name="Check Institution condition", expected_value="false",
             actual_value=institution_condition_2["crossCurrencySettlement"].simple_value)
    # endregion

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
