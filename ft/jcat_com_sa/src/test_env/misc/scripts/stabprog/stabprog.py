"""
1. Set a ClearCase view

2. Install pychart:
cd $MY_WORKSPACE/jcat_com_sa/src/test_env/misc/scripts/stabprog/pychart/PyChart-1.26.1
python setup.py install

3. Go to stab test log directory and run:
python stabprog.py

Charts has been created in "charts" directory!
"""

import csv, operator, re
from pychart import *

reader = csv.reader(open("procMemStatistics.mem_stats"), delimiter=";")

# sort file by slot, then by pid
sortedList = sorted(reader, key=operator.itemgetter(2,4), reverse=False)

# remove headers
sortedList.pop(len(sortedList)-1)

maxNode = 0
maxHour = 0
for hour, subrack, slot, processName, pid, vmPeak, vmSize, vmLck, vmHWM, vmRSS, vmData, vmStk, vmExe, vmLib, vmPTE in sortedList:
    if (int(slot) > maxNode):
        maxNode = int(slot)
    if (int(hour) > maxHour):
        maxHour = int(hour)

print "maxNode is %s" % maxNode
print "maxHour is %s" % maxHour

for node in range(1,maxNode+1):
    print "%s" % node
    dictionaryOfPidsAndProcessNames = {}
    dictionaryOfVmSizes = {}
    dictOfFirstAndLastPidForProcessName = {}
    for hour, subrack, slot, processName, pid, vmPeak, vmSize, vmLck, vmHWM, vmRSS, vmData, vmStk, vmExe, vmLib, vmPTE in sortedList:
        if int(slot) == node:
            if pid not in dictionaryOfVmSizes:
                dictionaryOfPidsAndProcessNames.update({pid: processName})
                dictionaryOfVmSizes.update({pid: [vmSize]})
            else:
                dictionaryOfVmSizes[pid].append(vmSize)
            if int(hour) == 1 or int(hour) == maxHour:
                if not re.search("^ta_", processName):
                    if processName not in dictOfFirstAndLastPidForProcessName:
                        dictOfFirstAndLastPidForProcessName.update({processName: [pid]})
                    else:
                        dictOfFirstAndLastPidForProcessName[processName].append(pid)
    
    for key, value in dictOfFirstAndLastPidForProcessName.items():
        if value[0] != value[1] or len(value) > 2:
            print "Possible process restart on node %s: %s, %s" % (node, key, value)
    
    dictionaryOfNonConsistentVmSizesOnly = {}
    # remove process that have consistent memory usage
    for pid, vmSizes in dictionaryOfVmSizes.items():
        differentVmSizes = False
        firstValue = vmSizes[0]
        for vmSize in vmSizes:
            if vmSize != firstValue:
                differentVmSizes = True
                break
        if differentVmSizes:
            if pid not in dictionaryOfNonConsistentVmSizesOnly:
                dictionaryOfNonConsistentVmSizesOnly.update({pid: vmSizes})
            else:
                dictionaryOfNonConsistentVmSizesOnly[pid].append(vmSizes)
    
    # create graphical charts
    ar = area.T(size = (700,700),
                x_axis = axis.X(format="%d", label="time (hour)"), 
                y_axis = axis.Y(format="%d", label="vmSize (kB)"))
    
    theme.get_options()
    theme.use_color = True
    theme.output_file="charts/memchart-node-%s.png" % node
    theme.reinitialize()
    
    for pid, vmSizes in dictionaryOfNonConsistentVmSizesOnly.items():
        data = []
        for hour, vmSize in enumerate(vmSizes):
            data.append([hour, int(vmSize)])
        ar.add_plot(line_plot.T(label=dictionaryOfPidsAndProcessNames[pid], data=data))
    
    ar.draw()
print "Done!"
