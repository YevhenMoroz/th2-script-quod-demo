from enum import Enum


class EnvironmentType(Enum):
    # region fix
    quod316_ganymede_standard = "quod316_ganymede_standard"
    quod316_ganymede_redburn = "quod316_ganymede_redburn"
    quod310_columbia_standard = "quod310_columbia_standard"
    quod314_luna_standard = "quod314_luna_standard"
    quod317_ganymede_standard_test = "quod317_ganymede_standard_test"
    quod317_ganymede_standard = "quod317_ganymede_standard"
    quod319_kuiper_kepler = "quod319_kuiper_kepler"
    quod309_kratos_standard = "quod309_kratos_standard"
    # endregion

    # region fe
    quod310_fe = "quod310_fe"
    quod315_fe = "quod315_fe"
    quod317_fe = "quod317_fe"
    quod316_fe = "quod316_fe"
    quod320_fe = "quod320_fe"
    quod315_luna_trading_desktop = "quod315_luna_trading_desktop"
    quod314_luna_fe = "quod314_luna_fe"
    # endregion

    # region java-api
    quod317_java_api = "317_java_api"
    quod314_java_api = "314_java_api"
    quod309_java_api = "309_java_api"
    # endregion

    # region web admin
    quod306_web_admin_saturn_chrome = "quod306_web_admin_saturn_chrome"
    quod306_web_admin_saturn_firefox = "quod306_web_admin_saturn_firefox"
    test_site_web_admin_chrome = "test_site_web_admin_chrome"
    quod315_luna_web_admin = "quod315_luna_web_admin"
    quod315_luna_web_admin_site = "quod315_luna_web_admin_site"
    quod320_kuiper_web_admin_site = "quod320_kuiper_web_admin_site"
    quod319_kuiper_web_admin_site = "quod319_kuiper_web_admin_site"
    quod316_ganymede_web_admin_site = "quod316_ganymede_web_admin_site"
    quod320_kuiper_web_admin = "quod320_kuiper_web_admin"
    quod317_ganymede_web_admin = "quod317_ganymede_web_admin"
    quod314_luna_web_admin = "quod314_luna_web_admin"
    quod310_columbia_web_admin_site = "quod310_columbia_web_admin_site"
    quod309_kratos_web_admin = "quod309_kratos_web_admin"
    # endregion

    # region web trading
    quod315_web_trading_luna_chrome = "quod315_web_trading_luna_chrome"
    quod320_web_trading_kuiper_chrome = "quod320_web_trading_kuiper_chrome"
    quod320_kuiper_web_trading = "quod320_kuiper_web_trading"
    quod315_luna_web_trading = "quod315_luna_web_trading"
    # endregion

    # region redlog
    quod317_read_log = 'quod317_read_log'
    # endregion

    # region ssh client
    quod317_ssh_client = "quod317_ssh_client"
    # endregion
