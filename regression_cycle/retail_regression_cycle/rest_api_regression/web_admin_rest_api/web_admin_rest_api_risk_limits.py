from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from test_cases.ret.REST_API.Web_Admin_REST.Risk_Limits_API.QAP_T3128 import QAP_T3128
from test_cases.ret.REST_API.Web_Admin_REST.Risk_Limits_API.QAP_T3129 import QAP_T3129
from test_cases.ret.REST_API.Web_Admin_REST.Risk_Limits_API.QAP_T3130 import QAP_T3130
from test_cases.ret.REST_API.Web_Admin_REST.Risk_Limits_API.QAP_T3142 import QAP_T3142
from test_cases.ret.REST_API.Web_Admin_REST.Risk_Limits_API.QAP_T3152 import QAP_T3152
from test_cases.ret.REST_API.Web_Admin_REST.Risk_Limits_API.QAP_T3153 import QAP_T3153
from test_cases.ret.REST_API.Web_Admin_REST.Risk_Limits_API.QAP_T3154 import QAP_T3154
from test_cases.ret.REST_API.Web_Admin_REST.Risk_Limits_API.QAP_T3155 import QAP_T3155
from test_cases.ret.REST_API.Web_Admin_REST.Risk_Limits_API.QAP_T3156 import QAP_T3156
from test_cases.ret.REST_API.Web_Admin_REST.Risk_Limits_API.QAP_T3157 import QAP_T3157
from test_cases.ret.REST_API.Web_Admin_REST.Risk_Limits_API.QAP_T3158 import QAP_T3158
from test_cases.ret.REST_API.Web_Admin_REST.Risk_Limits_API.QAP_T3159 import QAP_T3159
from test_cases.ret.REST_API.Web_Admin_REST.Risk_Limits_API.QAP_T3160 import QAP_T3160
from test_cases.ret.REST_API.Web_Admin_REST.Risk_Limits_API.QAP_T3161 import QAP_T3161
from test_cases.ret.REST_API.Web_Admin_REST.Risk_Limits_API.QAP_T3162 import QAP_T3162
from test_cases.ret.REST_API.Web_Admin_REST.Risk_Limits_API.QAP_T3163 import QAP_T3163
from test_cases.ret.REST_API.Web_Admin_REST.Risk_Limits_API.QAP_T3164 import QAP_T3164
from test_cases.ret.REST_API.Web_Admin_REST.Risk_Limits_API.QAP_T3165 import QAP_T3165
from test_cases.ret.REST_API.Web_Admin_REST.Risk_Limits_API.QAP_T3166 import QAP_T3166
from test_cases.ret.REST_API.Web_Admin_REST.Risk_Limits_API.QAP_T3167 import QAP_T3167
from test_cases.ret.REST_API.Web_Admin_REST.Risk_Limits_API.QAP_T3168 import QAP_T3168
from test_cases.ret.REST_API.Web_Admin_REST.Risk_Limits_API.QAP_T3169 import QAP_T3169
from test_cases.ret.REST_API.Web_Admin_REST.Risk_Limits_API.QAP_T3170 import QAP_T3170
from test_cases.ret.REST_API.Web_Admin_REST.Risk_Limits_API.QAP_T3171 import QAP_T3171
from test_cases.ret.REST_API.Web_Admin_REST.Risk_Limits_API.QAP_T3172 import QAP_T3172
from test_cases.ret.REST_API.Web_Admin_REST.Risk_Limits_API.QAP_T3173 import QAP_T3173
from test_cases.ret.REST_API.Web_Admin_REST.Risk_Limits_API.QAP_T3174 import QAP_T3174
from test_cases.ret.REST_API.Web_Admin_REST.Risk_Limits_API.QAP_T3196 import QAP_T3196
from test_cases.ret.REST_API.Web_Admin_REST.Risk_Limits_API.QAP_T3203 import QAP_T3203
from test_cases.ret.REST_API.Web_Admin_REST.Risk_Limits_API.QAP_T3214 import QAP_T3214
from test_cases.ret.REST_API.Web_Admin_REST.Risk_Limits_API.QAP_T3217 import QAP_T3217
from test_cases.ret.REST_API.Web_Admin_REST.Risk_Limits_API.QAP_T3263 import QAP_T3263
from test_cases.ret.REST_API.Web_Admin_REST.Risk_Limits_API.QAP_T3271 import QAP_T3271
from test_cases.ret.REST_API.Web_Admin_REST.Risk_Limits_API.QAP_T8618 import QAP_T8618
from test_cases.ret.REST_API.Web_Admin_REST.Risk_Limits_API.QAP_T8620 import QAP_T8620
from test_cases.ret.REST_API.Web_Admin_REST.Risk_Limits_API.QAP_T8621 import QAP_T8621
from test_cases.ret.REST_API.Web_Admin_REST.Risk_Limits_API.QAP_T8622 import QAP_T8622
from test_cases.ret.REST_API.Web_Admin_REST.Risk_Limits_API.QAP_T8623 import QAP_T8623
from test_framework.configurations.component_configuration import ComponentConfiguration

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()


def test_run(parent_id=None):
    report_id = bca.create_event("WA_REST_API_Risk_Limits", parent_id)
    configuration_admin_api_risk_limits = ComponentConfiguration("WA_REST_API_Risk_Limits")
    try:
        QAP_T3128(report_id, configuration_admin_api_risk_limits.data_set,
                  configuration_admin_api_risk_limits.environment).execute()
        QAP_T3129(report_id, configuration_admin_api_risk_limits.data_set,
                  configuration_admin_api_risk_limits.environment).execute()
        QAP_T3130(report_id, configuration_admin_api_risk_limits.data_set,
                  configuration_admin_api_risk_limits.environment).execute()
        QAP_T3142(report_id, configuration_admin_api_risk_limits.data_set,
                  configuration_admin_api_risk_limits.environment).execute()
        QAP_T3152(report_id, configuration_admin_api_risk_limits.data_set,
                  configuration_admin_api_risk_limits.environment).execute()
        QAP_T3153(report_id, configuration_admin_api_risk_limits.data_set,
                  configuration_admin_api_risk_limits.environment).execute()
        QAP_T3154(report_id, configuration_admin_api_risk_limits.data_set,
                  configuration_admin_api_risk_limits.environment).execute()
        QAP_T3155(report_id, configuration_admin_api_risk_limits.data_set,
                  configuration_admin_api_risk_limits.environment).execute()
        QAP_T3156(report_id, configuration_admin_api_risk_limits.data_set,
                  configuration_admin_api_risk_limits.environment).execute()
        QAP_T3157(report_id, configuration_admin_api_risk_limits.data_set,
                  configuration_admin_api_risk_limits.environment).execute()
        QAP_T3158(report_id, configuration_admin_api_risk_limits.data_set,
                  configuration_admin_api_risk_limits.environment).execute()
        QAP_T3159(report_id, configuration_admin_api_risk_limits.data_set,
                  configuration_admin_api_risk_limits.environment).execute()
        QAP_T3160(report_id, configuration_admin_api_risk_limits.data_set,
                  configuration_admin_api_risk_limits.environment).execute()
        QAP_T3161(report_id, configuration_admin_api_risk_limits.data_set,
                  configuration_admin_api_risk_limits.environment).execute()
        QAP_T3162(report_id, configuration_admin_api_risk_limits.data_set,
                  configuration_admin_api_risk_limits.environment).execute()
        QAP_T3163(report_id, configuration_admin_api_risk_limits.data_set,
                  configuration_admin_api_risk_limits.environment).execute()
        QAP_T3164(report_id, configuration_admin_api_risk_limits.data_set,
                  configuration_admin_api_risk_limits.environment).execute()
        QAP_T3165(report_id, configuration_admin_api_risk_limits.data_set,
                  configuration_admin_api_risk_limits.environment).execute()
        QAP_T3166(report_id, configuration_admin_api_risk_limits.data_set,
                  configuration_admin_api_risk_limits.environment).execute()
        QAP_T3167(report_id, configuration_admin_api_risk_limits.data_set,
                  configuration_admin_api_risk_limits.environment).execute()
        QAP_T3168(report_id, configuration_admin_api_risk_limits.data_set,
                  configuration_admin_api_risk_limits.environment).execute()
        QAP_T3169(report_id, configuration_admin_api_risk_limits.data_set,
                  configuration_admin_api_risk_limits.environment).execute()
        QAP_T3170(report_id, configuration_admin_api_risk_limits.data_set,
                  configuration_admin_api_risk_limits.environment).execute()
        QAP_T3171(report_id, configuration_admin_api_risk_limits.data_set,
                  configuration_admin_api_risk_limits.environment).execute()
        QAP_T3172(report_id, configuration_admin_api_risk_limits.data_set,
                  configuration_admin_api_risk_limits.environment).execute()
        QAP_T3173(report_id, configuration_admin_api_risk_limits.data_set,
                  configuration_admin_api_risk_limits.environment).execute()
        QAP_T3174(report_id, configuration_admin_api_risk_limits.data_set,
                  configuration_admin_api_risk_limits.environment).execute()
        QAP_T3196(report_id, configuration_admin_api_risk_limits.data_set,
                  configuration_admin_api_risk_limits.environment).execute()
        QAP_T3203(report_id, configuration_admin_api_risk_limits.data_set,
                  configuration_admin_api_risk_limits.environment).execute()
        QAP_T3214(report_id, configuration_admin_api_risk_limits.data_set,
                  configuration_admin_api_risk_limits.environment).execute()
        QAP_T3217(report_id, configuration_admin_api_risk_limits.data_set,
                  configuration_admin_api_risk_limits.environment).execute()
        QAP_T3263(report_id, configuration_admin_api_risk_limits.data_set,
                  configuration_admin_api_risk_limits.environment).execute()
        QAP_T3271(report_id, configuration_admin_api_risk_limits.data_set,
                  configuration_admin_api_risk_limits.environment).execute()
        QAP_T8618(report_id, configuration_admin_api_risk_limits.data_set,
                  configuration_admin_api_risk_limits.environment).execute()
        QAP_T8620(report_id, configuration_admin_api_risk_limits.data_set,
                  configuration_admin_api_risk_limits.environment).execute()
        QAP_T8621(report_id, configuration_admin_api_risk_limits.data_set,
                  configuration_admin_api_risk_limits.environment).execute()
        QAP_T8622(report_id, configuration_admin_api_risk_limits.data_set,
                  configuration_admin_api_risk_limits.environment).execute()
        QAP_T8623(report_id, configuration_admin_api_risk_limits.data_set,
                  configuration_admin_api_risk_limits.environment).execute()

    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
