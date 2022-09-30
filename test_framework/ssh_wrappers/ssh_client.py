import time

import paramiko


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
        if su_user and su_pass:
            self.channel.send(f"su {su_user}\n")
            time.sleep(self.TIMEOUT)
            self.channel.send(f"{su_pass}\n")
            time.sleep(self.TIMEOUT)

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
            command = "sudo -S -p '' %s" % command
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


if __name__ == "__main__":
    client = SshClient(host='', port=22, username='', password='', su_user='', su_pass='')
    try:
        res = client.execute('dmesg', sudo=True)
        print("  ".join(res["out"]), "  E ".join(res["err"]), res["retval"])
    finally:
        client.close()
