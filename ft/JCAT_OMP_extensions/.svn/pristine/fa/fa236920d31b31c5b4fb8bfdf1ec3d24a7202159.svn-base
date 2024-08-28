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
package se.ericsson.jcat.omp.fw;

/**
 * Superclass for all kinds of pluggable libraries for OMP OmpLibrary subclasses
 * should all have constructors taking an OmpSut as the only parameter
 */
abstract public class OmpLibrary {

    /**
     * Must have constructor taking OmpSut in Java classes, but Python classes
     * can have empty constructor
     */

    /**
     * Method called by LibraryBroker to set the Sut of the library
     */
    public abstract void setSut(OmpSut sut);

    /**
     * Get the unique name of the library, by which it will be referred to by
     * testcases etc.
     */
    public abstract String getName();

    /**
     * Called by the LibraryBroker on all libraries after they have been
     * instantiated. Optional to override and implement in the subclass
     */
    public void setUp() {

    }

    /**
     * Called by the LibraryBroker on all libraries before destruction of the
     * sut. Optional to override and implement in the subclass
     */
    public void tearDown() {

    }

    /**
     * Called by the LibraryBroker on all libraries during SUT initialisation to
     * see if a consistent set of libraries has been configured. Each library
     * shall provide this callback in order to tell the LibraryBroker which
     * libraries it has direct dependencies on at runtime. Note that only direct
     * dependencies shall be listed. If this library (A) has a dependency to
     * library B which in turn has a dependency to library C, then this library
     * shall list library B in its own dependency list.
     * 
     * @return A string array containing the unique names of the dependent
     *         libraries
     */
    public abstract String[] getRuntimeDependencies();

    /**
     * Called by the LibraryBroker on all libraries during SUT initialisation to
     * see what order the libraries should be setUp. Each library shall provide
     * this callback in order to tell the LibraryBroker which libraries it
     * expects already to have been setUp when its own setUp method will be
     * called. Note that only direct dependencies shall be listed. If this
     * library (A) has a setUp time dependency to library B which in turn has a
     * setUp time dependency to library C, then this library shall list library
     * B in its own dependency list.
     * 
     * @return A string array containing the unique names of the setUp time
     *         dependent libraries
     */
    public abstract String[] getSetupDependencies();

}
