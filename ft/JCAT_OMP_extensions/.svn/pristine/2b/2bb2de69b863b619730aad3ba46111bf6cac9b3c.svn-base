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

import java.util.ArrayList;
import java.util.List;

import org.apache.log4j.Logger;
import org.python.util.PythonInterpreter;

import se.ericsson.commonlibrary.CommonLibrary;
import se.ericsson.commonlibrary.CommonLibraryDataProvider;
import se.ericsson.jcat.fw.jython.Jythonizer;
import se.ericsson.jcat.omp.fw.OmpLibrary;
import se.ericsson.jcat.omp.fw.OmpLibraryException;
import se.ericsson.jcat.omp.fw.OmpSut;

public class RouterLibImpl extends OmpLibrary implements RouterLib {

    private static Logger logger = Logger.getLogger(RouterLibImpl.class);

    private PythonInterpreter interp = null;
    private List<Class<? extends CommonLibrary>> l;
    private CommonLibraryDataProvider data;

    OmpSut sut = null;

    public RouterLibImpl() {
        l = new ArrayList<Class<? extends CommonLibrary>>();
    }

    /**
     * Creates a new instance of <code>RouterLib</code>.
     * 
     * @param sut
     * @throws Exception
     */
    public RouterLibImpl(final OmpSut sut) throws Exception {
        this.sut = sut;
        this.interp = Jythonizer.getInstance();
    }

    /**
     * Returns the unique name of this library.
     */
    @Override
    public String getName() {
        return "RouterLib";
    }

    /**
     * Imports the python lib and executes the setup method.
     */
    public void setUp() {
        // TODO setup the python lib for router
    }

    /**
     * Executes teardown method in python lib.
     */
    public void tearDown() {
        // TODO teardown the python lib for router
    }

    @Override
    public void setLibraryDataProvider(CommonLibraryDataProvider data) {
        this.data = data;
    }

    @Override
    public CommonLibraryDataProvider getLibraryDataProvider() {
        return data;
    }

    @Override
    public Class<? extends CommonLibrary> getLibraryInterface() {
        return RouterLib.class;
    }

    @Override
    public String getUniqueIdentifier() {
        return "RDA Router lib";
    }

    @Override
    public void initialize() {
        this.setUp();
    }

    @Override
    public void shutdown() {
        this.tearDown();
    }

    @Override
    public List<Class<? extends CommonLibrary>> getRuntimeDependencyList() {
        return l;
    }

    @Override
    public List<Class<? extends CommonLibrary>> getSetupDependencyList() {
        return l;
    }

    @Override
    public String portDown(String target, String port) throws OmpLibraryException {
        throw new OmpLibraryException("Not supported yet in this router type!");
    }

    @Override
    public String portUp(String target, String port) throws OmpLibraryException {
        throw new OmpLibraryException("Not supported yet in this router type!");
    }

    @Override
    public boolean powerOff(String target) throws OmpLibraryException {
        throw new OmpLibraryException("Not supported yet in this router type!");
    }

    @Override
    public boolean powerOn(String target) throws OmpLibraryException {
        throw new OmpLibraryException("Not supported yet in this router type!");
    }

    @Override
    public void setSut(final OmpSut sut) {
        this.sut = sut;
    }

    @Override
    public String[] getRuntimeDependencies() {
        return new String[] {};
    }

    @Override
    public String[] getSetupDependencies() {
        return new String[] {};
    }

}
