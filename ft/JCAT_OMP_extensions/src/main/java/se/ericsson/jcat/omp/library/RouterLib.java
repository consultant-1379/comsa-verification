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

public interface RouterLib extends CommonLibrary {

    /**
     * Set target port to down.
     * 
     * @param target
     *            - Name of target router
     * @param port
     *            - router port
     * @return Result message, success or error
     * @throws OmpLibraryException
     */
    public String portDown(String target, String port) throws OmpLibraryException;

    /**
     * Set target port to up.
     * 
     * @param target
     *            - Name of target router
     * @param port
     *            - router port
     * @return Result message, success or error
     * @throws OmpLibraryException
     */
    public String portUp(String target, String port) throws OmpLibraryException;

    /**
     * Power off the target router.
     * 
     * @param target
     *            - Name of target router
     * @return true if success
     * @throws OmpLibraryException
     */
    public boolean powerOff(String target) throws OmpLibraryException;

    /**
     * Power on the target router.
     * 
     * @param target
     *            - Name of target router
     * @return true if success
     * @throws OmpLibraryException
     */
    public boolean powerOn(String target) throws OmpLibraryException;

}
