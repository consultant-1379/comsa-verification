"""
RotatingTestRunner
"""
import os
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from xml.dom import minidom

HOME = os.environ.get("HOME")
progPath = "%s/RotatingTestRunner" % HOME
streamPath = "%s/streams" % progPath
pollingLogPath = "%s/pollingLogs" % progPath
outputPath = "%s/output" % progPath
resultDataPath = "%s/resultdata" % progPath
userName = "hudsonuser"
SC1 = "134.138.66.81"
SC2 = "134.138.66.82"
testSuite = "RegressionTestSuite"
logDir = "%s/testLogs/" % progPath
delay = 180

def getStreamsFromFile():
    # read streams from file
    streamFile = open("%s" % streamPath, "r")
    streamContent = streamFile.readlines()
    streamFile.close()

    streams = []
    for line in streamContent:
        temp = line.split()
        streams.append(temp[0])

    print "File content is loaded:\n%s" % streamContent
    return streams

def getMailListFromFile(stream):
    # read streams from file
    streamFile = open("%s" % streamPath, "r")
    streamContent = streamFile.readlines()
    streamFile.close()

    for line in streamContent:
        temp = line.split()
        if temp[0] == stream:
            mailList = temp[1]

    return mailList

def getCurrentDate():
    return os.popen('date +"%d-%b-%y.%H:%M:%S"').read()[:-1]

def cleartoolExec(cmd, stream):
    #view = "%s_%s" % (userName, stream)
    fullCmd = '%s/cleartoolExec %s "%s"' % (HOME, stream, cmd)
    print fullCmd
    return os.popen(fullCmd).read()

def checkClearcaseHistory(lastCheckDate, stream):
    # check clearcase history since last checked date
    cmd = """cleartool lshistory -all -since %sutc+0000 -branch brtype:%s -nco /vobs/coremw/dev/release /vobs/coremw/dev/tools_config /vobs/coremw/test/apps /vobs/coremw/test/st /vobs/coremw/test/ft /vobs/coremw/dev/abs /vobs/coremw/dev/opensaf /vobs/coremw/dev/opensaf_api /vobs/coremw/dev/src_pkg /vobs/coremw/dev/deployment_templates /vobs/coremw/dev/install /vobs/coremw/dev/src""" % (lastCheckDate, stream)
    #print "cmd='%s'" % cmd
    return cleartoolExec(cmd, stream)

def logCurrentDateInPollingLog(stream):
    currentDate = getCurrentDate()
    pollingLogFile = open("%s/%s" % (pollingLogPath, stream), "a")
    pollingLogFile.write("%s\n" % currentDate)
    pollingLogFile.close()

def createLogStructure(stream):
    # check if polling log exists, otherwise create one
    if not os.path.exists("%s/%s" % (pollingLogPath, stream)):
        print "File does not exist, creating file '%s/%s'..." % (pollingLogPath, stream)
        pollingLogFile = open("%s/%s" % (pollingLogPath, stream), "w")
        pollingLogFile.close()

def getLastDateFromPollingLog(stream):
    # get last check date from polling log for the current stream
    pollingLogFile = open("%s/%s" % (pollingLogPath, stream), "r")
    pollingLogContent = pollingLogFile.readlines()
    pollingLogFile.close()

    # add current date if file is empty
    if pollingLogContent==[]:
        lastCheckDate = getCurrentDate()
    else:
        lastCheckDate = pollingLogContent[len(pollingLogContent)-1][:-1]

    #lastCheckDate = "23-Nov-11.12:11:11"
    return lastCheckDate

def triggerTestRun(stream, res, lastCheckDate):
    noPasswordCluster(stream)
    buildTestFramework(stream)
    buildCoremw(stream)
    deployAndInstall(stream)
    createTargetXML(stream)
    runTestSuite(stream, testSuite)
    testReportPath = createTestReport(stream)
    sendMail(stream, testReportPath, res, lastCheckDate)

def noPasswordCluster(stream):
    cmd = """unsetenv PYTHONHOME; /vobs/coremw/test/ft/scripts/nopassword_cluster.py %s -k %s/.ssh/key_rsa_1032""" % (SC1, HOME)
    cleartoolExec(cmd, stream)

def buildTestFramework(stream):
    cmd = """refresh; ant -v -f /vobs/coremw/test/ft/tests/build.xml clean compile-test"""
    cleartoolExec(cmd, stream)

def buildCoremw(stream):
    cmd = """unsetenv PYTHONHOME; refresh; cmwbuild --cleanall; cmwbuild all"""
    cleartoolExec(cmd, stream)

def deployAndInstall(stream):
    cmd = """/vobs/coremw/test/ft/scripts/deploy_and_install.sh %s %s/.ssh/key_rsa_1032""" % (SC1, HOME)
    cleartoolExec(cmd, stream)

def createTargetXML(stream):
    cmd = """/vobs/coremw/test/ft/scripts/createTargetXml.sh /vobs/coremw/test/ft/tests/files/config/mytarget.xml %s %s""" % (SC1, SC2)
    cleartoolExec(cmd, stream)

def runTestSuite(stream, testSuite):
    #cmd = """ant -v -DlogDir=%s -DsutTargetFile=/vobs/coremw/test/ft/tests/files/config/mytarget.xml -Dtestsuite.name=%s -f /vobs/coremw/test/ft/tests/build.xml run""" % (logDir, testSuite)
    cmd = """ant -DlogDir=%s/%s -DsutTargetFile=/vobs/coremw/test/ft/tests/files/config/mytarget.xml -buildfile /vobs/coremw/test/ft/tests/build.xml test -Dtestsuite.name=%s""" % (logDir, stream, testSuite)
    res = cleartoolExec(cmd, stream)
    print res
    outputFile = open("%s" % outputPath, "w")
    outputContent = outputFile.write(res)
    outputFile.close()

def getLogDirFromOutput():
    outputFile = open("%s" % outputPath, "r")
    outputContent = outputFile.readlines()
    outputFile.close()

    cmd = """tail -n 50 %s/output | grep "Logs are in" | awk '{print $7}'""" % progPath
    return os.popen(cmd).read()[:-1]

def sendMail(stream, testReportPath, res, lastCheckDate):
    me = 'do-NOT-reply@ericsson.com'
    mailList = getMailListFromFile(stream)
    print "mailList = %s" % mailList
    temp = mailList.split(",")
    #you = mailList
    you = []
    for item in temp:
        you.append(item)
    print "mailList = %s" % you

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Test report for: %s" % stream
    msg['From'] = me
    msg['To'] = ','.join(you)

    text = """Hi,\n\nHere are the test results for stream: %s\n\n%s\n\nLogs are here:\n%s\n\nNew activities since %s:\n%s\n\n/Test Team""" % (stream, readTestReport(stream, lastCheckDate), testReportPath, lastCheckDate, res)

    part1 = MIMEText(text, 'plain')
    #part2 = MIMEText(html, 'html')

    msg.attach(part1)
    #msg.attach(part2)

    s = smtplib.SMTP('localhost')
    s.sendmail(me, you, msg.as_string())
    s.quit()

def createTestReport(stream):
    testReportPath = getLogDirFromOutput()
    print "Logs are in: '%s'" % testReportPath
    cmd = """/usr/bin/xsltproc -o %s/%s/testreport.xml /vobs/coremw/tools/HUDSON_INTEGRATION/dt.xsl `find %s/ -name dt.xml`""" % (logDir, stream, testReportPath[:-10])
    cleartoolExec(cmd, stream)
    return testReportPath

def readTestReport(stream, lastCheckDate):
    doc = minidom.parse("%s/%s/testreport.xml" % (logDir, stream))
    nl = doc.getElementsByTagName("testsuite")
    e = nl[0]

    tests = int(e.getAttribute("tests"))
    failures = int(e.getAttribute("failures"))
    passed = tests-failures

    text = """Results: %s/%s passed. Failed: %s\n""" % (passed, tests, failures)
    
    # save test results to file
    resultDataFile = open("%s/%s" % (resultDataPath, stream), "a")
    resultDataFile.write("%s, %s, %s, %s, %s\n" % (lastCheckDate, stream, passed, tests, failures))
    resultDataFile.close()
    
    return text

while True:
    streams = getStreamsFromFile()
    for stream in streams:
        print "Current stream='%s'" % stream

        createLogStructure(stream)
        lastCheckDate = getLastDateFromPollingLog(stream)
        logCurrentDateInPollingLog(stream)
        res = checkClearcaseHistory(lastCheckDate, stream)
        print res
        if "create" in res:
            print "New activities:\n%s" % res
            print "\n*** TEST RUN STARTED %s ***\n" % getCurrentDate()
            triggerTestRun(stream, res, lastCheckDate)
        else:
            print "No changes since %s" % lastCheckDate
        print "Sleeping for %s seconds..." % delay
        time.sleep(delay)