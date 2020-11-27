import logging
import time
from datetime import datetime
from custom import basic_custom_actions as bca
from grpc_modules.act_fix_pb2_grpc import ActFixStub
from grpc_modules.event_store_pb2_grpc import EventStoreServiceStub
from grpc_modules.verifier_pb2_grpc import VerifierStub


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(case_name, report_id, case_params):
    act = ActFixStub(case_params['act'])
    event_store = EventStoreServiceStub(case_params['event-store'])
    verifier = VerifierStub(case_params['verifier'])

    seconds, nanos = bca.timestamps()  # Store case start time

# Prepare user input
    reusable_order_params = {   # This parameters can be used for ExecutionReport message
        'Account': case_params['Account'],

    }
    instrument_fx = {
        'Symbol': 'EUR/TWD',
        'InstrSymbol': 'EUR/TWD',
        'SecurityType': 'FXFWD',
        # 'SecurityID': 'SE0000818569',
        # 'SecurityIDSource': '4',
        # 'SecurityExchange': 'HSBC'
    }


    specific_order_params = {   # There are reusable and specific for submition parameters
        **reusable_order_params,
        'QuoteReqID': bca.client_orderid(9),
        'NoRelatedSymbols': [{
                                            'Side': '1',
                                            'Currency': 'EUR',
                                            'QuoteType': '1',
                                            'OrderQty': '10000000',
                                            'SettlDate': '20201009',
                                            'OrdType': 'D',
                                            'ExpireTime': '20201010-16:04:48.498',
                                            'TransactTime': (datetime.utcnow().isoformat()),
                                            'Account': 'MMCLIENT1',
                                            'SettlType': 'W1',
                                            'Instrument': instrument_fx}]
    }
    logger.debug("Send new order with ClOrdID = {}".format(specific_order_params['QuoteReqID']))
    # ut = Utils()
    # my_message = ut.build_value(message_type='QuoteRequest', content=specific_order_params)
    # print(bca.message_to_grpc('QuoteRequest', specific_order_params))
    enter_order = act.placeQuoteFIX(
        bca.convert_to_request(
            'Send QuoteRequest',
            case_params['TraderConnectivity'],
            case_params['case_id'],
            # DRAFT.dirty_message
            bca.message_to_grpc('QuoteRequest', specific_order_params)
            # ut.build_value(message_type='QuoteRequest', content=specific_order_params)
        ))

    bca.create_event(event_store, case_name, case_params['case_id'], report_id)  # Create sub-report for case
    logger.info("Case {} was executed in {} sec.".format(
        case_name, str(round(datetime.now().timestamp() - seconds))))