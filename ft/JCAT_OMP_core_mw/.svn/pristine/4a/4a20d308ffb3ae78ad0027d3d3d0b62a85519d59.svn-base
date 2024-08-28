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
import org.python.core.PyList;
import org.python.core.PyDictionary;
/**
 * The purpose of this class is to define the Java API methods for Python
 * library notification_lib.
 */
public interface NotificationLib {
    
    public PyDictionary readAllNotifications()throws OmpLibraryException;
    
    public String clearNotifications()throws OmpLibraryException;
    
    public String checkNotifications( PyList expectedPatternList, PyList ignoredPatternList, String notifType)throws OmpLibraryException;
    
}
