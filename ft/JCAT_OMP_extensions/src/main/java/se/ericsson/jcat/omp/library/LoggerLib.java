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

/**
 * The purpose of this class is to define the Java API methods for Python library logger_lib.
 */
public interface LoggerLib {
    public void setLogFile(String logFile);
    
    /**
     * * This function will write the log message to a file using the logging
     * module. If no handle are associated with the logging module a new log
     * file handle are created. TODO Need to handle ClassCastException
     * 
     * @param message
     * @param logLevel
     * @return
     */
    public String logMessage(String message, String logLevel);
    
    /**
     * This function will write the enter message, ('caller') >>> 'enter' where
     * 'caller' is the calling module and 'enter' is the function being
     * called, to the log file. If no handle is associated with the logging
     * module a new log file handle is created. TODO Need to handle
     * ClassCastException
     */
    public String enter();
    
    /**
     * This function will write the leave message, ('caller') <<< 'enter' where 'caller' is the calling module
     * and 'enter' is the function being called, to the log file. If no handle is associated 
     * with the logging module a new log file handle is created.
     * 
     * TODO Need to handle ClassCastException
     */
    public String leave();
}
