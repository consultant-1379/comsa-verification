import se.ericsson.jcat.omp.library.SshLibDataProvider as SshLibDataProvider

import omp.target.target_data as target_data

class sshlibdata(SshLibDataProvider):
    
    targetData=target_data.data    # a dictionary containing hardware specific information
    
    def getName(self):
        return "This is a default data provider";
    
    def initialize(self):
        self.targetData=target_data.data
    
    def shutdown(self):
        pass
        
    def getSetupDependencyList(self):
        return None
    
    def getRuntimeDependencyList(self):
        return None
    
    def getName(self) :
        return "This is a data provider implemented by demo user";
    
    def getTargetPcPattern(self):
        return self.targetData['testPcPattern']
    
    def getOamVip(self):
        return self.targetData['ipAddress']['vip']['vip_2']
    
    def getTrafficVip(self):
        return self.targetData['ipAddress']['vip']['vip_1']
    
    def getScIp(self, controller):
        return self.targetData['ipAddress']['ctrl'][controller]
    
    def getUsername(self):
        return self.targetData['user']
    
    def getPassword(self):
        return self.targetData['pwd']
    
    def getInternalIp(self, node):
        return self.targetData['ipAddress']['blades'][node]
    
    def getTestPcIp(self):
        return self.targetData['ipAddress']['ctrl']['testpc']
    
    def getNbIp(self):
        return self.targetData['ipAddress']['ctrl']['NB']
    
    def getIpmiAddress(self, blade):
        return self.targetData['ipAddress']['ipmi'][blade]
    