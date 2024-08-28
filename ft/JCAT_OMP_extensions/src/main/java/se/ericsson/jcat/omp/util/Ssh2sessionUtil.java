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
package se.ericsson.jcat.omp.util;

import java.io.IOException;

import org.apache.log4j.Logger;

import se.ericsson.jcat.fw.utils.Ssh2Session;

import com.trilead.ssh2.Connection;
import com.trilead.ssh2.LocalPortForwarder;

/**
 * The purpose of this class is ... TODO javadoc for class SafSshHelper TODO When we move this for real in a WP we need
 * to go through how this functionality handles insrances and so on...
 */
public class Ssh2sessionUtil {
    private final int defaultSshPort = 22;

    private String helperName = null;

    private Ssh2Session session;

    private Ssh2Session netconfSession;

    private final Logger logger = Logger.getLogger(this.getClass());

    static private String internalConnectionCommand = "rlogin";

    /**
     * Creates a new instance of <code>SafSshHelper</code>.
     * 
     * @param name
     */
    public Ssh2sessionUtil(final String name) {
        this.helperName = name;
    }

    /**
     * @return
     */
    public String getHelperName() {
        return this.helperName;
    }

    /**
     * @return
     */
    public boolean closeSession() {
        final boolean success = true;
        if (this.session != null) {
            this.session.disconnect();
        }
        this.session = null;
        if (this.netconfSession != null) {
            this.netconfSession.disconnect();
        }
        this.netconfSession = null;
        return success;
    }

    /**
     * @return
     */
    public boolean stopForwarding() {
        this.session.disconnect();
        return true;
    }

    /**
     * @return
     */
    public boolean startSafShell() {
        final String safUser = System.getProperty("safUser");
        final String safPass = System.getProperty("safPass");
        final String safIp = System.getProperty("safIp");

        return startSafShell(safIp, safUser, safPass);
    }

    /**
     * @param ip
     * @param port
     * @param user
     * @param pass
     * @param timeout
     * @param maxAttempts
     * @return
     */
    public boolean startSafShell(String ip, final int port, final String user, final String pass, final int timeout,
            final int maxAttempts) {
        String[] tries = { "First", "Second", "Third" };
        for (String s : tries) {
            this.session = startShell(ip, port, user, pass, timeout, maxAttempts);
            if (this.session == null) {
                logger.warn("The " + s + " try failed; Could not start SAF shell IP:" + ip + " Port: " + port
                        + " User: " + user + " Pass: " + "*********");
                // Sleep 5 seconds before we try again (humanlike)
                try {
                    Thread.sleep(5 * 1000);
                } catch (InterruptedException e) {
                    logger.error("Sleep has been interrupted! " + e.getMessage());
                }
            } else {
                // We got an connection.
                return true;
            }
        }
        // We tried 3 times without success.
        return false;
    }

    /**
     * @param ip
     * @param user
     * @param pass
     * @return
     */
    public boolean startSafShell(final String ip, final String user, final String pass) {
        return startSafShell(ip, defaultSshPort, user, pass);
    }

    /**
     * @param ip
     * @param port
     * @param user
     * @param pass
     * @return
     */
    public boolean startSafShell(final String ip, final int port, final String user, final String pass) {
        return startSafShell(ip, port, user, pass, 0, 0);
    }

    /**
     * @param ip
     * @param port
     * @param user
     * @param pass
     * @param timeout
     * @param maxAttempts
     * @return
     * @throws IOException
     */
    public Ssh2Session startNetconfSession(final String ip, final int port, final String user, final String pass,
            final int timeout, final int maxAttempts) throws IOException {
        final Ssh2Session newSession = startSession(ip, port, user, pass);
        newSession.startSubSystem("netconf", timeout, "]]>]]>");
        newSession.setTimeout(timeout);
        this.netconfSession = newSession;
        return this.netconfSession;
    }

    /**
     * @param msg
     * @param timeout
     * @return
     */
    public String sendNetconfMsg(final String msg, final int timeout) {
        try {
            return this.netconfSession.sendCommand(msg, timeout);
        } catch (final Exception e) {
            logger.error("Failed to send Netconf command", e);
            return null;
        }
    }

    /**
     * @param msg
     * @return
     */
    public String sendNetconfMsg(final String msg) {
        try {
            return this.netconfSession.sendCommand(msg);
        } catch (final Exception e) {
            logger.error("Failed to send Netconf command", e);
            return null;
        }
    }

    /**
     * @param bindAddress
     * @param bindPort
     * @param hostAddress
     * @param hostPort
     * @throws IOException
     */
    public void createRemoteTunnel(final String bindAddress, final int bindPort, final String hostAddress,
            final int hostPort) throws IOException {
        final Connection sshClient = this.session.getSshClient();
        sshClient.requestRemotePortForwarding(bindAddress, bindPort, hostAddress, hostPort);
    }

    /**
     * @param bindPort
     * @param hostAddress
     * @param hostPort
     * @return
     * @throws IOException
     */
    public LocalPortForwarder createLocalTunnel(final int bindPort, final String hostAddress, final int hostPort)
            throws IOException {
        final Connection sshClient = this.session.getSshClient();
        return sshClient.createLocalPortForwarder(bindPort, hostAddress, hostPort);
    }

    /**
     * @return
     */
    public Ssh2Session getSafShell() {
        if (session == null) {

        }
        return session;
    }

    /*
     *
     */
    private Ssh2Session startShell(final String ip, final int port, final String user, final String pass,
            final int timeout, final int maxAttempts) {
        final Ssh2Session newSession = startSession(ip, port, user, pass);
        // here you set the default values for the session
        if (newSession != null) {
            // newSession.setNumberOfRetries(-1);
            newSession.setRawOutput(false);
            newSession.setPtyWidth(2000);
            newSession.addShellCommand("rlogin");
            newSession.addShellCommand("rsh");
            newSession.addShellCommand("ssh");
            newSession.openSshShell(timeout, maxAttempts, newSession.getDefaultTerm());
            if (newSession.getSshClient() == null) {
                return null;
            }
        }
        return newSession;
    }

    /*
     *
     */
    private Ssh2Session startSession(final String ip, final int port, final String user, final String pass) {
        final Ssh2Session newSession = new Ssh2Session(ip, port, user, pass);
        return newSession;
    }

    public void resetInternalConnectionCommand() {
        try {
            String result = this.getSafShell().sendCommand("which rlogin");
            if (result.contains("which: no rlogin") || result.contains("command not found")
                    || result.contains("Command not found")) {
                Logger.getLogger(Ssh2sessionUtil.class).info("rlogin command not found on cluster. LOTC 4.1 installed? Use ssh instead");
                internalConnectionCommand = "ssh";
            } else {
                Logger.getLogger(Ssh2sessionUtil.class).info("rlogin command found on the cluster. Use rlogin");
                internalConnectionCommand = "rlogin";
            }
        } catch (IOException e) {
            Logger.getLogger(Ssh2sessionUtil.class).warn("Unable to test rlogin command on the cluster. Try with rlogin for now. "
                                                                 + e.getMessage());
        }
    }

    static public String getInternalConnectionCommand() {
        return internalConnectionCommand;
    }

    static public void determineInternalConnectionCommandNextTime() {
        internalConnectionCommand = "rlogin";
    }

    static public String getInternalBridgeCommand() {
        String command = getInternalConnectionCommand();
        return (command.equalsIgnoreCase("rlogin") ? "rsh" : command);
    }

}
