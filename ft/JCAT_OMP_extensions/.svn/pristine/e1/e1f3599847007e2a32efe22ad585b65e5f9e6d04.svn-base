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

import se.ericsson.jcat.omp.fw.OmpLibraryException;

/**
 * The purpose of this class is to define the Java API methods for Python
 * library snmp_lib.
 */
public interface SnmpLib {
    
    /**
     * Perform snmp get command towards primary_sc using ssh_lib.
     * 
     * @param community read community string
     * @param command string command to send
     * @return result string
     * @throws OmpLibraryException on command error
     */
    public String snmpGet(String community, String command)
            throws OmpLibraryException;

}
