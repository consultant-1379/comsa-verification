/*------------------------------------------------------------------------------
 *******************************************************************************
 * COPYRIGHT Ericsson 2009
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
import org.python.core.PyObject;
import org.python.core.PyTuple;
import org.python.core.PyList;
import org.python.core.PyDictionary;

import org.python.util.PythonInterpreter;

import se.ericsson.jcat.fw.jython.Jythonizer;
import se.ericsson.jcat.omp.fw.OmpLibrary;
import se.ericsson.jcat.omp.fw.OmpLibraryException;
import se.ericsson.jcat.omp.fw.OmpSut;

/**
 * Implements the Java API methods for Python library misc_lib. TODO: Implement
 * all methods.
 */
public class OpensafLibImpl extends OmpLibrary implements OpensafLib {
	private static Logger logger = Logger.getLogger(SshLibImpl.class);

    private PythonInterpreter interp = null;

    OmpSut sut = null;

    /**
     * Creates a new instance of <code>NotificationLib</code>.
     * 
     * @param sut
     * @throws Exception
     */
    public OpensafLibImpl(final OmpSut sut) throws Exception {
        this.sut = sut;
        this.interp = Jythonizer.getInstance();
    }

    /**
     * Returns the unique name of this library.
     */
    public String getName() {
        return "OpensafLib";
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
        interp.exec("import coremw.opensaf_lib as opensaf_lib");
        interp.exec("if(hasattr(opensaf_lib, 'setUp')): opensaf_lib.setUp()");
    }

    /**
     * Executes teardown method in python lib.
     */
    public void tearDown() {
        interp.exec("if(hasattr(opensaf_lib, 'tearDown')): opensaf_lib.tearDown()");
    }

    /**
     * Return runtime dependencies.
     */
    public String[] getRuntimeDependencies() {
        return new String[] { "LoggerLib", "SshLib" };
    }

    /**
     * Return setup dependencies.
     */
    public String[] getSetupDependencies() {
        return new String[] { "LoggerLib", "SshLib" };
    }

    /**
     * Executes linux command.
     * 
     * @param command
     */
    public String getControllerState(int subrack, int slot)
    throws OmpLibraryException{
        interp.exec("result = opensaf_lib.getControllerState(" + subrack + "," + slot + ")");
        
        final PyTuple result = (PyTuple) interp.get("result");
        return parseJythonResult(result);
    }

    /**
     * .
     * 
     * @param subrack int
     * @param slot int
     * @return  SUCCESS or ERROR
     * @throws OmpLibraryException on command error
     */
    
    public String getPayloadState(int subrack, int slot)
    throws OmpLibraryException{
        interp.exec("result = opensaf_lib.getPayloadState(" + subrack + "," + slot + ")");
        
        final PyTuple result = (PyTuple) interp.get("result");
        return parseJythonResult(result);
    }

    /**
     * .
     * 
     * @param subrack int
     * @param slot int
     * @return  SUCCESS or ERROR
     * @throws OmpLibraryException on command error
     */
    

    
    public String getServiceInstanceHaState(int subrack, int slot, final PyList serviceInstances)
    throws OmpLibraryException{
        interp.exec("result = opensaf_lib.getServiceInstanceHaState(" + subrack + "," + slot + "," + serviceInstances + ")");
        
        final PyTuple result = (PyTuple) interp.get("result");
        return parseJythonResult(result);
    }

    /**
     * .
     * 
     * @param subrack int
     * @param slot int
     * @return  SUCCESS or ERROR
     * @throws OmpLibraryException on command error
     */

    
    public String getCompOpState(int subrack, int slot, final PyList comp)
    throws OmpLibraryException{
        interp.exec("result = opensaf_lib.getCompOpState(" + subrack + "," + slot + "," + comp + ")");
        
        final PyTuple result = (PyTuple) interp.get("result");
        return parseJythonResult(result);
    }
    
    /**
     * .
     * 
     * @param subrack int
     * @param slot int
     * @return  SUCCESS or ERROR
     * @throws OmpLibraryException on command error
     */

    
    public PyDictionary getAllCompState()
    throws OmpLibraryException{
        interp.exec("result = opensaf_lib.getAllCompState()");
        
        final PyTuple result = (PyTuple) interp.get("result");
        return parseJythonResult1(result);
    }
  
    /**
     * .
     * 
     * @param subrack int
     * @param slot int
     * @return  SUCCESS or ERROR
     * @throws OmpLibraryException on command error
     */

    
    
    public String getSuReadinessState(int subrack, int slot, final PyList  serviceUnit)
    throws OmpLibraryException{
        interp.exec("result = opensaf_lib.getSuReadinessState(" + subrack + "," + slot + "," + serviceUnit + ")");
        
        final PyTuple result = (PyTuple) interp.get("result");
        return parseJythonResult(result);
    }

    /**
     * .
     * 
     * @param subrack int
     * @param slot int
     * @return  SUCCESS or ERROR
     * @throws OmpLibraryException on command error
     */

    
    
    public String getCompReadiState(int subrack, int slot, final PyList comp)
    throws OmpLibraryException{
        interp.exec("result = opensaf_lib.getCompReadiState(" + subrack + "," + slot + "," + comp + ")");
        
        final PyTuple result = (PyTuple) interp.get("result");
        return parseJythonResult(result);
    }

    /**
     * .
     * 
     * @param subrack int
     * @param slot int
     * @param comp string
     * @return  SUCCESS or ERROR
     * @throws OmpLibraryException on command error
     */
    
    
    public String getControllerHAState(int subrack, int slot)
    throws OmpLibraryException{
        interp.exec("result = opensaf_lib.getControllerHAState(" + subrack + "," + slot + ")");
        
        final PyTuple result = (PyTuple) interp.get("result");
        return parseJythonResult(result);
    }

    /**
     * .
     * 
     * @param subrack int
     * @param slot int
     * @return  SUCCESS or ERROR
     * @throws OmpLibraryException on command error
     */   
    
    private String parseJythonResult(final PyTuple pt)
    throws OmpLibraryException {
        PyObject pyVerdict;
        PyObject pyMessage;
        try {
            pyVerdict = pt.__getitem__(0);
            logger.debug("Parsing PyTuple arg0: " + pyVerdict.toString());
            pyMessage = pt.__getitem__(1);
            logger.debug("Parsing PyTuple arg1: " + pyMessage.toString());
        }
        catch(final PyException pe) {
            logger.error("Parsing error, PyTyple key not found", pe);
            return null;
        }

        // Do we need null checks on these?
        final String verdict = pyVerdict.toString();
        final String message = pyMessage.toString();

        if(!verdict.equalsIgnoreCase("SUCCESS")) {
            throw new OmpLibraryException(message);
        }

        return message;
    }
    
    /**
     * Returns a PyDictionary from a tuple containing <String, PyDictionary>
     * 
     * @param  PyTuple	The parsed response
     * @return PyDictionary The result dictionary
     * @throws OmpLibraryException on if error String not equals 'SUCCESS' or 
     */ 
    private PyDictionary parseJythonResult1(final PyTuple pt)
    		throws OmpLibraryException {
    	
    	PyObject pyVerdict;
    	PyDictionary pyMessage;
    	
	    try {
	        pyVerdict = pt.__getitem__(0);
	        pyMessage = (PyDictionary) pt.__getitem__(1);
	    }
	    catch(final PyException pe) {
	        throw new OmpLibraryException(pe.toString());
	    }
	    
	    if(!pyVerdict.toString().equalsIgnoreCase("SUCCESS")) {
	        throw new OmpLibraryException(pyVerdict.toString());
	    }
	
	    return pyMessage;
	}
}
