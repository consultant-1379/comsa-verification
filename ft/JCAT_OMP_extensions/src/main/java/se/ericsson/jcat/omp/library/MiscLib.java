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
 * Defines the Java API methods for Python library misc_lib. TODO: Define all
 * methods.
 */
public interface MiscLib {

    /**
     * Executes linux command.
     * 
     * @param command
     */
    public String execCommand(String command)throws OmpLibraryException;
    
    /**
     * suspend test execution.
     * 
     * @param sleep_time seconds
     * @param progress bool, enables the sleep progress
     * @return  sleep_time result
     * @throws OmpLibraryException on command error
     */
    public String waitTime(int sleep_time)throws OmpLibraryException;
}
