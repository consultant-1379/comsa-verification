package se.ericsson.jcat.omp.fw;

import org.apache.log4j.Logger;

import se.ericsson.jcat.fw.NonUnitTestCase;
import se.ericsson.jcat.fw.SUTHolder;
/** A base class for all Jython based OMP (SAF or MMAS) test cases
 * 
 * @author uabcsru
 *
 */
public class OmpTestCase extends NonUnitTestCase {
    private static Logger logger;
    public OmpSut[] safSuts=null;
    private static OmpTestCase currentTC;
    String testClass;
    String testMethod;
    protected static OmpSut currentSut;

    public OmpTestCase(String name) {
        super(name);
        logger = Logger.getLogger(this.getClass());
        logger.info("Test name: "+name);
    }

    public static OmpTestCase currentTestCase(){
        return currentTC;
    }

    public static OmpSut currentSystemUnderTest(){
        return currentSut;
    }

    /**
     * Overrides <code>TestCase</code> and is called before each testcase.
     * <p>
     * Cleares any outstanding events and creates a new log file.
     * <p>
     * It is important to note that if this method is overrided in a test class, 
     * that method must call <code>super.setUp()</code>.
     */
    protected void setUp() throws Exception {

    	super.setUp();
        currentTC = this;
        currentSut = (OmpSut)SUTHolder.getInstance().zones[0];

    }

    /**
     * Overrides <code>TestCase</code> and is called after each testcase.
     * <p>
     * Triggers traffic delta calculation and evaluates events status and saved 
     * assert statements.
     * <p>
     * It is important to note that if this method is overrided in a test class, 
     * that method must call <code>super.tearDown()</code>.
     */
    protected void tearDown() throws Exception {
        super.tearDown();
        currentTC = null;
    }

    /**
     * This needs to be moved to framework
     * save a String array into a file
     * @param name name of the file
     * @param info String array to be saved
     */
    public void  setTestFileInfo(String name, String info){
        String dir=this.getName();
        if(dir==null) dir="tmp";
        logger.info("See the logs here: " + setTestFile(name, info, dir));
    }

    //eanmatt: We always want to log to JCAT log4j regardless of python or Java library
    //so this is the same as logMsgToFile
    public void logMsg(String msg){
        setTestInfo(msg);
    }

    //eanmatt: We always want to log to JCAT log4j regardless of python or Java library
    //so this is the same as logMsgToFile
    public void logMsgToFile(String msg){
        logger.info(msg);
    }

    public void logSuccessInfo(String msg){
        //setStatus(msg);
    }

    public void assert_(boolean value, String msg){
        assertTrue(msg, value);
    }
}
