import xml.etree.ElementTree as ET
import re
import sys

files = sys.argv[1:]
for file in files:
    filename = file
    suffix = "_sorted"
    newfilename = filename + suffix
    
    o = open(filename + "_top", "w")
    o.close()
    
    o = open(filename + "_top", "a")
    for line in open(filename):
        if 'IMMSchema">' in line:
            newline = line.replace('IMMSchema">', 'IMMSchema">\n<top>')
        elif '</imm:IMM-contents>' in line:
            newline = line.replace('</imm:IMM-contents>', '</top>\n</imm:IMM-contents>')
        else:
            newline = line
        o.write(newline)
    o.close()
    
    filename = filename + "_top"
    
    tree = ET.parse(filename)
    class_container = tree.getiterator("class")
    object_container = tree.getiterator("object")
    top = tree.getiterator("top")
    
    data = []
    for elem in class_container:
        key = elem.attrib
        data.append((key, elem))
    
    data2 = []
    
    for elem in object_container:
        key = elem.attrib
        key2 = elem.findtext("dn")
        data2.append((key2, elem))
    
    data.sort()
    data2.sort()
    
    for elem in data2:
        data.append(elem)
    
    top[0].clear()
    
    for key in range(0,len(data)):
        top[0].append(data[key][1])
    
    ignoreList = ["productionDate", "timeOfLastStatusUpdate", "timeActionStarted", "SaImmAttrAdminOwnerName", "mdfModelTypeNode", "opensafImmEpoch", "saSmfBundleInstallOfflineScope", "saSmfBundleInstallOfflineCmdUri", "timeOfInstallation", "timeOfActivation", "opensafImmClassNames"]
    print "ignoreList=%s" % ignoreList
    
    counter = 0
    g = tree.find("top")
    for i in g:
        if i.tag == "object":
            a = i.findall("attr")
            for e in a:
                n = e.findall("name")
                for h in n:
                    if h.text in ignoreList:
                        i.remove(e)
                        counter = counter + 1
    print "%s attributes were removed from %s" % (counter, newfilename)
    
    tree.write(newfilename)