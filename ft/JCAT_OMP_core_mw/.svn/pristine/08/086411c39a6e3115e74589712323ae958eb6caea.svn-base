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

import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

import org.apache.log4j.Logger;
import org.python.core.PyDictionary;
import org.python.core.PyException;
import org.python.core.PyList;
import org.python.core.PyObject;
import org.python.core.PyTuple;
import org.python.util.PythonInterpreter;

import se.ericsson.jcat.fw.jython.Jythonizer;
import se.ericsson.jcat.omp.fw.OmpLibrary;
import se.ericsson.jcat.omp.fw.OmpLibraryException;
import se.ericsson.jcat.omp.fw.OmpSut;
import se.ericsson.jcat.omp.util.monitor.Monitor;
import se.ericsson.jcat.omp.util.monitor.MonitorData;
import se.ericsson.jcat.omp.util.monitor.MonitorDataArray;
import se.ericsson.jcat.omp.util.monitor.Monitorable;
import se.ericsson.jcat.omp.util.monitor.Pollable;

/**
 * The purpose of this class is ... TODO javadoc for class TestappLibImpl
 */
public class TestappLibImpl extends OmpLibrary implements TestappLib, Monitorable {
    private static Logger logger = Logger.getLogger(TestappLibImpl.class);
    private SafLib saf = null;
    private PythonInterpreter interp = null;
    // We allow 5% deviation from configured intensity by default.
    private static final double DEFAULT_INTENSITY_DEVIATION = 0.05;
    private static final String TESTAPP_SAF_APP_NAME = "ta_global";
    private OmpSut sut = null;
    private Monitorable self = null;

    private final Lock lock = new ReentrantLock();

    /**
     * Creates a new instance of <code>TestappLib</code>.
     * 
     * @param sut
     * @throws Exception
     */
    public TestappLibImpl(final OmpSut sut) throws Exception {
        this.sut = sut;
        this.interp = Jythonizer.getInstance();
        this.self = this;
    }

    /**
     * Only for Junit test
     * 
     * @param o
     */
    protected void setMonitorIndentifier(Monitorable o) {
        this.self = o;
    }

    /**
     * Returns the unique name of this library.
     */
    public String getName() {
        return "TestAppLib";
    }

    /**
     * Method called by LibraryBroker to set the Sut of the library
     */
    public void setSut(final OmpSut sut) {
        this.sut = sut;
    }

    /**
     * Method called by LibraryBroker to setup the library.
     */
    public void setUp() {
        // Do imports
        interp.exec("import coremw.testapp_lib as testapp_lib");
        interp.exec("if(hasattr(testapp_lib, 'setUp')): testapp_lib.setUp()");
        // interp.exec("testapp_lib.removeAllInstances()");
        // interp.exec("testapp_lib.addInstance('PL', 8001, 8002, 0 , 999999)");
        saf = (SafLib) sut.getLibrary("SafLib");
    }

    /**
     * Method called by LibraryBroker to teardown the library.
     */
    public void tearDown() {
        interp.exec("if(hasattr(testapp_lib, 'tearDown')): testapp_lib.tearDown()");
    }

    /**
     * Returns LoggerLib as runtime dependency.
     */
    public String[] getRuntimeDependencies() {
        return new String[] { "SshLib", "LoggerLib", "TargetDataLib", "SafLib" };
    }

    /**
     * Returns LoggerLib as setup dependency.
     */
    public String[] getSetupDependencies() {
        return new String[] { "LoggerLib", "TargetDataLib", "SshLib", "SafLib" };
    }

    /**
     * remove all testapp instances.
     */
    public void removeAllInstances() throws OmpLibraryException {
        interp.exec("testapp_lib.removeAllInstances()");
    }

    /**
     * remove all testapp instances.
     */
    public void addInstance(final String instance, final int tappPort, final int coordPort, final int min, final int max)
            throws OmpLibraryException {
        interp.exec("testapp_lib.addInstance('" + instance + "'," + tappPort + "," + coordPort + "," + min + "," + max
                + ")");
    }

    /**
     * Get the current testapp configuration.
     * 
     * @throws OmpLibraryException
     *             on command error
     */
    public String getConfiguration() throws OmpLibraryException {
        interp.exec("result = testapp_lib.getConfiguration()");
        final PyList result = (PyList) interp.get("result");
        return parseJythonResult(result);
    }

    /**
     * Get the current testapp configuration.
     * 
     * @throws OmpLibraryException
     *             on command error
     * @param instance
     */
    public String getConfiguration(final String instance) throws OmpLibraryException {
        interp.exec("result = testapp_lib.getConfiguration('" + instance + "')");
        final PyList result = (PyList) interp.get("result");
        return parseJythonResult(result);
    }

    /**
     * Get the current testapp call statistics.
     * 
     * @throws OmpLibraryException
     *             on command error
     */
    public String getStatistics() throws OmpLibraryException {
        interp.exec("result = testapp_lib.getStatistics()");
        final PyList result = (PyList) interp.get("result");
        return parseJythonResult(result);
    }

    /**
     * Get the current testapp call statistics.
     * 
     * @param instance
     * @throws OmpLibraryException
     *             on command error
     */
    public String getStatistics(final String instance) throws OmpLibraryException {
        interp.exec("result = testapp_lib.getStatistics('" + instance + "')");
        final PyList result = (PyList) interp.get("result");
        return parseJythonResult(result);
    }

    /**
     * Get the current testapp call statistics.
     * 
     * @throws OmpLibraryException
     *             on command error
     */
    public Map<String, String> getTotalStatistics() throws OmpLibraryException {
        interp.exec("result = testapp_lib.getTotalStatistics()");
        final PyList result = (PyList) interp.get("result");
        return parseJythonResult1(result);
    }

    /**
     * Get the current testapp call statistics.
     * 
     * @param instance
     * @throws OmpLibraryException
     *             on command error
     */
    public Map<String, String> getTotalStatistics(final String instance) throws OmpLibraryException {
        interp.exec("result = testapp_lib.getTotalStatistics('" + instance + "' )");
        final PyList result = (PyList) interp.get("result");
        return parseJythonResult1(result);
    }

    /**
     * Stop testapp traffic.
     */
    public String stopTraffic() throws OmpLibraryException {
        interp.exec("result = testapp_lib.stopTraffic()");
        final PyList result = (PyList) interp.get("result");
        return parseJythonResult(result);
    }

    /**
     * Reset the testapp statistical counters.
     */
    public String resetStatistics() throws OmpLibraryException {
        interp.exec("result = testapp_lib.resetStatistics()");
        final PyList result = (PyList) interp.get("result");
        return parseJythonResult(result);
    }

    /**
     * Reset the testapp statistical counters.
     * 
     * @param instance
     */
    public String resetStatistics(final String instance) throws OmpLibraryException {
        interp.exec("result = testapp_lib.resetStatistics('" + instance + "')");
        final PyList result = (PyList) interp.get("result");
        return parseJythonResult(result);
    }

    /**
     * Get the testapp configured intensity.
     * 
     * @param intesity
     * @throws OmpLibraryException
     *             on command error
     */
    public String getConfiguredIntensity() throws OmpLibraryException {
        interp.exec("result = testapp_lib.getConfiguredIntensity()");
        final PyList result = (PyList) interp.get("result");
        return parseJythonResult(result);
    }

    /**
     * Get the testapp configured intensity.
     * 
     * @param intesity
     * @throws OmpLibraryException
     *             on command error
     */
    public String getConfiguredIntensity(final String instance) throws OmpLibraryException {
        interp.exec("result = testapp_lib.getConfiguredIntensity('" + instance + "')");
        final PyList result = (PyList) interp.get("result");
        return parseJythonResult(result);
    }

    /**
     * Get the testapp actual intensity.
     * 
     * @throws OmpLibraryException
     *             on command error
     */
    public String getActualIntensity() throws OmpLibraryException {
        interp.exec("result = testapp_lib.getActualIntensity()");
        final PyList result = (PyList) interp.get("result");
        return parseJythonResult(result);
    }

    /**
     * Get the testapp actual intensity.
     * 
     * @param instance
     * @param intrval
     * @throws OmpLibraryException
     *             on command error
     */
    public String getActualIntensity(final String instance, final int interval) throws OmpLibraryException {
        interp.exec("result = testapp_lib.getActualIntensity('" + instance + "'," + interval + ")");
        final PyList result = (PyList) interp.get("result");
        return parseJythonResult(result);
    }

    /**
     * Set the testapp configuration.
     * 
     * @throws OmpLibraryException
     *             on command error
     */
    public String setConfiguration() throws OmpLibraryException {
        interp.exec("result = testapp_lib.setConfiguration()");
        final PyList result = (PyList) interp.get("result");
        return parseJythonResult(result);
    }

    /**
     * Set the testapp configuration.
     * 
     * @param instance
     * @param message
     * @throws OmpLibraryException
     *             on command error
     */
    public String setConfigurationString(final String instance, final String message) throws OmpLibraryException,
            FileNotFoundException, IOException {
        interp.exec("result = testapp_lib.setConfigurationString('" + instance + "','" + message + "')");
        final PyList result = (PyList) interp.get("result");
        return parseJythonResult(result);
    }

    /**
     * Set the testapp configuration.
     * 
     * @throws OmpLibraryException
     *             on command error
     */
    public String setConfigurationFile(final String instance, final String fileName) throws OmpLibraryException,
            FileNotFoundException, IOException {
        final FileReader fr = new FileReader(fileName);
        String message = "";
        for (;;) {
            final int i = fr.read();
            if (i == -1) {
                break;
            }
            final char c = (char) i;
            // jython cannot handle the '\n' character, instead it wants a '\'
            // and a 'n' character!
            if (c == '\n') {
                message = message + "\\n";
            } else {
                message = message + c;
            }
        }
        interp.exec("result = testapp_lib.setConfigurationString('" + instance + "','" + message + "')");
        final PyList result = (PyList) interp.get("result");
        return parseJythonResult(result);
    }

    /**
     * Set the testapp configuration.
     * 
     * @param instance
     * @param profile
     * @param intensity
     * @param logLevel
     * @param tcpConn
     * @param tcpTime
     * @throws OmpLibraryException
     *             on command error
     */
    public String setConfiguration(final String instance, final String profile, final int intensity,
            final String logLevel, final int tcpConn, final int tcpTime) throws OmpLibraryException {
        interp.exec("result = testapp_lib.setConfiguration('" + instance + "','" + profile + "'," + intensity + ",'"
                + logLevel + "'," + tcpConn + "," + tcpTime + ")");
        final PyList result = (PyList) interp.get("result");
        return parseJythonResult(result);
    }

    private String parseJythonResult(final PyList pl) throws OmpLibraryException {
        PyObject pyVerdict;
        PyObject pyMessage;
        try {
            pyVerdict = pl.__getitem__(0);
            logger.debug("Parsing PyList arg0: " + pyVerdict.toString());
            pyMessage = pl.__getitem__(1);
            logger.debug("Parsing PyList arg1: " + pyMessage.toString());
        } catch (final PyException pe) {
            logger.error("Parsing error, PyList key not found", pe);
            throw new OmpLibraryException(pe.toString());
        }

        // Do we need null checks on these?
        final String verdict = pyVerdict.toString();
        final String message = pyMessage.toString();

        if (!verdict.equalsIgnoreCase("SUCCESS")) {
            throw new OmpLibraryException(message);
        }

        return message;
    }

    private Map<String, String> parseJythonResult1(final PyList pl) throws OmpLibraryException {
        final Map<String, String> statistics = new HashMap<String, String>();

        PyObject pyVerdict;
        PyDictionary pyMessage;
        try {
            pyVerdict = pl.__getitem__(0);
            logger.debug("Parsing PyList arg0: " + pyVerdict.toString());
            pyMessage = (PyDictionary) pl.__getitem__(1);
            logger.debug("Parsing PyList arg1: " + pyMessage.toString());
        } catch (final PyException pe) {
            logger.error("Parsing error, PyList key not found", pe);
            throw new OmpLibraryException(pe.toString());
        }

        // Do we need null checks on these?
        final String verdict = pyVerdict.toString();
        final String message = pyMessage.toString();
        if (!verdict.equalsIgnoreCase("SUCCESS")) {
            throw new OmpLibraryException(message);
        }

        final PyList items = pyMessage.items();
        for (int i = 0; i <= items.__len__() - 1; i++) {
            final PyTuple item = (PyTuple) items.__getitem__(i);
            statistics.put(item.__getitem__(0).toString(), item.__getitem__(1).toString());
        }

        return statistics;
    }

    @Override
    public boolean isTrafficOk(Map<String, String> tblStart, Map<String, String> tblEnd, double loss, double timeout,
            double fail) {
        logger.debug("Start Status:");
        logger.debug((new TestappResult(tblStart)).toString());
        logger.debug("End Status:");
        logger.debug((new TestappResult(tblEnd)).toString());
        TestappResult diffResult = new TestappResult(tblStart, tblEnd);
        return isTrafficOk(diffResult, loss, timeout, fail);
    }

    public boolean isTrafficOk(final TestappResult diffResult, final double loss, final double timeout,
            final double fail) {
        logger.debug("Diff:");
        logger.debug(diffResult.toString());

        boolean failed = false;
        if (diffResult.getRealLoss() > loss) {
            logger.info("Too much loss traffic! " + diffResult.getRealLoss() + "% (Expected: " + loss + "%)");
            failed = true;
        }
        if (diffResult.getRealFail() > fail) {
            logger.info("Too much failed traffic! " + diffResult.getRealFail() + "% (Expected: " + fail + "%)");
            failed = true;
        }
        if (diffResult.getRealTimeout() > timeout) {
            logger.info("Too much timeout traffic! " + diffResult.getRealTimeout() + "% (Expected: " + timeout + "%)");
            failed = true;
        }
        if (diffResult.getSend() == 0) {
            logger.info("No traffic sent!");
            failed = true;
        }
        if (failed) {
            logger.info("\n Send: " + diffResult.getSend() + " Receive: " + diffResult.getRecv() + "\nFail: "
                    + diffResult.getFail() + " (" + diffResult.getRealFail() + "%)" + " Timeout: "
                    + diffResult.getTimeout() + " (" + diffResult.getRealTimeout() + "%)" + " Loss: "
                    + diffResult.getRealLoss() + "%");
            logger.info("Traffic not stable!");
            return false;
        } else {
            logger.info("\n Send: " + diffResult.getSend() + " Receive: " + diffResult.getRecv());
            // logger.info("Traffic is stable.");
            return true;

        }
    }

    public boolean isStable() {
        return isStable(1.0, 1.0, 1.0);

    }

    /**
     * Takes a snapshot of the traffic and then sleeps for 30 seconds, then takes another snapshot. With the information
     * from the snapshots isStable uses the function isTrafficOk to determine if the traffic is stable.
     */
    public boolean isStable(final double loss, final double timeout, final double fail) {
        return isStable(loss, timeout, fail, -1);
    }

    public boolean isStable(final int intensity) {
        return isStable(1.0, 1.0, 1.0, intensity);
    }

    public boolean isStable(final int intensity, final double intensityDeviation) {
        return isStable(1.0, 1.0, 1.0, intensity, 10, intensityDeviation);
    }

    public boolean isStable(final double loss, final double timeout, final double fail, final int intensity) {
        return isStable(loss, timeout, fail, intensity, 10, DEFAULT_INTENSITY_DEVIATION);
    }

    /**
     * Takes a snapshot of the traffic and then sleeps for 30 seconds, then takes another snapshot. The function also
     * fetches the actual traffic intensity. With the information from the snapshots isStable uses the function
     * isTrafficOk and the intensity variable to determine if the traffic is stable.
     */
    public boolean isStable(final double loss, final double timeout, final double fail, final int intensity,
            int sleepTime, final double intensityDeviation) {
        TestappResult[] tblStatus = getTblStatues(sleepTime, true);
        if (tblStatus == null) {
            return false;
        }
        TestappResult tblStart = tblStatus[0];
        TestappResult tblEnd = tblStatus[1];
        TestappResult tblDiff = new TestappResult(tblStart, tblEnd);
        int actualIntensity = getActualIntensity(tblDiff, sleepTime);

        if (isTrafficOk(tblDiff, loss, timeout, fail)) {
            if (intensity == -1) {
                logger.info("Traffic is stable, intensity = " + actualIntensity);
                return true;
            } else {
                if (actualIntensity < intensity * (1 - intensityDeviation)
                        || actualIntensity > intensity * (1 + intensityDeviation)) {
                    logger.info("Error Intensity! " + actualIntensity + " (Expected range: " + intensity
                            * (1 - intensityDeviation) + " to " + intensity * (1 + intensityDeviation) + ")");
                    return false;
                } else {
                    logger.info("Traffic is stable, intensity = " + actualIntensity);
                    return true;
                }
            }
        } else {
            logger.warn("Traffic is not stable, intensity = " + actualIntensity);
            return false;
        }
    }

    public boolean isStable(final double loss, final double timeout, final double fail, final int intensity,
            int sleepTime) {
        return isStable(loss, timeout, fail, intensity, sleepTime, DEFAULT_INTENSITY_DEVIATION);
    }

    private TestappResult[] getTblStatues(int sleepTime, boolean fromCache) {
        // Try to get the data from Monitor first.
        MonitorDataArray dataArray = null;
        if (fromCache) {
            dataArray = Monitor.getInstance().getLastMonitorData(this.self);
        }
        if (dataArray == null || dataArray.getDataArray().size() < 2) {
            try {
                lock.lock();
                Map<String, String> tblStart = getTotalStatistics();
                logger.debug("Start Status:");
                logger.debug((new TestappResult(tblStart)).toString());
                Thread.sleep(sleepTime * 1000);
                Map<String, String> tblEnd = getTotalStatistics();
                logger.debug("End Status:");
                logger.debug((new TestappResult(tblEnd)).toString());
                return new TestappResult[] { new TestappResult(tblStart), new TestappResult(tblEnd) };
            } catch (final OmpLibraryException e1) {
                e1.printStackTrace();
                return null;
            } catch (InterruptedException e) {
                e.printStackTrace();
                return null;
            } finally {
                lock.unlock();
            }
        } else {
            MonitorData data = dataArray.getDataArray().get(0);
            TestappResult tblEnd = (TestappResult) data.getData();
            TestappResult tblStart = new TestappResult(0, 0, 0, 0, 0);
            return new TestappResult[] { tblStart, tblEnd };
        }
    }

    private int getActualIntensity(TestappResult tblDiff, int sleepTime) {
        return tblDiff.getSend() / sleepTime;
    }

    public boolean waitUntilStable(int timeoutSeconds) {
        return waitUntilStable(timeoutSeconds, -1);
    }

    public boolean waitUntilStable(int timeoutSeconds, int intensity) {
        return waitUntilStable(timeoutSeconds, intensity, DEFAULT_INTENSITY_DEVIATION);
    }

    public boolean waitUntilStable(int timeoutSeconds, int intensity, double intensityDeviation) {
        logger.info("Wait until traffic keep stable, for max " + timeoutSeconds + " seconds");
        long startTime = System.currentTimeMillis();
        long timeout = startTime + timeoutSeconds * 1000;
        long curTime = 0;

        while (System.currentTimeMillis() < timeout) {
            curTime = System.currentTimeMillis();
            logger.info("Duration: " + (curTime - startTime) / 1000 + " seconds");
            if (isStable(intensity, intensityDeviation)) {
                logger.info("Traffic is stable");
                return true;
            }
        }
        logger.warn("TestApp traffic not stable after waited at least " + timeoutSeconds + " seconds");
        return false;
    }

    public Map<String, Map<String, String>> getTestAppHAState() throws OmpLibraryException {
        return saf.getSafAppHAState(TESTAPP_SAF_APP_NAME);
    }

    public boolean isTrafficStopped(int sleepTime) {
        TestappResult[] tblStatus = getTblStatues(sleepTime, true);
        if (tblStatus == null) {
            return false;
        }
        TestappResult tblStart = tblStatus[0];
        TestappResult tblEnd = tblStatus[1];
        TestappResult tblDiff = new TestappResult(tblStart, tblEnd);
        return tblDiff.getRealLoss() == 100;
    }

    @Override
    public Map<String, Map<String, String>> getTestAppHAState(String currentHAState) throws OmpLibraryException {
        logger.info("Fetching testapp haState from cached HA state");
        return saf.getSafAppHAState(TESTAPP_SAF_APP_NAME, currentHAState);
    }

    @Override
    public Pollable pollData() {
        int sleepTime = 10;
        TestappResult[] tblStatus = getTblStatues(sleepTime, false);
        if (tblStatus == null) {
            return null;
        }
        TestappResult tblStart = tblStatus[0];
        TestappResult tblEnd = tblStatus[1];
        TestappResult tblDiff = new TestappResult(tblStart, tblEnd);
        int actualIntensity = getActualIntensity(tblDiff, sleepTime);
        tblDiff.setActualIntensity(actualIntensity);
        return tblDiff;
    }

    @Override
    public String getMonitorableName() {
        return "TestApp";
    }

    @Override
    public int getStartupDelay() {
        return 5;
    }

    @Override
    public int getPollDataDelay() {
        return 5;
    }
}
