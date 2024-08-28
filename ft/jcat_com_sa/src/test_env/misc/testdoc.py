#!/vobs/tsp_saf/tools/Python/linux/bin/python
#coding=iso-8859-1
###############################################################################
#
# Copyright Ericsson AB 2010 All rights reserved.
# The information in this document is the property of Ericsson.
# Except as specifically authorized in writing by Ericsson,
# the receiver of this document shall keep the information contained herein
# confidential and shall protect the same in whole or in part from disclosure
# and dissemination to third parties.
# Disclosure and disseminations to the receivers employees shall only be made
# on a strict need to know basis.
#
###############################################################################

"""
GENERAL INFORMATION:

    Test cases:
    TC-DOC-001 - Testdoc generation 
    
    Sensitivity:
    Low
    
    Description:
    Generate a tag tool test document/specification of all the testcases.
    
    Restrictions:
    -
    
    Test tools:
    -
    
    Help:
    -
    
    Test script:   
    N/A
    
    Configuration:    
    2SC+nPL

    Restore:
    N/A
    
==================================         
    TEST CASE SPECIFICATION:

    Tag: 
    TC-DOC-001 
       
    Id:  
    Testdoc generation
    
    Priority:


    Requirement:
    -

    Test script: 
    N/A
    
    Configuration: 
    2SC+nPL

    Action:
    Go through all test case files and ignore those specified in the
    ignorelist file.
    
    For each file, cut the comments between the first and the seconds
    occurrence of situation quotes and paste it to a new temporary file.
    
    From this temporary file, insert suitable xml tags so that we can
    use tag tool to open it. For all those lines including something
    specified in the boldwords file, insert a tag to make them bold.
    
    Result:
    A generated test document/specification. 

    Restore:
    -

==================================
"""
import re
import os

if __name__ == "__main__":   
    ''' Testdoc generation
    '''
    
    repository = os.environ['HOME'] + '/workspace/jcat_com_sa/src'
    inputDir = '%s/test_env/testcases/' % repository
    outputFile = '%s/test_env/misc/testdocres' % repository
    ignoreListFile = '%s/test_env/misc/ignorelist' % repository
    pretextFile = '%s/test_env/misc/pretext' % repository
    boldFile = '%s/test_env/misc/boldwords' % repository
    
    ignorelist = []
    
    fignorelist = open(ignoreListFile, 'r')
    for line in fignorelist:
        ignorelist.append(line)
    fignorelist.close()
    
    #print 'The following files will be ignored:\n%s'
    
    thefiles=[]
    from os.path import join, getsize
    for root, dirs, files in os.walk(inputDir):
        for name in files:
            if "$" in name:
                name = name.replace("$",".")
            if ".class" in name:
                name = name.replace(".class","")
            if "svn-base" not in name and root==inputDir and name not in ignorelist:
                thefiles.append(name)   

    #print 'The following files will be included in the test doc:\n%s' % thefiles
        
    # Clear file
    ftestcase = open(outputFile, 'w')
    ftestcase.close()
    
    for file in thefiles:
        ftestcase = open('%s/%s' % (inputDir, file), 'r')
        linenumber = 0
        first = True
        for line in ftestcase:
            if ((("\"\"\"" in line) or ("'''" in line)) and (first==False)):
                stop = linenumber
                break
            linenumber = linenumber+1
            if ((("\"\"\"" in line) or ("'''" in line)) and (first==True)):
                start = linenumber
                first = False
        #ftestcase.close()
        
        #ftestcase = open('%s/%s' % (inputDir, file), 'r')
        ftemp = open(outputFile, 'a')
        
        linenumber = 0
        ftemp.write('\n\n*************%s*************\n\n' % file)
        for line in ftestcase:
            if linenumber>=linenumber and linenumber<stop:
                ftemp.write(line) 
            linenumber = linenumber+1
        ftestcase.close() 
        ftemp.close()            
        
    # Clear file
    foutput = open('%s.xml' % outputFile, 'w')
    foutput.close()
    
    foutput = open("%s.xml" % outputFile, 'a')
    ftestcase = open(outputFile, 'r')
    #f4 = open(outputFile, 'r')
    fpretext = open(pretextFile)
    
    for line in fpretext:
        foutput.write(line)
        
    fboldletters = open(boldFile)
    
    boldletters = []        
    for line in fboldletters:
        if '\n' in line:
            line = line.replace('\n','')
        boldletters.append(line)
    
    #print 'The following words are in the boldletters list:\n%s' % boldletters
    
    fboldletters.close()
    
    theid=0
    notes = False
    first = True
    isbold = False
    
    for line in ftestcase:
        if "<" in line:
            line = line.replace("<","")
        if ">" in line:
            line = line.replace(">","")
        if "&" in line:
            line = line.replace("&","")
        if "*******" in line:
            if(first == False):
                foutput.write("<?Pub Caret1?>\n</chl1>\n")
                notes = False
            foutput.write("<chl1><title xml:id=\"id_%s\">%s</title>" % (theid, line[13:-14]))
            theid = theid+1
            first = False
            notes = True
        else:
            if notes == True:                
                for item in boldletters:
                    if item in line:
                        foutput.write("\n<p><emph type=\"medium\">%s</emph></p>" % line[0:-1])
                        isbold = True
                if isbold == False:
                    foutput.write("\n<p>%s</p>" % line[0:-1])
            isbold = False
       
    foutput.write("\n</chl1>\n</body>\n</doc>\n<?Pub *0000001012 0?>")    
     
    foutput.close()
    ftestcase.close()
    fpretext.close()  
    
    #self.fail('FAIL', self.additionalInfoText)
    print 'The file %s.xml was generated successfully!' % outputFile
