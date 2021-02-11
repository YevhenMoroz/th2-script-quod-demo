import logging
from datetime import datetime
from custom import basic_custom_actions as bca
from stubs import Stubs
from th2_grpc_sim_quod.sim_pb2 import TemplateQuodNOSRule, TemplateQuodOCRRule
from th2_grpc_common.common_pb2 import ConnectionID
from test_cases import QAP_1641
from test_cases import QAP_1987
from test_cases import QAP_2407
from test_cases import QAP_2409
from test_cases import QAP_2425_SIM
from test_cases import QAP_2462_SIM
from test_cases import QAP_2540
from test_cases import QAP_2561
from test_cases import QAP_2620
from test_cases import QAP_2684
from test_cases import QAP_2702
from test_cases import QAP_2740
from test_cases import QAP_2769
from th2_grpc_sim.sim_pb2 import RuleID
from win_gui_modules.utils import prepare_fe, close_fe
from google.protobuf.empty_pb2 import Empty


logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False

channels = dict()


def test_run():
    # Generation id and time for test run
    report_id = bca.create_event('QUOD demo ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))
    logger.info(f"Root event was created (id = {report_id.id})")
    # Reference data for test cases

    instrument = {
        'Symbol': 'FR0000121329',
        'SecurityID': 'FR0000121329',
        'SecurityIDSource': '4',
        'SecurityExchange': 'XPAR'

    }

    instrument_2 = {
        'Symbol': 'SE0000818569_SEK',
        'SecurityID': 'SE0000818569',
        'SecurityIDSource': '4',
        'SecurityExchange': 'XSTO'
    }
    instrument_3 = {
        'Symbol': 'FR0010263202_EUR',
        'SecurityID': 'FR0010263202',
        'SecurityIDSource': 4,
        'SecurityExchange': 'XPAR'
    }

    instrument_4 = {
        'Symbol': 'FR0000125007',
        'SecurityID': 'FR0000125007',
        'SecurityIDSource': '4',
        'SecurityExchange': 'XPAR'
    }
    instrument_5 = {
        'Symbol': 'FR0010542647_EUR',
        'SecurityID': 'FR0010542647',
        'SecurityIDSource': '4',
        'SecurityExchange': 'XPAR'
    }

    instrument_6 = {
        'Symbol': 'FR0000125460_EUR',
        'SecurityID': 'FR0000125460',
        'SecurityIDSource': '4',
        'SecurityExchange': 'XPAR'
    }

    # Specific data for test case test
    test_cases = {
        'QAP-2425': {
            **channels,
            'case_id': bca.create_event_id(),
            'TraderConnectivity': 'gtwquod3',
            'Account': 'KEPLER',
            'HandlInst': '2',
            'Side': '1',
            'SenderCompID': 'QUODFX_UAT',
            'TargetCompID': 'QUOD3',
            'OrderQty': '500',
            'OrdType': '2',
            'Price': '20',
            'TimeInForce': '0',
            'Instrument': instrument_3
        },
        'QAP-2422': {
            **channels,
            'case_id': bca.create_event_id(),
            'TraderConnectivity': 'gtwquod3',
            'SenderCompID': 'QUODFX_UAT',
            'TargetCompID': 'QUOD3',
            'Account': 'KEPLER',
            'HandlInst': '2',
            'Side': '1',
            'OrderQty': '400',
            'OrdType': '2',
            'Price': '20',
            'TimeInForce': '0',
            'Instrument': instrument_2
        },
        'QAP-AMEND': {
            **channels,
            'case_id': bca.create_event_id(),
            'TraderConnectivity': 'gtwquod3',
            'SenderCompID': 'QUODFX_UAT',
            'TargetCompID': 'QUOD3',
            'Account': 'KEPLER',
            'HandlInst': '2',
            'Side': '1',
            'OrderQty': '400',
            'newOrderQty': '500',
            'OrdType': '2',
            'Price': '20',
            'newPrice': '19',
            'TimeInForce': '0',
            'Instrument': instrument_3
        },
        'QUOD-TRADE': {
            **channels,
            'case_id': bca.create_event_id(),
            'TraderConnectivity': 'gtwquod3',
            'SenderCompID': 'QUODFX_UAT',
            'Account': 'KEPLER',
            'HandlInst': '2',
            'OrderQty': '500',
            'OrdType': '2',
            'Price': '20',
            'TimeInForce': '0',
            'TargetCompID': 'QUOD3',
            'Instrument': instrument_2
        },
        'QUOD-TRADE2': {
            **channels,
            'case_id': bca.create_event_id(),
            'TraderConnectivity': 'gtwquod3',
            'SenderCompID': 'QUODFX_UAT',
            'Account': 'KEPLER',
            'HandlInst': '1',
            'OrderQty_ord1': '200',
            'OrderQty_ord2': '100',
            'OrdType': '2',
            'Price': '20',
            'TimeInForce': '0',
            'TargetCompID': 'QUOD3',
            'Instrument': instrument_2
        },
        'QUOD-AMEND-TRADE': {
            **channels,
            'case_id': bca.create_event_id(),
            'TraderConnectivity': 'gtwquod3',
            'SenderCompID': 'QUODFX_UAT',
            'Account': 'KEPLER',
            'HandlInst': '2',
            'OrderQty': '500',
            'OrdType': '2',
            'Price1': '20',
            'Price2': '23',
            'TimeInForce': '0',
            'TargetCompID': 'QUOD3',
            'Instrument': instrument_2
        },
        'QUOD_PART_TRADE': {
            **channels,
            'case_id': bca.create_event_id(),
            'TraderConnectivity': 'gtwquod3',
            'SenderCompID': 'QUODFX_UAT',
            'Account': 'KEPLER',
            'HandlInst': '2',
            'OrderQty1': '500',
            'OrderQty2': '800',
            'OrdType': '2',
            'Price': '20',
            'TimeInForce': '0',
            'TargetCompID': 'QUOD3',
            'Instrument': instrument_2
        },
        'RFQ_example': {
            **channels,
            'case_id': bca.create_event_id(),
            'TraderConnectivity': 'gtwquod5-fx',
            'Account': 'MMCLIENT1',
            'SenderCompID': 'QUODFX_UAT',
            'TargetCompID': 'QUOD5',
        }
    }

    # start rule
    # NOS_1 = Stubs.simulator.createQuodNOSRule(request=TemplateQuodNOSRule(
    #     connection_id=ConnectionID(session_alias='fix-bs-eq-paris')
    # ))
    # OCR_1 = Stubs.simulator.createQuodOCRRule(request=TemplateQuodOCRRule(
    #     connection_id=ConnectionID(session_alias='fix-bs-eq-paris')))
    # NOS_2 = Stubs.simulator.createQuodNOSRule(request=TemplateQuodNOSRule(
    #     connection_id=ConnectionID(session_alias='fix-bs-eq-trqx')
    # ))
    # OCR_2 = Stubs.simulator.createQuodOCRRule(request=TemplateQuodOCRRule(
    #     connection_id=ConnectionID(session_alias='fix-bs-eq-trqx')))
    # logger.info(f"Start rules with id's: \n {NOS_1}, {OCR_1}, {NOS_2}, {OCR_2}")

    try:
        # amend_and_trade.execute('QUOD-AMEND-TRADE', report_id, test_cases['QUOD-AMEND-TRADE'])
        # part_trade.execute('QUOD_PART_TRADE', report_id, test_cases['QUOD_PART_TRADE'])
        # send_and_amend.execute('QAP-AMEND', report_id, test_cases['QAP-AMEND'])
        # simple_trade2.execute('QUOD-TRADE2', report_id, test_cases['QUOD-TRADE2'])
        # simple_trade.execute('QUOD-TRADE', report_id, test_cases['QUOD-TRADE'])
        # RFQ_example.execute('RFQ_example', report_id, test_cases['RFQ_example'])

        # QAP_1641.execute(report_id)
        QAP_1987.execute(report_id)
        # QAP_2407.execute(report_id)
        # QAP_2409.execute(report_id)
        # QAP_2425_SIM.execute(report_id)
        # QAP_2462_SIM.execute(report_id)
        # QAP_2540.execute(report_id)
        # QAP_2561.execute(report_id)
        # QAP_2620.execute(report_id)
        # QAP_2684.execute(report_id)
        # QAP_2702.execute(report_id)
        # QAP_2740.execute(report_id)
        # QAP_2769.execute(report_id)

    except Exception as e:
        logging.error("Error execution", exc_info=True)

    # stop rule
    # Stubs.core.removeRule(NOS_1)
    # Stubs.core.removeRule(OCR_1)
    # Stubs.core.removeRule(NOS_2)
    # Stubs.core.removeRule(OCR_2)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()
