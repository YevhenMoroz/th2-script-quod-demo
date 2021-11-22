import time

import paramiko
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect('10.0.22.77', 22, username='quod308', password='quod308')
stdin,stdout,stderr=ssh_client.exec_command("ll")
time.sleep(2)
stdout=stdout.readlines()
ssh_client.close()
print(stdout)

for line in stdout:
    output=output+line
if output!="":
    print(output)
else:
    print("There was no output for this command")