#draft

import paramiko

server = "10.42.43.10"
username = "root"
password = "u83jp62k7"
cmd = '/Applications/biteSMS.app/biteSMS -send -carrier 5622994141 "Yo"'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(server, username=username, password=password)
ssh.exec_command(cmd)

