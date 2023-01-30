import time
import traceback
from datetime import timedelta

from test_framework.configurations.component_configuration import ComponentConfiguration
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from custom import basic_custom_actions as bca
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3116 import QAP_T3116
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3398 import QAP_T3398
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3544 import QAP_T3544
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3569 import QAP_T3569
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3570 import QAP_T3570
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3660 import QAP_T3660
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3687 import QAP_T3687
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3689 import QAP_T3689
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3716 import QAP_T3716
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3771 import QAP_T3771
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3773 import QAP_T3773
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3774 import QAP_T3774
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3775 import QAP_T3775
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3776 import QAP_T3776
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3778 import QAP_T3778
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3818 import QAP_T3818
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3819 import QAP_T3819
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3820 import QAP_T3820
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3821 import QAP_T3821
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3863 import QAP_T3863
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3864 import QAP_T3864
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3865 import QAP_T3865
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3866 import QAP_T3866
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3867 import QAP_T3867
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3868 import QAP_T3868
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3869 import QAP_T3869
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3870 import QAP_T3870
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3871 import QAP_T3871
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3872 import QAP_T3872
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3877 import QAP_T3877
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3886 import QAP_T3886
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3923 import QAP_T3923
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3924 import QAP_T3924
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3994 import QAP_T3994
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3995 import QAP_T3995
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3996 import QAP_T3996
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3997 import QAP_T3997
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T4000 import QAP_T4000
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T4001 import QAP_T4001
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T4003 import QAP_T4003
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T4004 import QAP_T4004
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T4005 import QAP_T4005
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T4006 import QAP_T4006
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T4007 import QAP_T4007
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T4008 import QAP_T4008
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T4814 import QAP_T4814
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T4815 import QAP_T4815
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T4816 import QAP_T4816
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T7930 import QAP_T7930


class RunOrderManagement:
    def __init__(self, root_report_id):
        self.second_lvl_id = bca.create_event("WA_Order_Management", root_report_id)
        self.web_driver_container = None

    def execute(self):
        try:
            configuration = ComponentConfiguration("WA_Order_Management")
            self.web_driver_container = WebDriverContainer(
                configuration.environment.get_list_web_admin_environment()[0].web_browser,
                configuration.environment.get_list_web_admin_environment()[0].site_url)
            start_time = time.monotonic()

            QAP_T3116(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()

            # TODO: остановились тут
            # Мануал ОК. Авто падал из-за симпл даты.
            # Неполный авто тест. Нет проверки степов 1, 4 из ТК.
            # Не совсем понимаю для чего в АТ клик на вкл/выкл. В ТК не увидел проверки
            QAP_T4008(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()

            # Нет проверки степа 4 из ТК. Ф
            QAP_T4007(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()

            # Не соответствут Error message степ 2 и 4. Нет степа 5 из ТК. В авто проблемы с датой.
            QAP_T4006(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()

            QAP_T4005(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()

            # Не увидел проверки степа 4 из ТК. Реализацию степа 5. Нет проверки, что действительно удалили параметр.
            # Не увидел реализацию степа 7
            # Мануал - ФЕЙЛ. Степ 7. Нельзя создать все параметры.
            QAP_T4004(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()

            # Не увидел проверок для степа 3, 4, 5.
            QAP_T4003(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()

            # ОК. Не соответствует ErRor message.
            QAP_T4001(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()

            # ОК. Не соответствует ErRor message.
            QAP_T4000(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()

            QAP_T3997(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()

            QAP_T3996(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()

            # Error message не соответствуют ТК. Pass - проставил.
            QAP_T3995(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()

            # Степ 1 из ТК, не увидел проверки на реквайред поле
            QAP_T3994(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()

            QAP_T3924(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()

            # АТ не делает провку отображения кнопок из ТК степ 3. Не увидел проверки степа 6 из ТК.
            QAP_T3923(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()

            # шото непонятное твориться в Try. Отсутствуют проверки степа 6 из ТК
            # Проблемы с симл датой.
            # Мануал ОК, Авто- фейл.
            QAP_T3886(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            #
            QAP_T3877(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()

            # Для чего после выполнения кейс отключать стратегию?
            QAP_T3872(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3871(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3870(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3869(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3868(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3867(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3866(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()

            QAP_T3865(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3864(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3863(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()

            # LISResidentTime: 5000 и LISPools: CHIXLIS/TQDARK - не увидел проверку этих параметров. в АТ только LISPhase: Y
            QAP_T3819(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3821(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3820(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()

            # Не увидел проверки, что кнопка действительно сменила статус (Степ 4, 6, 8, 10)
            QAP_T3818(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()

            # Задублирована переменная page. Степы 120-129 заменил бы на проверку того что у нас присутствует 2 сущности с одинаковым именем и венью.
            # Создалбы отдельный метод для создания сущности, что бы не дублировать код.
            QAP_T3778(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            #
            # Не понимаю происходящего в ТК.
            QAP_T3776(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()

            QAP_T3775(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()

            # Не увидел проверку, что после клика по чекбоксу он не изменился.
            QAP_T3774(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()

            QAP_T3773(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3771(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()

            # Зачем заходить в эдит для проверки сохраненных данных. Почему првоерям только Роут, и не учитываем exec_policy и percentage?
            QAP_T3716(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()

            QAP_T3689(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()

            # В ТК не увидел реализацию степа 64 из автотеста (click_on_delete_at_results_sub_wizard)
            # Почему мы делаем удаление и добавление новой exec_policy вместо редактирования?
            # Почему в верификации первая дата для проверки забита гвоздем а не парсится?
            QAP_T3687(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()

            # Почему проверяем имун только для имени?
            QAP_T3660(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()

            QAP_T3570(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3569(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()

            # Не полный тест. Мы делаем только клик для перехода в Лит, но не чекаем что действительно он открылся.
            QAP_T3544(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3398(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T4814(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T4815(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T4816(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T7930(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()

            end_time = time.monotonic()
            print("Run Order Management ~execution time~ = " + str(timedelta(seconds=end_time - start_time)))

        except Exception:
            print(traceback.format_exc() + " Execute ERROR !->  " + self.__class__.__name__)
