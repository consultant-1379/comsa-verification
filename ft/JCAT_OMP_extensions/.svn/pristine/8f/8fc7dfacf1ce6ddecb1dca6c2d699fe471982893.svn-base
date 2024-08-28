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

import org.python.core.PyDictionary;

import se.ericsson.commonlibrary.CommonLibrary;
import se.ericsson.jcat.omp.fw.OmpLibraryException;

/**
 * The purpose of this class is to define the Java API methods for Python library ssh_lib.
 */
public interface SshLib extends CommonLibrary {

    public PyDictionary getTargetData();

    /**
     * This function is the exported function for others to call when communication towards a interactive remote shell
     * is required. First: The function checks weather a handle is created for the remote machine accessing. If not, a
     * new handle is created. (Login sequence initiated!) Secondly: Validates that user is logged in to the correct
     * blade. Third: Executes the command.
     * 
     * @param command
     *            to execute
     * @param subrack
     *            subrack number
     * @param blade
     *            blade number
     * @return command result
     * @throws OmpLibraryException
     *             on command error
     */
    public String sendCommand(String command, int subrack, int blade) throws OmpLibraryException;

    public String sendCommand(String command, int subrack, int blade, boolean retry) throws OmpLibraryException;

    public String sendCommand(String command) throws OmpLibraryException;

    public String sendCommand(String command, boolean retry) throws OmpLibraryException;

    /**
     * This function is the exported function for others to call when communication towards a interactive remote shell
     * is required over the north bound interface
     * 
     * @param command
     *            to execute
     * @return command result
     * @throws OmpLibraryException
     *             on command error
     */
    public String sendCommandNbi(String command) throws OmpLibraryException;

    /**
     * This function is used to change the timeout used when using SendCommand(). This will be the new timeout setting
     * valid for the handle.
     * 
     * @param timeout
     *            value in seconds
     * @param subrack
     *            number
     * @param slot
     *            number
     * @return command result
     * @throws OmpLibraryException
     *             on command error
     */
    public String setTimeout(int timeout, int subrack, int slot) throws OmpLibraryException;

    public String setTimeout(int timeout) throws OmpLibraryException;

    /**
     * This method is used to fetch the timeout used when using SendCommand().
     * 
     * @param subrack
     *            number
     * @param slot
     *            number
     * @return command result
     * @throws OmpLibraryException
     *             on command error
     */
    public String getTimeout(int subrack, int slot) throws OmpLibraryException;

    /**
     * This function is the exported function for others to call when communication towards an interactive remote shell
     * is required.
     * 
     * @param host
     *            name
     * @param command
     *            to execute
     * @param user
     *            login user name
     * @param password
     *            login password
     * @param timeout
     *            value in seconds
     * @return command result
     * @throws OmpLibraryException
     *             on command error
     */
    public String sendRawCommand(String host, String command, String user, String password, int timeout)
            throws OmpLibraryException;

    /**
     * This function is the exported function for others to call when communication towards an interactive remote shell
     * is required.
     * 
     * @param host
     *            name
     * @param port
     *            port
     * @param command
     *            to execute
     * @param user
     *            login user name
     * @param password
     *            login password
     * @param timeout
     *            value in seconds
     * @return command result
     * @throws OmpLibraryException
     *             on command error
     */
    public String sendRawCommand(String host, String command, String user, String password, int timeout, int port)
            throws OmpLibraryException;

    /**
     * This method is used to login into cluster HW equipment using a user name with a password
     * 
     * @param subrack
     *            number
     * @param slot
     *            number
     * @param attempts
     *            number of attempts
     * @param user
     *            login user name
     * @param pwd
     *            login password
     * @return command result
     * @throws OmpLibraryException
     *             on command error
     */
    public String loginTest(int subrack, int slot, int attempts, String user, String pwd) throws OmpLibraryException;

    /**
     * This method will set up a ssh tunnel to an internal adress (via one of the controller nodes) directly from the
     * test machine. This is needed for communicating with the LoadClient.
     * 
     * @param blade
     *            name
     * @param localPort
     *            number
     * @param destinationPort
     *            number
     * @return command result
     * @throws OmpLibraryException
     *             on command error
     */
    public String bindAddresses(String blade, int localPort, int destinationPort) throws OmpLibraryException;

    /**
     * Method for reading a file within the cluster using tunnel.
     * 
     * @param blade
     *            name
     * @param localPort
     *            number
     * @param fileName
     *            to read
     * @param request
     *            read type
     * @return command result
     * @throws OmpLibraryException
     *             on command error
     */
    public String readFile(String blade, int localPort, String fileName, String request) throws OmpLibraryException;

    /**
     * Method for copying a file from a remote destination.
     * 
     * @param file
     * @param destination
     * @param timeout
     * @param numberOfRetries
     * @return
     * @throws OmpLibraryException
     */
    public String remoteCopy(String file, String destination, int timeout, int numberOfRetries)
            throws OmpLibraryException;

    public String remoteCopyFrom(String file, String destination, int timeout) throws OmpLibraryException;

    /**
     * This function copies a file
     * 
     * @param file
     * @param host
     * @param destpath
     * @param user
     * @param passwd
     * @param timeout
     * @return
     * @throws OmpLibraryException
     */
    public String sCopy(String file, String host, String destpath, String user, String passwd, int timeout)
            throws OmpLibraryException;

    public void tearDownHandles();

    /**
     * Set where to send the commands be default (if no subrack, slot is mentioned)
     * 
     * @param subrack
     * @param slot
     * @param number
     *            the same as slot
     */
    public void setConfig(int subrack, int slot, int number);

    /**
     * Set where to send the commands by default also considering to use vip oam or not.
     * 
     * @param subrack
     * @param slot
     * @param number
     * @param useVipOam
     */
    public void setConfig(int subrack, int slot, int number, boolean useVipOam);

    /**
     * Automatically set where to send the commands be default (if no subrack, slot is mentioned). Basing on the
     * connectivity of the SSH ports on both of the SCs. If both of them are on, SC1 has higher priority.
     */
    public boolean setConfig();

    public boolean setConfig(boolean useVipOam);

    /**
     * Get current setting of the default SC where commands will be sent to
     * 
     * @return int[] {subrack, slot}
     */
    public int[] getConfig();

    public boolean getUseVipOam();

    /**
     * This method waits a predetermined amount of time for connection to a given interface
     * 
     * @param subrack
     * @param slot
     * @param timeout
     * @return
     */
    public boolean waitForConnection(int subrack, int slot, int timeout);

    /**
     * Waits a predetermined amount of time whereby it can be established that the equipment in question is not possible
     * to connect to.
     * 
     * @param subrack
     * @param slot
     * @param timeout
     * @return
     */
    public boolean waitForNoConnection(int subrack, int slot, int timeout);

    /**
     * Get hostname from blade
     * 
     * @param subrack
     * @param blade
     * @return result of "hostname" command
     * @throws OmpLibraryException
     */
    public String getHostname(int subrack, int blade) throws OmpLibraryException;

    /**
     * Get the internal connection command. rlogin or ssh.
     * 
     * @return the command can be used
     */
    public String getInternalConnectionCommand();

    /**
     * Get the internal bridge command which can be used to send commands. ssh or rsh
     * 
     * @return
     */
    public String getInternalBridgeCommand();

    /**
     * Reset (recheck) internal connection command. rlogin or ssh.
     */
    public void resetInternalConnectionCommand();

    /**
     * Recheck internal connection command next time when creating handlers. use rlogin or ssh.
     */
    public void determineInternalConnectionCommandNextTime();
}
