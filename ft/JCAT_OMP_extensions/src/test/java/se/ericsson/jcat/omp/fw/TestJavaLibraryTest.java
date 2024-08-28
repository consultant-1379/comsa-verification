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

import junit.framework.TestSuite;

import org.junit.After;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;

import se.ericsson.jcat.fw.SUTHolder;

public class TestJavaLibraryTest {

    private OmpTestSetup setup = null;

    private final String JAVA_LIB_A = "se.ericsson.jcat.omp.fw.JavaLibrary:se.ericsson.jcat.omp.fw.A_JavaLibrary";
    private final String JAVA_LIB_B = "se.ericsson.jcat.omp.fw.JavaLibrary:se.ericsson.jcat.omp.fw.B_JavaLibrary";
    private final String JAVA_LIB_C = "se.ericsson.jcat.omp.fw.JavaLibrary:se.ericsson.jcat.omp.fw.C_JavaLibrary";
    private final String JAVA_LIB_MISSING = "se.ericsson.jcat.omp.fw.JavaLibrary:se.ericsson.jcat.omp.fw.MISSING_JavaLibrary";
    private final String PY_LIB_X = "se.ericsson.jcat.omp.fw.PythonLibrary:testlibrary.X_PythonLibrary.X_PythonLibrary";
    private final String PY_LIB_Y = "se.ericsson.jcat.omp.fw.PythonLibrary:testlibrary.Y_PythonLibrary.Y_PythonLibrary";
    private final String PY_LIB_Z = "se.ericsson.jcat.omp.fw.PythonLibrary:testlibrary.Z_PythonLibrary.Z_PythonLibrary";
    private final String PY_LIB_MISSING = "se.ericsson.jcat.omp.fw.PythonLibrary:testlibrary.MISSING_PythonLibrary.MISSING_PythonLibrary";

    @Before
    public void setUp() {
        setup = new OmpTestSetup(new TestSuite());
        System.clearProperty(JAVA_LIB_A);
        System.clearProperty(JAVA_LIB_B);
        System.clearProperty(JAVA_LIB_C);
        System.clearProperty(JAVA_LIB_MISSING);
        System.clearProperty(PY_LIB_X);
        System.clearProperty(PY_LIB_Y);
        System.clearProperty(PY_LIB_Z);
        System.clearProperty(PY_LIB_MISSING);
    }

    @After
    public void tearDown() {
        setup.tearDown();
        OmpSut.removeSut();
    }

    @Test
    public void testCreateIndependentJavaLibrary() {
        System.setProperty(JAVA_LIB_C, "");
        setup.setUp();
        final OmpSut sut = (OmpSut) SUTHolder.getInstance().zones[0];

        final TestLibrary library = (TestLibrary) sut.getLibrary("C_JavaLibrary");
        Assert.assertTrue(library != null);
        Assert.assertTrue(library.isSettedUp());
        Assert.assertTrue(!(library.isTornDown()));
    }

    @Test(expected = RuntimeException.class)
    public void testCreateMissingJavaLibrary() {
        System.setProperty(JAVA_LIB_MISSING, "");
        setup.setUp();
    }

    @Test(expected = RuntimeException.class)
    public void testCreateJavaLibraryWithoutItsDependant() {
        System.setProperty(JAVA_LIB_B, "");
        setup.setUp();
    }

    @Test
    public void testCreateJavaLibraryWithItsDependant() {
        System.setProperty(JAVA_LIB_B, "");
        System.setProperty(JAVA_LIB_C, "");
        setup.setUp();
        final OmpSut sut = (OmpSut) SUTHolder.getInstance().zones[0];
        final TestLibrary library = (TestLibrary) sut.getLibrary("C_JavaLibrary");
        Assert.assertTrue(library != null);
        Assert.assertTrue(library.isSettedUp());
        Assert.assertTrue(!(library.isTornDown()));
        final TestLibrary library2 = (TestLibrary) sut.getLibrary("B_JavaLibrary");
        Assert.assertTrue(library2 != null);
        Assert.assertTrue(library2.isSettedUp());
        Assert.assertTrue(!(library2.isTornDown()));
    }

    @Test
    public void testCreateJavaLibraryWithItsSecondLevelDependant() {
        System.setProperty(JAVA_LIB_A, "");
        System.setProperty(JAVA_LIB_B, "");
        System.setProperty(JAVA_LIB_C, "");
        setup.setUp();
        final OmpSut sut = (OmpSut) SUTHolder.getInstance().zones[0];
        final TestLibrary library = (TestLibrary) sut.getLibrary("C_JavaLibrary");
        Assert.assertTrue(library != null);
        Assert.assertTrue(library.isSettedUp());
        Assert.assertTrue(!(library.isTornDown()));
        final TestLibrary library2 = (TestLibrary) sut.getLibrary("B_JavaLibrary");
        Assert.assertTrue(library2 != null);
        Assert.assertTrue(library2.isSettedUp());
        Assert.assertTrue(!(library2.isTornDown()));
        final TestLibrary library3 = (TestLibrary) sut.getLibrary("A_JavaLibrary");
        Assert.assertTrue(library3 != null);
        Assert.assertTrue(library3.isSettedUp());
        Assert.assertTrue(!(library3.isTornDown()));
    }

    @Test(expected = RuntimeException.class)
    public void testCreateJavaLibraryWithoutItsSecondLevelDependant() {
        System.setProperty(JAVA_LIB_A, "");
        System.setProperty(JAVA_LIB_B, "");
        setup.setUp();
    }

    @Test
    public void testCreateIndependentPythonLibrary() {
        System.setProperty(PY_LIB_Z, "");
        setup.setUp();
        final OmpSut sut = (OmpSut) SUTHolder.getInstance().zones[0];
        final TestLibrary library = (TestLibrary) sut.getLibrary("Z_PythonLibrary");
        Assert.assertTrue(library != null);
        Assert.assertTrue(library.isSettedUp());
        Assert.assertTrue(!(library.isTornDown()));
    }

    @Test(expected = RuntimeException.class)
    public void testCreateMissingPythonLibrary() {
        System.setProperty(PY_LIB_MISSING, "");
        setup.setUp();
    }

    @Test(expected = RuntimeException.class)
    public void testCreatePythonLibraryWithoutItsDependant() {
        System.setProperty(PY_LIB_Y, "");
        setup.setUp();
    }

    @Test
    public void testCreatePythonLibraryWithItsDependant() {
        System.setProperty(PY_LIB_Y, "");
        System.setProperty(PY_LIB_Z, "");
        setup.setUp();
        final OmpSut sut = (OmpSut) SUTHolder.getInstance().zones[0];
        final TestLibrary library = (TestLibrary) sut.getLibrary("Y_PythonLibrary");
        Assert.assertTrue(library != null);
        Assert.assertTrue(library.isSettedUp());
        Assert.assertTrue(!(library.isTornDown()));
        final TestLibrary library2 = (TestLibrary) sut.getLibrary("Z_PythonLibrary");
        Assert.assertTrue(library2 != null);
        Assert.assertTrue(library2.isSettedUp());
        Assert.assertTrue(!(library2.isTornDown()));
    }

    @Test
    public void testCreatePythonLibraryWithItsSecondLevelDependant() {
        System.setProperty(PY_LIB_X, "");
        System.setProperty(PY_LIB_Y, "");
        System.setProperty(PY_LIB_Z, "");
        setup.setUp();
        final OmpSut sut = (OmpSut) SUTHolder.getInstance().zones[0];
        final TestLibrary library = (TestLibrary) sut.getLibrary("X_PythonLibrary");
        Assert.assertTrue(library != null);
        Assert.assertTrue(library.isSettedUp());
        Assert.assertTrue(!(library.isTornDown()));
        final TestLibrary library2 = (TestLibrary) sut.getLibrary("Y_PythonLibrary");
        Assert.assertTrue(library2 != null);
        Assert.assertTrue(library2.isSettedUp());
        Assert.assertTrue(!(library2.isTornDown()));
        final TestLibrary library3 = (TestLibrary) sut.getLibrary("Z_PythonLibrary");
        Assert.assertTrue(library3 != null);
        Assert.assertTrue(library3.isSettedUp());
        Assert.assertTrue(!(library3.isTornDown()));
    }

    @Test(expected = RuntimeException.class)
    public void testCreatePythonLibraryWithoutItsSecondLevelDependant() {
        System.setProperty(PY_LIB_X, "");
        System.setProperty(PY_LIB_Y, "");
        setup.setUp();
    }
}
