rename_process("ftpd")
term.write("Exiting to FTP..")
from supervisor import set_next_code_file

set_next_code_file("ftp_serv.py")
del set_next_code_file
ljinux.based.run("reload")
