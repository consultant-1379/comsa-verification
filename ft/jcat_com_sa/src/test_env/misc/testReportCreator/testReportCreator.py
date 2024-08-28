#Usage: testReportCreator.py [options]
#
#Options:
#  -h, --help    show this help message and exit
#  -r REPORTDIR  report directory [default: reports]
#  -o OUTPUTDIR  output directory [default: myoutputdir]
#  
#TODO:
#Target/config table showing Vip and LOTC setup
#Column showing total passrate in mytestsummary

from subprocess import Popen, PIPE
import xml.etree.ElementTree as et
import os, re, csv, shutil
from optparse import OptionParser

#classname2testobj is a dictionary used to map a testcase (classname) to a testarea
classname2testobj = {}
classname2testobj['Performance'] = ['CpuUsage', 'RamUsage']
classname2testobj['Load'] = ['Load']
classname2testobj['Maintainability'] = ['BackupandRestore', 'ReInstall', 'SmfCampaignInstall', \
                                        'UpgradeWithSchemaChanges', 'backupUninstallRestoreOfNtfSubscriberApp', \
                                        'clearActiveAlarms', 'clusterNodeUnavailable', 'cmwSingleStepUpgrade', \
                                        'cmwmdfverify', 'upgradePackage', 'smfRollbackTestClass']
classname2testobj['Robustness'] = ['powerResetOfNode', 'reloadOfNode', 'Robustness', 'haltOfcontrollerNodes', \
                                   'powerResetOfCluster', 'rebootOfCluster', 'reloadOf2PLSimultant']
classname2testobj['Stability'] = ['Stability']
classname2testobj['Security'] = ['Security']
classname2testobj['Trouble Reports'] = ['troubleReportVerification']
classname2testobj['Characteristics'] = ['PerformanceCharacteristicsMeasurement', 'TestAppMeasurements', 'ntfMeasureClass', 'testappMeasurements2', 'suFailoverMeasurements']

#blttestarea = '/proj/coremw_scratch/blt'
blttestarea = '/home/eanjoel/workspace_phoenix/jcat_com_sa/src/test_env/misc/testReportCreator/temp/blt'

parser = OptionParser()
parser.add_option('-r', dest='reportdir', default='reports', help='report directory [default: %default]')
parser.add_option('-o', dest='outputdir', default='myoutputdir', help='output directory [default: %default]')
parser.add_option('-l', dest='lastfinder', default=False, help='finds the last blt folder and sets input/output [default: %default]')
(options, args) = parser.parse_args()

reportdir = options.reportdir
outputdir = options.outputdir
lastfinder = options.lastfinder

def findLastFolder():
    folderprefix = 'blt_'
    bltfolders = os.listdir(blttestarea)
    max=0
    for folder in bltfolders:
        if re.search(folderprefix, folder):
            value = int(folder.split('_')[1])
            if value > max:
                max = value
    lastfolder = '%s%s' % (folderprefix, value)
    return lastfolder

if lastfinder:
    lastfolder = findLastFolder()
    reportdir = '%s/%s' % (blttestarea, lastfolder)
    outputdir = reportdir

def xsltproc(file):
    # converts dt.xml to a more easily read format
    workspace = os.environ['MY_REPOSITORY']
    output = 'testdt.xml'
    p = Popen("/usr/bin/xsltproc -o reports/%s/%s %s/test_env/misc/testReportCreator/dt.xsl reports/%s/dt.xml" % (file, output, workspace, file), shell=True, stdout=PIPE)
    p.wait()

def getValueFromTag(file, tag):
    f = open('%s/%s/properties.htm' % (reportdir, file))
    lines = f.readlines()
    f.close()
    for line in lines:
        if re.search(tag, line):
            myxml = et.fromstring(line)
            f = myxml.findall(".//td")
            return f[1].text

def getTestReports():
    testreports = [] 
    temp = os.listdir(reportdir)
    for item in temp:
        if os.path.isdir('%s/%s' % (reportdir, item)):
            testreports.append(item)
    return testreports
    
def cleanUp():
    print outputdir
    shutil.rmtree(outputdir, ignore_errors=True)
    os.mkdir(outputdir)

def getTestType(report):
    testtype = 'FT'
    dummy = getValueFromTag(report, 'tracelogLevel') #any property that only exist in ST (and not in FT) would do the trick
    if dummy != None:
        testtype = 'ST'
    return testtype

def getOccurrences(lookfor, list):
    count=0
    for item in list:
        if item == lookfor:
            count=count+1
    return count

def removeDuplicates(testcases):
#    This is far from the most optimal solution...
#    This is the logic:
#    Go through all testcases.  If there are no duplicates for a key, then add it directly to noDuplicates.
#    If there are duplicates for a key, save the duplicates in duplicatedata and the rest of the testcases for that key in restdata
#    Check which testcases to keep. If there is a failed testcase: keep it, and ignore the others.
#    If there are no failed testcases, pick one and ignore the others.
#    Finally, add restdata tobeadded to noDuplicates.
    
    noDuplicates = {}
    duplicatedata = {}
    restdata = {}
    #testcases dimensions: 11, 148
    
    #copy stage
    for key, item in testcases.items():
        testcasesonly = []
        for i in item:
            #create a testcasesonly list with only testcase names
            testcasesonly.append(i[0])
        duplicatesOnly = []
        for tc in testcasesonly:
            #go through all testcases and check if there are any duplicates
            occurrences = getOccurrences(tc, testcasesonly)
            if occurrences > 1:
                #duplicates exist, add it to duplicatesOnly
                duplicatesOnly.append(tc)
        if duplicatesOnly == []:
            #if there are no duplicates, proceed as normal
            for i in item:
                if noDuplicates.has_key(key):
                    noDuplicates[key].append(i)
                else:
                    noDuplicates[key] = [i]
        else:
            #if there are duplicates, add all duplicates to the dictionary duplicatedata and handle everything later
            for i in item:
                if i[0] in duplicatesOnly: 
                    if duplicatedata.has_key(key):
                        duplicatedata[key].append(i)
                    else:
                        duplicatedata[key] = [i]
                else:
                    if restdata.has_key(key):
                        restdata[key].append(i)
                    else:
                        restdata[key] = [i]
    
    #add some-of-the-duplicates-stage
    tobeadded = {}
    
    for key, item in duplicatedata.items():
        #check if there are failed testcases
        failed=False
        for i in item:
            if i[1] == 1:
                failed=True

        #if there is one failed testcase...
        if failed:
            for i in item:
                if i[1] == 1:
                    if tobeadded.has_key(key):
                        pass
                        #tobeadded[key].append(i)
                    else:
                        print 'keep failed:'
                        print key, i
                        tobeadded[key] = [i]
        else:
            for i in item:
                print 'passed'
                print key, i
                if tobeadded.has_key(key):
                    pass
                    #tobeadded[key].append(i)
                else:
                    tobeadded[key] = [i]
    
    #now, final stage, add restdata and tobeadded items to noDuplicates, phew!
    print 'restdata:'
    print restdata
    for key, item in restdata.items():
        for i in item:
            if noDuplicates.has_key(key):
                noDuplicates[key].append(i)
            else:
                noDuplicates[key] = [i]
    
    print 'tobeadded:'
    print restdata
    for key, item in tobeadded.items():
        for i in item:
            if noDuplicates.has_key(key):
                noDuplicates[key].append(i)
            else:
                noDuplicates[key] = [i]
    
    count=0
    for key, item in noDuplicates.items():
        for i in item:
            #print key, i
            count=count+1
    print len(noDuplicates)
    print count
        
def getTestData(testreports):
    testcases = {}
    for report in testreports:
        xsltproc(report)
        sc = int(getValueFromTag(report, 'nrOfScNodes'))
        pl = int(getValueFromTag(report, 'nrOfPlNodes'))
        testtype = getTestType(report)
        r = et.parse('%s/%s/testdt.xml' % (reportdir, report)).getroot()
        f = r.findall(".//testcase")
        for e in f:
            if testtype == 'ST':
                testclass = e.attrib['classname'].split('$')[-2]
                notInDict = True
                for key, item in classname2testobj.items():
                    if testclass in item:
                        testobj = key
                        notInDict = False
                        break
                if notInDict:
                    #if a testcase name gets here, it means that's not in the classname2testobj dictionary.
                    #If you want it to be specified in another test area group, please add it to the dictionary.
                    testobj = 'Miscellaneous'
                    print '%s does not belong to any test area group! Added to \'%s\'!' % (testclass, testobj)
            else:
                #handle this as a FT testreport
                testclass = e.attrib['classname'].split('.')[-2]
                testobj = testclass
            testtime = e.attrib['time']
            key = (sc, pl, testobj, testtype) 
            value = (e.attrib['name'], len(e.findall(".//failure")), testtime)
            if testcases.has_key(key):
                testcases[key].append(value)
            else:
                testcases[key] = [value]
    return testcases

#cleanUp()
testreports = getTestReports()
testcases = getTestData(testreports)
#TODO: don't remove duplicates of FT testcases?
removeDuplicates(testcases)
passrate = {}
nodelist = [] #tuple (sc, pl, testtype)
  
for key, item in testcases.items():
    failed = 0
    blocked = 0
    for tc in item:
        if tc[1] > 0:
            failed = failed+1
        if tc[2] == '':
            blocked = blocked+1
    executed = len(item)
    passed = executed-failed-blocked
    passpercent = 100*(float(passed)/float(executed))
    sc = key[0]
    pl = key[1]
    testobj = key[2]
    testtype = key[3]
    key = (sc, pl, testobj, testtype)
    value = (executed, passed, failed, blocked, round(passpercent, 1))
    if passrate.has_key(key):
        passrate[key].append(value)
    else:
        passrate[key] = value
    if testtype == 'ST':
        if (sc, pl) not in nodelist:
            nodelist.append((sc, pl))

nodelist.sort()
node2index = {}
for i in range(len(nodelist)):
    node2index[nodelist[i]] = i

tabledict = {}
for key, item in sorted(passrate.items()):
    sc = key[0]
    pl = key[1]
    testtype = key[3]
    table = [key[2], item[0], item[1], item[2], item[3], item[4]]
    key = (sc, pl, testtype)
    value = table
    if tabledict.has_key(key):
        tabledict[key].append(value)
    else:
        tabledict[key] = [value]

for key, item in tabledict.items():
    sc = key[0]
    pl = key[1]
    testtype = key[2]
    c = csv.writer(open('%s/PassRatePerConfiguration%sPlus%s_%s.csv' % (outputdir, sc, pl, testtype), 'wb'))
    row = ['Test Object', 'Exec', 'Passed', 'Failed', 'Blocked', 'Pass/Exec%']
    c.writerow(row)
    for row in item:
        c.writerow(row)

#and now generate the final summary report with passrates from all testreports
tablesummary = {}
for key, item in sorted(passrate.items()):
    passpercent = item[4]
    sc = key[0]
    pl = key[1]
    testtype = key[3]
    if testtype == 'ST':
        testobj = key[2]
        value = (sc, pl, passpercent, testtype)
        if tablesummary.has_key(testobj):
            tablesummary[testobj].append(value)
        else:
            tablesummary[testobj] = [value]

c = csv.writer(open('%s/PassRatePerConfigurationSummary.csv' % outputdir, 'wb'))
row = ['']*len(nodelist)

for index, item in enumerate(row):
    row[index] = '%s+%s' % (nodelist[index][0], nodelist[index][1])
row.insert(0,'Test Object')
c.writerow(row)
for key, item in tablesummary.items():
    row = ['']*len(nodelist)
    for result in item:
        row[node2index[(result[0], result[1])]] = result[2]
    row.insert(0, key)
    c.writerow(row)

targetdict = {}
for report in testreports:
    sc = int(getValueFromTag(report, 'nrOfScNodes'))
    pl = int(getValueFromTag(report, 'nrOfPlNodes'))
    target = getValueFromTag(report, '__TARGET_SYSTEM__')
    testtype = getTestType(report)
    key = (sc, pl, testtype)
    value = (target)
    if targetdict.has_key(key):
        targetdict[key].append(value)
    else:
        targetdict[key] = [value]
        
for key, item in targetdict.items():
    print 'testtype=%s, SC=%s, PL=%s, targets=%s' % (key[2], key[0], key[1], item)
    
