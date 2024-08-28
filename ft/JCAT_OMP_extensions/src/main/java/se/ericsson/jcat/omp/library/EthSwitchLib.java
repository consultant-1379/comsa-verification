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
 * Defines the Java API methods for Python library ethswitch_lib.
 */
public interface EthSwitchLib extends CommonLibrary {

    /**
     * Set target port to down.
     * 
     * @param target - Name of target switch
     * @param port - Switch port
     * @return Result message, success or error
     * @throws OmpLibraryException
     */
    public String portDown(String target, String port)
            throws OmpLibraryException;

    /**
     * Set target port to up.
     * 
     * @param target - Name of target switch
     * @param port - Switch port
     * @return Result message, success or error
     * @throws OmpLibraryException
     */
    public String portUp(String target, String port) throws OmpLibraryException;

    /**
     * Set all target ports, except from the management ports, to down state.
     * 
     * @param target - Name of target switch
     * @return Result message, success or error
     * @throws OmpLibraryException
     */
    public String checkAndFixAllPortToDown(String target)
            throws OmpLibraryException;

    /**
     * Set all target ports, except from the management ports, to up state.
     * 
     * @param target - Name of target switch
     * @return Result message, success or error
     * @throws OmpLibraryException
     */
    public String checkAndFixAllPortToUp(String target)
            throws OmpLibraryException;

    /**
     * Set all target ports, except from the management ports, to up state.
     * 
     * @param target - Name of target switch
     * @param ports - A String Array with the port numbers 
     * @return Result message, success or error
     * @throws OmpLibraryException
     */ 
    public String checkAndFixAllListedPortsToUp(final String target, final String[] ports)
            throws OmpLibraryException;

    /**
     * Set all target ports, except from the management ports, to down state.
     * 
     * @param target - Name of target switch
     * @param ports - A String Array with the port numbers 
     * @return Result message, success or error
     * @throws OmpLibraryException
     */ 
    public String checkAndFixAllListedPortsToDown(final String target, final String[] ports)
            throws OmpLibraryException;

    /**
     * Return information of which port that are operational in 'Up' state.
     * 
     * @param target - Name of target switch
     * @return Result message, success or error
     * @throws OmpLibraryException
     */
    public String getListIfUpOperStatus(String target)
            throws OmpLibraryException;
    
    /**
     * Return information of if the port is Up and functional.
     * 
     * @param switchName - Name of switch to verify
     * @param port - port to verify
     * @return Result message, up or down
     * @throws OmpLibraryException
     */
    public String getPortState(String switchName, int port )
            throws OmpLibraryException;

    /**
     * Return information of which port that are operational and active in 'Up'
     * state.
     * 
     * @param target - Name of target switch
     * @return Result message, success or error
     * @throws OmpLibraryException
     */
    public String getListIfUpAdminStatus(String target)
            throws OmpLibraryException;

    /**
     * Return information of which port that are NOT operational in 'Up' state.
     * 
     * @param target - Name of target switch
     * @return Result message, success or error
     * @throws OmpLibraryException
     */
    public String getListIfNotUpOperStatus(String target)
            throws OmpLibraryException;

    /**
     * Return information of which port that are operational and NOT active in
     * 'Up' state.
     * 
     * @param target - Name of target switch
     * @return Result message, success or error
     * @throws OmpLibraryException
     */
    public String getListIfNotUpAdminStatus(String target)
            throws OmpLibraryException;

}
