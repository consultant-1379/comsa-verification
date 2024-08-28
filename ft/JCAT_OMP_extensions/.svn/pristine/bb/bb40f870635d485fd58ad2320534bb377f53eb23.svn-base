package se.ericsson.jcat.omp.library;

import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.HashMap;
import java.util.List;

import org.apache.log4j.Logger;

import se.ericsson.jcat.fw.utils.Ssh2Session;
import se.ericsson.jcat.omp.fw.OmpLibrary;
import se.ericsson.jcat.omp.fw.OmpLibraryException;
import se.ericsson.jcat.omp.fw.OmpSut;

/**
 * This class parses any log file from remote host.
 */
public class LogParserLibImpl extends OmpLibrary implements LogParserLib {

    private final Logger logger = Logger.getLogger(LogParserLibImpl.class);

    private final HashMap<String, LogSession> sessionMap;

    public LogParserLibImpl(final OmpSut sut) throws Exception {
        sessionMap = new HashMap<String, LogSession>();
    }

    @Override
    public String getName() {
        return "LogParserLib";
    }

    @Override
    public String[] getRuntimeDependencies() {
        return new String[] {};
    }

    @Override
    public String[] getSetupDependencies() {
        return new String[] {};
    }

    @Override
    public void setSut(final OmpSut sut) {
    }

    public void setUp() {
        logger.info("LogParserLib started.");
    }

    public boolean startLogSession(final String sessionId, final String ip, final String username,
            final String password, final String logFile, final String timePattern) {
        return startLogSession(sessionId, ip, username, password, logFile, timePattern, null);
    }

    public boolean startLogSessionForVarLogMessage(final String sessionId, final String ip, final String username,
            final String password) {
        return startLogSessionForVarLogMessage(sessionId, ip, username, password, null);
    }

    public boolean startLogSessionForVarLogMessage(final String sessionId, final String ip, final String username,
            final String password, final Date startTime) {
        return startLogSession(sessionId, ip, username, password, "/var/log/messages", "MMM'.*'d HH:mm", startTime);
    }

    public boolean startLogSession(final String sessionId, final String ip, final String username,
            final String password, final String logFile, final String timePattern, final Date startTime) {
        logger.info("Start log session: " + sessionId);
        final LogSession session = new LogSession(ip, username, password, logFile, timePattern);
        boolean start = false;
        if (startTime != null) {
            start = session.startLog(startTime);
        } else {
            start = session.startLog();
        }
        if (start) {
            sessionMap.put(sessionId, session);
            return true;
        } else {
            logger.error("Cannot create logSession.");
            return false;
        }
    }

    public boolean resetStartTime(final String sessionId) {
        return resetStartTime(sessionId, null);
    }

    public boolean resetStartTime(final String sessionId, final Date startTime) {
        logger.info("Reset log session time: " + sessionId);
        final LogSession session = sessionMap.get(sessionId);
        if (session == null) {
            logger.error("Cannot find log session with id " + sessionId);
            return false;
        }
        if (startTime != null) {
            return session.startLog(startTime);
        } else {
            return session.startLog();
        }
    }

    public List<String> getLogMessages(final String sessionId) {
        return getLogMessages(sessionId, "", null);
    }

    public List<String> getLogMessages(final String sessionId, final Date stopTime) {
        return getLogMessages(sessionId, "", stopTime);
    }

    public List<String> getLogMessages(final String sessionId, final String pattern) {
        return getLogMessages(sessionId, pattern, null);
    }

    public List<String> getLogMessages(final String sessionId, final String pattern, final Date stopTime) {
        logger.info("Getting messages from log session: " + sessionId);
        final LogSession session = sessionMap.get(sessionId);
        if (session == null) {
            logger.error("Cannot find log session with id " + sessionId);
            return null;
        }
        if (stopTime != null) {
            return session.getMessages(pattern, stopTime);
        } else {
            return session.getMessages(pattern);
        }
    }

    public boolean waitForMessage(final String sessionId, final String pattern, final Date startTime,
            final int maxWaitTime) {
        logger.info("Waiting for log session: " + sessionId);
        int maxTime = maxWaitTime;
        final LogSession session = sessionMap.get(sessionId);
        if (session == null) {
            logger.error("Cannot find log session with id " + sessionId);
            return false;
        }
        while (!session.checkMessage(pattern, startTime, null)) {
            try {
                Thread.sleep(15 * 1000);
            } catch (final InterruptedException e) {
                logger.error("Should not happen! " + e.getMessage());
                return false;
            }
            maxTime -= 15;
            if (maxTime <= 0) {
                return false;
            }
        }
        return true;
    }

    public boolean waitForMessage(final String sessionId, final String pattern, final int maxWaitTime) {
        return waitForMessage(sessionId, pattern, null, maxWaitTime);
    }

    /**
     * Log session which keeps ip, username, password, etc.
     */
    private class LogSession {

        private final Logger logger = Logger.getLogger(LogSession.class);

        private boolean started = false;

        private final String ip;

        private final String username;

        private final String password;

        private final String logFile;

        private final String timePattern;

        private Date startTime;

        public LogSession(final String ip, final String username, final String password, final String logFile,
                final String timePattern) {
            this.ip = ip;
            this.username = username;
            this.password = password;
            this.logFile = logFile;
            this.timePattern = timePattern;
        }

        /**
         * Start log session with current time
         * 
         * @return true if success
         */
        public boolean startLog() {
            return startLog(getCurrentTimeOnServer());
        }

        /**
         * Get current from server first, if failed, get current time from local
         * 
         * @return current time
         */
        private Date getCurrentTimeOnServer() {
            try {
                final Ssh2Session ssh = getSshSession();
                if (ssh.getSshClient() == null) {
                    return Calendar.getInstance().getTime();
                }
                final String time = sendCommand(ssh, "date +\"%Y-%m-%d %H:%M\"");
                final SimpleDateFormat dateFormater = new SimpleDateFormat("yyyy-MM-dd HH:mm");
                return dateFormater.parse(time);
            } catch (final Exception e) {
                logger.warn("Cannot get current time from server! " + e.getMessage());
                return Calendar.getInstance().getTime();
            }
        }

        /**
         * Start log session with start time
         * 
         * @param startTime
         *            Start time
         * @return true if success
         */
        public boolean startLog(final Date startTime) {
            if (startTime == null) {
                logger.error("Start time cannot be null!");
                return false;
            }
            this.startTime = startTime;
            started = true;
            return true;
        }

        /**
         * Parses a log by grep-ing on the specified timePattern and any additional pattern.
         * 
         * @param pattern
         *            A string pattern matches the result
         */
        private ArrayList<String> parse(final String pattern, final Date tmpStartTime, final Date stopTime) {
            final ArrayList<String> logMessages = new ArrayList<String>();

            final SimpleDateFormat sdf = new SimpleDateFormat(timePattern);

            Date time = null;
            if (tmpStartTime == null) {
                time = (Date) startTime.clone();
            } else {
                time = (Date) tmpStartTime.clone();
            }

            String additionalGrep = "";

            if (pattern != null && pattern.length() != 0) {
                additionalGrep = "| grep \"" + pattern + "\"";
            }

            try {
                while (time.compareTo(stopTime) <= 0) {
                    final Ssh2Session ssh = getSshSession();
                    if (ssh.getSshClient() == null) {
                        logger.error("Cannot connect to server!");
                        return null;
                    }
                    final String response = sendCommand(ssh,
                                                        "cat " + logFile + " | grep \"" + sdf.format(time.getTime())
                                                                + "\"" + additionalGrep);
                    final String[] result = response.trim().split("\\n");
                    for (int x = 0; x < result.length; x++) {
                        logMessages.add(result[x]);
                    }
                    time.setTime(time.getTime() + 60000);
                }
            } catch (final Exception e) {
                logger.error("Cannot get log from remote. " + e.getMessage());
            }

            return logMessages;
        }

        public List<String> getMessages(final String pattern) {
            final Date stopTime = getCurrentTimeOnServer();
            return getMessages(pattern, stopTime);
        }

        public List<String> getMessages(final String pattern, final Date stopTime) {
            return getMessages(pattern, null, stopTime);
        }

        public List<String> getMessages(final String pattern, final Date tmpStartTime, final Date stopTime) {
            if (!started) {
                logger.error("Log session must be started first!");
                return null;
            }
            if (stopTime == null) {
                logger.error("Stop time cannot be null!");
                return null;
            }
            final ArrayList<String> messages = parse(pattern, tmpStartTime, stopTime);
            return messages;
        }

        public boolean checkMessage(final String pattern, final Date tmpStartTime, final Date stopTime) {
            Date tmpStopTime = null;

            if (stopTime == null) {
                tmpStopTime = getCurrentTimeOnServer();
            } else {
                tmpStopTime = (Date) stopTime.clone();
            }

            final List<String> messages = getMessages(pattern, tmpStartTime, tmpStopTime);
            if (messages.size() == 0) {
                return false;
            }
            for (final String s : messages) {
                if (!s.trim().equals("")) {
                    return true;
                }
            }
            return false;
        }

        private Ssh2Session getSshSession() throws OmpLibraryException {
            final Ssh2Session ssh = new Ssh2Session(ip, username, password);
            return ssh;
        }

        private String sendCommand(final Ssh2Session ssh, final String command) throws IOException {
            ssh.openSshShell();
            ssh.setRawOutput(false);
            ssh.setTimeout(20 * 1000);
            final String time = ssh.sendCommand(command);
            ssh.closeSshShell();
            return time;
        }
    }

}
