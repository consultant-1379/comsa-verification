/*------------------------------------------------------------------------------
 *******************************************************************************
 * COPYRIGHT Ericsson 2011
 *
 * The copyright to the computer program(s) herein is the property of
 * Ericsson Inc. The programs may be used and/or copied only with written
 * permission from Ericsson Inc. or in accordance with the terms and
 * conditions stipulated in the agreement/contract under which the
 * program(s) have been supplied.
 *******************************************************************************
 *----------------------------------------------------------------------------*/
package se.ericsson.jcat.omp.library;

import se.ericsson.jcat.omp.fw.OmpLibraryException;

/**
 * Defines the Java API methods for Python library smartedge_lib.
 */
public interface SmartEdgeLib {

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
     * Finds out which port number to use for the port with the given port name. 
     * For example, port with name "2/2" could have port number 3. This port number 
     * is the number to use when managing the port over SNMP. 
     * @param target
     * @param portName
     * @return
     * @throws OmpLibraryException
     */
    public int getIfNumberForPort(String target, String portName) throws OmpLibraryException;

}
