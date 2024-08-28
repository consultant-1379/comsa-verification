#!/usr/bin/python


from optparse import OptionParser
usage = '''
scp the comsa so files to target servers.

%prog [-p port] [-u user] [--password password] host1 [host2]'''

parser = OptionParser(usage=usage)
parser.add_option("-P", "-p", dest="port", default='22', help='specify the scp port, default is 22')
parser.add_option("-u", "--user", dest="user", default='root', help='specify the user on the target machine, default is root')
parser.add_option("--password", dest="password", default='rootroot', help='specify the password on the target machine, default is 22')

(options, args) = parser.parse_args()
if len(args) < 1:
	parser.print_usage()
	exit()

import getpass

src_dir = '/tmp/COM_SA_RESULT-{user}/'.format(user=getpass.getuser())
dest_dir = '/opt/com/lib/comp/'
tp_dest_dir = '/cluster/storage/system/software/comsa_for_coremw-apr9010555/lib64/'


import pexpect

def scp(file, host, path, user='root', password='rootroot', port='22'):
	try:
		cmd = "scp -P %s %s %s@%s:%s"%(port, file, user, host, path)
		print(cmd)
		child = pexpect.spawn(cmd)
		i = child.expect(['assword:', r"yes/no"], timeout=30)
	except:
		print('can not execute')

	if i==0:
		child.sendline(password)
	elif i==1:
		child.sendline("yes")
		child.expect("assword:", timeout=30)
		child.sendline(password)
	try:
		data = child.read()
		print(data)
	except:
		print('can not read')

	child.close()

for ip in args:
	scp(file=src_dir + 'comsa_tp.so',
		host=ip,
		path=tp_dest_dir,
		port=options.port,
		user=options.user,
		password=options.password)

	scp(file=src_dir + 'coremw-com-sa.so',
                host=ip,
                path=dest_dir,
                port=options.port,
                user=options.user,
                password=options.password)

	scp(file=src_dir + 'coremw-pmt-sa.so',
                host=ip,
                path=dest_dir,
                port=options.port,
                user=options.user,
                password=options.password)
