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

import java.util.ArrayList;
import java.util.Calendar;
import java.util.HashMap;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.TimeoutException;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.apache.log4j.Logger;

import se.ericsson.jcat.omp.fw.OmpLibrary;
import se.ericsson.jcat.omp.fw.OmpLibraryException;
import se.ericsson.jcat.omp.fw.OmpSut;
import se.ericsson.jcat.omp.util.Runner;
import se.ericsson.jcat.omp.util.RunnerFactory;
import se.ericsson.jcat.omp.util.ScriptRunner;

/**
 * Implementation of OsLib interface.
 * 
 */

public class OsLibImpl extends OmpLibrary implements OsLib {
    private static Logger logger = Logger.getLogger(OsLib.class);

    OmpSut sut = null;

    /**
     * Creates a new instance of <code>SshLib</code>.
     * 
     * @param sut
     * @throws Exception
     */
    public OsLibImpl(final OmpSut sut) {
        this.sut = sut;
    }

    /**
     * Returns the unique name of this library.
     */
    public String getName() {
        return "OsLib";
    }

    /**
     * Method called by LibraryBroker to set the Sut of the library
     */
    public void setSut(final OmpSut sut) {
        this.sut = sut;
    }

    public void setUp() {
    }

    public void tearDown() {
    }

    public String[] getRuntimeDependencies() {
        return new String[] { "SshLib" };
    }

    public String[] getSetupDependencies() {
        return new String[] { "SshLib" };
    }

    public boolean waitFordrbdState(Map<String, OsLib.DrbdState> preferredDrbdState, final int maxTimeSecond)
            throws OmpLibraryException {
        long endTime = Calendar.getInstance().getTimeInMillis() + maxTimeSecond * 1000;
        logger.info("Waiting for drbdState");
        boolean returnValue = false;

        try {
            while (!isDrbdState(preferredDrbdState)) {
                waitAndJudge(10, endTime);
                logger.info("Waiting for drbdState...");
            }
            returnValue = true;
        } catch (TimeoutException e) {
            logger.warn("Time out while waiting for nodes (Drbd)");
        }
        return returnValue;
    }

    private void waitAndJudge(int waitTime, long endTime) throws TimeoutException {
        try {
            logger.info("Sleeping for " + waitTime + " seconds...");
            Thread.sleep(waitTime * 1000);
        } catch (java.lang.InterruptedException ie) {
        }
        if (Calendar.getInstance().getTimeInMillis() > endTime) {
            throw new TimeoutException();
        }
    }

    public Map<String, DrbdState> getUpStateDrbd() throws OmpLibraryException {
        Map<String, DrbdState> stateMap = new HashMap<String, DrbdState>();
        SshLib ssh = (SshLib) sut.getLibrary("SshLib");
        String firstController = ssh.sendCommand("hostname", 2, 1, true);
        String secondController = ssh.sendCommand("hostname", 2, 2, true);

        stateMap.put(firstController, DrbdState.PRIMARY_SECONDARY);
        stateMap.put(secondController, DrbdState.SECONDARY_PRIMARY);

        // ************************* DRBD primary/primary is removed by LOTC
        // String version = getDrbdVersion();

        // if (version.equals("8.3.7")) {
        // stateMap.put(firstController, DrbdState.PRIMARY_PRIMARY);
        // stateMap.put(secondController, DrbdState.PRIMARY_PRIMARY);
        // } else if (version.equals("0.7.22")) {
        // stateMap.put(firstController, DrbdState.PRIMARY_SECONDARY);
        // stateMap.put(secondController, DrbdState.SECONDARY_PRIMARY);
        // } else {
        // throw new OmpLibraryException("Drbd version: " + version + " not supported!!");
        // }

        for (String key : stateMap.keySet()) {
            logger.info("State for " + key + " : " + stateMap.get(key).getState());
        }
        return stateMap;
    }

    // ************************* DRBD primary/primary is removed by LOTC
    // /**
    // * Auxiliary method for fetching current version of drbd on cluster.
    // * @return current version of drbd
    // * @throws OmpLibraryException if not able to fetch drbd version
    // */
    // private String getDrbdVersion() throws OmpLibraryException {
    // final SshLib sshLib = (SshLib) sut.getLibrary("SshLib");
    // final String output =
    // sshLib.sendCommand("drbdadm");
    // Pattern p = Pattern.compile(".*Version: (\\d+\\.\\d+\\.\\d+) \\(api.*",
    // Pattern.DOTALL);
    // Matcher m = p.matcher(output);
    // String version;
    //
    // if (m.matches()) {
    // version = m.group(1);
    // logger.info("Drbd version: " + version);
    // } else {
    // throw new OmpLibraryException("Couldn't find drbd version");
    // }
    // return version;
    // }

    public boolean isDrbdState(Map<String, DrbdState> preferredStateMap) throws OmpLibraryException {
        Map<String, DrbdState> drbdStateMap = getDrbdState();
        boolean returnValue = false;
        DrbdState state;

        logger.info("Compare current with preferred drbd state");
        for (String keyPreferred : preferredStateMap.keySet()) {
            state = preferredStateMap.get(keyPreferred);
            returnValue = false;

            logger.info("Preferred state for " + keyPreferred + ": <b>" + state.getState() + "</b>");
            for (String keyDrbd : drbdStateMap.keySet()) {
                if (drbdStateMap.get(keyDrbd) == state) {
                    logger.info("State <b>" + state.getState() + "</b> found on cluster for " + keyDrbd);
                    drbdStateMap.remove(keyDrbd);
                    returnValue = true;
                    break;
                }
            }

            if (returnValue == false) {
                logger.info("Couldn't find state: <b>" + state.getState() + "</b> on cluster");
                logger.info("State not valid");
                returnValue = false;
                break;
            } else {
                logger.info("State valid");
            }

        }
        return returnValue;
    }

    public Map<String, DrbdState> getDrbdState() throws OmpLibraryException {
        String controller;
        DrbdState state;
        Map<String, DrbdState> drbdStateMap = new HashMap<String, DrbdState>();

        final SshLib sshLib = (SshLib) sut.getLibrary("SshLib");
        for (int i = 1; i <= 2; i++) {
            controller = sshLib.sendCommand("hostname", 2, i);
            state = getDrbdState(2, i);
            drbdStateMap.put(controller, state);
        }
        return drbdStateMap;
    }

    /**
     * Auxiliary method for return drbd state on specific blade.
     * 
     * @param subrack
     * @param slot
     * @return drbd state on blade with subrack "subrack" and slot "slot"
     * @throws OmpLibraryException
     *             if not able to fetch drbd state on blade
     */
    private DrbdState getDrbdState(final int subrack, final int slot) throws OmpLibraryException {
        String result = null;

        final SshLib sshLib = (SshLib) sut.getLibrary("SshLib");
        final String output = sshLib.sendCommand("cat /proc/drbd", subrack, slot);

        final Pattern p = Pattern.compile(".*(st|ro):(\\w+/\\w+) (ld|ds):.*", Pattern.DOTALL);
        final Matcher m = p.matcher(output);

        if (m.matches()) {
            result = m.group(2);
        } else {
            throw new OmpLibraryException("No drbd state found: " + output);
        }

        DrbdState drbdState = null;
        for (DrbdState state : DrbdState.values()) {
            if (state.getState().equals(result)) {
                logger.info("Drbd state on cluster for " + sshLib.sendCommand("hostname", subrack, slot) + ": "
                        + state.getState());
                drbdState = state;
                break;
            }
        }
        if (drbdState != null)
            return drbdState;
        else
            throw new OmpLibraryException("Didn't expect drdb state " + result);

    }

    public String[] getNodeHostnames() throws OmpLibraryException {
        Set<String> hostnames = getConfiguredNodes2().keySet();
        ArrayList<String> al = new ArrayList<String>();
        for (String hostname : hostnames) {
            al.add(hostname);
        }

        return (String[]) al.toArray(new String[al.size()]);
    }

    public String[] getLiveNodes() throws OmpLibraryException {
        ArrayList<String> nodeNames = new ArrayList<String>();
        SshLib sshLib = (SshLib) sut.getLibrary("SshLib");
        String nodeList = sshLib.sendCommand("tipc-config -n", true);
        Pattern p = Pattern.compile("\\d.\\d.(\\d+)>: up");
        Matcher nodeListMatcher = p.matcher(nodeList);

        String hostname = sshLib.sendCommand("hostname", true);
        nodeNames.add(hostname);

        while (nodeListMatcher.find()) {
            int i = Integer.parseInt(nodeListMatcher.group(1));
            nodeNames.add(sshLib.sendCommand("hostname", 2, i, true));
        }

        return (String[]) nodeNames.toArray(new String[nodeNames.size()]);
    }

    public boolean waitForDrbdSynch(final int subrack, final int slot, final int timeoutSec) throws OmpLibraryException {
        int synchTimeout = timeoutSec;
        final int sleepTime = 10;

        final SshLib sshLib = (SshLib) sut.getLibrary("SshLib");

        while (sshLib.sendCommand("/bin/cat /proc/drbd", subrack, slot).contains("SyncSource") && (synchTimeout > 0)) {
            logger.info("Drbd not yet in synch: Waiting for " + sleepTime + " seconds");
            try {
                Thread.sleep(sleepTime * 1000);
            } catch (final InterruptedException e) {
            }
            synchTimeout -= sleepTime;
        }

        if (synchTimeout > 0) {
            logger.info("Drbd is Synchronized");
            return true;
        } else {
            logger.error("Drbd is not Synchronized after " + timeoutSec + " seconds");
            return false;
        }

    }

    public Map<String, Integer> getConfiguredNodes2() throws OmpLibraryException {
        final SshLib sshLib = (SshLib) sut.getLibrary("SshLib");
        Map<String, Integer> nodes = new HashMap<String, Integer>();
        String result = sshLib.sendCommand("cat /cluster/etc/cluster.conf | grep \"^ *node\"", true);
        Pattern p = Pattern.compile("^\\s*node\\s+(\\d+)\\s+(control|payload)\\s+(\\S+).*$", Pattern.MULTILINE);
        Matcher m = p.matcher(result);
        while (m.find()) {
            Integer slot = Integer.parseInt(m.group(1));
            String hostname = m.group(3);
            nodes.put(hostname, slot);
        }
        return nodes;
    }

    public int getSubrack(String hostname) throws OmpLibraryException {
        return 2;
    }

    public int getSlot(String hostname) throws OmpLibraryException {
        return getConfiguredNodes2().get(hostname);
    }

    public String getHostname(int subrack, int blade) throws OmpLibraryException {
        final SshLib sshLib = (SshLib) sut.getLibrary("SshLib");
        return sshLib.getHostname(subrack, blade);
    }

    public void backup(String ip, String user, String password, String scriptPath, String storageUser,
            String storagePassword, String backupIp, String backupStorage) throws OmpLibraryException {

        // TODO: Check backup size
        // TODO: Check destination system available space

        ScriptRunner runner = (ScriptRunner) runScript(scriptPath, "lotcbackup.exp " + ip + " " + user + " " + password
                + " " + scriptPath + " " + storageUser + " " + storagePassword + " " + backupIp + " " + backupStorage);

        if (runner.getExitValue() != 0) {
            throw new OmpLibraryException("Failed to backup system.");
        }
    }

    /**
     * Runs a script
     * 
     * @param scriptPath
     *            the script path
     * @param script
     *            the script
     * @return the Runner
     */
    private Runner runScript(String scriptPath, String script) {
        String[] cmd = { "/bin/sh", "-c", scriptPath + script, "" };
        ScriptRunner runner = (ScriptRunner) RunnerFactory.createScriptRunner(cmd);
        runner.run();

        return runner;
    }

    public int getPid(final int subrack, final int slot, final String process) throws OmpLibraryException {
        final SshLib ssh = (SshLib) sut.getLibrary("SshLib");
        final String command = "pgrep -f \"" + process + "\"";
        String pidString = null;
        int pid = 0;

        pidString = ssh.sendCommand(command, subrack, slot);
        if (pidString.matches("\\d+")) {
            pid = Integer.parseInt(pidString);
        } else {
            throw new OmpLibraryException("Couldn't find process: \"" + process + "\"");
        }
        return pid;
    }

    public int[] getPids(final int subrack, final int slot, final String process) throws OmpLibraryException {
        final SshLib ssh = (SshLib) sut.getLibrary("SshLib");
        final String command = "pgrep -f \"" + process + "\"";
        String pidString = null;
        int[] pids = new int[] {};

        pidString = ssh.sendCommand(command, subrack, slot, true);
        if (!(pidString.matches(""))) {
            String[] pidList = pidString.split("\\s+");
            pids = new int[pidList.length];
            for (int i = 0; i < pidList.length; i++) {
                pids[i] = new Integer(pidList[i]);
            }
        }
        return pids;
    }

    public boolean killProcess(final int subrack, final int slot, final int pid) throws OmpLibraryException {
        final SshLib ssh = (SshLib) sut.getLibrary("SshLib");
        final String killCommand = "kill -9 " + pid;
        final String aliveCommand = "kill -0 " + pid;
        final long startTime = System.currentTimeMillis();
        final long stopTime = startTime + 15000;

        String result = ssh.sendCommand(killCommand, subrack, slot, true);
        if (!result.equals("")) {
            throw new OmpLibraryException(result);
        }
        while (System.currentTimeMillis() < stopTime) {
            result = ssh.sendCommand(aliveCommand, subrack, slot);
            if (!result.equals("")) {
                return true;
            }
            try {
                logger.info("Process " + pid + " is still alive after " + (System.currentTimeMillis() - startTime)
                        + " milliseconds.");
                Thread.sleep(1000);
            } catch (final InterruptedException e) {
            }
        }
        logger.warn("Process " + pid + " is still alive after " + (System.currentTimeMillis() - startTime)
                + " milliseconds.");
        return false;
    }

    public boolean isProcessAlive(final int subrack, final int slot, final String process) throws OmpLibraryException {
        final SshLib ssh = (SshLib) sut.getLibrary("SshLib");
        final String command = "pgrep -f \"" + process + "\"";
        String pidString = null;

        pidString = ssh.sendCommand(command, subrack, slot, true);
        System.err.println("pidString: \"" + pidString + "\"");
        if (pidString.matches("\\d+[.\\s\\d\\w]*")) {
            return true;
        } else {
            return false;
        }
    }

    public void backup(String ip, String user, String password, String scriptPath, String storageUser,
            String storagePassword, String backupStorage) throws OmpLibraryException {
        // TODO Auto-generated method stub

    }

    public String[] getCoreDumps() throws OmpLibraryException {
        final SshLib ssh = (SshLib) sut.getLibrary("SshLib");
        String[] result = ssh.sendCommand("ls -1rt /cluster/dumps", true).split("\\n");
        if (result.length == 1 && result[0].trim().isEmpty()) {// Check to see that it really contains a coredump and
                                                               // not just an empty line from ls command. JIRA TR
                                                               // RDAVP-268
            return new String[0];
        } else {
            return result;
        }
    }

    @Deprecated
    public String[] getConfiguredNodes() throws OmpLibraryException {
        final SshLib sshLib = (SshLib) sut.getLibrary("SshLib");
        String[] nodes = null;
        String result = sshLib.sendCommand("grep \\'^node .*\\' /cluster/etc/cluster.conf | awk \\'{print $4}\\'");
        nodes = result.split("\n");

        return nodes;
    }
}
