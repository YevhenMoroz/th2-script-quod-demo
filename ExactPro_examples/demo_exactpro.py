import logging
from datetime import datetime
from custom import basic_custom_actions as bca
from ExactPro_examples.examples import fix_analyzer_probe
from stubs import Stubs

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

        # QAP_T3070.TestCase(report_id).execute()
        # QAP_T3065.TestCase(report_id).execute()
        # QAP_T3030.TestCase(report_id).execute()
        # QAP_T3029.TestCase(report_id).execute()
        # QAP_T3024.TestCase(report_id).execute()
        # QAP_T2866.TestCase(report_id).execute()
        # QAP_T2805.TestCase(report_id).execute()
        # QAP_T2766.TestCase(report_id).execute()
        # QAP_T4974.TestCase(report_id).execute()
        # QAP_T2967.TestCase(report_id).execute()
        # example_rest_nos.TestCase(report_id).execute()
        # example_java_api.TestCase(report_id).execute()
        # Recon_75496.execute(report_id)
        # TWAP_slices_check.execute(report_id)
        # QAP_T5087.execute(report_id)
        # QAP_T4138.execute(report_id)
        # QAP_T2887.TestCase(report_id).execute()
        # QAP_T5076.execute(report_id)
        # QAP_T5074.execute(report_id)
        # QAP_2425_SIM.execute(report_id)
        # QAP_2462_SIM.execute(report_id)
        # QAP_T5051.execute(report_id)
        # QAP_T4974.execute(report_id)
        # QAP_T7617.execute(report_id)
        # QAP_T5025.execute(report_id)
        # QAP_T4996.execute(report_id)
        # QAP_2684_reader.execute(report_id)
        # QAP_T4946.execute(report_id)
        # read_log_SATS_qty.execute(report_id)
        # QAP_T4991.execute(report_id)
        # QAP_T4960.execute(report_id)
        # QAP_T4950.execute(report_id)
        # Send_and_replace.execute(report_id)
        fix_analyzer_probe.execute(report_id)
        # NOS_OCRR_OCR.TestCase(report_id).execute()

    except Exception:
        logging.error("Error execution in main part", exc_info=True)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()
