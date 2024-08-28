package se.ericsson.jcat.omp.util;

/***
 * Used together with the waitUntilTrue method in Tools class
 * 
 * @author ejieyuu
 * 
 */
public interface Waitable {
    /***
     * A description why to wait
     * 
     * @return
     */
    String getDescription();

    /**
     * get check result
     * 
     * @return waiting will be ended when getting true here
     * @throws WaitTerminationException
     *             terminate the waiting if this exception is thrown, but the exception will not be thrown to upper
     *             level
     * @throws WaitCriticalException
     *             terminate the waiting if this exception is thrown, and the exception will be thrown to upper level
     */
    boolean getCheckResult() throws WaitTerminationException, WaitCriticalException;
}
