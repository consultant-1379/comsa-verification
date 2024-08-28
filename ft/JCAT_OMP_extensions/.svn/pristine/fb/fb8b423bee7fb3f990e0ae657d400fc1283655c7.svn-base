package se.ericsson.jcat.omp.fw;

import org.apache.log4j.FileAppender;
import org.apache.log4j.Logger;
import org.apache.log4j.PatternLayout;

import se.ericsson.jcat.fw.SUTHolder;
import se.ericsson.jcat.fw.jython.NonUnitJythonTestCase;
import se.ericsson.jcat.fw.utils.TestInfo;

/**
 * A base class for all Jython based OMP (SAF or MMAS) test cases
 * 
 * @author uabcsru
 * 
 */
public class OmpJythonTestCase extends NonUnitJythonTestCase {
    private static Logger logger;
    private static OmpJythonTestCase currentTC;
    String testClass;
    String testMethod;
    // Jython subclasses cannot read this variable even if it is protected.
    // It can only be read if set to public. Use currentSystemUnderTest() for now.
    protected static OmpSut currentSut;
    private static int counter;

    /**
     * Special constructor used from Saf testcases, which for legacy reasons (linked to Pyunit) assume that the single
     * method in the testcase is a method called runTest.
     * 
     * @throws Exception
     */
    public OmpJythonTestCase() throws Exception {
        this("runTest");
    }

    /**
     * Normal "JUnit style" constructor taking the name of the test method to be run
     * 
     * @param name
     *            test method to be run by this instance
     * @throws Exception
     */
    public OmpJythonTestCase(String name) throws Exception {
        super(name);
        currentTC = this;
        logger = Logger.getLogger(this.getClass());
        logger.info("Test name: " + name);
    }

    public static OmpJythonTestCase currentTestCase() {
        return currentTC;
    }

    public static OmpSut currentSystemUnderTest() {
        return currentSut;
    }

    /**
     * Overrides <code>TestCase</code> and is called before each testcase.
     * <p>
     * Cleares any outstanding events and creates a new log file.
     * <p>
     * It is important to note that if this method is overrided in a test class, that method must call
     * <code>super.setUp()</code>.
     */
    protected void setUp() throws Exception {
        super.setUp();
        currentTC = this;
        currentSut = (OmpSut) SUTHolder.getInstance().zones[0];
        setTestcase(name, name);
        logger = Logger.getLogger(this.getClass());
        logger.removeAllAppenders();
        logger.setAdditivity(false);
        logger.addAppender(new FileAppender(new PatternLayout(), TestInfo.getLogDir() + "/" + counter + "_" + name
                + ".out", false));
        counter += 1;
    }

    /**
     * Overrides <code>TestCase</code> and is called after each testcase.
     * <p>
     * Triggers traffic delta calculation and evaluates events status and saved assert statements.
     * <p>
     * It is important to note that if this method is overrided in a test class, that method must call
     * <code>super.tearDown()</code>.
     */
    protected void tearDown() throws Exception {
        setTestStep("For more info, see <a href=" + (counter - 1) + "_" + name + ".out" + ">LOG FILE</a>");
        super.tearDown();
        currentTC = null;
    }

    /**
     * This needs to be moved to framework save a String array into a file
     * 
     * @param name
     *            name of the file
     * @param info
     *            String array to be saved
     */
    public void setTestFileInfo(String name, String info) {
        String dir = this.getName();
        if (dir == null)
            dir = "tmp";
        logger.info("See the logs here: " + setTestFile(name, info, dir));
    }

    OmpSut MYSUT = null;

    public void logMsg(String msg) {
        setTestInfo(msg);
    }

    public void logMsgToFile(String msg) {
        logger.info(msg);
    }

    public void logSuccessInfo(String msg) {
        logger.info(msg);
    }

    /**
     * Mark testcase as failed, and immediately stop execution of this testcase if the condition is false.
     * 
     * @param value
     *            condition to test for true
     * @param msg
     *            message to print if the condition should be false, and execution is aborted
     */
    public void assert_(boolean value, String msg) {
        assertTrue(msg, value);
    }

    /**
     * Mapping from PyUnit Compares two booleans which are expected not to be equal and immediately stop execution of
     * this testcase if they are
     * 
     * @param a
     * @param b
     */
    public void failIfEqual(boolean a, boolean b) {
        assertFalse("boolean " + a + " equal to boolean " + b, a == b);
    }

    /**
     * Mapping from PyUnit Compares two bytes which are expected not to be equal and immediately stop execution of this
     * testcase if they are
     * 
     * @param a
     * @param b
     */
    public void failIfEqual(byte a, byte b) {
        assertFalse("byte " + a + " equal to byte " + b, a == b);
    }

    /**
     * Mapping from PyUnit Compares two chars which are expected not to be equal and immediately stop execution of this
     * testcase if they are
     * 
     * @param a
     * @param b
     */
    public void failIfEqual(char a, char b) {
        assertFalse("char " + a + " equal to char " + b, a == b);
    }

    /**
     * Mapping from PyUnit Compares two doubles which are expected not to be equal and immediately stop execution of
     * this testcase if they are
     * 
     * @param a
     * @param b
     */
    public void failIfEqual(double a, double b) {
        assertFalse("double " + a + " equal to double " + b, a == b);
    }

    /**
     * Mapping from PyUnit Compares two floats which are expected not to be equal and immediately stop execution of this
     * testcase if they are
     * 
     * @param a
     * @param b
     */
    public void failIfEqual(float a, float b) {
        assertFalse("float " + a + " equal to float " + b, a == b);
    }

    /**
     * Mapping from PyUnit Compares two ints which are expected not to be equal and immediately stop execution of this
     * testcase if they are
     * 
     * @param a
     * @param b
     */
    public void failIfEqual(int a, int b) {
        assertFalse("int " + a + " equal to int " + b, a == b);
    }

    /**
     * Mapping from PyUnit Compares two longs which are expected not to be equal and immediately stop execution of this
     * testcase if they are
     * 
     * @param a
     * @param b
     */
    public void failIfEqual(long a, long b) {
        assertFalse("long " + a + " equal to long " + b, a == b);
    }

    /**
     * Mapping from PyUnit Compares two Object which are expected not to be equal and immediately stop execution of this
     * testcase if they are
     * 
     * @param a
     * @param b
     */
    public void failIfEqual(Object a, Object b) {
        assertFalse("Object " + a + " equal to Object " + b, a.equals(b));
    }

    /**
     * Mapping from PyUnit Compares two strings which are expected not to be equal and immediately stop execution of
     * this testcase if they are
     * 
     * @param a
     * @param b
     */
    public void failIfEqual(String a, String b) {
        assertFalse("String " + a + " equal to String " + b, a.equals(b));
    }

    /**
     * Mapping from PyUnit Compares two shorts which are expected not to be equal and immediately stop execution of this
     * testcase if they are
     * 
     * @param a
     * @param b
     */
    public void failIfEqual(short a, short b) {
        assertFalse("short " + a + " equal to short " + b, a == b);
    }

    /**
     * Mapping from PyUnit Compares two booleans which are expected to be equal and immediately stop execution of this
     * testcase if not
     * 
     * @param a
     * @param b
     */
    public void failUnlessEqual(boolean a, boolean b) {
        assertEquals("boolean " + a + " not equal to boolean " + b, a, b);
    }

    /**
     * Mapping from PyUnit Compares two bytes which are expected to be equal and immediately stop execution of this
     * testcase if not
     * 
     * @param a
     * @param b
     */
    public void failUnlessEqual(byte a, byte b) {
        assertEquals("byte " + a + " not equal to byte " + b, a, b);
    }

    /**
     * Mapping from PyUnit Compares two chars which are expected to be equal and immediately stop execution of this
     * testcase if not
     * 
     * @param a
     * @param b
     */
    public void failUnlessEqual(char a, char b) {
        assertEquals("char " + a + " not equal to char " + b, a, b);
    }

    /**
     * Mapping from PyUnit Compares two doubles which are expected to be equal and immediately stop execution of this
     * testcase if not
     * 
     * @param a
     * @param b
     */
    public void failUnlessEqual(double a, double b) {
        assertEquals("double " + a + " not equal to double " + b, a, b);
    }

    /**
     * Mapping from PyUnit Compares two floats which are expected to be equal and immediately stop execution of this
     * testcase if not
     * 
     * @param a
     * @param b
     */
    public void failUnlessEqual(float a, float b) {
        assertEquals("float " + a + " not equal to float " + b, a, b);
    }

    /**
     * Mapping from PyUnit Compares two ints which are expected to be equal and immediately stop execution of this
     * testcase if not
     * 
     * @param a
     * @param b
     */
    public void failUnlessEqual(int a, int b) {
        assertEquals("int " + a + " not equal to int " + b, a, b);
    }

    /**
     * Mapping from PyUnit Compares two longs which are expected to be equal and immediately stop execution of this
     * testcase if not
     * 
     * @param a
     * @param b
     */
    public void failUnlessEqual(long a, long b) {
        assertEquals("long " + a + " not equal to long " + b, a, b);
    }

    /**
     * Mapping from PyUnit Compares two objects which are expected to be equal and immediately stop execution of this
     * testcase if not
     * 
     * @param a
     * @param b
     */
    public void failUnlessEqual(Object a, Object b) {
        assertEquals("Object " + a + " not equal to Object " + b, a, b);
    }

    /**
     * Mapping from PyUnit Compares two strings which are expected to be equal and immediately stop execution of this
     * testcase if not
     * 
     * @param a
     * @param b
     */
    public void failUnlessEqual(String a, String b) {
        assertEquals("String " + a + " not equal to String " + b, a, b);
    }

    /**
     * Mapping from PyUnit Compares two shorts which are expected to be equal and immediately stop execution of this
     * testcase if not
     * 
     * @param a
     * @param b
     */
    public void failUnlessEqual(short a, short b) {
        assertEquals("short " + a + " not equal to short " + b, a, b);
    }

    /**
     * Mapping from PyUnit Tests condition, and if false, immediately stop execution of this testcase
     * 
     * @param condition
     *            The condition to test
     */
    public void failUnless(boolean condition) {
        assertTrue(condition);
    }

    /**
     * Mapping from PyUnit Tests condition, and if true, immediately stop execution of this testcase
     * 
     * @param condition
     *            The condition to test
     */
    public void failIf(boolean condition) {
        assertFalse(condition);
    }

}
