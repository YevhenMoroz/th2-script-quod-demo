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

    # region Create Institution with default values according to 3rd step
    institution_parameters = {
        "institutionName": "Test_Institution(QAP-5818)",
        "posFlatteningTime": "1635508800000"
    }

    api_message.create_institution(institution_parameters)
    api_manager.send_post_request(api_message)

    api_message.find_all_institution()
    institution_condition = api_manager.get_response_details(response=api_manager.send_get_request(api_message),
                                                             response_name="InstitutionResponse",
                                                             expected_entity_name="Test_Institution(QAP-5818)",
                                                             entity_field_id="institutionName")

    verifier(case_id=case_id, event_name="Check Institution condition", expected_value="",
             actual_value=institution_condition["crossCurrencySettlement"].simple_value)
    # endregion

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
