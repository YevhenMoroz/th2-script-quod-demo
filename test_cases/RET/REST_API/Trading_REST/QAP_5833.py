import os
import logging
from datetime import datetime

from th2_grpc_act_rest_quod.act_rest_quod_pb2 import SubmitMessageMultipleResponseRequest, ExpectedMessage
from th2_grpc_common.common_pb2 import ConnectionID
from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd
from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps, wrap_message
from stubs import Stubs
from test_cases.wrapper.RestApiMessages import RestApiMessages
from test_cases.wrapper.RestApiManager import RestApiManager
from test_cases.wrapper.ret_wrappers import verifier

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id):
    case_name = os.path.basename(__file__)

    seconds, nanos = timestamps()

    case_id = bca.create_event((os.path.basename(__file__)[:-3]), report_id)

    api_message = RestApiMessages()
    api_manager = RestApiManager(session_alias='rest_wa315luna', case_id=case_id)

    # region Modify Institution with 'CrossCurrencySettlement" checked according to pre-condition
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

    # region Create Order with needed "SettlCurrency" according to 1st step
    nos_params = {
        'ClOrdID': bca.client_orderid(9),
        'Side': 'Buy',
        'OrdType': 'Limit',
        'Price': 100,
        'SettlCurrency': 'USD',
        'TimeInForce': 'Day',
        'TransactTime': (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y-%m-%dT%H:%M:%S'),
        'ClientAccountGroupID': 'HAKKIM',
        'OrdQty': 10,
        'Instrument': {
            'InstrSymbol': 'INE002A01018',
            'SecurityID': '2885',
            'SecurityIDSource': 'EXC',
            'InstrType': 'Equity',
            'SecurityExchange': 'XNSE'
        }
    }

    nos_request = SubmitMessageMultipleResponseRequest(
        message=wrap_message(nos_params, 'NewOrderSingle', 'trading_ret'),
        parent_event_id=case_id,
        description="Send NewOrderSingle",
        expected_messages=[
            ExpectedMessage(
                message_type='OrderUpdate',
                key_fields={"OrderStatus": "Open"},
                connection_id=ConnectionID(
                    session_alias='api_session_ret'
                )
            )
        ]
    )

    messages_response = Stubs.api_service.submitMessageWithMultipleResponse(nos_request).response_message

    verifier(case_id=case_id, event_name="Check Order Status", expected_value="Open",
             actual_value=messages_response[0].fields["OrderStatus"].simple_value)
    verifier(case_id=case_id, event_name="Check Order SettlCurrency", expected_value="USD",
             actual_value=messages_response[0].fields["SettlCurrency"].simple_value)
    # endregion

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
