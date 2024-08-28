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


public interface SnmpNotification {
    
    
    public enum NotificationType {
        Alarm, Alert, Heartbeat, Other
    };
    
    /**
     * 
     * @return 
     */
    public NotificationType getNotificationType();
    
    /**
     * 
     * @return  text information about snmp notification
     */
    public String[] toLogText();
}
