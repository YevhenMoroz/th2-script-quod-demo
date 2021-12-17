from test_framework.fix_wrappers.DataSet import Connectivity


class SessionAliasOMS:
    def __init__(self):
        self.bs_connectivity = Connectivity.Ganymede_317_bs.value
        self.ss_connectivity = Connectivity.Ganymede_317_ss.value
        self.dc_connectivity = Connectivity.Ganymede_317_dc.value
        self.wa_connectivity = Connectivity.Ganymede_317_wa.value
        self.ja_connectivity = Connectivity.Ganymede_317_ja.value
