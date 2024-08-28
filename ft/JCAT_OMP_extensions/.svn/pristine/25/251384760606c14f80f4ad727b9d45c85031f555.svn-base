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

import java.util.List;

import org.apache.log4j.Logger;
import org.python.core.PyDictionary;
import org.python.core.PyException;
import org.python.core.PyList;
import org.python.core.PyObject;
import org.python.core.PyTuple;
import org.python.util.PythonInterpreter;

import se.ericsson.commonlibrary.CommonLibrary;
import se.ericsson.commonlibrary.CommonLibraryDataProvider;
import se.ericsson.jcat.fw.jython.Jythonizer;
import se.ericsson.jcat.omp.fw.OmpLibrary;
import se.ericsson.jcat.omp.fw.OmpLibraryException;
import se.ericsson.jcat.omp.fw.OmpSut;
import se.ericsson.jcat.omp.util.Ssh2sessionUtil;
import se.ericsson.jcat.omp.util.Tools;
import se.ericsson.jcat.omp.util.Tools.SutInfoTag;

/**
 * The purpose of this class is ... TODO javadoc for class SshLib
 */
public class SshLibImpl extends OmpLibrary implements SshLib {
    private static Logger logger = Logger.getLogger(SshLibImpl.class);

    private PythonInterpreter interp = null;

    OmpSut sut = null;

    /**
     * Creates a new instance of <code>SshLib</code>.
     * 
     * @param sut
     * @throws Exception
     */
    public SshLibImpl(final OmpSut sut) throws Exception {
        this.sut = sut;
        this.interp = Jythonizer.getInstance();
    }

    /**
     * Returns the unique name of this library.
     */
    public String getName() {
        return "SshLib";
    }

    /**
     * Method called by LibraryBroker to set the Sut of the library
     */
    public void setSut(final OmpSut sut) {
        this.sut = sut;
    }

    public void setUp() {
        // Do imports
        interp.exec("import omp.tf.ssh_lib as ssh_lib");
        interp.set("sut", sut);
        interp.exec("if(hasattr(ssh_lib, 'setUp')): ssh_lib.setUp(2, 1, 1, sut)");
    }

    public void tearDown() {
        interp.exec("if(hasattr(ssh_lib, 'tearDown')): ssh_lib.tearDown()");
    }

    /**
     * Returns LoggerLib as runtime dependency.
     */
    public String[] getRuntimeDependencies() {
        return new String[] { "LoggerLib", "TargetDataLib" };
    }

    /**
     * Returns LoggerLib as setup dependency.
     */
    public String[] getSetupDependencies() {
        return new String[] { "LoggerLib", "TargetDataLib" };
    }

    public PyDictionary getTargetData() {
        interp.exec("targetData = omp_target_data.getTargetHwData()");
        final PyDictionary targetData = (PyDictionary) interp.get("targetData");

        return targetData;
    }

    public String sendCommand(final String command, final int subrack, final int blade) throws OmpLibraryException {
        logger.info(command);
        interp.exec("result = ssh_lib.sendCommand('" + command + "', " + subrack + ", " + blade + ")");

        final PyTuple result = (PyTuple) interp.get("result");
        String cmdRes = parseJythonResult(result);
        logger.info(cmdRes);
        teardownHandlersIfNeeded(cmdRes);
        return cmdRes;
    }

    @Override
    public String sendCommand(final String command, final int subrack, final int blade, boolean retry)
            throws OmpLibraryException {
        try {
            return sendCommand(command, subrack, blade);
        } catch (Exception e) {
            if (retry) {
                logger.warn("Could not send command \"" + command + "\" to " + subrack + "-" + blade
                        + " due to Exception: '" + e.getMessage() + "'. Will try again.");
                tearDownHandles();
                return sendCommand(command, subrack, blade);
            } else {
                if (e instanceof OmpLibraryException)
                    throw (OmpLibraryException) e;
                else {
                    logger.warn("Exception: ", e);
                    throw new OmpLibraryException("Command execution failed.", e);
                }
            }
        }
    }

    public String sendCommand(final String command) throws OmpLibraryException {
        logger.info(command);
        interp.exec("result = ssh_lib.sendCommand('" + command + "')");

        final PyTuple result = (PyTuple) interp.get("result");
        String cmdRes = parseJythonResult(result);
        logger.info(cmdRes);
        teardownHandlersIfNeeded(cmdRes);
        return cmdRes;
    }

    @Override
    public String sendCommand(final String command, boolean retry) throws OmpLibraryException {
        try {
            return sendCommand(command);
        } catch (Exception e) {
            if (retry) {
                logger.warn("Could not send command \"" + command + "\" due to Exception: '" + e.getMessage()
                        + "'. Will try again.");
                tearDownHandles();
                return sendCommand(command);
            } else {
                if (e instanceof OmpLibraryException)
                    throw (OmpLibraryException) e;
                else {
                    logger.warn("Exception: ", e);
                    throw new OmpLibraryException("Command execution failed.", e);
                }
            }
        }
    }

    private void teardownHandlersIfNeeded(String cmdRes) {
        if (cmdRes.contains("command not found") || cmdRes.contains("Command not found")) {
            logger.warn("Command not found! Try to solve this by teardown the old handlers");
            tearDownHandles();
        }
    }

    public String sendCommandNbi(final String command) throws OmpLibraryException {
        interp.exec("result = ssh_lib.sendCommandNBI('" + command + "')");

        final PyTuple result = (PyTuple) interp.get("result");
        return parseJythonResult(result);
    }

    public String setTimeout(final int timeout, final int subrack, final int slot) throws OmpLibraryException {
        interp.exec("result = ssh_lib.setTimeout(" + timeout + ", " + subrack + ", " + slot + ")");

        final PyTuple result = (PyTuple) interp.get("result");
        return parseJythonResult(result);
    }

    public String setTimeout(final int timeout) throws OmpLibraryException {
        interp.exec("result = ssh_lib.setTimeout(" + timeout + ")");

        final PyTuple result = (PyTuple) interp.get("result");
        return parseJythonResult(result);
    }

    public String getTimeout(final int subrack, final int slot) throws OmpLibraryException {
        interp.exec("result = ssh_lib.getTimeout(" + subrack + ", " + slot + ")");

        final PyTuple result = (PyTuple) interp.get("result");
        return parseJythonResult(result);
    }

    public String sendRawCommand(final String host, final String command, final String user, final String password,
            final int timeout, int port) throws OmpLibraryException {
        interp.exec("result = ssh_lib.sendRawCommand('" + host + "', '" + command + "', '" + user + "', '" + password
                + "', " + timeout + " , " + port + ")");

        final PyTuple result = (PyTuple) interp.get("result");
        return parseJythonResult(result);
    }

    public String sendRawCommand(final String host, final String command, final String user, final String password,
            final int timeout) throws OmpLibraryException {
        return sendRawCommand(host, command, user, password, timeout, 22);
    }

    public String bindAddresses(final String blade, final int localPort, final int destinationPort)
            throws OmpLibraryException {
        interp.exec("result = ssh_lib.bindAddresses('" + blade + ", " + localPort + ", " + destinationPort + "')");

        final PyTuple result = (PyTuple) interp.get("result");
        return parseJythonResult(result);
    }

    public String loginTest(final int subrack, final int slot, final int attempts, final String user, final String pwd)
            throws OmpLibraryException {
        interp.exec("result = ssh_lib.loginTest(" + subrack + ", " + slot + ", " + attempts + " , '" + user + "' , '"
                + pwd + "')");

        final PyTuple result = (PyTuple) interp.get("result");
        return parseJythonResult(result);
    }

    public String readFile(final String blade, final int localPort, final String fileName, final String request)
            throws OmpLibraryException {
        interp.exec("result = ssh_lib.readFile('" + blade + ", " + localPort + ", " + fileName + " , " + request + "')");

        final PyTuple result = (PyTuple) interp.get("result");
        return parseJythonResult(result);
    }

    public String remoteCopy(final String file, final String destination, final int timeout, final int numberOfRetries)
            throws OmpLibraryException {
        interp.exec("result = ssh_lib.remoteCopy('" + file + "', '" + destination + "', " + timeout + " , "
                + numberOfRetries + ")");

        final PyTuple result = (PyTuple) interp.get("result");
        return parseJythonResult(result);
    }

    public String remoteCopyFrom(final String file, final String destination, final int timeout)
            throws OmpLibraryException {
        interp.exec("result = ssh_lib.remoteCopyFrom('" + file + "', '" + destination + "', " + timeout + ")");

        final PyTuple result = (PyTuple) interp.get("result");
        return parseJythonResult(result);
    }

    public String sCopy(final String file, final String host, final String destpath, final String user,
            final String passwd, final int timeout) throws OmpLibraryException {
        interp.exec("result = ssh_lib.sCopy('" + file + "', '" + host + "', '" + destpath + "', '" + user + "', '"
                + passwd + "' , " + timeout + ")");

        final PyTuple result = (PyTuple) interp.get("result");
        return parseJythonResult(result);
    }

    public void tearDownHandles() {
        interp.exec("ssh_lib.tearDownHandles()");
    }

    public void setConfig(int subrack, int slot, int number) {
        interp.exec("ssh_lib.setConfig(" + subrack + ", " + slot + ", " + number + ")");
    }

    public void setConfig(int subrack, int slot, int number, boolean useVipOam) {
        if (useVipOam)
            interp.exec("ssh_lib.setConfig(" + subrack + ", " + slot + ", " + number + ", True)");
        else
            interp.exec("ssh_lib.setConfig(" + subrack + ", " + slot + ", " + number + ", False)");
    }

    public int[] getConfig() {
        interp.exec("result = ssh_lib.getConfig()");
        final PyTuple tmpResult = (PyTuple) interp.get("result");
        int subrack = Integer.parseInt(tmpResult.__getitem__(0).toString());
        int slot = Integer.parseInt(tmpResult.__getitem__(1).toString());
        return new int[] { subrack, slot };
    }

    public boolean getUseVipOam() {
        interp.exec("result = ssh_lib.getUseVipOam()");
        final PyObject tmpResult = (PyObject) interp.get("result");
        if (tmpResult.toString().equals("1") || tmpResult.toString().equals("True"))
            return true;
        else
            return false;
    }

    public boolean setConfig() {
        return setConfig(false);
    }

    public boolean setConfig(boolean useVipOam) {
        if (useVipOam) {
            int[] currentSetting = getConfig();
            if (currentSetting[0] == 2 && currentSetting[1] == 1) {
                try {
                    sendCommand("hostname");
                } catch (OmpLibraryException e) {
                    setConfig(2, 2, 2, useVipOam);
                }
            } else {
                try {
                    sendCommand("hostname");
                } catch (OmpLibraryException e) {
                    setConfig(2, 1, 1, useVipOam);
                }
            }
            return true;
        } else {
            String ip1 = Tools.getIPFromAddress(Tools.getSutInfo(sut, SutInfoTag.IP_SC1));
            String ip2 = Tools.getIPFromAddress(Tools.getSutInfo(sut, SutInfoTag.IP_SC2));
            String ip = null;

            if (verifyConnection(2, 1)) { // check if SC1 is accessible
                ip = ip1;
            } else if (verifyConnection(2, 2)) { // check if SC2 is accessible
                ip = ip2;
            }

            int[] currentSetting = getConfig();
            if (ip == null) {
                return false; // non of the SCs is accessible
            } else {
                if (ip.equals(ip1)) {
                    if (!(currentSetting[0] == 2 && currentSetting[1] == 1)) {
                        setConfig(2, 1, 1, useVipOam);
                    }
                    return true;
                } else if (ip.equals(ip2)) {
                    if (!(currentSetting[0] == 2 && currentSetting[1] == 2)) {
                        setConfig(2, 2, 2, useVipOam);
                    }
                    return true;
                } else {
                    logger.warn("Cannot match " + ip + " with " + ip1 + " or " + ip2);
                    return false;
                }
            }
        }
    }

    public String getHostname(int subrack, int blade) throws OmpLibraryException {
        return this.sendCommand("hostname", subrack, blade);
    }

    public boolean waitForConnection(int subrack, int slot, int timeout) {
        boolean result;
        interp.exec("result = ssh_lib.waitForConnection(" + subrack + ", " + slot + ", " + timeout + ")");
        try {
            final PyList tmpResult = (PyList) interp.get("result");
            if (parseJythonListResult(tmpResult).equals("1") || parseJythonListResult(tmpResult).equals("True"))
                result = true;
            else
                result = false;
        } catch (Exception e) {
            result = false;
        }
        return result;
    }

    public boolean waitForNoConnection(int subrack, int slot, int timeout) {
        boolean result;
        interp.exec("result = ssh_lib.waitForNoConnection(" + subrack + ", " + slot + ", " + timeout + ")");
        try {
            final PyList tmpResult = (PyList) interp.get("result");

            if (parseJythonListResult(tmpResult).equals("1") || parseJythonListResult(tmpResult).equals("True"))
                result = true;
            else
                result = false;
        } catch (Exception e) {
            result = false;
        }

        return result;
    }

    /*
     * Parse the PyList result structure returned from the Jython API method.
     */
    private String parseJythonListResult(final PyList pl) throws OmpLibraryException {
        PyObject pyVerdict;
        PyObject pyMessage;
        try {
            pyVerdict = pl.__getitem__(0);
            logger.debug("Parsing PyList arg0: " + pyVerdict.toString());
            pyMessage = pl.__getitem__(1);
            logger.debug("Parsing PyList arg1: " + pyMessage.toString());
        } catch (final PyException pe) {
            logger.error("Parsing error, PyList key not found", pe);
            return null;
        }

        // Do we need null checks on these?
        final String verdict = pyVerdict.toString();
        final String message = pyMessage.toString();

        if (!verdict.equalsIgnoreCase("SUCCESS")) {
            throw new OmpLibraryException(message);
        }

        return message;
    }

    /*
     * Parse the PyTuple result structure returned from the Jython API method. TODO: Throw OmpLibraryException if
     * PyTuple parse fails?
     */
    private String parseJythonResult(final PyTuple pt) throws OmpLibraryException {
        PyObject pyVerdict;
        PyObject pyMessage;
        try {
            pyVerdict = pt.__getitem__(0);
            logger.debug("Parsing PyTuple arg0: " + pyVerdict.toString());
            pyMessage = pt.__getitem__(1);
            logger.debug("Parsing PyTuple arg1: " + pyMessage.toString());
        } catch (final PyException pe) {
            logger.error("Parsing error, PyTyple key not found", pe);
            return null;
        }

        // Do we need null checks on these?
        final String verdict = pyVerdict.toString();
        final String message = pyMessage.toString();

        if (!verdict.equalsIgnoreCase("SUCCESS")) {
            throw new OmpLibraryException(message);
        }

        return message;
    }

    public String getInternalConnectionCommand() {
        return Ssh2sessionUtil.getInternalConnectionCommand();
    }

    public String getInternalBridgeCommand() {
        return Ssh2sessionUtil.getInternalBridgeCommand();
    }

    public void resetInternalConnectionCommand() {
        interp.exec("ssh_lib.resetInternalConnectionCommand()");
    }

    public void determineInternalConnectionCommandNextTime() {
        logger.info("Internal Connection Command will be reconfigured next time when creating handlers");
        Ssh2sessionUtil.determineInternalConnectionCommandNextTime();
        this.tearDownHandles();
    }

    /**
     * check if the specified blade is accessible or not
     * 
     * @param subrack
     * @param slot
     * @param connectionTimeoutSeconds
     * @return true if the blade is accessible false otherwise
     */
    public boolean verifyConnection(final int subrack, final int slot) {
        try {
            String loginResult = this.loginTest(subrack, slot, 1, sut.getConfigDataString("user"),
                                                sut.getConfigDataString("pwd"));
            logger.info("loging result " + loginResult);
            if (loginResult.toLowerCase().contains("connected!!")) {
                return true;
            }
        } catch (OmpLibraryException e) {
            logger.error("unable to lgoing");
            return false;
        }
        return false;
    }

    @Override
    public void setLibraryDataProvider(CommonLibraryDataProvider data) {
    }

    @Override
    public CommonLibraryDataProvider getLibraryDataProvider() {
        return null;
    }

    @Override
    public Class<? extends CommonLibrary> getLibraryInterface() {
        return null;
    }

    @Override
    public String getUniqueIdentifier() {
        return null;
    }

    @Override
    public void initialize() {
    }

    @Override
    public void shutdown() {
    }

    @Override
    public List<Class<? extends CommonLibrary>> getRuntimeDependencyList() {
        return null;
    }

    @Override
    public List<Class<? extends CommonLibrary>> getSetupDependencyList() {
        return null;
    }
}
