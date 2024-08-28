package se.ericsson.jcat.omp.library;

import java.util.List;
import java.util.Vector;

import org.apache.log4j.Logger;
import org.python.core.PyDictionary;
import org.python.core.PyException;
import org.python.core.PyList;
import org.python.core.PyTuple;

import se.ericsson.commonlibrary.CommonLibrary;
import se.ericsson.commonlibrary.CommonLibraryDataProvider;
import se.ericsson.jcat.omp.fw.OmpLibraryException;
import se.ericsson.jcat.omp.fw.OmpSut;
import se.ericsson.jcat.omp.util.Ssh2sessionUtil;
import se.ericsson.jcat.omp.util.Tools;
import se.ericsson.jcat.omp.util.Tools.SutInfoTag;

public abstract class SshCommonLibAbstractImpl implements SshLib {

    private static Logger logger = Logger.getLogger(SshCommonLibAbstractImpl.class);
    private OmpSut sut = OmpSut.getOmpSut();
    private SshLibDataProvider data;

    // ---------------------
    // CommonLibrary Methods
    // ---------------------

    @Override
    public void setLibraryDataProvider(CommonLibraryDataProvider data) {
        this.data = (SshLibDataProvider) data;
        python_setLibraryDataProvider(this.data);
    }

    @Override
    public CommonLibraryDataProvider getLibraryDataProvider() {
        return data;
    }

    @Override
    public Class<? extends CommonLibrary> getLibraryInterface() {
        return SshLib.class;
    }

    @Override
    public String getUniqueIdentifier() {
        return "SshCommonLib";
    }

    @Override
    public void initialize() {
        logger.info("Initializing SshCommonLib");
        python_initialize();
    }

    @Override
    public void shutdown() {
        python_shutdown();
    }

    @Override
    public List<Class<? extends CommonLibrary>> getRuntimeDependencyList() {
        return new Vector<Class<? extends CommonLibrary>>();
    }

    @Override
    public List<Class<? extends CommonLibrary>> getSetupDependencyList() {
        return new Vector<Class<? extends CommonLibrary>>();
    }

    // -----------------------
    // Python Abstract Methods
    // -----------------------

    protected abstract void python_setLibraryDataProvider(SshLibDataProvider data);

    protected abstract OmpSut python_getLibraryDataProvider();

    protected abstract void python_initialize();

    protected abstract void python_shutdown();

    protected abstract void python_setConfig(int subrack, int slot, int number, boolean useVipOam);

    protected abstract void python_setConfig(int subrack, int slot, int number);

    protected abstract PyTuple python_getConfig();

    protected abstract PyDictionary python_getTargetData();

    protected abstract PyTuple python_sendCommand(String command, int subrack, int blade);

    protected abstract PyTuple python_sendCommand(String command);

    protected abstract PyTuple python_sendCommandNbi(String command);

    protected abstract PyTuple python_setTimeout(int timeout, int subrack, int slot);

    protected abstract PyTuple python_setTimeout(int timeout);

    protected abstract PyTuple python_getTimeout(int subrack, int slot);

    protected abstract PyTuple python_sendRawCommand(String host, String command, String user, String password,
            int timeout);

    protected abstract PyTuple python_loginTest(int subrack, int slot, int attempts, String user, String pwd);

    protected abstract PyTuple python_bindAddresses(String blade, int localPort, int destinationPort);

    protected abstract PyTuple python_readFile(String blade, int localPort, String fileName, String request);

    protected abstract PyTuple python_remoteCopy(String file, String destination, int timeout, int numberOfRetries);

    protected abstract PyTuple python_remoteCopyFrom(String file, String destination, int timeout);

    protected abstract PyTuple python_sCopy(String file, String host, String destpath, String user, String passwd,
            int timeout);

    protected abstract void python_tearDownHandles();

    protected abstract boolean python_getUseVipOam();

    protected abstract PyList python_waitForConnection(int subrack, int slot, int timeout);

    protected abstract PyList python_waitForNoConnection(int subrack, int slot, int timeout);

    protected abstract void python_resetInternalConnectionCommand();

    // ------------
    // Java Methods
    // ------------

    public void setConfig(int subrack, int slot, int number, boolean useVipOam) {
        python_setConfig(subrack, slot, number, useVipOam);
    }

    public void setConfig(int subrack, int slot, int number) {
        python_setConfig(subrack, slot, number);
    }

    public int[] getConfig() {
        PyTuple py = python_getConfig();
        return new int[] { (Integer) py.get(0), (Integer) py.get(1) };
    }

    public PyDictionary getTargetData() {
        return python_getTargetData();
    }

    public String sendCommand(String command, int subrack, int blade) throws OmpLibraryException {
        PyTuple py = python_sendCommand(command, subrack, blade);
        String response = parseJythonResult(py);
        teardownHandlersIfNeeded(response);
        return response;
    }

    public String sendCommand(String command) throws OmpLibraryException {
        PyTuple py = python_sendCommand(command);
        String response = parseJythonResult(py);
        teardownHandlersIfNeeded(response);
        return response;
    }

    public String sendCommandNbi(String command) throws OmpLibraryException {
        return parseJythonResult(python_sendCommandNbi(command));
    }

    public String setTimeout(int timeout, int subrack, int slot) throws OmpLibraryException {
        return parseJythonResult(python_setTimeout(timeout, subrack, slot));
    }

    public String setTimeout(int timeout) throws OmpLibraryException {
        return parseJythonResult(python_setTimeout(timeout));
    }

    public String getTimeout(int subrack, int slot) throws OmpLibraryException {
        return parseJythonResult(python_getTimeout(subrack, slot));
    }

    public String sendRawCommand(String host, String command, String user, String password, int timeout)
            throws OmpLibraryException {
        return parseJythonResult(python_sendRawCommand(host, command, user, password, timeout));
    }

    public String loginTest(int subrack, int slot, int attempts, String user, String pwd) throws OmpLibraryException {
        return parseJythonResult(python_loginTest(subrack, slot, attempts, user, pwd));
    }

    public String bindAddresses(String blade, int localPort, int destinationPort) throws OmpLibraryException {
        return parseJythonResult(python_bindAddresses(blade, localPort, destinationPort));
    }

    public String readFile(String blade, int localPort, String fileName, String request) throws OmpLibraryException {
        return parseJythonResult(python_readFile(blade, localPort, fileName, request));
    }

    public String remoteCopy(String file, String destination, int timeout, int numberOfRetries)
            throws OmpLibraryException {
        return parseJythonResult(python_remoteCopy(file, destination, timeout, numberOfRetries));
    }

    public String remoteCopyFrom(String file, String destination, int timeout) throws OmpLibraryException {
        return parseJythonResult(python_remoteCopyFrom(file, destination, timeout));
    }

    public String sCopy(String file, String host, String destpath, String user, String passwd, int timeout)
            throws OmpLibraryException {
        return parseJythonResult(python_sCopy(file, host, destpath, user, passwd, timeout));
    }

    public void tearDownHandles() {
        python_tearDownHandles();
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
            String ip1 = Tools.getSutInfo(sut, SutInfoTag.IP_SC1);
            String ip2 = Tools.getSutInfo(sut, SutInfoTag.IP_SC2);
            String ip = Tools.getScByPort(sut, Tools.SSH_PORT);
            int[] currentSetting = getConfig();
            if (ip == null) {
                return false;
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

    public boolean getUseVipOam() {
        return python_getUseVipOam();
    }

    public boolean waitForConnection(int subrack, int slot, int timeout) {
        PyList py = python_waitForConnection(subrack, slot, timeout);
        return (Boolean) py.get(1);
    }

    public boolean waitForNoConnection(int subrack, int slot, int timeout) {
        PyList py = python_waitForNoConnection(subrack, slot, timeout);
        return (Boolean) py.get(1);
    }

    public String getHostname(int subrack, int blade) throws OmpLibraryException {
        return this.sendCommand("hostname", subrack, blade);
    }

    public String getInternalConnectionCommand() {
        return Ssh2sessionUtil.getInternalConnectionCommand();
    }

    public String getInternalBridgeCommand() {
        return Ssh2sessionUtil.getInternalBridgeCommand();
    }

    public void resetInternalConnectionCommand() {
        python_resetInternalConnectionCommand();
    }

    public void determineInternalConnectionCommandNextTime() {
        logger.info("Internal Connection Command will be reconfigured next time when creating handlers");
        Ssh2sessionUtil.determineInternalConnectionCommandNextTime();
        this.tearDownHandles();
    }

    private void teardownHandlersIfNeeded(String cmdRes) {
        if (cmdRes.contains("command not found") || cmdRes.contains("Command not found")) {
            logger.warn("Command not found! Try to solve this by teardown the old handlers");
            tearDownHandles();
        }
    }

    private String parseJythonResult(final PyTuple pt) throws OmpLibraryException {
        // Do we need null checks on these?
        String verdict = null;
        String message = null;

        try {
            verdict = pt.get(0).toString();
            logger.debug("Parsing PyTuple arg0: " + verdict);
            message = pt.get(1).toString();
            logger.debug("Parsing PyTuple arg1: " + message);
        } catch (final PyException pe) {
            logger.error("Parsing error, PyTyple key not found", pe);
            return null;
        }

        if (!verdict.equalsIgnoreCase("SUCCESS")) {
            throw new OmpLibraryException(message);
        }

        return message;
    }
}
