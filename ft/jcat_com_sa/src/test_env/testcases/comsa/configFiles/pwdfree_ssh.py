#!/usr/bin/env python
import sys
import shlex
import os
import pexpect
from optparse import OptionParser
from subprocess import check_call
from commands import getstatusoutput

USER='root'
PASSWORD='rootroot'
HOST=''
PRIVKEY="./cluster_key"
PUBKEY=PRIVKEY + ".pub"
VERBOSE=False

def log(str):
    if VERBOSE:
        print(str)

def generate_ssh_keys():
    """ Generates a passwordless rsa keypair """
    try:
        check_call(["test", "-e", PRIVKEY])
    except:
        try:
            child = pexpect.spawn("ssh-keygen", ["-t", "rsa", "-N", "", "-f", PRIVKEY])
            child.logfile = sys.stdout
            index = child.expect(['Overwrite \(y\/n\)\? ', pexpect.EOF])
            if index == 0:
                child.sendline("y")
            child.expect(pexpect.EOF)
        except pexpect.ExceptionPexpect, e:
            print e

def test_ssh_passwordless():
    """ Test if we can log in without a password """
    log('testing passwordless login through ssh...')
    ret, msg = getstatusoutput('ssh -i {0} -o "BatchMode=yes" {1}@{2} exit'.format(PRIVKEY, USER, HOST))
    if ret != 0 or msg != '':
        log("passwordless login is not active. \nreturnval: {0} \nssh output: {1}".format(ret, msg))
        return False
    log("passwordless login seems to be setup")
    return True

def send_password(child):
    child.sendline(PASSWORD)
    child.expect(pexpect.EOF)
    
def setup_ssh_connection():
    print("Starting passwordless setup...")
    try:
        child = pexpect.spawn('ssh-copy-id', ['-i', PUBKEY, '{0}@{1}'.format(USER,HOST)])
        if VERBOSE: 
            child.logfile = sys.stdout
        index = child.expect([r'(?i)Password: ', 'continue connecting (yes/no)?', pexpect.EOF])
        if index == 0:
            send_password(child)
        elif index == 1:
            child.sendline('yes')
            index = child.expect([r'(?i)Password: ', pexpect.EOF])
            if index == 0:
                send_password(child)
    except pexpect.ExceptionPexpect, e:
        print e
    # Make this persistent over reboot
    sshcmd = "ssh -i {0} {1}@{2} ".format(PRIVKEY, USER, HOST)
    getstatusoutput(sshcmd + "mkdir /boot/patch /boot/patch/root /boot/patch/root/.ssh")
    cmd = shlex.split(sshcmd + 'echo "root/.ssh/authorized_keys" >> /boot/patch/files')
    check_call(cmd)
    getstatusoutput(sshcmd + "cp /root/.ssh/authorized_keys /boot/patch/root/.ssh/")
    print("Passwordless setup is done and persistent.")
    print("Use ssh -i {0} {1}@{2} to login.".format(PRIVKEY, USER, HOST))

def cleanup():
    print("Not implemented")
    return
    sshcmd = "ssh -i {0} {1}@{2} ".format(PRIVKEY, USER, HOST)
    os.system(sshcmd + "rm -f /boot/patch/root/.ssh/authorized_keys")
    os.system("rm -f {0} {1}".format(PRIVKEY, PUBKEY))

def test():
    try:
        child = pexpect.spawn('service', ['ldap', 'restart'])
        if VERBOSE: 
            child.logfile = sys.stdout
        index = child.expect(['Enter LDAP Password: ', pexpect.EOF])
        if index == 0:
            send_password(child)
    except pexpect.ExceptionPexpect, e:
        print e

def main(argv):
    global VERBOSE, HOST, PRIVKEY, PUBKEY
    desc = 'tool for setting up a persistent passwordless ssh key to a cluster'
    help1 = 'test if passwordless ssh is active'
    help2 = 'optional file name of the key, default is: {0}'.format(PRIVKEY)
    help3 = 'clean up from a previous setup'
    parser = OptionParser(prog='HOST ADDRES', description=desc)
    parser.add_option('-t', dest='test_ssh', default=False, action='store_true', help=help1)
    parser.add_option('-v', dest='verbose', default=False, action='store_true', help='verbose mode')
    parser.add_option('-k', dest='privkey', default=PRIVKEY, help=help2)
    parser.add_option('-c', dest='clean', default=False, action='store_true', help=help3)
    options, args = parser.parse_args(argv)
    if (len(args) != 1): 
        print('host address missing')
        return 1
    VERBOSE = options.verbose
    HOST = args[0]
    PRIVKEY = options.privkey
    PUBKEY = PRIVKEY + ".pub"
    if options.clean:
        return cleanup()
    if options.test_ssh:
        return test_ssh_passwordless()
    generate_ssh_keys()
    if test_ssh_passwordless() == False:
        setup_ssh_connection()
    else:
        print("Passwordless is already setup")
    
if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
    pass
