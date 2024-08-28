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

import org.python.util.PythonInterpreter;

import se.ericsson.jcat.fw.jython.Jythonizer;
import se.ericsson.jcat.omp.fw.OmpLibrary;
import se.ericsson.jcat.omp.fw.OmpLibraryException;
import se.ericsson.jcat.omp.fw.OmpSut;

/**
 * Implements the Java API methods for Python library misc_lib. TODO: Implement
 * all methods.
 */
public class MiscLibImpl extends OmpLibrary implements MiscLib {
	private static Logger logger = Logger.getLogger(SshLibImpl.class);

    private PythonInterpreter interp = null;

    OmpSut sut = null;

    /**
     * Creates a new instance of <code>MiscLib</code>.
     * 
     * @param sut
     * @throws Exception
     */
    public MiscLibImpl(final OmpSut sut) throws Exception {
        this.sut = sut;
        this.interp = Jythonizer.getInstance();
    }

    /**
     * Returns the unique name of this library.
     */
    public String getName() {
        return "MiscLib";
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
        interp.exec("import omp.tf.misc_lib as misc_lib");
        interp.exec("if(hasattr(misc_lib, 'setUp')): misc_lib.setUp()");
    }

    /**
     * Executes teardown method in python lib.
     */
    public void tearDown() {
        interp.exec("if(hasattr(misc_lib, 'tearDown')): misc_lib.tearDown()");
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

    public String execCommand(final String command) 
    throws OmpLibraryException{
        interp.exec("result = misc_lib.execCommand('" + command + "')");
        
        final PyTuple result = (PyTuple) interp.get("result");
        return parseJythonResult(result);
    }

    public String waitTime(final int sleep_time) 
    throws OmpLibraryException{
        interp.exec("result = misc_lib.waitTime(" + sleep_time + ")");
        
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
}
