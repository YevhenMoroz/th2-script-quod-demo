import logging
from datetime import datetime

from test_framework.db_wrapper.db_manager import DBManager

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class PreConditionForPosition:
    def __init__(self, environment):
        self._environment = environment
        self._db_manager = DBManager(environment.get_list_data_base_environment()[0])

    def add_record_or_updating_fields_in_daily_posit_table(self, account, instr_id, currency):
        try:
            today_date = datetime.strftime(datetime.now(), "%Y%m%d")
            out = self._db_manager.execute_query(
                f"SELECT * FROM dailyposit WHERE clearingbusinessdate = '{today_date}' AND accountid = '{account}' AND instrid = '{instr_id}'")
            if out == ():
                self._insert_request(today_date, account, instr_id, currency)
            else:
                self._update_query(today_date, account, instr_id)
        finally:
            self._db_manager.close_connection()

    def _insert_request(self, today_date, account, instr_id, currency):
        query = f"""INSERT INTO dailyposit (accountid,instrid, positiontype, clearingbusinessdate, dailyfeeamt,
                        dailyagentfeeamt,dailyclientcommission,dailyrealizedgrosspl,dailyrealizednetpl, dailynetbuyexecamt,
                        dailynetsellexecamt,dailygrossbuyexecamt, dailygrosssellexecamt, currency, alive, originator)
                                           VALUES ('{account}','{instr_id}','N', '{today_date}','0','0','0','1','1','0','0','0','0','{currency}','Y','PKS');"""
        self._db_manager.update_insert_query(query)

    def _update_query(self, today_date, account, instr_id):
        query = f"""UPDATE  dailyposit SET  dailyrealizedgrosspl = 1, dailyrealizednetpl = 1, dailynetbuyexecamt=0,
                       dailynetsellexecamt = 0, dailygrossbuyexecamt=0 ,dailygrosssellexecamt=0 
                        WHERE accountid = '{account}' AND clearingbusinessdate = '{today_date}' AND instrid = '{instr_id}';"""
        self._db_manager.update_insert_query(query)

    def reset_values_for_posit_table(self, account, instr_id):
        query = f"""UPDATE  posit SET  cumbuyqty = 0, cumsellqty = 0, positqty=0,
                               netweightedavgpx = 1, cumbuyamt=0 ,cumsellamt=0,
                                transferredinamt = 0, transferredoutamt=0,
                                buyavgpx = 0, sellavgpx = 0
                                WHERE accountid = '{account}'  AND instrid = '{instr_id}';"""
        self._db_manager.update_insert_query(query)
