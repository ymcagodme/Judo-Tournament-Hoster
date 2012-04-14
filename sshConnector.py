#draft

import paramiko

ssh = paramiko.SSHClient()
ssh.connect(server, username, password)
ssh.exec_command(cmd)

cmd = '/Applications/biteSMS.app/biteSMS -send -carrier 5622994141 "Yo"'
