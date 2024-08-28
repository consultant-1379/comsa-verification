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
import org.python.core.PyList;
import org.python.core.PyObject;
import org.python.core.PyTuple;
import org.python.util.PythonInterpreter;

import se.ericsson.jcat.fw.jython.Jythonizer;
import se.ericsson.jcat.omp.fw.OmpLibrary;
import se.ericsson.jcat.omp.fw.OmpLibraryException;
import se.ericsson.jcat.omp.fw.OmpSut;

public class SnmpLibImpl extends OmpLibrary implements SnmpLib {


    private static Logger logger = Logger.getLogger(SnmpLibImpl.class);

    private PythonInterpreter interp = null;

    OmpSut sut = null;

    /**
     * Creates a new instance of <code>SshLib</code>.
     * 
     * @param sut
     * @throws Exception
     */
    public SnmpLibImpl(final OmpSut sut) throws Exception {
        this.sut = sut;
        this.interp = Jythonizer.getInstance();
    }

    /**
     * Returns the unique name of this library.
     */
    public String getName() {
        return "SnmpLib";
    }

    /**
     * Method called by LibraryBroker to set the Sut of the library
     */
    public void setSut(final OmpSut sut) {
        this.sut = sut;
    }

    public void setUp() {
        interp.exec("import omp.tf.snmp_lib as snmp_lib");
        interp.exec("if(hasattr(snmp_lib, 'setUp')): snmp_lib.setUp()");
    }

    public void tearDown() {
        interp.exec("if(hasattr(snmp_lib, 'tearDown')): snmp_lib.tearDown()");
    }

    /**
     * Returns LoggerLib as runtime dependency.
     */
    public String[] getRuntimeDependencies() {
        return new String[] { "LoggerLib", "TargetDataLib", "SshLib",
                "MiscLib" };
    }

    /**
     * Returns LoggerLib as setup dependency.
     */
    public String[] getSetupDependencies() {
        return new String[] { "LoggerLib", "TargetDataLib", "SshLib",
                "MiscLib" };
    }

    public String snmpGet(final String community, final String command)
            throws OmpLibraryException {
        interp.exec("result = snmp_lib.snmpGet('opensaf', '" + command + "')");

        final PyObject result = interp.get("result");
        if(result instanceof PyList) {
            return parseJythonListResult((PyList) result);
        }
        else if(result instanceof PyTuple) {
            return parseJythonResult((PyTuple) result);
        }
        else {
            throw new OmpLibraryException(
                    "Failed to parse snmp_lib.snmpGet result "
                            + result.toString());
        }
    }

    /*
     * Parse the PyList result structure returned from the Jython API method.
     * TODO: Throw OmpLibraryException if PyList parse fails?
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
            logger.error("Parsing error, PyList key not found", pe);
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

    /*
     * Parse the PyTuple result structure returned from the Jython API method.
     * TODO: Throw OmpLibraryException if PyTuple parse fails?
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
    
}
