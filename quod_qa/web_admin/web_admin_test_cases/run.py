import logging
from datetime import datetime
from stubs import Stubs
from custom import basic_custom_actions as bca
from quod_qa.web_admin import QAP_758, login_logout_example

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False

channels = dict()

test_cases = {
    '303': [login_logout_example,
            QAP_758,
            ],
    '305': [login_logout_example,
            ]
}

# NOTE: for now the following code is using only to check implementation of pages. It will be updated in the future
def test_run():
    # Generation ID and time for test run
    report_id = bca.create_event(f'{Stubs.custom_config["web_admin_login"]} tests '
                                 + datetime.now().strftime('%Y%m%d-%H:%M:%S'))
    logger.info(f"Root event was created (id = {report_id.id})")

    # content


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()
