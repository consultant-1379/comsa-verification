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

import se.ericsson.jcat.omp.fw.OmpLibrary;
import se.ericsson.jcat.omp.fw.OmpSut;

public class C_JavaLibrary extends OmpLibrary implements TestLibrary {
    OmpSut sut;

    boolean settedUp = false;

    boolean tornDown = false;

    public C_JavaLibrary(final OmpSut sut) {
        this.sut = sut;
    }

    public void setSut(final OmpSut sut) {
        this.sut = sut;
    }

    public String getName() {
        return "C_JavaLibrary";
    }

    public void setUp() {
        System.out.println(getName() + " setUp called");
        settedUp = true;
    }

    public void tearDown() {
        System.out.println(getName() + " tearDown called");
        tornDown = true;
    }

    public String[] getRuntimeDependencies() {
        return new String[0];
    }

    public String[] getSetupDependencies() {
        return new String[0];
    }

    /**
     * Following methods just used by JUnit tests, and should not be part of
     * normal libraries
     */

    public boolean isSettedUp() {
        return settedUp;
    }

    public void setSettedUp(final boolean settedUp) {
        this.settedUp = settedUp;
    }

    public boolean isTornDown() {
        return tornDown;
    }

    public void setTornDown(final boolean tornDown) {
        this.tornDown = tornDown;
    }

}
