import os
import re
import time

import paramiko
import xml.etree.ElementTree as ET
from stubs import ROOT_DIR


class SshClient:
    """A wrapper of paramiko.SSHClient"""
    TIMEOUT = 1

    def __init__(self, host, port, username, password, su_user=None, su_pass=None):
        self.username = username
        self.password = password
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(host, port, username=username, password=password)
        self.sftp_client = self.client.open_sftp()
        self.channel = self.client.invoke_shell()
        self.channel_data = str()
        self.su_user = su_user
        if su_user and su_pass:
            self.channel.send(f"su {su_user}\n")
            time.sleep(self.TIMEOUT)
            self.channel.send(f"{su_pass}\n")
            time.sleep(self.TIMEOUT)

    def __del__(self):
        self.sftp_client.close()

    def get_file(self, remote_path, local_path):
        self.sftp_client.get(remote_path, local_path)
        time.sleep(self.TIMEOUT)

    def put_file(self, remote_path, local_path):
        self.sftp_client.put(local_path, remote_path)
        time.sleep(self.TIMEOUT)

    def send_command(self, command):
        """use for: qstart, qstop etc."""
        self.channel.send(f"{command}\n")
        time.sleep(self.TIMEOUT)

    def execute(self, command, sudo=False):
        """use for: "ls -l /home" etc."""
        feed_password = False
        if sudo and self.username != "root":
            command = f"sudo -S -p '' {command}"
            feed_password = self.password is not None and len(self.password) > 0
        stdin, stdout, stderr = self.client.exec_command(command)
        if feed_password:
            stdin.write(self.password + "\n")
            stdin.flush()
        time.sleep(self.TIMEOUT)
        return {'out': stdout.readlines(),
                'err': stderr.readlines(),
                'retval': stdout.channel.recv_exit_status()}

    def close(self):
        if self.client is not None:
            self.client.close()
            self.client = None

    def get_and_update_file(self, component_config: str, xpath_config_value: dict) -> str:
        self.get_file(f"/home/{self.su_user}/quod/cfg/{component_config}", f"{ROOT_DIR}/test_resources/temp_config.xml")
        tree = ET.parse(f"{ROOT_DIR}/test_resources/temp_config.xml")
        quod = tree.getroot()
        for key in xpath_config_value.keys():
            base_config = quod.find(key).text
            quod.find(key).text = xpath_config_value[key]
            tree.write(f"{ROOT_DIR}/test_resources/temp_config.xml")
        self.send_command("~/quod/script/site_scripts/change_permission_script")
        self.put_file(f"/home/{self.su_user}/quod/cfg/{component_config}", f"{ROOT_DIR}/test_resources/temp_config.xml")
        os.remove(f"{ROOT_DIR}/test_resources/temp_config.xml")
        return base_config

    def find_regex_pattern(self, path_to_log_file: str, pattern: str):
        """returns bool value True if matching pattern is found in log file, returns False otherwise.

        use path_to_log_file variable to navigate log file in backend
        use pattern variable to apply regex for the log file

        Usage example:
            self.result = self.ssh_client.findall_in_logs("/Logs/quod314/QUOD.QS_ESP_FIX_TH2.log",
                                                          rf"^.*{order_id}.*ClientAccountGroupID=.Silver1.*$")"""
        temp_path = os.path.join(os.path.expanduser('~'), 'PycharmProjects', 'th2-script-quod-demo', 'temp')
        self.get_file(path_to_log_file, temp_path)
        logs = open(temp_path, "r")
        for line in logs:
            key = re.findall(pattern, line)
            if key:
                logs.close()
                os.remove(temp_path)
                return True
        return False


if __name__ == "__main__":
    client = SshClient(host='', port=22, username='', password='', su_user='', su_pass='')
    try:
        res = client.execute('dmesg', sudo=True)
        print("  ".join(res["out"]), "  E ".join(res["err"]), res["retval"])
    finally:
        client.close()
