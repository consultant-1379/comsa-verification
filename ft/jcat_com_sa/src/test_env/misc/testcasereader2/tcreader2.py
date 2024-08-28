import xml.etree.ElementTree as et
from subprocess import Popen, PIPE
import csv
import os
import re

def xsltproc(file):
    # converts dt.xml to a more easily read format
    output = 'testdt.xml'
    p = Popen("/usr/bin/xsltproc -o reports/%s/%s dt.xsl reports/%s/dt.xml" % (file, output, file), shell=True, stdout=PIPE)
    p.wait()
    
def getValueFromTag(file, tag):
    f = open('reports/%s/properties.htm' % file)
    lines = f.readlines()
    f.close()
    for line in lines:
        if re.search(tag, line):
            myxml = et.fromstring(line)
            f = myxml.findall(".//td")
            return f[1].text

def getTestResults(file, pls, ft=False):
    r = et.parse('reports/%s/testdt.xml' % file).getroot()
    f = r.findall(".//testcase")
    testcases = {}
    table = []
    for e in f:
        if ft:
            key = e.attrib['classname'].split('.')[-2]
        else:
            key = e.attrib['classname']
        value = [e.attrib['name'], len(e.findall(".//failure"))]
        if testcases.has_key(key):
            if value in testcases[key]:
                pass
                #print 'dublicate of %s' % value
                # only store unique test cases
            testcases[key].append(value)
        else:
            testcases[key] = [value]
    totalTCs = 0
    totalFailed = 0
    totalPassExecPercent = 0
    for key in testcases.keys():
        failedTCs = 0
        for item in testcases[key]:
            if item[1] > 0:
                failedTCs = failedTCs+1
        if ft:
            testObject = key
        else:
            temp = key.split('$')
            testObject = temp[-2]
        executed = len(testcases[key])
        passed = executed-failedTCs
        passExecPercent = 100*(float(passed)/float(executed))
        table.append([testObject, executed, passExecPercent, passed, failedTCs])
        summarytable.append([testObject, passExecPercent, pls])
        totalPassExecPercent = totalPassExecPercent+passExecPercent
        totalFailed = totalFailed+failedTCs
        totalTCs = totalTCs+len(testcases[key])
    totalPassed = totalTCs-totalFailed
    
    if ft:
        c = csv.writer(open('output/mytestreportFT.csv', 'wb'))
    else:
        c = csv.writer(open('output/mytestreport2p%s.csv' % pls, 'wb'))
    #c.writerow(['totalTCs', totalTCs, 100*(float(totalTCs)/float(totalTCs))])
    #c.writerow(['totalPassed', totalPassed, 100*(float(totalPassed)/float(totalTCs))])
    #c.writerow(['totalFailed', totalFailed, 100*(float(totalFailed)/float(totalTCs))])
    c.writerow(['testObject', 'executed', 'passExecPercent', 'passed', 'failedTCs'])
    for row in table:
        c.writerow(row)
    return testcases

def writeSummary():
    nodelist = []
    for key in superd.keys():
        nodelist.append(key)
    
    nodelist.sort()
    indexToNode = {}
    
    for i in range(len(nodelist)):
        indexToNode[nodelist[i]] = i
    
    summary = {}
    for item in summarytable:
        key = item[0]
        value = item[1:]
        if summary.has_key(key):
            summary[key].append(value)
        else:
            summary[key] = [value]
    
    finalsummary = []
    
    for key in summary.keys():
        row = ['']*len(nodelist)
        for index in range(len(summary[key])):
            row[indexToNode[summary[key][index][1]]] = summary[key][index][0]
        row.insert(0,key)
        finalsummary.append(row)
    
    c = csv.writer(open('output/mytestsummary.csv', 'wb'))
    nodelist.insert(0,'testObject')
    c.writerow(nodelist)
    for row in finalsummary:
        c.writerow(row)

def createHwSwDict(file):
    configs = {}
    pls = getValueFromTag(reportpath, 'nrOfPlNodes')
    target = getValueFromTag(reportpath, '__TARGET_SYSTEM__')
    key = pls
    value = target
    if configs.has_key(key):
        configs[key].append(value)
    else:
        configs[key] = [value]
        print configs

#ST
configs = {}
superd = {}
summarytable = []
testreports = os.listdir('reports/st')
for report in testreports:
    reportpath = 'st/%s' % report
    xsltproc(reportpath)
    pls = int(getValueFromTag(reportpath, 'nrOfPlNodes'))
    testcases = getTestResults(reportpath, pls)
    superd[pls] = testcases
    createHwSwDict(reportpath)

#FT
testreports = os.listdir('reports/ft')
for report in testreports:
    reportpath = 'ft/%s' % report
    xsltproc(reportpath)
    testcases = getTestResults(reportpath, '2', True)




    