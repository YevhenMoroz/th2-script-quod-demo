from enum import Enum


class EnvironmentType(Enum):
    quod316_ganymede_standard = "quod316_ganymede_standard"
    quod316_ganymede_redburn = "quod316_ganymede_redburn"
    quod310_columbia_standard = "quod310_columbia_standard"
    quod314_luna_standard = "quod314_luna_standard"
    quod314_luna_web_admin = "quod314_luna_web_admin"
    quod314_luna_fe = "quod314_luna_fe"
    quod317_ganymede_standard_test = "quod317_ganymede_standard_test"
    quod317_ganymede_standard = "quod317_ganymede_standard"
    quod317_fe = "quod317_fe"
    quod316_fe = "quod316_fe"
    quod317_java_api = "quod317_java_api"
    quod317_read_log = 'quod317_read_log'


    #region web admin
    quod306_web_admin_saturn_chrome = "quod306_web_admin_saturn_chrome"
    quod306_web_admin_saturn_firefox = "quod306_web_admin_saturn_firefox"
    #endregion
    #region web trading
    quod315_web_trading_luna_chrome = "quod315_web_trading_luna_chrome"
    #endregion
