package se.ericsson.jcat.omp.library;

import java.util.Date;
import java.util.List;

public interface LogParserLib {

    /**
     * Start a log session with the sessionId. Start time will be generated
     * automatically by current time on remote server. If the server is not
     * available, current time on local machine will be used instead.
     * 
     * @param sessionId Session Id
     * @param ip The IP address of remote
     * @param username Username
     * @param password Password
     * @param logFile The full path to the log file
     * @param timePattern The pattern of the time stamps in log. e.g.
     *        "MMM'.*'d HH:mm"
     * @return true if success
     */
    public boolean startLogSession(String sessionId, String ip,
            String username, String password, String logFile, String timePattern);

    /**
     * Start a log session with the sessionId.
     * 
     * @param sessionId Session Id
     * @param ip The IP address of remote
     * @param username Username
     * @param password Password
     * @param logFile The full path to the log file
     * @param timePattern The pattern of the time stamps in log. e.g.
     *        "MMM'.*'d HH:mm"
     * @param startTime The start time of the session
     * @return true if success
     */
    public boolean startLogSession(String sessionId, String ip,
            String username, String password, String logFile,
            String timePattern, Date startTime);

    /**
     * Start a log session for /var/log/message file. Start time will be
     * generated automatically by current time on remote server. If the server
     * is not available, current time on local machine will be used instead.
     * 
     * @param sessionId Session Id
     * @param ip The IP address of remote
     * @param username Username
     * @param password Password
     * @return true if success
     */
    public boolean startLogSessionForVarLogMessage(String sessionId, String ip,
            String username, String password);

    /**
     * Start a log session for /var/log/message file.
     * 
     * @param sessionId Session Id
     * @param ip The IP address of remote
     * @param username Username
     * @param password Password
     * @param startTime The start time of the session
     * @return true if success
     */
    public boolean startLogSessionForVarLogMessage(String sessionId, String ip,
            String username, String password, Date startTime);

    /**
     * Reset the start time of a log session. Start time will be generated
     * automatically by current time on remote server. If the server is not
     * available, current time on local machine will be used instead.
     * 
     * @param sessionId Session Id
     * @return true if success
     */
    public boolean resetStartTime(String sessionId);

    /**
     * Reset the start time of a log session.
     * 
     * @param sessionId Session Id
     * @param startTime The new start time of the session
     * @return true if success
     */
    public boolean resetStartTime(String sessionId, Date startTime);

    /**
     * Get all log messages between start time and current time.
     * 
     * @param sessionId Session Id
     * @return a list contains all messages
     */
    public List<String> getLogMessages(String sessionId);

    /**
     * Get all log messages between start time and given end time.
     * 
     * @param sessionId Session Id
     * @param stopTime The given end time
     * @return a list contains all messages
     */
    public List<String> getLogMessages(String sessionId, Date stopTime);

    /**
     * Get all log messages match the pattern between start time and current
     * time.
     * 
     * @param sessionId Session Id
     * @param pattern String pattern to match result. e.g. "ERROR"
     * @return a list contains all messages
     */
    public List<String> getLogMessages(String sessionId, String pattern);

    /**
     * Get all log messages match the pattern between start time and given end
     * time.
     * 
     * @param sessionId Session Id
     * @param pattern String pattern to match result. e.g. "ERROR"
     * @param stopTime stopTime The given end time
     * @return a list contains all messages
     */
    public List<String> getLogMessages(String sessionId, String pattern,
            Date stopTime);

    /**
     * Block current thread and wait for at least one message matches the
     * pattern appear after the specified start time. If no message found after
     * max waiting time, the method returns false.
     * 
     * @param sessionId Session Id
     * @param pattern String pattern to match result. e.g. "ERROR"
     * @param startTime Start time
     * @param maxWaitTime Max time for waiting.
     * @return true if found
     */
    public boolean waitForMessage(String sessionId, String pattern,
            Date startTime, int maxWaitTime);

    /**
     * Block current thread and wait for at least one message matches the
     * pattern appear after the start time of the session. If no message found
     * after max waiting time, the method returns false.
     * 
     * @param sessionId Session Id
     * @param pattern String pattern to match result. e.g. "ERROR"
     * @param maxWaitTime Max time for waiting.
     * @return true if found
     */
    public boolean waitForMessage(String sessionId, String pattern,
            int maxWaitTime);
}
