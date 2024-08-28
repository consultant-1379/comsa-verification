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

import java.io.File;
import java.text.SimpleDateFormat;
import java.util.Calendar;

import org.apache.log4j.Logger;

import se.ericsson.jcat.fw.ExtendedFetchLogs;
import se.ericsson.jcat.fw.NonUnitTestCase;
import se.ericsson.jcat.fw.SUT;
import se.ericsson.jcat.fw.utils.Ssh2Session;

/**
 * Fetch logs.
 * 
 * 1. Run a script / command to collect all the logs and package them as a archive. <br>
 * 2. Find the archive's path from the output of previous step. <br>
 * 3. Copy the archive from remote host.
 * 
 * @author ejieyuu
 * 
 */
public abstract class OmpExtendedFetchLogs implements ExtendedFetchLogs {

    private static Logger logger = Logger.getLogger(OmpExtendedFetchLogs.class);

    private final String fetchLogScript;

    /**
     * The final path shown in report html
     */
    private String finalPath;

    /**
     * the name of the logs. Shown in report html
     */
    private final String name;

    /**
     * IP address to SC_2_1 and SC_2_2
     */
    private final String ip1, ip2;

    private final String username, password;

    public OmpExtendedFetchLogs(final String fetchLogScript, final String name, final String ip1, final String ip2,
            final String username, final String password) {
        this.fetchLogScript = fetchLogScript;
        this.name = name;
        this.ip1 = ip1;
        this.ip2 = ip2;
        this.username = username;
        this.password = password;
    }

    protected String getFetchLogScript() {
        return this.fetchLogScript;
    }

    public void fetchLogs(final SUT[] sut, final NonUnitTestCase testCase, final String logfilePath) {
        if (isInstalledOnSystem()) {
            logger.info("Start fetching logs for " + name);
            final String result = runFetchlogScript();
            String[] path = null;
            if (result != null) {
                // Parse result
                path = getFilePath(result);
                // Create sub directory
                Calendar cal = Calendar.getInstance();
                SimpleDateFormat sdf = new SimpleDateFormat("yyyyMMdd_HHmmss");
                String subDir = File.separator + "collect_info" + File.separator + testCase.getId() + "_"
                        + testCase.getName() + "_" + sdf.format(cal.getTime());
                File dir = new File(logfilePath + subDir);
                dir.mkdirs();
                // Copy file
                copyFile(path, dir.getPath());
                // Define file's url.
                finalPath = "." + subDir + File.separator + path[1];
                logger.info(name + " has been copied to: " + finalPath + " in the JCAT logdir");
            }
        } else {
            logger.info("Not fetching " + name + " (product is not installed on system)");
        }
    }

    /**
     * Copy logs from remote host
     * 
     * @param path
     *            A string array. The first element represents the remote path, the second represents the file name
     * @param logfilePath
     *            Where to place the file on local host
     */
    private void copyFile(final String[] path, final String logfilePath) {
        logger.info("Copy file from remote.");
        final String remoteFile = (path[0].endsWith("/") ? path[0] : (path[0] + "/")) + path[1];
        try {
            final Ssh2Session ssh = getSshSession();
            ssh.scpGet(remoteFile, logfilePath);
        } catch (final Exception e) {
            logger.error("Cannot copy log file: " + remoteFile + "! " + e.getMessage());
        }
    }

    /**
     * SSH connection. Try both ip1 and ip2
     * 
     * @return
     * @throws OmpLibraryException
     */
    protected Ssh2Session getSshSession() throws OmpLibraryException {
        Ssh2Session ssh = new Ssh2Session(ip1, username, password);
        if (ssh.getSshClient() == null) {
            // another try
            if (ip2 == null) {
                throw new OmpLibraryException("Cannot connect to server with both " + ip1 + " and " + ip2);
            }
            ssh = new Ssh2Session(ip2, username, password);
            if (ssh.getSshClient() == null) {
                throw new OmpLibraryException("Cannot connect to server with both " + ip1 + " and " + ip2);
            }
        }
        return ssh;
    }

    /**
     * Run the fetchlog script or command
     * 
     * @return
     */
    private String runFetchlogScript() {
        logger.info("Running command " + fetchLogScript);
        try {
            final Ssh2Session ssh = getSshSession();
            // Usually it takes very long time
            ssh.openSshShell();
            ssh.setRawOutput(false);
            ssh.setTimeout(60 * 1000 * 15);
            String printOut = ssh.sendCommand(fetchLogScript);
            ssh.closeSshShell();
            return printOut;
        } catch (final Exception e) {
            logger.error("Cannot run fetchlog script: " + fetchLogScript + "! " + e.getMessage());
            return null;
        }
    }

    /**
     * The parser which finds out where the collected log file is.
     * 
     * @param info
     *            The screen output got from running fetchlog command
     * @return A string array. The first element represents the remote path, the second represents the file name
     */
    public abstract String[] getFilePath(String info);

    protected abstract boolean isInstalledOnSystem();

    public String getName() {
        return name;
    }

    public String getPath() {
        return finalPath;
    }

}
