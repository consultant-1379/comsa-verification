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

import org.junit.Assert;
import org.junit.Test;

import se.ericsson.jcat.omp.util.LibraryDependencySorter;

public class TestLibrarySetupDependency {

    class DummyLibrary extends OmpLibrary {
        String name;

        String[] setupDeps;

        DummyLibrary(final String name, final String[] setupDeps) {
            this.name = name;
            this.setupDeps = setupDeps;
        }

        public String getName() {
            return name;
        }

        public String[] getRuntimeDependencies() {
            return new String[0];
        }

        public String[] getSetupDependencies() {
            return setupDeps;
        }

        public void setSut(final OmpSut sut) {

        }

    }

    @Test
    public void test_a_depends_on_b() {
        final DummyLibrary a = new DummyLibrary("a", new String[] { "b" });
        final DummyLibrary b = new DummyLibrary("b", new String[] {});
        final OmpLibrary[] array = new OmpLibrary[2];
        array[0] = a;
        array[1] = b;
        new LibraryDependencySorter().sort(array);
        // printList(array);
        Assert.assertTrue(array[0].getName().equals(b.getName()));
        Assert.assertTrue(array[1].getName().equals(a.getName()));
        array[0] = b;
        array[1] = a;
        new LibraryDependencySorter().sort(array);
        // printList(array);
        Assert.assertTrue(array[0].getName().equals(b.getName()));
        Assert.assertTrue(array[1].getName().equals(a.getName()));

    }

    @Test
    public void test_a_depends_on_b_depends_on_c() {
        final DummyLibrary a = new DummyLibrary("a", new String[] { "b" });
        final DummyLibrary b = new DummyLibrary("b", new String[] { "c" });
        final DummyLibrary c = new DummyLibrary("c", new String[] {});
        final OmpLibrary[] array = new OmpLibrary[3];
        array[0] = a;
        array[1] = b;
        array[2] = c;
        new LibraryDependencySorter().sort(array);
        // printList(array);
        Assert.assertTrue(array[0].getName().equals(c.getName()));
        Assert.assertTrue(array[1].getName().equals(b.getName()));
        Assert.assertTrue(array[2].getName().equals(a.getName()));
        array[0] = c;
        array[1] = b;
        array[2] = a;
        new LibraryDependencySorter().sort(array);
        // printList(array);
        Assert.assertTrue(array[0].getName().equals(c.getName()));
        Assert.assertTrue(array[1].getName().equals(b.getName()));
        Assert.assertTrue(array[2].getName().equals(a.getName()));

    }

    @Test(expected = RuntimeException.class)
    public void test_a_depends_on_b_depends_on_a_1() {
        final DummyLibrary a = new DummyLibrary("a", new String[] { "b" });
        final DummyLibrary b = new DummyLibrary("b", new String[] { "a" });
        final OmpLibrary[] array = new OmpLibrary[2];
        array[0] = a;
        array[1] = b;
        new LibraryDependencySorter().sort(array);
    }

    @Test(expected = RuntimeException.class)
    public void test_a_depends_on_b_depends_on_a_2() {
        final DummyLibrary a = new DummyLibrary("a", new String[] { "b" });
        final DummyLibrary b = new DummyLibrary("b", new String[] { "a" });
        final OmpLibrary[] array = new OmpLibrary[2];
        array[0] = b;
        array[1] = a;
        new LibraryDependencySorter().sort(array);
    }

    @Test(expected = RuntimeException.class)
    public void test_a_depends_on_b_depends_on_c_depends_on_a_1() {
        final DummyLibrary a = new DummyLibrary("a", new String[] { "b" });
        final DummyLibrary b = new DummyLibrary("b", new String[] { "c" });
        final DummyLibrary c = new DummyLibrary("c", new String[] { "a" });
        final OmpLibrary[] array = new OmpLibrary[3];
        array[0] = a;
        array[1] = b;
        array[2] = c;
        new LibraryDependencySorter().sort(array);
    }

    @Test(expected = RuntimeException.class)
    public void test_a_depends_on_b_depends_on_c_depends_on_a_2() {
        final DummyLibrary a = new DummyLibrary("a", new String[] { "b" });
        final DummyLibrary b = new DummyLibrary("b", new String[] { "c" });
        final DummyLibrary c = new DummyLibrary("c", new String[] { "a" });
        final OmpLibrary[] array = new OmpLibrary[3];
        array[0] = c;
        array[1] = b;
        array[2] = a;
        new LibraryDependencySorter().sort(array);
    }

}
