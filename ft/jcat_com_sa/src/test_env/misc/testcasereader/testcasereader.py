"""
testcasereader.py reads through all tests (dt.xml files) and presents all unique test cases 
executed and in which area they were executed in. The left column shows the test area and the right
column shows the number of executed test cases in that area. Finally, the total number of test
cases executed is showed to the right of 'total number of testcases'.

HOWTO
1. Put all your dt.xml files (stored in your test log directory) in the original folder (subfolder to this test script)
2. Run testcasereader from command line: "python testcasereader.py"
3. The number of executed test cases will be printed out and in which area they were executed in


EXAMPLE
[eanjoel_coremw3.1_dev@esekits1037]:/home/eanjoel/workspace/jcat_com_sa/src/test_env/misc/testcasereader> cp /home/eanjoel/tmp/201209/CMW_FT_20120921212501/dt.xml original/
[eanjoel_coremw3.1_dev@esekits1037]:/home/eanjoel/workspace/jcat_com_sa/src/test_env/misc/testcasereader> cp /home/xgarlee/tmp/201208/CMW_FT_20120817023143/dt.xml original/dt2.xml
[eanjoel_coremw3.1_dev@esekits1037]:/home/eanjoel/workspace/jcat_com_sa/src/test_env/misc/testcasereader> python testcasereader.py
collectInfo 1
mdf 85
reinstallCMW 2
callbackVerify 22
installationUpgrade 15
upgradePackage 39
backupRestore 28
performanceManagement 306
nodeMgmt 1
imm 18

total number of testcases: 517

"""

import xml.etree.ElementTree as et
from subprocess import Popen, PIPE

testCaseDict = {}

p = Popen('\rm -f testreports/*', shell=True, stdout=PIPE)
p.wait()

p = Popen('ls original/', shell=True, stdout=PIPE)
p.wait()

res = p.communicate()[0]
fileList = res.split()

for file in fileList:
    p = Popen("/usr/bin/xsltproc -o testreports/testreport_%s dt.xsl original/%s" % (file, file), shell=True, stdout=PIPE)
    p.wait()
    
    r = et.parse("testreports/testreport_%s" % file).getroot()
    f = r.findall(".//testcase")

    for e in f:
        key = e.attrib["classname"].split(".")[5]
        value = e.attrib["classname"].split(".")[6] + "." + e.attrib["name"]
        if key not in testCaseDict:
            testCaseDict[key] = value
        else:
            if value not in testCaseDict[key]:
                testCaseDict[key] = testCaseDict[key] + "," + value
                
numberOfTestCases = 0
for item in testCaseDict:
    print item, len(testCaseDict[item].split(","))
    numberOfTestCases = numberOfTestCases + len(testCaseDict[item].split(","))
    
print "\ntotal number of testcases: %s" % numberOfTestCases
