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

import org.python.util.PythonInterpreter;

import se.ericsson.jcat.fw.jython.Jythonizer;
import se.ericsson.jcat.omp.fw.OmpLibrary;
import se.ericsson.jcat.omp.fw.OmpSut;

/**
 * The purpose of this class is ... TODO javadoc for class
 */
public class CleartoolLibImpl extends OmpLibrary implements CleartoolLib {
    private PythonInterpreter interp = null;

    OmpSut sut = null;

    /**
     * Creates a new instance of <code>CleartoolLib</code>.
     * 
     * @param sut
     * @throws Exception
     */
    public CleartoolLibImpl(final OmpSut sut) throws Exception {
        this.sut = sut;
        this.interp = Jythonizer.getInstance();
    }

    /**
     * Returns the unique name of this library.
     */
    public String getName() {
        return "CleartoolLib";
    }

    /**
     * Method called by LibraryBroker to set the Sut of the library
     */
    public void setSut(final OmpSut sut) {
        this.sut = sut;
    }

    public void setUp() {
        interp.exec("import omp.tf.cleartool_lib as cleartool_lib");
        interp.exec("if(hasattr(cleartool_lib, 'setUp')): cleartool_lib.setUp()");
    }

    public void tearDown() {
        interp.exec("if(hasattr(cleartool_lib, 'tearDown')): cleartool_lib.tearDown()");
    }

    /**
     * No depentencies
     */
    public String[] getRuntimeDependencies() {
        return new String[] { };
    }

    /**
     * No depentencies
     */
    public String[] getSetupDependencies() {
        return new String[] { };
    }

}
