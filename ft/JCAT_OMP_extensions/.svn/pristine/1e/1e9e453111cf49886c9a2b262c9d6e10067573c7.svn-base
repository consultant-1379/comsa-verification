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

import org.python.core.PyString;
import org.python.util.PythonInterpreter;

import se.ericsson.jcat.fw.jython.Jythonizer;
import se.ericsson.jcat.omp.fw.OmpLibrary;
import se.ericsson.jcat.omp.fw.OmpSut;

/**
 * The purpose of this class is ... TODO javadoc for class LoggerLibImpl
 */
public class LoggerLibImpl extends OmpLibrary implements LoggerLib {
    private PythonInterpreter interp = null;

    OmpSut sut = null;

    /**
     * Creates a new instance of <code>SshLib</code>.
     * 
     * @param sut
     * @throws Exception
     */
    public LoggerLibImpl(final OmpSut sut) throws Exception {
        this.sut = sut;
        this.interp = Jythonizer.getInstance();
    }

    /**
     * Returns the unique name of this library.
     */
    public String getName() {
        return "LoggerLib";
    }

    /**
     * Method called by LibraryBroker to set the Sut of the library
     */
    public void setSut(final OmpSut sut) {
        this.sut = sut;
    }

    public void setUp() {
        // Do imports
        interp.exec("import omp.tf.logger_lib as logger_lib");
        // TODO: Where do we read log level from?
        // TODO: Always log event.out to /tmp?
        interp.exec("if(hasattr(logger_lib, 'setUp')): logger_lib.setUp('info', '/tmp')");
    }

    public void tearDown() {
        interp.exec("if(hasattr(logger_lib, 'tearDown')): logger_lib.tearDown()");
    }

    /**
     * Returns LoggerLib as runtime dependency.
     */
    public String[] getRuntimeDependencies() {
        return new String[] { "LoggerLib" };
    }

    /**
     * Returns LoggerLib as setup dependency.
     */
    public String[] getSetupDependencies() {
        return new String[0];
    }

    public String enter() {
        interp.exec("result = logger_lib.enter()");

        final PyString result = (PyString) interp.get("result");
        return result.toString();
    }

    public String leave() {
        interp.exec("result = logger_lib.leave()");

        final PyString result = (PyString) interp.get("result");
        return result.toString();
    }

    public String logMessage(final String message, final String logLevel) {
        interp.exec("result = logger_lib.logMessage('" + message + ", "
                + logLevel + "')");

        final PyString result = (PyString) interp.get("result");
        return result.toString();
    }

    public void setLogFile(final String logFile) {
        interp.exec("logger_lib.leave('" + logFile + "')");
    }

}
