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

import org.apache.commons.lang.NotImplementedException;
import org.apache.log4j.Logger;
import org.python.core.PyException;
import org.python.core.PyObject;
import org.python.core.PyTuple;
import org.python.util.PythonInterpreter;

import se.ericsson.commonlibrary.CommonLibrary;
import se.ericsson.commonlibrary.CommonLibraryDataProvider;
import se.ericsson.jcat.fw.jython.Jythonizer;
import se.ericsson.jcat.omp.fw.OmpLibrary;
import se.ericsson.jcat.omp.fw.OmpLibraryException;
import se.ericsson.jcat.omp.fw.OmpSut;
import se.ericsson.jcat.omp.util.Tools;

import com.ericsson.commonlibrary.remotecli.Cli;
import com.ericsson.commonlibrary.remotecli.CliBuilder;
import com.ericsson.commonlibrary.remotecli.CliFactory;
import com.ericsson.commonlibrary.remotecli.exceptions.RemoteCliException;

/**
 * The purpose of this class is ... TODO javadoc for class HwLibImpl
 */
public class HwLibImpl extends OmpLibrary implements HwLib {
    private static Logger logger = Logger.getLogger(SshLibImpl.class);

    private PythonInterpreter interp = null;

    OmpSut sut = null;

    /**
     * Creates a new instance of <code>SshLib</code>.
     * 
     * @param sut
     * @throws Exception
     */
    public HwLibImpl(final OmpSut sut) throws Exception {
        this.sut = sut;
        this.interp = Jythonizer.getInstance();
    }

    /**
     * Returns the unique name of this library.
     */
    public String getName() {
        return "HwLib";
    }

    /**
     * Method called by LibraryBroker to set the Sut of the library
     */
    public void setSut(final OmpSut sut) {
        this.sut = sut;
    }

    public void setUp() {
        // Do imports
        interp.exec("import omp.tf.hw_lib as hw_lib");
        interp.exec("if(hasattr(hw_lib, 'setUp')): hw_lib.setUp()");
    }

    public void tearDown() {
        interp.exec("if(hasattr(hw_lib, 'tearDown')): hw_lib.tearDown()");
    }

    /**
     * Returns LoggerLib as runtime dependency.
     */
    public String[] getRuntimeDependencies() {
        return new String[] { "SshLib", "LoggerLib", "TargetDataLib" };
    }

    /**
     * Returns LoggerLib as setup dependency.
     */
    public String[] getSetupDependencies() {
        return new String[] { "LoggerLib", "TargetDataLib", "SshLib" };
    }

    public boolean powerOff(final int subrack, final int slot) throws OmpLibraryException {

        interp.exec("result = hw_lib.powerOff(" + subrack + "," + slot + ")");
        final PyTuple result = (PyTuple) interp.get("result");
        String r = parseJythonResult(result);
        if (r.equals("Chassis Power Control: Down/Off")) {
            return true;
        } else if (r.contains("succeeded")) {
            return true;
        } else {
            return false;
        }
    }

    public boolean powerOn(final int subrack, final int slot) throws OmpLibraryException {

        interp.exec("result = hw_lib.powerOn(" + subrack + "," + slot + ")");
        final PyTuple result = (PyTuple) interp.get("result");
        String r = parseJythonResult(result);
        if (r.equals("Chassis Power Control: Up/On")) {
            return true;
        } else if (r.contains("succeeded")) {
            return true;
        } else {
            return false;
        }
    }

    public boolean powerReset(final int subrack, final int slot) throws OmpLibraryException {

        interp.exec("result = hw_lib.powerReset(" + subrack + "," + slot + ")");
        final PyTuple result = (PyTuple) interp.get("result");
        String r = parseJythonResult(result);
        if (r.equals("Chassis Power Control: Reset")) {
            return true;
        } else {
            return false;
        }
    }

    public boolean powerStatus(final int subrack, final int slot) throws OmpLibraryException {

        interp.exec("result = hw_lib.powerStatus(" + subrack + "," + slot + ")");
        final PyTuple result = (PyTuple) interp.get("result");
        String r = parseJythonResult(result);
        if (r.equals("Chassis Power is on")) {
            return true;
        } else if (r.equals("Chassis Power is off")) {
            return false;
        } else {
            throw new OmpLibraryException("Unknow status! " + r);
        }
    }

    public boolean clusterPowerReset() throws OmpLibraryException {

        interp.exec("result = hw_lib.clusterPowerReset()");
        final PyTuple result = (PyTuple) interp.get("result");
        logger.info(parseJythonResult(result));
        return true;
    }

    public boolean immediateClusterPowerReset() {
        logger.info("Immediate reset all the blades");
        int size = Integer.parseInt(sut.getConfigDataString("physical_size"));
        // Power off all the blades
        logger.info("power off all the blades");
        if (!powerStateChangeAll(size, "off")) {
            return false;
        }
        logger.info("Should be powered off, waiting 10 sec, then checking state");
        try {
            Thread.sleep(10000);
        } catch (final InterruptedException e) {
            e.printStackTrace();
        }

        // Check if all blades are off
        if (!waitForStateChangeAll(size, "off")) {
            return false;
        }
        // Power on all the blades
        logger.info("power on all the blades");
        if (!powerStateChangeAll(size, "on")) {
            return false;
        }
        logger.info("Should be powered on, waiting 10 sec, then checking state");
        try {
            Thread.sleep(10000);
        } catch (final InterruptedException e) {
            e.printStackTrace();
        }
        // Check if all blades are on
        if (!waitForStateChangeAll(size, "on")) {
            return false;
        }

        return true;
    }

    private boolean waitForStateChangeAll(int size, String state) {
        for (int i = 1; i <= size; i++) {
            logger.info("Waiting for blade " + i + " to be " + state);
            try {
                while (!(powerStatus(2, i) ? "on" : "off").equalsIgnoreCase(state)) {
                    Thread.sleep(2000);
                }
            } catch (Exception e) {
                logger.error("Power management failed! " + e.getMessage());
                logger.info("Trying to recover!");
                powerStateChangeAll(size, "on");
                return false;
            }
        }
        return true;
    }

    private boolean powerStateChangeAll(int size, String state) {
        String commandline = "";
        String commandline_long = "";

        SshLib ssh = (SshLib) sut.getLibrary("SshLib");

        String gwpc = sut.getConfigDataString("ipAddress.ctrl.testpc");

        // If localhost, then do it one by one. Otherwize just create a long
        // string and do it later
        for (int i = 1; i <= size; i++) {
            String ip = sut.getConfigDataString("ipAddress.ipmi.blade_2_" + i);
            commandline = "ipmitool -I lan -U root -P rootroot -H " + ip + " chassis power " + state;
            commandline_long += "ipmitool -I lan -U root -P rootroot -H " + ip + " chassis power " + state + "; ";
            if (gwpc.trim().equalsIgnoreCase("localhost")) {
                logger.info("Doing localhost command, commandline " + commandline);
                Process p;
                try {
                    p = Runtime.getRuntime().exec(commandline);
                    p.waitFor();
                } catch (Exception e) {
                    logger.error("Cannot power " + state + " the blades! " + e.getMessage());
                    if (state.equalsIgnoreCase("off")) {
                        logger.info("Trying to recover!");
                        powerStateChangeAll(size, "on");
                    }
                    return false;
                }
            }
        }

        // If not localhost, then execute the long string
        if (!gwpc.trim().equalsIgnoreCase("localhost")) {
            try {
                logger.info("Doing ssh.sendCommand, commandline " + commandline_long);
                ssh.sendCommand(commandline_long, 9, 9, true);
            } catch (Exception e) {
                logger.error("Cannot power " + state + " the blades! " + e.getMessage());
                if (state.equalsIgnoreCase("off")) {
                    logger.info("Trying to recover!");
                    powerStateChangeAll(size, "on");
                }
                return false;
            }
        }
        return true;
    }

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

    @Override
    public CommonLibraryDataProvider getLibraryDataProvider() {
        throw new NotImplementedException();
    }

    @Override
    public Class<? extends CommonLibrary> getLibraryInterface() {
        throw new NotImplementedException();
    }

    @Override
    public List<Class<? extends CommonLibrary>> getRuntimeDependencyList() {
        throw new NotImplementedException();
    }

    @Override
    public List<Class<? extends CommonLibrary>> getSetupDependencyList() {
        throw new NotImplementedException();
    }

    @Override
    public String getUniqueIdentifier() {
        throw new NotImplementedException();
    }

    @Override
    public void initialize() {
        throw new NotImplementedException();
    }

    @Override
    public void setLibraryDataProvider(CommonLibraryDataProvider arg0) {
        throw new NotImplementedException();
    }

    @Override
    public void shutdown() {
        throw new NotImplementedException();
    }

    /**
     * Get MAC address of the specified interface on a specified SUN blade via CMM.
     * 
     * @param mgmtIpAddress
     *            String CMM ip address
     * @param username
     *            String username for CMM
     * @param password
     *            String password for CMM
     * @param hwId
     *            String blade digital ID in CMM, e.x. 0 for BL0
     * @param intfIndex
     *            int index for network interface name. e.x. 0 for eth0
     * @throws Exception
     */
    public String getMacAddress(String mgmtIpAddress, String username, String password, String hwId, int intfIndex)
            throws OmpLibraryException {
        String output = null;

        int bladeIndex = Integer.parseInt(hwId);

        final CliBuilder sshBuilder = CliFactory.newSshBuilder();
        sshBuilder.setHost(mgmtIpAddress).setUsername(username).setPassword(password);
        final Cli ilomCli = sshBuilder.build();
        ilomCli.setExpectedRegexPrompt("->\\s");

        try {
            ilomCli.connect();
            ilomCli.send("start -script /CH/BL" + bladeIndex + "/SP/cli");
            ilomCli.send("cd SYS/MB/NET0");
            output = ilomCli.send("show fru_serial_number");
            if (output.contains("fru_serial_number = (none)")) {
                output = ilomCli.send("show fru_macaddress");
            }
        } catch (RemoteCliException e) {
            throw new OmpLibraryException("Unable to get mac Address!", e);
        } finally {
            ilomCli.disconnect();
        }

        output = output.substring(output.indexOf("=") + 1);
        String firstMac = output.replaceAll("\\r\\n", "").trim();

        String targetMac = null;
        switch (intfIndex) {
            case 0:
                // on sun blade, eth0 = first MAC address from /SYS/MB/NET0
                targetMac = firstMac;
                break;
            case 1:
                // eth1 on all blades = eth0 +1
                targetMac = Tools.getRelativeMacAddress(firstMac, 1);
                break;
            default:
                throw new IllegalArgumentException("Getting MAC Address of Interface eth" + intfIndex
                        + " not Implemented!");
        }
        return targetMac;
    }
}
