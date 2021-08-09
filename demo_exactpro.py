import logging
from datetime import datetime
from custom import basic_custom_actions as bca
from examples import read_log_SATS_qty, fix_analyzer_probe, example_java_api
from stubs import Stubs
from test_cases import QAP_2715, QAP_2740, QAP_2769, QAP_2540, QAP_2702, QAP_2684_reader

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False

channels = dict()


def test_run():
    # Generation id and time for test run
    report_id = bca.create_event('nrogozhin tests ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))
    logger.info(f"Root event was created (id = {report_id.id})")
    try:

        # QAP_569.TestCase(report_id).execute()
        # QAP_574.TestCase(report_id).execute()
        # QAP_638.TestCase(report_id).execute()
        # QAP_639.TestCase(report_id).execute()
        # QAP_682.TestCase(report_id).execute()
        # QAP_2129.TestCase(report_id).execute()
        # QAP_2505.TestCase(report_id).execute()
        # QAP_2761.TestCase(report_id).execute()
        # QAP_2740.TestCase(report_id).execute()
        # QAP_1557.TestCase(report_id).execute()
        # example_rest_nos.TestCase(report_id).execute()
        # example_java_api.TestCase(report_id).execute()
        # Recon_75496.execute(report_id)
        # TWAP_slices_check.execute(report_id)
        # QAP_1641.execute(report_id)
        # QAP_1951.execute(report_id)
        # QAP_2090.TestCase(report_id).execute()
        # QAP_2407.execute(report_id)
        # QAP_2409.execute(report_id)
        # QAP_2425_SIM.execute(report_id)
        # QAP_2462_SIM.execute(report_id)
        # QAP_2540.execute(report_id)
        # QAP_2740.execute(report_id)
        # QAP_2000.execute(report_id)
        # QAP_2620.execute(report_id)
        # QAP_2684.execute(report_id)
        # QAP_2684_reader.execute(report_id)
        # QAP_2864.execute(report_id)
        # read_log_SATS_qty.execute(report_id)
        # QAP_2702.execute(report_id)
        # QAP_2769.execute(report_id)
        # QAP_2838.execute(report_id)
        # Send_and_replace.execute(report_id)
        fix_analyzer_probe.execute(report_id)
        # NOS_OCRR_OCR.TestCase(report_id).execute()

    except Exception:
        logging.error("Error execution in main part", exc_info=True)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()
