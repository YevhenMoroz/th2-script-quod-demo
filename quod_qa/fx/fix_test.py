import logging
import os
from datetime import datetime
from custom import basic_custom_actions as bca

from quod_qa.wrapper.fix_manager import FixManager
from quod_qa.wrapper.fix_message import FixMessage
from quod_qa.wrapper.fix_verifier import FixVerifier
from rule_management import RuleManager

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id):


    connectivity = 'fix-ss-308-mercury-standard'
    case_id = bca.create_event(os.path.basename(__file__), report_id)
    fix_manager_308 = FixManager(connectivity, case_id)





    md_req_params = {
        'Account': "CLIENT1",
        'HandlInst': "2",
        'Side': "2",
        'OrderQty': "1000000",
        'TimeInForce': "3",
        'Price': "1",
        'OrdType': "2",
        'TransactTime': datetime.utcnow().isoformat(),
        'Currency': 'EUR',
        'Instrument': {
            'Symbol': 'EUR/USD'
        },
        'SettlType': '0',
        'SettlDate': '20210311',
        'SecurityType': 'FXSPOT'

    }

    fix_message_nos = FixMessage(md_req_params)
    fix_message_nos.add_random_ClOrdID()
    fix_manager_308.Send_NewOrderSingle_FixMessage(fix_message_nos)