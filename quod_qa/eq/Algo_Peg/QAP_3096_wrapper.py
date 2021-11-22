import logging
from datetime import datetime
from custom import basic_custom_actions as bca

from quod_qa.wrapper.fix_manager import FixManager
from test_framework.old_wrappers.fix_message import FixMessage
from quod_qa.wrapper.fix_verifier import FixVerifier

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id):

    case_id = bca.create_event("Test", report_id)
    fix_manager_fh_trqx = FixManager('fix-fh-eq-trqx', case_id)
    fix_manager_qtwquod5 = FixManager('gtwquod5', case_id)
    fix_verifier = FixVerifier('gtwquod5', case_id)

    # NOS = Stubs.simulator.createQuodNOSRule(request=TemplateQuodNOSRule(
    #     connection_id=ConnectionID(session_alias='fix-bs-eq-trqx')
    # ))
    # OCR = Stubs.simulator.createQuodOCRRule(request=TemplateQuodOCRRule(
    #     connection_id=ConnectionID(session_alias='fix-bs-eq-trqx')))
    # OCRR = Stubs.simulator.createQuodOCRRRule(request=TemplateQuodOCRRRule(
    #     connection_id=ConnectionID(session_alias='fix-bs-eq-trqx')))

    seconds, nanos = bca.timestamps()  # Store case start time
    case_params = {
        'TraderConnectivity': 'gtwquod5',
        'TraderConnectivity2': 'fix-bs-eq-trqx',
        'SenderCompID': 'QUODFX_UAT',
        'TargetCompID': 'QUOD3',
        'SenderCompID2': 'KCH_QA_RET_CHILD',
        'TargetCompID2': 'QUOD_QA_RET_CHILD',
        'Account': 'KEPLER',
        'Account2': 'TRQX_KEPLER',
        'HandlInst': '2',
        'Side': '1',
        'OrderQty': 1100,
        'OrdType': '2',
        'Price': 45,
        'TimeInForce': '0',
        'Instrument': {
            'Symbol': 'IT0000076189_EUR',
            'SecurityID': 'IT0000076189',
            'SecurityIDSource': '4',
            'SecurityExchange': 'MTAA'
        }
    }



    symbol = "2320"


    try:



        mdfr_params = {
            'MDReportID': "1",
            'NoMDEntries': [
                {
                    'MDEntryType': '0',
                    'MDEntryPx': '10',
                    'MDEntrySize': '650',
                    'MDEntryPositionNo': '1'
                },
                {
                    'MDEntryType': '1',
                    'MDEntryPx': '11',
                    'MDEntrySize': '500',
                    'MDEntryPositionNo': '1'
                }
        ]}

        mdfr_params_2 = {
            'MDReportID': "1",
            'NoMDEntries': [
                {
                    'MDEntryType': '0',
                    'MDEntryPx': '10.5',
                    'MDEntrySize': '650',
                    'MDEntryPositionNo': '1'
                },
                {
                    'MDEntryType': '1',
                    'MDEntryPx': '11',
                    'MDEntrySize': '500',
                    'MDEntryPositionNo': '1'
                }
        ]}

        # Step 1
        # Send Peg order
        sor_order_params = {
            'Account': "CLIENT1",
            'HandlInst': "2",
            'Side': "1",
            'OrderQty': "200",
            'TimeInForce': "0",
            'Price': "10.6",
            'OrdType': "2",
            # 'ClOrdID': bca.client_orderid(9),
            'TransactTime': datetime.utcnow().isoformat(),
            'Instrument': {
                'Symbol': 'IT0000076189_EUR',
                'SecurityID': 'IT0000076189',
                'SecurityIDSource': '4',
                'SecurityExchange': 'MTAA'
            },
            'OrderCapacity': 'A',
            'Currency': 'EUR',
            'TargetStrategy': "1009",
            "PegOffsetType": "2",
            "PegOffsetValue": "0",
            "PegPriceType": "5"
        }
        fix_message_peg = FixMessage(sor_order_params)
        response = fix_manager_qtwquod5.Send_NewOrderSingle_FixMessage(fix_message_peg)
        # step 2
        # send MD with BBID 10 BASK 11
        fix_message_md_update = FixMessage(mdfr_params)
        fix_manager_fh_trqx.Send_MarketDataFullSnapshotRefresh_FixMessage(fix_message_md_update, symbol)

        execution_report1_params = {
            'ClOrdID': sor_order_params['ClOrdID'],
            'OrderID': response.response_messages_list[0].fields['OrderID'].simple_value,
            'TransactTime': '*',
            'CumQty': '0',
            'LastPx': '0',
            'LastQty': '0',
            'QtyType': '0',
            'AvgPx': '0',
            'OrdStatus': 'A',
            'ExecType': 'A',
            'LeavesQty': sor_order_params['OrderQty'],
            'Instrument': sor_order_params['Instrument']
        }
        # fix_verifier.CheckExecutionReport(execution_report1_params, response.checkpoint_id)
        reject_params = {
            'ClOrdID': sor_order_params['ClOrdID'],
            'TransactTime': '*',
            'CumQty': '0',
            'LastPx': '0',
            'LastQty': '0',
            'QtyType': '0',
            'AvgPx': '0',
            'OrdStatus': 'A',
            'ExecType': 'A',
            'LeavesQty': sor_order_params['OrderQty'],
            'Instrument': sor_order_params['Instrument']
        }
        fix_verifier.CheckReject(reject_params, response.checkpoint_id)


    except Exception:
        logger.error("Error execution", exc_info=True)
    # finally:

        # Stubs.core.removeRule(NOS)
        # Stubs.core.removeRule(OCR)
        # Stubs.core.removeRule(OCRR)

