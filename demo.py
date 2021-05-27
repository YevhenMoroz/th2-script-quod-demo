import logging
from datetime import datetime
from custom import basic_custom_actions as bca
from quod_qa.fx.fx_mm_esp import test, QAP_1560

from stubs import Stubs


logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False

channels = dict()


def test_run():
    # Generation id and time for test run

    # report_id = bca.create_event(' tests ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))

    report_id = bca.create_event('FIX_ESP_308' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))

    logger.info(f"Root event was created (id = {report_id.id})")

    test_cases = {
        'RFQ_example': {
            **channels,
            'case_id': bca.create_event_id(),
            'TraderConnectivity': 'gtwquod5-fx',
            'Account': 'MMCLIENT1',
            'SenderCompID': 'QUODFX_UAT',
            'TargetCompID': 'QUOD5',
            },
        'QAP_1558': {
            **channels,
            'case_id': bca.create_event_id(),
            'Connectivity': 'fix-ss-308-mercury-standard'
            # 'Connectivity': 'fix-qsesp-303'
        },
        'QAP_1520': {
            **channels,
            'case_id': bca.create_event_id(),
            'Connectivity': 'fix-ss-308-mercury-standard'
            # 'Connectivity': 'fix-qsesp-303'
        },
        'QAP_1518': {
            **channels,
            'case_id': bca.create_event_id(),
            'Connectivity': 'fix-ss-308-mercury-standard'
            # 'Connectivity': 'fix-qsesp-303'
        },
        'QAP_2086': {
            **channels,
            'case_id': bca.create_event_id(),
            'Connectivity': 'fix-ss-308-mercury-standard'
            # 'Connectivity': 'fix-qsesp-303'
        },
        'QAP_2084': {
            **channels,
            'case_id': bca.create_event_id(),
            'Connectivity': 'fix-ss-308-mercury-standard'
            # 'Connectivity': 'fix-qsesp-303'
        },
        'QAP_2085': {
            **channels,
            'case_id': bca.create_event_id(),
            'Connectivity': 'fix-ss-308-mercury-standard'
            # 'Connectivity': 'fix-qsesp-303'
        },
        'QAP_3841': {
            **channels,
            'case_id': bca.create_event_id(),
            'Connectivity': 'fix-ss-308-mercury-standard'
            # 'Connectivity': 'fix-qsesp-303'
        },
        'QAP_1559': {
            **channels,
            'case_id': bca.create_event_id(),
            'Connectivity': 'fix-ss-308-mercury-standard'
            # 'Connectivity': 'fix-qsesp-303'
        },
        'QAP_2797': {
            **channels,
            'case_id': bca.create_event_id(),
            # 'Connectivity': 'fix-ss-308-mercury-standard'
            'Connectivity': 'fix-qsesp-303'
        },
        'QAP_2079': {
            **channels,
            'case_id': bca.create_event_id(),
            'Connectivity': 'fix-ss-308-mercury-standard'
            # 'Connectivity': 'fix-qsesp-303'
        },
        'test': {
            **channels,
            'case_id': bca.create_event_id(),
            'Connectivity': 'fix-ss-308-mercury-standard'
            # 'Connectivity': 'fix-qsesp-303'
        },
        'QAP_1554': {
            **channels,
            'case_id': bca.create_event_id(),
            'Connectivity': 'fix-ss-308-mercury-standard'
            # 'Connectivity': 'fix-qsesp-303'
        },
        'QAP_1597': {
            **channels,
            'case_id': bca.create_event_id(),
            'Connectivity': 'fix-ss-308-mercury-standard'
            # 'Connectivity': 'fix-qsesp-303'
        },
        'QAP_4094': {
            **channels,
            'case_id': bca.create_event_id(),
            'Connectivity': 'fix-ss-308-mercury-standard'
            # 'Connectivity': 'fix-qsesp-303'
        },
        'SendMD': {
            **channels,
            'case_id': bca.create_event_id(),
            'Connectivity': 'fix-fh-314-luna'
            # 'Connectivity': 'fix-qsesp-303'
        },
        'qap_3390': {
            **channels,
            'case_id': bca.create_event_id(),
            'Connectivity': 'fix-fh-314-luna'
            # 'Connectivity': 'fix-qsesp-303'
        },
        'qap_2750': {
            **channels,
            'case_id': bca.create_event_id(),
            'Connectivity': 'fix-fh-314-luna'
            # 'Connectivity': 'fix-qsesp-303'
        },
        'qap_1560': {
            **channels,
            'case_id': bca.create_event_id(),
            'Connectivity': 'fix-fh-314-luna'
            # 'Connectivity': 'fix-qsesp-303'
        },
        }
    try:

        # QAP_1518.execute(report_id)
        # QAP_2086.execute(report_id)
        # QAP_2084.execute(report_id)
        # QAP_2085.execute(report_id)
        # QAP_3841.execute(report_id)
        # QAP_2079.execute(report_id)
        # QAP_2797.execute(report_id)
        # # QAP_1558.execute(report_id)
        # QAP_1559.execute(report_id)
        # QAP_1554.execute(report_id)
        # QAP_1597.execute(report_id)
        # QAP_4094.execute(report_id)
        # QAP_3555_bloked.execute(report_id)
        # test.execute(report_id)
        # SendMD.execute(report_id)
        # QAP_3390.execute(report_id)
        # QAP_2750.execute(report_id)
        QAP_1560.execute(report_id)

        # QAP_1012.execute(report_id)
        # not_ready_QAP_1597.TestCase(report_id).execute()
        # frommeth.execute(report_id)
        # test.execute(report_id)
        # QAP_2082.TestCase(report_id).execute()
        # QAP_1520.TestCase(report_id).execute()




        # QAP_2797.TestCase(report_id).execute()

        # QAP_2956.execute('QAP-2956', report_id, test_cases['QAP-2956'])
        # QAP_1746.execute(report_id, test_cases['RFQ_example'])
        # TEST_QAP_2000.execute(report_id)
        # QAP_585.execute(report_id)
        # QAP_568.execute(report_id)
        # QAP_569.execute(report_id)
        # QAP_570.execute(report_id)
        # testing.execute(report_id)
        # QAP_574.execute(report_id)
        # QAP_578.execute(report_id)
        # QAP_579.execute(report_id)
        # QAP_580.execute(report_id)

        # rfq_tile_example.execute(report_id)

        # rm = RuleManager()
        # rm.print_active_rules()
        # rm.remove_rule_by_id()


    except Exception:
        logging.error("Error execution",exc_info=True)
   # try:
#
    #    rm = RuleManager()
#
   #     rm.print_active_rules()
#
    #   ui_tests.execute(report_id)

    #except Exception:
        #logging.error("Error execution", exc_info=True)

if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()

