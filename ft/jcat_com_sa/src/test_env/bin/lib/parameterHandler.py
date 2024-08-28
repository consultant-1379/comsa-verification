#!/usr/bin/env python
# coding=iso-8859-15
###############################################################################
#
# © Ericsson AB 2009 All rights reserved.
# The information in this document is the property of Ericsson.
# Except as specifically authorized in writing by Ericsson,
# the receiver of this document shall keep the information contained
# herein confidential and shall protect the same in whole or in partF
# from disclosure and dissemination to third parties.
# Disclosure and disseminations to the receivers employees shall only be made
# on a strict need to know basis.
#
###############################################################################

import sys
import string
import xml.dom.minidom as dom 
import re

def getConfigData(dict):

    configData = {}

    for key in dict['config'].keys() :
        if key in dict.keys():
            configData[key] = dict[key]
        else:
            configData[key] = dict['config'][key]

    return configData

def getData(dict, dns):
    
    # stupid way to fix problems reading xml dynamic
    l = dns.split(':')    
    p = string.join(l, '"]["')
    p = '["' + p + '"]' + '["' + l[-1] + '"]' 
    res = None
    try:
        res = eval("%s%s" % (dict, p))
    except Exception, e:
        print "ERROR: Unknown key %s" % e
        
    #cast 
    try:
        r = eval(res)
    except:
        r = res    
        
    return r
   
   
def getXmlConfig(xmlFile):
    '''
        Information:
        
        Arguments:
        
        Returns:
        
    '''

    elements = {}
    doc = _readXmlFile(xmlFile)
    
    def recursive(node): 
        if node.hasChildNodes():
	    if not elements.has_key(node.tagName.encode()):
	        elements[node.tagName.encode()] = {}
            for child in node.childNodes:
                if child.nodeType == child.ELEMENT_NODE:
                    if child.hasChildNodes():
                        if not elements[node.tagName.encode()].has_key(child.tagName.encode()):
		     	            elements[node.tagName.encode()][child.tagName.encode()] = {}                       
                        for c in child.childNodes:
                            if c.nodeType == c.ELEMENT_NODE:
                                if c.hasChildNodes():
                                    if not elements[node.tagName.encode()][child.tagName.encode()].has_key(c.tagName.encode()):
                                        elements[node.tagName.encode()][child.tagName.encode()][c.tagName.encode()] = {}
                                    for a in c.childNodes:
                                        if a.nodeType == a.ELEMENT_NODE:
                                            if a.hasChildNodes(): 
                                                if not elements[node.tagName.encode()][child.tagName.encode()][c.tagName.encode()].has_key(a.tagName.encode()):
                                                    elements[node.tagName.encode()][child.tagName.encode()][c.tagName.encode()][a.tagName.encode()] = {}
                                                for n in a.childNodes:
                                                    if n.nodeType == n.ELEMENT_NODE:
                                                        if n.hasChildNodes(): 
                                                            if not elements[node.tagName.encode()][child.tagName.encode()][c.tagName.encode()][a.tagName.encode()].has_key(n.tagName.encode()):
                                                                elements[node.tagName.encode()][child.tagName.encode()][c.tagName.encode()][a.tagName.encode()][n.tagName.encode()] = {}
                                                            for x in n.childNodes:
                                                                if x.nodeType == x.ELEMENT_NODE:
                                                                    if x.hasChildNodes(): 
                                                                        if not elements[node.tagName.encode()][child.tagName.encode()][c.tagName.encode()][n.tagName.encode()][a.tagName.encode()].has_key(x.tagName.encode()):
                                                                            elements[node.tagName.encode()][child.tagName.encode()][c.tagName.encode()][a.tagName.encode()][n.tagName.encode()][x.tagName.encode()] = {}
                                                                
                                                                elif x.nodeType == x.TEXT_NODE:
                                                                    elements[node.tagName.encode()][child.tagName.encode()][c.tagName.encode()][a.tagName.encode()][n.tagName.encode()][x.parentNode.tagName.encode()] = x.data.encode()    
                                                    elif n.nodeType == n.TEXT_NODE:
                                                        elements[node.tagName.encode()][child.tagName.encode()][c.tagName.encode()][a.tagName.encode()][n.parentNode.tagName.encode()] = n.data.encode()    
                                        elif a.nodeType == a.TEXT_NODE:
                                            elements[node.tagName.encode()][child.tagName.encode()][c.tagName.encode()][a.parentNode.tagName.encode()] = a.data.encode()                            
                            elif c.nodeType == c.TEXT_NODE:
                                elements[node.tagName.encode()][child.tagName.encode()][c.parentNode.tagName.encode()] = c.data.encode()
# Why do we not have this elseif below???
#                elif child.nodeType == child.TEXT_NODE:
#                    elements[node.tagName.encode()][child.parentNode.tagName.encode()] = child.data.encode()
                    
    de = doc.documentElement.tagName
    nodes = doc.getElementsByTagName(de)[0]  
    recursive(nodes)
    
    return elements[de]
           

def _readXmlFile(file):

    fd = None
    xmlString = None
    doc = None
    
    #print file
    try:
        try:

            fd = open(file, 'r')   
            xmlString = fd.read()
        except Exception, e:
            print "ERROR: %s" % e
    finally:
        if fd != None:
            fd.close()
    
    if xmlString != None:
        doc = dom.parseString(xmlString)
    
    return doc


def fixSuite(suiteFile):
    """
    this funktion fix so all testcases are in order... if there is a XML error in 
    the testcase before or after the changes this function aborts
    
    example:
    input file:
    <testcase2>first</testcase2>
    <testcaseXXX>second</testcaseXXX>
    <testcase1>third</testcase1>
    becomes:
    <testcase1>first</testcase1>
    <testcase2>second</testcase2>
    <testcase3>third</testcase3>
    """
    
    
    
    fd = None
    
    #read file
    try:
        fd = open(suiteFile, 'r') 
        org_xmlString = fd.read()
        xmlString = org_xmlString
        dom.parseString(xmlString)
    except Exception, e:
        print "suite(%s) has errors before we start so we abort: %s" % (suiteFile, e)
        return 
    finally:
        if fd != None:
            fd.close()
        fd = None
    ##replaces all testcase tags whit spesial magik strins
    
    magikStringStart = """Very_spesial_string_not_used_in_the_XML_file_-_start_of_testcase"""
    magikStringEnd = """Very_spesial_string_not_used_in_the_XML_file_-_end_of_testcase"""
    
    regTestcase = "<\s*testcase.*?>"#< testcase[something]> 
    regTestcaseEnd = "<\s*/\s*testcase.*?>"#< / testcase[something]>
    
    xmlString = re.sub(regTestcase, magikStringStart, xmlString)
    xmlString = re.sub(regTestcaseEnd, magikStringEnd, xmlString)
    
    
    #replaces magic strings whit a correct testcase tag    
    counter = 1
    while(xmlString.find(magikStringStart) != -1):        
        testcase = "testcase%d" % counter        
        xmlString = xmlString.replace(magikStringStart, "<%s>" % testcase, 1)
        xmlString = xmlString.replace(magikStringEnd, "</%s>" % testcase, 1)
        counter += 1
    
    #if there is a difference whit the new XML and the old one we write the new one to file
    if(org_xmlString != xmlString):
        #write the file back if it can be parsed
        try:
            dom.parseString(xmlString)
        except:
            return
            
        
        fd = None
        #text can be parsed so it safe to write
        try:
            fd = open(suiteFile, 'w+')
            fd.write(xmlString)
        except Exception, e:
            print "\nERROR!!!\nERROR!!!"
            print "ERROR!!! while writing back the altered suite, file might in worst case be empty: \"%s\".\n\t%s" % (suiteFile, e)
            print "ERROR!!!\nERROR!!!\n"
            return
        finally:
            if fd != None:
                fd.close()


if __name__ == "__main__":
    dict = getXmlConfig(sys.argv[1])
    print getData(dict, 'testInstanceConfiguration:sc:profile')

