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

import se.ericsson.commonlibrary.CommonLibrary;
import se.ericsson.jcat.omp.fw.OmpLibraryException;

/**
 * The purpose of this class is to define the Java API methods for Python library ssh_lib.
 */
public interface HwLib extends CommonLibrary {
    /**
     * Power off node(IPMI).
     * 
     * @param subrack
     *            number
     * @param slot
     *            number
     * @return true if success
     * @throws OmpLibraryException
     *             on command error
     */
    public boolean powerOff(int subrack, int blade) throws OmpLibraryException;

    /**
     * Power on node(IPMI).
     * 
     * @param subrack
     *            number
     * @param slot
     *            number
     * @return true if success
     * @throws OmpLibraryException
     *             on command error
     */
    public boolean powerOn(int subrack, int blade) throws OmpLibraryException;

    /**
     * Power Reset node(IPMI).
     * 
     * @param subrack
     *            number
     * @param slot
     *            number
     * @return true if success
     * @throws OmpLibraryException
     *             on command error
     */
    public boolean powerReset(int subrack, int blade) throws OmpLibraryException;

    /**
     * Get power status for node(IPMI).
     * 
     * @param subrack
     *            number
     * @param slot
     *            number
     * @return true if on
     * @throws OmpLibraryException
     *             on command error
     */
    public boolean powerStatus(int subrack, int blade) throws OmpLibraryException;

    /**
     * Reset the cluster, power off/on, all valid blades(IPMI).
     * 
     * @return true if success
     * @throws OmpLibraryException
     *             on command error
     */
    public boolean clusterPowerReset() throws OmpLibraryException;

    public boolean immediateClusterPowerReset();

    public String getMacAddress(String mgntIpAddress, String username, String password, String hwId, int intfIndex)
            throws OmpLibraryException;

}
