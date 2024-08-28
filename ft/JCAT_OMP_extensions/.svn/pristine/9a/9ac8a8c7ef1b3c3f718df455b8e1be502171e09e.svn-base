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

import java.io.IOException;
import java.util.EnumSet;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.TimeUnit;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.apache.commons.lang.NotImplementedException;
import org.apache.log4j.Logger;

import se.ericsson.commonlibrary.CommonLibrary;
import se.ericsson.commonlibrary.CommonLibraryDataProvider;
import se.ericsson.jcat.omp.fw.OmpLibrary;
import se.ericsson.jcat.omp.fw.OmpLibraryException;
import se.ericsson.jcat.omp.fw.OmpSut;
import se.ericsson.jcat.omp.util.Tools;

import com.ericsson.commonlibrary.remotecli.Cli;
import com.ericsson.commonlibrary.remotecli.CliBuilder;
import com.ericsson.commonlibrary.remotecli.CliFactory;
import com.ericsson.commonlibrary.remotecli.exceptions.RemoteCliException;

public class HpHwLibImpl extends OmpLibrary implements HwLib {
    private final static Logger LOGGER = Logger.getLogger(HpHwLibImpl.class);

    private OmpSut sut;

    public HpHwLibImpl(OmpSut sut) {
        this.sut = sut;
    }

    @Override
    public void setSut(OmpSut sut) {
        this.sut = sut;
    }

    @Override
    public String getName() {
        return "HpHwLib";
    }

    @Override
    public String[] getRuntimeDependencies() {
        return new String[0];
    }

    @Override
    public String[] getSetupDependencies() {
        return new String[0];
    }

    @Override
    public void setLibraryDataProvider(CommonLibraryDataProvider commonLibraryDataProvider) {
        throw new NotImplementedException();
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
    public String getUniqueIdentifier() {
        throw new NotImplementedException();
    }

    @Override
    public void initialize() {
        throw new NotImplementedException();
    }

    @Override
    public void shutdown() {
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

    private void repeatCommand(String command, int sleepInSecond, int numOfTimes) throws OmpLibraryException {
        try {
            for (int i = 0; i < numOfTimes; i++) {
                Tools.runCommandLocal(command);
                TimeUnit.SECONDS.sleep(sleepInSecond);
            }
        } catch (IOException e) {
            throw new OmpLibraryException("Failed to power off blade", e);
        } catch (InterruptedException e) {
            throw new OmpLibraryException("Failed to power off blade", e);
        }
    }

    @Override
    public boolean powerOff(int subrack, int blade) throws OmpLibraryException {
        try {
            Tools.runCommandLocal(createPowerOffCmd(blade));
        } catch (IOException e) {
            throw new OmpLibraryException("Failed to power off blade " + subrack + " " + blade, e);
        } catch (InterruptedException e) {
            throw new OmpLibraryException("Failed to power off blade " + subrack + " " + blade, e);
        }
        waitForStatus(blade, HpPowerStatus.OFF, 10, 3);
        return true;
    }

    @Override
    public boolean powerOn(int subrack, int blade) throws OmpLibraryException {
        // Tools.runCommandLocal(createPowerOnCmd(blade));
        repeatCommand(createPowerOnCmd(blade), 2, 3);
        waitForStatus(blade, HpPowerStatus.ON, 10, 3);
        return true;
    }

    @Override
    public boolean powerReset(int subrack, int blade) throws OmpLibraryException {
        HpPowerStatus currStatus = readPowerStatus(blade);
        try {
            Tools.runCommandLocal(createPowerResetCmd(blade));
            if (currStatus.equals(HpPowerStatus.OFF))
                return true; // reset an off blade remains off
        } catch (IOException e) {
            throw new OmpLibraryException("Failed to power reset blade " + subrack + " " + blade, e);
        } catch (InterruptedException e) {
            throw new OmpLibraryException("Failed to power reset blade " + subrack + " " + blade, e);
        }
        waitForStatus(blade, HpPowerStatus.ON, 10, 3);
        return true;
    }

    @Override
    public boolean powerStatus(int subrack, int blade) throws OmpLibraryException {
        return readPowerStatus(blade).equals(HpPowerStatus.ON);
    }

    private HpPowerStatus readPowerStatus(int blade) throws OmpLibraryException {
        try {
            String cmd = createPowerStatusCmd(blade);
            String result = removeLineBreak(Tools.runCommandLocal(cmd).output);
            return HpPowerStatus.get(result);
        } catch (IOException e) {
            throw new OmpLibraryException("Failed to query power status on blade " + blade, e);
        } catch (InterruptedException e) {
            throw new OmpLibraryException("Failed to query power status on blade " + blade, e);
        }
    }

    private String removeLineBreak(String text) {
        return text.replaceAll(System.getProperty("line.separator"), "");
    }

    @Override
    public boolean clusterPowerReset() throws OmpLibraryException {
        Map<Integer, HpPowerStatus> currStats = new HashMap<Integer, HpPowerStatus>();
        for (int i = 1; i <= readNumOfBlades(); i++) {
            currStats.put(i, readPowerStatus(i));
        }
        for (int i = 1; i <= readNumOfBlades(); i++) {
            try {
                Tools.runCommandLocal(createPowerResetCmd(i));
            } catch (IOException e) {
                throw new OmpLibraryException("Failed to get power reset on blade " + i, e);
            } catch (InterruptedException e) {
                throw new OmpLibraryException("Failed to get power reset on blade " + i, e);
            }
        }
        for (int i = 1; i <= readNumOfBlades(); i++) {
            if (currStats.get(i).equals(HpPowerStatus.OFF)) {
                continue;
            }
            waitForStatus(i, HpPowerStatus.ON, 10, 3);
        }
        return true;
    }

    @Override
    public boolean immediateClusterPowerReset() {
        try {
            clusterPowerReset();
        } catch (OmpLibraryException e) {
            LOGGER.info("Failed to reset power on cluster " + e.getMessage(), e);
            return false;
        }
        return true;
    }

    private int readNumOfBlades() {
        return Integer.valueOf(sut.getConfigDataString("physical_size"));
    }

    private String readIpmiUser() {
        return sut.getConfigDataString("ipmiUser");
    }

    private String readIpmiPassword() {
        return sut.getConfigDataString("ipmiPwd");
    }

    private String readHostname(int blade) {
        return sut.getConfigDataString(String.format("ipAddress.ipmi.blade_2_%d", blade));
    }

    private String createPowerOffCmd(int blade) {
        return String.format("ipmitool -U %s -P %s -I lanplus -H %s power off", readIpmiUser(), readIpmiPassword(),
                             readHostname(blade));
    }

    private String createPowerOnCmd(int blade) {
        return String.format("ipmitool -U %s -P %s -I lanplus -H %s power on", readIpmiUser(), readIpmiPassword(),
                             readHostname(blade));
    }

    private String createPowerStatusCmd(int blade) {
        return String.format("ipmitool -U %s -P %s -I lanplus -H %s power status", readIpmiUser(), readIpmiPassword(),
                             readHostname(blade));
    }

    private String createPowerResetCmd(int blade) {
        return String.format("ipmitool -U %s -P %s -I lanplus -H %s power reset", readIpmiUser(), readIpmiPassword(),
                             readHostname(blade));
    }

    private void waitForStatus(int blade, HpPowerStatus status, int sleepInSec, int numOfRetry)
            throws OmpLibraryException {

        LOGGER.info("Power Status for blade is " + readPowerStatus(blade));

        for (int i = 0; i < numOfRetry; i++) {
            LOGGER.info("Waiting for blade to become " + status);

            if (readPowerStatus(blade).equals(status)) {
                LOGGER.info("Status Changed to " + readPowerStatus(blade));
                return;
            }
            try {
                TimeUnit.SECONDS.sleep(sleepInSec);
            } catch (InterruptedException e) {
                LOGGER.info("interupted error!", e);
            }
        }
        throw new OmpLibraryException("Blade is not " + status + " before timeout!");
    }

    /**
     * Get MAC address of the specified interface on a specified HP blade via OA.
     * 
     * @param mgmtIpAddress
     *            String OA ip address
     * @param username
     *            String username for OA
     * @param password
     *            String password for OA
     * @param hwId
     *            String index of device bay, e.x. 1, 2 etc. It should be mapped from the amf logical number for HP
     *            system.
     * @param intfIndex
     *            int index for network interface name. e.x. 0 for eth0
     * @throws Exception
     */
    public String getMacAddress(String mgmtIpAddress, String username, String password, String hwId, int intfIndex)
            throws OmpLibraryException {
        String output = null;

        int deviceBayIndex = Integer.parseInt(hwId);

        final Map<Integer, String> index = new HashMap<Integer, String>();
        index.put(0, "1-a");
        index.put(1, "2-a");
        index.put(2, "1-b");
        index.put(3, "2-b");

        // New
        index.put(4, "1-c");
        index.put(5, "2-c");
        index.put(6, "1-d");
        index.put(7, "2-d");

        final CliBuilder sshBuilder = CliFactory.newSshBuilder();
        sshBuilder.setHost(mgmtIpAddress).setUsername(username).setPassword(password).setNewline("\r");
        final Cli iloCli = sshBuilder.build();

        String targetMac = null;
        try {
            // prompt here is something like "OA-984BE16162D5>"
            iloCli.setExpectedRegexPrompt("OA\\S*>\\s");
            iloCli.connect();
            output = iloCli.send("show SERVER INFO " + deviceBayIndex);

            if (output.contains("Not a valid request while running in standby mode")) {
                throw new OmpLibraryException("MAC address query not valid on standby OA.");
            }
            int nicIndex = intfIndex + 1;

            // Create pattern to extract mac address from strings:
            // "Ethernet FlexNIC LOM:X-x - XX:XX:XX:XX:XX:XX"
            // "NIC X MAC Address: XX:XX:XX:XX:XX:XX"
            // "Ethernet FlexNIC (NIC x) LOM:x-x XX:XX:XX:XX:XX:XX"
            // "Ethernet FlexNIC (NIC x) LOM1:x-x XX:XX:XX:XX:XX:XX"
            Pattern pattern = Pattern.compile("((Ethernet FlexNIC LOM:" + index.get(intfIndex) + "\\s*-\\s*)"
                    + "|(NIC\\s*" + nicIndex + "\\s*MAC Address:\\s*)" + "|(Ethernet FlexNIC\\s\\(NIC\\s*" + nicIndex
                    + "\\)\\s*LOM:" + index.get(intfIndex) + "\\s*)" + "|(Ethernet FlexNIC\\s\\(NIC\\s*" + nicIndex
                    + "\\)\\s*LOM1:" + index.get(intfIndex) + "\\s*))((([0-9a-fA-F]){1,2}[-:]){5}[0-9a-fA-F]{1,2})");

            Matcher m = pattern.matcher(output);
            while (m.find()) {
                targetMac = m.group(6);
            }

        } catch (RemoteCliException e) {
            throw new OmpLibraryException("Unable to get mac Address!", e);
        } finally {
            iloCli.disconnect();
        }

        if (targetMac == null) {
            throw new OmpLibraryException("MAC Address of eth" + intfIndex + " not found in:" + output);
        }
        return targetMac;
    }
}

enum HpPowerStatus {
    ON("Chassis Power is on"), OFF("Chassis Power is off");

    private static final Map<String, HpPowerStatus> lookup = new HashMap<String, HpPowerStatus>();

    static {
        for (HpPowerStatus s : EnumSet.allOf(HpPowerStatus.class)) {
            lookup.put(s.getConsoleOutput(), s);
        }
    }

    private String consoleOutput;

    HpPowerStatus(String consoleOutput) {
        this.consoleOutput = consoleOutput;
    }

    public String getConsoleOutput() {
        return consoleOutput;
    }

    public static HpPowerStatus get(String consoleOutput) {
        return lookup.get(consoleOutput);
    }

    public static HpPowerStatus fromBoolean(boolean bool) {
        return bool ? ON : OFF;
    }

    public boolean toBoolean(HpPowerStatus status) {
        return status.equals(ON);
    }
}
