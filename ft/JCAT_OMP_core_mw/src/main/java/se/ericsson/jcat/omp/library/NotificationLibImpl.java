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

import org.python.core.PyDictionary;
import org.python.core.PyException;
import org.python.core.PyObject;
import org.python.core.PyList;
import org.python.core.PyTuple;


import org.python.util.PythonInterpreter;

import se.ericsson.jcat.fw.jython.Jythonizer;
import se.ericsson.jcat.omp.fw.OmpLibrary;
import se.ericsson.jcat.omp.fw.OmpLibraryException;
import se.ericsson.jcat.omp.fw.OmpSut;

/**
 * Implements the Java API methods for Python library misc_lib. TODO: Implement
 * all methods.
 */
public class NotificationLibImpl extends OmpLibrary implements NotificationLib {
	private static Logger logger = Logger.getLogger(SshLibImpl.class);

    private PythonInterpreter interp = null;

    OmpSut sut = null;

    /**
     * Creates a new instance of <code>NotificationLib</code>.
     * 
     * @param sut
     * @throws Exception
     */
    public NotificationLibImpl(final OmpSut sut) throws Exception {
        this.sut = sut;
        this.interp = Jythonizer.getInstance();
    }

    /**
     * Returns the unique name of this library.
     */
    public String getName() {
        return "NotificationLib";
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
        interp.exec("import coremw.notification_lib as notification_lib");
        interp.exec("if(hasattr(notification_lib, 'setUp')): notification_lib.setUp()");
    }

    /**
     * Executes teardown method in python lib.
     */
    public void tearDown() {
        interp.exec("if(hasattr(notification_lib, 'tearDown')): notification_lib.tearDown()");
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
     * @param  expectedPatternList array
     * @param ignoredPatternList array
     * @return command result
     * @throws OmpLibraryException on command error
     */
    public String checkNotifications(final PyList expectedPatternList, final PyList ignoredPatternList, final String notifType) 
    throws OmpLibraryException{
        interp.exec("result = notification_lib.checkNotifications(" + expectedPatternList + "," + ignoredPatternList + ", '" + notifType + "' )");
        
        final PyTuple result = (PyTuple) interp.get("result");
        return parseJythonResult(result);
    }

    /**
     * Executes linux command.
     * 
     * @param  expectedPatternList array
     * @param ignoredPatternList array
     * @return command result
     * @throws OmpLibraryException on command error
     */
    public PyDictionary readAllNotifications() 
    throws OmpLibraryException{
        interp.exec("result = notification_lib.readAllNotifications()");
        
        final PyTuple result = (PyTuple) interp.get("result");
        return parseJythonResult1(result);
    }
    /**final PyDictionary targetData = (PyDictionary) interp.get("result");*/

    /**
     * clear all notifications.
     * 
     * @param  none
     * @return command result
     * @throws OmpLibraryException on command error
     */
    public String clearNotifications() 
    throws OmpLibraryException{
        interp.exec("result = notification_lib.clearNotifications()");
        
        final PyTuple result = (PyTuple) interp.get("result");
        return parseJythonResult(result);
    }
    
    
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

