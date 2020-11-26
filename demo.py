from sys import stdout
import logging
from datetime import datetime
from custom import basic_custom_actions as bca
from grpc_modules.event_store_pb2_grpc import EventStoreServiceStub
from grpc_modules.quod_simulator_pb2_grpc import TemplateSimulatorServiceStub
from grpc_modules.simulator_pb2_grpc import ServiceSimulatorStub
from grpc_modules.quod_simulator_pb2 import TemplateQuodNOSRule
from grpc_modules.quod_simulator_pb2 import TemplateQuodOCRRule
from grpc_modules.quod_simulator_pb2 import TemplateQuodMDRRule
from grpc_modules.quod_simulator_pb2 import TemplateQuodSingleExecRule
from grpc_modules.quod_simulator_pb2 import TemplateNoPartyIDs
from grpc_modules.infra_pb2 import ConnectionID
import grpc
from ConfigParser import ParseConfig
from schemas import *

logging.basicConfig(stream=stdout)
logger = logging.getLogger('demo')
logger.setLevel(logging.INFO)
timeouts = False

# TH2 Components addresses retrieval
components = ParseConfig()

logger.debug("Connecting to TH2 components...")
channels = dict()
channels['act'] = grpc.insecure_channel(components['ACT'])
channels['act_1'] = grpc.insecure_channel(components['ACT_1'])
channels['event-store'] = grpc.insecure_channel(components['EVENTSTORAGE'])
channels['verifier'] = grpc.insecure_channel(components['VERIFIER'])
channels['simulator'] = grpc.insecure_channel(components['SIMULATOR'])

event_store = EventStoreServiceStub(channels['event-store'])


def test_run():
    # Generation id and time for test run
    report_id = bca.create_event_id()
    bca.create_event(
        event_store,
        '__quod_demo_1 ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'),
        report_id
    )
    logger.info("Root event was created (report id = {})".format(report_id))
    # Reference data for test cases

    instrument = {
        'Symbol': 'FR0010263202_EUR',
        'SecurityID': 'FR0010263202',
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
        'QAP_2425_SIM': {
            **channels,
            'case_id': bca.create_event_id(),
            'TraderConnectivity': 'gtwquod3',
            'TraderConnectivity2': 'kch-qa-ret-child',
            'SenderCompID': 'QUODFX_UAT',
            'TargetCompID': 'QUOD3',
            'SenderCompID2': 'KCH_QA_RET_CHILD',
            'TargetCompID2': 'QUOD_QA_RET_CHILD',
            'Account': 'KEPLER',
            'HandlInst': '2',
            'Side': '2',
            'OrderQty': '600',
            'OrdType': '2',
            'Price': '20',
            'TimeInForce': '0',
            'ExDestination': 'XPAR',
            'DeliverToCompID': 'PARIS',
            'Instrument': instrument_3
        },
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
        'QAP_2462_SIM': {
            **channels,
            'case_id': bca.create_event_id(),
            'TraderConnectivity': 'gtwquod3',
            'TraderConnectivity2': 'kch-qa-ret-child',
            'SenderCompID': 'QUODFX_UAT',
            'TargetCompID': 'QUOD3',
            'SenderCompID2': 'KCH_QA_RET_CHILD',
            'TargetCompID2': 'QUOD_QA_RET_CHILD',
            'Account': 'KEPLER',
            'HandlInst': '2',
            'Side': '2',
            'OrderQty': '500',
            'OrdType': '2',
            'Price': '20',
            'TimeInForce': '0',
            'ExDestination': 'XPAR',
            'DeliverToCompID': 'PARIS',
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
        },
        'QAP_2409': {
            **channels,
            'case_id': bca.create_event_id(),
            'TraderConnectivity': 'gtwquod3',
            'TraderConnectivity2': 'fix-bs-eq-paris',
            'TraderConnectivity3': 'fix-bs-eq-trqx',
            'SenderCompID': 'QUODFX_UAT',
            'TargetCompID': 'QUOD3',
            'SenderCompID2': 'KCH_QA_RET_CHILD',
            'TargetCompID2': 'QUOD_QA_RET_CHILD',
            'Account': 'KEPLER',
            'Account2': 'TRQX_KEPLER',
            'HandlInst': '2',
            'Side': '1',
            'OrderQty': '1100',
            'OrdType': '2',
            'Price': '45',
            'TimeInForce': '0',
            'Instrument': instrument_5
        },
        'QAP_2684': {
            **channels,
            'case_id': bca.create_event_id(),
            'TraderConnectivity': 'gtwquod3',
            'TraderConnectivity2': 'fix-bs-eq-paris',
            'TraderConnectivity3': 'fix-bs-eq-trqx',
            'SenderCompID': 'QUODFX_UAT',
            'TargetCompID': 'QUOD3',
            'SenderCompID2': 'KCH_QA_RET_CHILD',
            'TargetCompID2': 'QUOD_QA_RET_CHILD',
            'Account': 'KEPLER',
            'Account2': 'TRQX_KEPLER',
            'HandlInst': '2',
            'Side': '1',
            'OrderQty': '1000',
            'OrdType': '2',
            'Price': '20',
            'TimeInForce': '0',
            'TargetStrategy': 1011,
            'Instrument': instrument_6
        },
        'QAP_2540': {
            **channels,
            'case_id': bca.create_event_id(),
            'TraderConnectivity': 'gtwquod3',
            'TraderConnectivity2': 'fix-bs-eq-paris',
            'TraderConnectivity3': 'fix-bs-eq-trqx',
            'SenderCompID': 'QUODFX_UAT',
            'TargetCompID': 'QUOD3',
            'SenderCompID2': 'KCH_QA_RET_CHILD',
            'TargetCompID2': 'QUOD_QA_RET_CHILD',
            'Account': 'KEPLER',
            'Account2': 'TRQX_KEPLER',
            'HandlInst': '2',
            'Side': '1',
            'OrderQty': '400',
            'OrdType': '2',
            'Price': '20',
            'TimeInForce': '0',
            'TargetStrategy': 1004,
            'Instrument': instrument_3
        },

        'QAP_2620': {
            **channels,
            'case_id': bca.create_event_id(),
            'TraderConnectivity': 'gtwquod3',
            'TraderConnectivity2': 'fix-bs-eq-paris',
            'TraderConnectivity3': 'fix-bs-eq-trqx',
            'SenderCompID': 'QUODFX_UAT',
            'TargetCompID': 'QUOD3',
            'SenderCompID2': 'KCH_QA_RET_CHILD',
            'TargetCompID2': 'QUOD_QA_RET_CHILD',
            'Account': 'KEPLER',
            'Account2': 'TRQX_KEPLER',
            'HandlInst': '2',
            'Side': '1',
            'OrderQty': '400',
            'OrdType': '2',
            'Price': '20',
            'TimeInForce': '0',
            'TargetStrategy': 1004,
            'Instrument': instrument_3
        },
        'QAP_2702': {
            **channels,
            'case_id': bca.create_event_id(),
            'TraderConnectivity': 'gtwquod3',
            'Sender': '',
            'SenderCompID': 'QUOD3',
            'TargetCompID': 'QUODFX_UAT',
            'Account': 'KEPLER',
            'HandlInst': '2',
            'Side': '1',
            'OrderQty': '2',
            'OrdType': '2',
            'Price': '1',
            'NewPrice': '2',
            'TimeInForce': '0',
            'Instrument': instrument_5,
            'TargetStrategy': 1011
        },
        'QAP_2561': {
            **channels,
            'case_id': bca.create_event_id(),
            'TraderConnectivity': 'gtwquod3',
            'Sender': '',
            'SenderCompID': 'QUOD3',
            'TargetCompID': 'QUODFX_UAT',
            'Account': 'KEPLER',
            'HandlInst': '2',
            'Side': '1',
            'OrderQty': '400',
            'OrdType': '2',
            'Price': '20',
            'NewPrice': '25',
            'TimeInForce': '0',
            'Instrument': instrument_5,
            'TargetStrategy': 1004
        }
    }

    # start rule
    simulator = TemplateSimulatorServiceStub(channels['simulator'])
    NOS_1 = simulator.createQuodNOSRule(request=TemplateQuodNOSRule(
        connection_id=ConnectionID(session_alias='fix-bs-eq-paris')
    ))
    OCR_1 = simulator.createQuodOCRRule(request=TemplateQuodOCRRule(
        connection_id=ConnectionID(session_alias='fix-bs-eq-paris')))
    NOS_2 = simulator.createQuodNOSRule(request=TemplateQuodNOSRule(
        connection_id=ConnectionID(session_alias='fix-bs-eq-trqx')
    ))
    OCR_2 = simulator.createQuodOCRRule(request=TemplateQuodOCRRule(
        connection_id=ConnectionID(session_alias='fix-bs-eq-trqx')))
    MDR_paris = simulator.createQuodMDRRule(request=TemplateQuodMDRRule(
        connection_id=ConnectionID(session_alias="fix-fh-eq-paris"),
        sender="QUOD_UTP",
        md_entry_size={1000: 1000},
        md_entry_px={40: 30}))
    MDR_turquise = simulator.createQuodMDRRule(request=TemplateQuodMDRRule(
        connection_id=ConnectionID(session_alias="fix-fh-eq-trqx"),
        sender="QUOD_UTP",
        md_entry_size={1000: 1000},
        md_entry_px={40: 30}))
    print(f"Start rules with id's: \n {NOS_1}, {OCR_1}, {NOS_2}, {OCR_2}, {MDR_paris}, {MDR_turquise}")

    # amend_and_trade.execute('QUOD-AMEND-TRADE', report_id, test_cases['QUOD-AMEND-TRADE'])
    # part_trade.execute('QUOD_PART_TRADE', report_id, test_cases['QUOD_PART_TRADE'])
    # QAP_2425_SIM.execute('QAP_2425_SIM', report_id, test_cases['QAP_2425_SIM'])
    # QAP_2462_SIM.execute('QAP_2462_SIM', report_id, test_cases['QAP_2462_SIM'])
    # send_and_amend.execute('QAP-AMEND', report_id, test_cases['QAP-AMEND'])
    # simple_trade2.execute('QUOD-TRADE2', report_id, test_cases['QUOD-TRADE2'])
    # simple_trade.execute('QUOD-TRADE', report_id, test_cases['QUOD-TRADE'])
    # RFQ_example.execute('RFQ_example', report_id, test_cases['RFQ_example'])
    # QAP_2409.execute('QAP_2409', report_id, test_cases['QAP_2409'])
    # QAP_2684.execute('QAP_2684', report_id, test_cases['QAP_2684'])
    # QAP_2561.execute('QAP_2561', report_id, test_cases['QAP_2561'])
    # QAP_2702.execute('QAP_2702', report_id, test_cases['QAP_2702'])
    # QAP_2540.execute('QAP_2540', report_id, test_cases['QAP_2540'])
    QAP_2620.execute('QAP_2620', report_id, test_cases['QAP_2620'])

    # stop rule
    core = ServiceSimulatorStub(channels['simulator'])
    core.removeRule(NOS_1)
    core.removeRule(OCR_1)
    core.removeRule(NOS_2)
    core.removeRule(OCR_2)
    core.removeRule(MDR_paris)
    core.removeRule(MDR_turquise)

    for channel_name in channels.keys():
        channels[channel_name].close()


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
