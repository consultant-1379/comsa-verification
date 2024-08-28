package se.ericsson.jcat.omp.util;

import java.io.File;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

import org.junit.Assert;
import org.junit.BeforeClass;
import org.junit.Test;

import se.ericsson.jcat.omp.fw.OmpLibraryException;

public class ToolsTest {

    @Test
    public void testPortCheckAndRunCommandLocal() {
        // Should always fail unless there is a host called "non_existing_host", and it has port 23654 open
        Assert.assertFalse(Tools.isPortOpen("non_existing_host", 23654));
    }

    @Test
    public void testWaitUntilTrue() {
        Assert.assertTrue(Tools.waitUntilTrue(new SthToWait(), "secondTimeIsTrue", new Object[] { "dummy" }, 1, 3));
    }

    @Test
    public void testWaitUntilTrueFalseCase() {
        Assert.assertFalse(Tools.waitUntilTrue(new SthToWait(), "alwaysFalse", new Object[] { 1 }, 1, 2));
    }

    @Test(expected = OmpLibraryException.class)
    public void testWaitUntilTrueStopOnFailureCase1() throws OmpLibraryException {
        Tools.waitUntilTrue(new SthToWait(), "throwExceptions", new Object[] { true }, 1, 20, true);
    }

    @Test
    public void testWaitUntilTrueStopOnFailureCase2() throws OmpLibraryException {
        Assert.assertFalse(Tools.waitUntilTrue(new SthToWait(), "throwExceptions", new Object[] { true }, 1, 1, false));
    }

    @Test(expected = RuntimeException.class)
    public void testWaitUntilTrueExceptionCase1() throws OmpLibraryException {
        Tools.waitUntilTrue(new SthToWait(), "secondTimeIsTrue", new Object[] { 1 }, 1, 20, true);
    }

    @Test(expected = RuntimeException.class)
    public void testWaitUntilTrueExceptionCase2() throws OmpLibraryException {
        Tools.waitUntilTrue(new SthToWait(), "notexist", new Object[] { 1 }, 1, 20, true);
    }

    @Test(expected = RuntimeException.class)
    public void testWaitUntilTrueExceptionCase3() throws OmpLibraryException {
        Tools.waitUntilTrue(new SthToWait(), "notWaitable", null, 1, 20, true);
    }

    @Test
    public void testWaitUntilTrueNullArgCase() throws OmpLibraryException {
        Assert.assertTrue(Tools.waitUntilTrue(new SthToWait(), "alwaysTrue", null, 1, 20, true));
    }

    @Test
    public void testWaitUntilTrueSwticherCase() throws OmpLibraryException {
        Assert.assertTrue(Tools.waitUntilTrue(new SthToWait(), "switcher", new Object[] { true }, 1, 20, true));
        Assert.assertFalse(Tools.waitUntilTrue(new SthToWait(), "switcher", new Object[] { false }, 1, 2, true));
    }

    @Test
    public void testWaitUntilTrueMapCase() throws OmpLibraryException {
        Assert.assertTrue(Tools.waitUntilTrue(new SthToWait(), "alwaysTrue", new Object[] {
                new HashMap<String, String>(), 1, (long) 2, 3 }, 1, 20, true));
        Assert.assertTrue(Tools.waitUntilTrue(new SthToWait(), "alwaysTrue", new Object[] {
                new HashMap<String, String>(), 1, (long) 2, new Integer(3) }, 1, 20, true));
        Map<String, String> map = new HashMap<String, String>();
        Assert.assertTrue(Tools.waitUntilTrue(new SthToWait(), "alwaysTrue", new Object[] { map, new Integer(1),
                new Long(2), 3 }, 1, 20, true));
    }

    @Test
    public void testGetResource() throws IOException {
        File tempFile = new File("target/tmpfile");
        Tools.extractResourceFile("testfile", this.getClass(), tempFile, false);
        String result = Tools.readFileToString(tempFile);
        Tools.deleteQuietly(tempFile);
        Assert.assertFalse(tempFile.exists());
        Assert.assertTrue("File content not match!", result.equals("Do not change the content"));
    }

    @Test
    public void testGetResourceAndRead() throws IOException {
        String txt = Tools.extractResourceFileAndReadContent("testfile", this.getClass(), null);
        Assert.assertTrue("File content not match!", txt.equals("Do not change the content"));
    }

    @Test
    public void testGetRelativePath() {
        File tempFile = new File("target/tmpfile");
        Tools.extractResourceFile("testfile", this.getClass(), tempFile, false);
        String[] base = new String[] { "target/", tempFile.getParentFile().getAbsolutePath(),
                tempFile.getAbsolutePath() };
        String sampleFile1 = "target/file1";
        String sampleFile2 = "file2";
        String sampleFile3 = tempFile.getParent() + "/sdsd/file3";
        String sampleFile4 = "sdsd/file4";
        String sampleFile5 = tempFile.getAbsolutePath();
        String sampleFile6 = tempFile.getPath();
        String sampleFile7 = "target";
        String sampleFile8 = ".";
        checkPathMultiBase("file1", sampleFile1, base);
        checkPathMultiBase("../file2", sampleFile2, base);
        checkPathMultiBase("sdsd/file3", sampleFile3, base);
        checkPathMultiBase("../sdsd/file4", sampleFile4, base);
        checkPathMultiBase("tmpfile", sampleFile5, base);
        checkPathMultiBase("tmpfile", sampleFile6, base);
        checkPathMultiBase(".", sampleFile7, base);
        checkPathMultiBase("..", sampleFile8, base);
    }

    @Test
    public void testGetRelativeMacAddress() throws OmpLibraryException {
        Assert.assertEquals("ff:ff:ff:ff:ff:fe", Tools.getRelativeMacAddress("ff:ff:ff:ff:ff:ff", -1));
        Assert.assertEquals("00:00:00:00:00:00", Tools.getRelativeMacAddress("FF:FF:FF:FF:FF:FF", 1));
        Assert.assertEquals("4f:ff:f9:d3:e0:fd", Tools.getRelativeMacAddress("20:89:4f:ff:F9:d3:E0:FE", -1));
        Assert.assertEquals("90:3e:7b:9a:0c:7e", Tools.getRelativeMacAddress("90:3e:7b:9a:0c:7f", 0xffffffff));
        Assert.assertEquals("90:3e:7b:99:fd:91", Tools.getRelativeMacAddress("90:3E:7B:9a:0c:7f", -0xeee));
    }

    private void checkPathMultiBase(String expect, String sample, String... base) {
        for (String b : base) {
            Assert.assertEquals(expect, Tools.getRelativePath(b, sample));
        }
    }

    @BeforeClass
    public static void createTargetDir() {
        File targetDir = new File("target");
        if (!targetDir.exists() || !targetDir.isDirectory()) {
            targetDir.mkdirs();
        }
    }

    public class SthToWait {

        private int counter = 0;

        public SthToWait() {
        }

        // The dummy argument is only for code coverage
        public boolean secondTimeIsTrue(String dummy) {
            counter++;
            return counter >= 2;
        }

        public boolean alwaysTrue(Map<String, String> dummy, int a, long b, Integer c) {
            return true;
        }

        public boolean alwaysFalse(int dummy) {
            return false;
        }

        public boolean throwExceptions(boolean dummy) throws OmpLibraryException {
            throw new OmpLibraryException("Throw exception for testing. It is expected to get this.");
        }

        public int notWaitable() {
            return 1;
        }

        public boolean alwaysTrue() {
            return true;
        }

        public boolean switcher(boolean result) {
            return result;
        }
    }
}
