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

import java.util.Map;
import se.ericsson.jcat.omp.fw.OmpLibraryException;
import se.ericsson.jcat.omp.library.OsLib;

/**
 * The purpose of this class is to define the Java API methods for Python
 * library ssh_lib.
 */
public interface OsLib {
	
	/**
     * Enumeration of states available for drbd
     */
    public enum DrbdState {
    	PRIMARY_PRIMARY("Primary/Primary"),
    	PRIMARY_SECONDARY("Primary/Secondary"),
    	SECONDARY_PRIMARY("Secondary/Primary"),
    	SECONDARY_SECONDARY("Secondary/Secondary");
    	
    	private final String state;
    	
    	DrbdState(String state) {
    		this.state = state;
    	}
    	
    	String getState() {
    		return this.state;
    	}
    } 
   
    /**
     * Get the drbd st state from the specified blade.
     * 
     * @param subrack number
     * @param slot number
     * @return the drbd state as string or null if match failed
     * @throws OmpLibraryException on command error
     */
    public Map<String,DrbdState> getDrbdState() throws OmpLibraryException;
   
    /**
     * Compares predefined drbd state against drbd state on cluster
     * If preferredStateMap contains valid states compared to current states on cluster return true, 
     * otherwise false
     */
    public boolean isDrbdState(Map<String,DrbdState> preferdStateMap) throws OmpLibraryException;
    

    /**
     * Returns expected up state for current version of drbd on cluster.
     */
    public Map<String,DrbdState> getUpStateDrbd() throws OmpLibraryException;
       	
    
    /**
     * Wait for DRBD to become synhcronized after a reboot or installation.
     * 
     * @param subrack number
     * @param slot number
     * @param timeoutSec maximum time to wait in seconds
     * @return true if drbd is synchronized within timeout
     * @throws OmpLibraryException on command error
     */
    public boolean waitForDrbdSynch(int subrack, int blade, int timeoutSec) throws OmpLibraryException;
    
    /**
     * 
     * @return a String array with the active nodes on the cluster
     * @throws OmpLibraryException
     */
    public String[] getLiveNodes() throws OmpLibraryException;
    
    /**
     * Return a Map with all configured hostnames as keys and their node number as the value
     * The node number can also be used as the last digit in a tipc address or 
     * as a slot in a subrack, slot pair
     *
     * @return A map with hostnames as keys and their node number as value.
     * @throws OmpLibraryException
     */
    public Map<String, Integer> getConfiguredNodes2() throws OmpLibraryException;

	/**
	 * Get the subrack of the hostname
	 * 
	 * @param hostname
	 * @return the subrack of the hostname
	 * @throws OmpLibraryException
	 */
    public int getSubrack(String hostname) throws OmpLibraryException;
    
    /**
     * Get the slot of the hostname
     * 
     * @param hostname
     * @return the slot of the hostname
     * @throws OmpLibraryException
     */
    public int getSlot(String hostname) throws OmpLibraryException;

    /**
     * Get the hostname for subrack and slot
     * 
     * @param subrack
     * @param slot
     * @return the hostname of the node
     * @throws OmpLibraryException
     */
    
    public String getHostname(int subrack, int slot) throws OmpLibraryException;
    
    /**
     * Gets a process ID
     * 
     * @param subrack
     * @param slot
     * @param process
     * @return
     * @throws OmpLibraryException if something goes wrong with the connection between the cluster
     */
    public int getPid(int subrack, int slot, String process)
        throws OmpLibraryException;

    
    /**
     * Return the pids for the processes that matches the string "process"
     * @param subrack
     * @param slot
     * @param process
     * @return
     * @throws OmpLibraryException
     */
    public int[] getPids(int subrack, int slot, String process)
        throws OmpLibraryException;
    /**
     * Kills the given process
     * @param subrack
     * @param slot
     * @param pid The process identifier
     * @return false if the process is still alive 5 seconds after command is sent.
     * @throws OmpLibraryException
     */
    public boolean killProcess(int subrack, int slot, int pid)
            throws OmpLibraryException;
    
    /**
     * Check if a process is running
     * 
     * @param subrack
     * @param slot
     * @param process name
     * @throws OmpLibraryException
     */
    public boolean isProcessAlive(final int subrack, final int slot, final String process) throws OmpLibraryException;
 
	/**
	 * Creates a lotc backup.
	 * @param ip - the host to take backup from
	 * @param user - backup host credential
	 * @param password - backup host credential
	 * @param scriptPath - the scriptpath
	 * @param storageUser - 
	 * @param storagePassword
	 * @param backupStorage
	 * @throws OmpLibraryException
	 */
    public void backup(String ip, String user, String password, String scriptPath, String storageUser, String storagePassword, String backupIp, String backupStorage) throws OmpLibraryException;
    
    /**
     * 
     * @return all current core files on the system
     * @throws OmpLibraryException
     */
    public String[] getCoreDumps() throws OmpLibraryException;
    
    
    /**
     * Pre condition SSH connection against sc-2-1 and sc-2-2
     * This method wait for drbd on the cluster to become as the state "prefferedDrbdState"
     * @param preferredDrbdState a map containing the state to wait for on the cluster
     * @param maxTimeSecond is the maximum time to wait for drbd to match the "preferredDrbdState"
     * @return true if the drbd on the cluster matches the "preferredDrbdState" before waiting more then "maxTimeSecond", 
     * otherwise return false
     * @throws OmpLibraryException
     */
    public boolean waitFordrbdState(Map<String,OsLib.DrbdState> preferredDrbdState, final int maxTimeSecond) throws OmpLibraryException;
    
    /**
     * Get all hostnames on the system using cluster.conf.
     * 
     * @return a string array with node hostnames
     * @throws OmpLibraryException
     */
    public String[] getNodeHostnames() throws OmpLibraryException;
    
    @Deprecated
    /**
     * Reports the configured nodes using cluster.conf
     *
     * @return The configured nodes this system consists of.     * @throws OmpLibraryException
     * @deprecated since 2010-08-11 use getConfiguredNodes2() instead, will be removed 2011-01-01
     */
    public String[] getConfiguredNodes() throws OmpLibraryException;
    
}
