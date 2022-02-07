from test_framework.data_sets.constants import Connectivity


class SessionAliasOMS:
    def __init__(self):
        self.bs_connectivity = Connectivity.Ganymede_317_bs.value
        self.ss_connectivity = Connectivity.Ganymede_317_ss.value
        self.dc_connectivity = Connectivity.Ganymede_317_dc.value
        self.wa_connectivity = Connectivity.Ganymede_317_wa.value
        self.ja_connectivity = Connectivity.Ganymede_317_ja.value
        self.als_email_report = Connectivity.Ganymede_317_als_email_report.value


class SessionAliasFX:
    def __init__(self):
        self.ss_rfq_connectivity = Connectivity.Luna_314_ss_rfq.value
        self.bs_rfq_connectivity = Connectivity.Luna_314_bs_rfq.value
        self.ss_esp_connectivity = Connectivity.Luna_314_ss_esp.value
        self.ss_esp_t_connectivity = Connectivity.Luna_314_ss_esp_t.value
        self.fx_fh_connectivity = Connectivity.Luna_314_Feed_Handler.value
        self.fx_fh_q_connectivity = Connectivity.Luna_314_Feed_Handler_Q.value
        self.dc_connectivity = Connectivity.Luna_314_dc.value
        self.wa_connectivity = Connectivity.Luna_314_wa.value
