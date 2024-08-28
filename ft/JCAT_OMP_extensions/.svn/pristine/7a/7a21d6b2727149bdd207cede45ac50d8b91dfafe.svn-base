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
public interface HpNetworkLib extends CommonLibrary {

    /**
     * Get the status of Virtual Connect either it is primary of secondary.
     * 
     * @param target
     *            - Name of target VC
     * @return Result message, Success or failure
     * @throws OmpLibraryException
     */

    public boolean getActiveVcStatus() throws OmpLibraryException;

    /**
     * Shutdown the Virtual Connect if it is available to working.
     * 
     * @param target
     *            - Address of target VC
     * @return Result message, Success or failure
     * @throws OmpLibraryException
     */
    public boolean virtualConnectDown() throws OmpLibraryException;

    /**
     * Reset the Virtual Connect. Shutdown and then switch it on again. Check status for fail over.
     * 
     * @param target
     *            - Address of target VC
     * @return Result message, Success or failure
     * @throws OmpLibraryException
     */

    public boolean virtualConnectReset() throws OmpLibraryException;

    /**
     * Switch on the Virtual Connect if it is down.
     * 
     * @param target
     *            - Address of target VC
     * @return Result message, Success or failure
     * @throws OmpLibraryException
     */
    public boolean virtualConnectUp() throws OmpLibraryException;

    /**
     * Shutdown the onboard admin if it is available to working.
     * 
     * @param target
     *            - Address of target OA
     * @return Result message, Success or failure
     * @throws OmpLibraryException
     */
    public boolean onboadAdminShutdown() throws OmpLibraryException;

    /**
     * Switch on the onboard admin if it is down.
     * 
     * @param target
     *            - Address of target OA
     * @return Result message, Success or failure
     * @throws OmpLibraryException
     */
    public boolean onboadAdminUp() throws OmpLibraryException;

    /**
     * Reset the onboard admin. Shutdown and then switch it on again. Check status for fail over.
     * 
     * @param target
     *            - Address of target OA
     * @return Result message, Success or failure
     * @throws OmpLibraryException
     */
    public boolean onboadAdminReset() throws OmpLibraryException;

}
