import se.ericsson.jcat.omp.fw.OmpLibrary as OmpLibrary
import se.ericsson.jcat.omp.fw.TestLibrary as TestLibrary
import se.ericsson.jcat.omp.fw.OmpSut as OmpSut
import sys

class Z_PythonLibrary(OmpLibrary, TestLibrary):
    sut = None
    settedUp = False;

    tornDown = False;

    # Construction
    def __init__(sut) :
        sut = None

        
    def setSut(self, sut):
        self.sut = sut;
    
    def getName(self) :
        return "Z_PythonLibrary";


    def setUp(self) :
        sys.stdout.write(self.getName() + " setUp called");
        self.settedUp = True;
    
    def tearDown(self) :
        sys.stdout.write(self.getName() + " tearDown called");
        self.tornDown = True;
    

    def getRuntimeDependencies(self) :
        depArray = [];
        return depArray;

    def getSetupDependencies(self) :
        depArray = [];
        return depArray;

    #
    # Following methods just used by JUnit tests, and should not be part of
    # normal libraries
    #

    def isSettedUp(self):
        return self.settedUp;
    

    def setSettedUp(self, settedUp) :
        self.settedUp = settedUp;


    def isTornDown(self) :
        return self.tornDown;


    def setTornDown(self, tornDown) :
        self.tornDown = tornDown;



