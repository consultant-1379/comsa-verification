import org.apache.log4j.Logger as Logger

import se.ericsson.jcat.omp.library.SshCommonLibAbstractImpl as SshCommonLibAbstractImpl
import se.ericsson.commonlibrary.CommonLibrary as CommonLibrary
import java.util.ArrayList as ArrayList
import se.ericsson.jcat.omp.fw.OmpSut as OmpSut

import omp.target.target_data as target_data
import omp.tf.ssh_lib as ssh

class sshlib(SshCommonLibAbstractImpl):
    
    sut = None
    
    def python_setLibraryDataProvider(self, data):
        self.data = data;

    def python_getLibraryDataProvider(self):
        return self.data;

    def python_initialize(self):
        sut = OmpSut.getOmpSut()
        ssh.setUp(2, 1, 1, sut)

    def python_shutdown(self):
        ssh.tearDown()

    def python_setConfig(self, subrack, slot, number, useVipOam=False):
        ssh.setConfig(subrack, slot, number, useVipOam)
        
    def python_getConfig(self):
        return ssh.getConfig()
    
    def python_getTargetData(self):
        return omp_target_data.getTargetHwData()
    
    def python_sendCommand(self, command, subrack=0, slot=0):
        return ssh.sendCommand(command, subrack, slot)
    
    def python_sendCommandNbi(self, command):
        return ssh.sendCommandNBI(command)
    
    def python_setTimeout(self, timeout, subrack=0, slot=0):
        return ssh.setTimeout(timeout, subrack, slot)
    
    def python_getTimeout(self, subrack, slot):
        return ssh.getTimeout(subrack, slot)
    
    def python_sendRawCommand(self, host, cmd, user, psw, timeout = 30):
        return ssh.sendRawCommand(host, cmd, user, psw, timeout)
    
    def python_loginTest(self, subrack, slot, attempts = 1, user = '' , pwd = '' ):
        return ssh.loginTest(subrack, slot, attempts, user, pwd)
    
    def python_bindAddresses(self, blade ,localPort, destinationPort):
        return ssh.bindAddresses(blade ,localPort, destinationPort)
    
    def python_readFile(self, blade, localPort, fileName, request='cat'):
        return ssh.readFile(blade, localPort, fileName, request)
    
    def python_remoteCopy(self, file, destination, timeout = 30, numberOfRetries = 5):
        return ssh.remoteCopy(file, destination, timeout, numberOfRetries)
    
    def python_remoteCopyFrom(self, file, destination, timeout = 30):
        return ssh.remoteCopyFrom(file, destination, timeout)
    
    def python_sCopy(self, file, host, destpath, user, passwd, timeout = 30):
        return ssh.sCopy(file, host, destpath, user, passwd, timeout)
    
    def python_tearDownHandles(self):
        ssh.tearDownHandles()
        
    def python_getUseVipOam(self):
        return ssh.getUseVipOam()
    
    def python_waitForConnection(self, subrack, slot, timeout):
        return ssh.waitForConnection(subrack, slot, timeout)
    
    def python_waitForNoConnection(self, subrack, slot, timeout):
        return ssh.waitForNoConnection(subrack, slot, timeout)
    
    def python_resetInternalConnectionCommand(self):
        ssh.resetInternalConnectionCommand()