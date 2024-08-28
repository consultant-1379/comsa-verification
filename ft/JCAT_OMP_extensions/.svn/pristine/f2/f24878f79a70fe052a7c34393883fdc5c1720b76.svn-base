/*------------------------------------------------------------------------------
 *******************************************************************************
 * COPYRIGHT Ericsson 2011
 *
 * The copyright to the computer program(s) herein is the property of
 * Ericsson Inc. The programs may be used and/or copied only with written
 * permission from Ericsson Inc. or in accordance with the terms and
 * conditions stipulated in the agreement/contract under which the
 * program(s) have been supplied.
 *******************************************************************************
 *----------------------------------------------------------------------------*/
package se.ericsson.jcat.omp.library;

import org.apache.log4j.Logger;
import org.python.core.PyException;
import org.python.core.PyList;
import org.python.core.PyObject;
import org.python.util.PythonInterpreter;

import se.ericsson.jcat.fw.jython.Jythonizer;
import se.ericsson.jcat.omp.fw.OmpLibrary;
import se.ericsson.jcat.omp.fw.OmpLibraryException;
import se.ericsson.jcat.omp.fw.OmpSut;

/**
 * Implements the Java API methods for Python library ethswitch_lib.
 */
public class SmartEdgeLibImpl extends OmpLibrary implements SmartEdgeLib {

    private static Logger logger = Logger.getLogger(SmartEdgeLibImpl.class);

    private PythonInterpreter interp = null;

    OmpSut sut = null;

    /**
     * Creates a new instance of <code>EthSwitchLib</code>.
     * 
     * @param sut
     * @throws Exception
     */
    public SmartEdgeLibImpl(final OmpSut sut) throws Exception {
        this.sut = sut;
        this.interp = Jythonizer.getInstance();
    }

    /**
     * Returns the unique name of this library.
     */
    public String getName() {
        return "SmartEdgeLib";
    }

    /**
     * Method called by LibraryBroker to set the Sut of the library.
     */
    public void setSut(final OmpSut sut) {
        this.sut = sut;
    }

    /**
     * Imports the python lib and executes the setup method.
     */
    public void setUp() {
        interp.exec("import omp.tf.smartedge_lib as smartedge_lib");
        interp
                .exec("if(hasattr(smartedge_lib, 'setUp')): smartedge_lib.setUp()");
    }

    /**
     * Executes teardown method in python lib.
     */
    public void tearDown() {
        interp
                .exec("if(hasattr(smartedge_lib, 'tearDown')): smartedge_lib.tearDown()");
    }

    /**
     * Return runtime dependencies.
     */
    public String[] getRuntimeDependencies() {
        return new String[] { "LoggerLib", "TargetDataLib", "SnmpLib" };
    }

    /**
     * Return setup dependencies.
     */
    public String[] getSetupDependencies() {
        return new String[] { "LoggerLib", "TargetDataLib", "SnmpLib" };
    }
    
    public String portDown(final String target, final String port)
    throws OmpLibraryException {
    	/*
        interp.exec("result = smartedge_lib.portDown('" + target + "', '"
        + port + "')");
        final PyList result = (PyList) interp.get("result");
        String cmdRes = parseJythonListResult(result);
        logger.info(cmdRes);    
        return result.toString();*/
    	throw new OmpLibraryException("Unsupported in current SE-100 IF-MIB implementation");
     }   

    public String portUp(final String target, final String port)
            throws OmpLibraryException {
        interp.exec("result = smartedge_lib.portUp('" + target + "', '" + port
                + "')");
        final PyList result = (PyList) interp.get("result");
        String cmdRes = parseJythonListResult(result);
        logger.info(cmdRes);
        return result.toString();
    }
    
    public int getIfNumberForPort(final String target, final String portName)
    	throws OmpLibraryException {
    	String cmdRes = null;
    	int port = 1;
    	PyList result = null;
    	do { 
    		interp.exec("result = smartedge_lib.getIfName('" + target + "', '" + port
                + "')");
    		result = (PyList) interp.get("result");
    		cmdRes = parseJythonListResult(result);
    		logger.info(cmdRes);
    		if (cmdRes.contains(portName)){
    			return port;
    		}
    		else{
    			port++;
    		}
    	}
    	while (port < 20);
    	throw new OmpLibraryException("Giving up after 20 attempts. Unable to find port number for port name " + portName);
    }
    

    /*
     * Parse the PyTuple result structure returned from the Jython API method.
     */
    private String parseJythonListResult(final PyList pl)
            throws OmpLibraryException {
        PyObject pyVerdict;
        PyObject pyMessage;
        PyObject pyCommand;
        try {
            pyVerdict = pl.__getitem__(0);
            logger.debug("Parsing PyList arg0: " + pyVerdict.toString());
            pyMessage = pl.__getitem__(1);
            logger.debug("Parsing PyList arg1: " + pyMessage.toString());
            pyCommand = pl.__getitem__(2);
            logger.debug("Parsing PyList arg2: " + pyCommand.toString());
        }
        catch(final PyException pe) {
            throw new OmpLibraryException(
        			"Parsing error, PyList key not found. PyException was: " + pe.toString());
        }

        // Do we need null checks on these?
        final String verdict = pyVerdict.toString();
        final String message = pyMessage.toString();

        if(!verdict.equalsIgnoreCase("SUCCESS")) {
            throw new OmpLibraryException(message);
        }

        return message;
    }
}
