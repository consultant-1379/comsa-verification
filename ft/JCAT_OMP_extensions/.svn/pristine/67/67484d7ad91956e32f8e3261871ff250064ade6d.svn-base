package se.ericsson.jcat.omp.util;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.lang.reflect.InvocationTargetException;
import java.net.URL;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Calendar;
import java.util.Date;
import java.util.StringTokenizer;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.apache.commons.beanutils.MethodUtils;
import org.apache.commons.io.FileUtils;
import org.apache.commons.io.IOUtils;
import org.apache.log4j.Logger;

import se.ericsson.jcat.fw.utils.Ssh2Session;
import se.ericsson.jcat.omp.fw.OmpLibraryException;
import se.ericsson.jcat.omp.fw.OmpSut;
import se.ericsson.jcat.omp.library.SshLib;

public class Tools {

    private static Logger logger = Logger.getLogger(Tools.class);

    public static enum SutInfoTag {
        USER, PASSWORD, IP_SC1, IP_SC2, SUT_SIZE, VIP_TRAFFIC, VIP_OAM
    }

    public static int SSH_PORT = 22;

    /**
     * Get info from SUT
     * 
     * @param sut
     *            OmpSut
     * @param tag
     *            {@link SutInfoTag}
     * @return String
     */
    public static String getSutInfo(OmpSut sut, SutInfoTag tag) {
        switch (tag) {
            case USER:
                return sut.getConfigDataString("user");
            case PASSWORD:
                return sut.getConfigDataString("pwd");
            case IP_SC1:
                return sut.getConfigDataString("ipAddress.ctrl.ctrl1");
            case IP_SC2:
                return sut.getConfigDataString("ipAddress.ctrl.ctrl2");
            case SUT_SIZE:
                return sut.getConfigDataString("physical_size");
            case VIP_TRAFFIC:
                return sut.getConfigDataString("ipAddress.vip.vip_1");
            case VIP_OAM:
                return sut.getConfigDataString("ipAddress.vip.vip_2");
            default:
                return null;
        }
    }

    /**
     * Check if certain port is available on server
     * 
     * @param ip
     *            ip address
     * @param port
     *            port number to check
     * @return true if port is open
     */
    public static boolean isPortOpen(final String ip, final int port) {
        try {
            return runCommandLocal("netcat -w 20 -z " + ip + " " + port).returnValue == 0;
        } catch (IOException e) {
            logger.warn("Cannot execute command! " + e.getMessage());
            return false;
        } catch (InterruptedException e) {
            logger.error("Interrupted! " + e.getMessage());
            return false;
        }
    }

    /**
     * Get Ssh2Session connection. Try SC-2-1 first, if not available, try SC-2-2
     * 
     * @deprecated will be removed 2011-03-01
     * @param sut
     *            OmpSut
     * @return ssh2Session / null if connection is not available
     */
    @Deprecated
    public static Ssh2Session getSshSession(OmpSut sut) {

        final String username = getSutInfo(sut, SutInfoTag.USER);
        final String password = getSutInfo(sut, SutInfoTag.PASSWORD);
        final String ip1 = getSutInfo(sut, SutInfoTag.IP_SC1);
        final String ip2 = getSutInfo(sut, SutInfoTag.IP_SC2);

        Ssh2Session ssh = getSshSession(ip1, username, password);
        if (ssh == null) {
            // another try
            ssh = getSshSession(ip2, username, password);
            if (ssh == null) {
                logger.error("Cannot connect to server with both " + ip1 + " and " + ip2);
                return null;
            }
        }
        return ssh;
    }

    /**
     * Create a new SSH session inside an existing SSH session, using ssh command.
     * 
     * @param host
     *            Host name or IP address
     * @param user
     *            Username
     * @param pass
     *            Password
     * @param existingSshSession
     *            The existing SSH session
     * @return the result of hostname command on new host. Null if failed.
     */
    public static String sshBridge(String host, String user, String pass, Ssh2Session existingSshSession) {
        throw new RuntimeException("Method removed for now to keep BC");
        /*
         * try { existingSshSession.setRegexPrompt("Password:"); existingSshSession.sendCommand("ssh " + ((user == null
         * || user.equals("")) ? "" : user + "@") + host); existingSshSession.setRegexPrompt(null);
         * existingSshSession.sendCommand(pass); return existingSshSession.sendCommand("hostname"); } catch (IOException
         * e) { e.printStackTrace(); logger.error("Cannot create new SSH connection"); return null; }
         */
    }

    /**
     * Get Ssh2Session by ip, username and password
     * 
     * @param ip
     *            IP address
     * @param username
     *            username
     * @param password
     *            password
     * @return ssh2Session / null if connection is not available
     */
    public static Ssh2Session getSshSession(String ip, String username, String password) {
        Ssh2Session ssh = new Ssh2Session(ip, username, password);
        if (ssh.getSshClient() == null) {
            logger.error("Cannot connect to server: " + ip);
            return null;
        }
        ssh.setRawOutput(false);
        ssh.setDefaultTerm("vt100");
        ssh.openSshShell();
        return ssh;
    }

    /**
     * Check if certain port is open on SCs.
     * 
     * @param sut
     *            OmpSut
     * @param port
     *            port number to check
     * @param both
     *            if the port has to be open on both of the SCs
     * @return if (both==false), return true when the port is open at least on one SC. <br>
     *         if (both==true), return true when the port is open on both of the SCs.
     */
    public static boolean isPortOpenOnSc(OmpSut sut, int port, boolean both) {
        final String ip1 = getSutInfo(sut, SutInfoTag.IP_SC1);
        final String ip2 = getSutInfo(sut, SutInfoTag.IP_SC2);
        boolean sc1Open = isPortOpen(ip1, port);
        boolean sc2Open = isPortOpen(ip2, port);
        return both ? (sc1Open && sc2Open) : (sc1Open || sc2Open);
    }

    /**
     * Get SC where certain port is open. SC1 has higher priority
     * 
     * @param sut
     *            OmpSut
     * @param port
     *            port number to check
     * @return IP address to SC where port is open.
     */
    public static String getScByPort(OmpSut sut, int port) {
        final String ip1 = getIPFromAddress(getSutInfo(sut, SutInfoTag.IP_SC1));
        final String ip2 = getIPFromAddress(getSutInfo(sut, SutInfoTag.IP_SC2));
        if (isPortOpen(ip1, port)) {
            return ip1;
        }
        if (isPortOpen(ip2, port)) {
            return ip2;
        }
        return null;
    }

    /**
     * This method will check if the address is in the format IP:Port and return the IP part of the address Note, this
     * is not applicable for IPv6 address
     * 
     * @param address
     *            String in the format IP:Port or IP
     * @return String the IP part of the address
     */
    public static String getIPFromAddress(String address) {
        logger.debug("extracting the IP address from " + address);
        String ip = null;
        if ((address != null)) {
            if (address.contains(":")) {
                ip = address.split(":")[0];
            } else {
                ip = address;
            }
        }
        logger.debug("extracted IP is " + ip);
        return ip;
    }

    /**
     * This method will check if the address is in the format IP:Port and return the Port part of the address
     * 
     * @param address
     *            String in the format IP:Port or IP
     * @return String the Port part of the address
     */
    public static int getPortFromAddress(String address) {
        logger.debug("extracting the port number from " + address);
        int port = 0;
        if ((address != null) && (address.contains(":"))) {
            port = Integer.valueOf(address.split(":")[1]);
        }
        logger.debug("extracted port is " + port);
        return port;
    }

    /**
     * Wait and check if certain port is open on the server during period
     * 
     * @param ip
     *            IP address to server
     * @param port
     *            port number to check
     * @param retries
     *            number of retry times
     * @param timeInterval
     *            time interval between checks
     * @return true if port opened on server during period
     * @throws OmpLibraryException
     */
    public static boolean waitForPortOpen(final String ip, final int port, int retries, final int timeInterval)
            throws OmpLibraryException {
        return waitUntilTrue(new Tools(), "isPortOpen", new Object[] { ip, port }, timeInterval,
                             timeInterval * retries, false);
    }

    /**
     * Wait for a method until it returns true. Only allow methods with Simple Type Parameters. e.x. allow m(int i) but
     * NOT m(Integer i). However, for types with no corresponding simple type available, complex type is also allowed.
     * e.x. m(Hashmap h) is allowed. Exceptions from method will be ignored (does not interrupt the waiting)
     * 
     * @param obj
     *            The Object where the method relies on.
     * @param method
     *            Method name
     * @param args
     *            Arguments. An Object array. If the method does not need any argument, please send in an empty Object
     *            array or null
     * @param checkInterval
     *            Time interval
     * @param timeoutSecond
     *            Timeout in second
     * @return true if the method in argument returns true before timeout.
     * @throws OmpLibraryException
     */
    public static boolean waitUntilTrue(Object obj, String method, Object[] args, int checkInterval, int timeoutSecond) {
        try {
            return waitUntilTrue(obj, method, args, checkInterval, timeoutSecond, false);
        } catch (OmpLibraryException e) {
            throw new RuntimeException("Got exception when stopOnFailure is false... Should not happen! "
                    + e.getMessage());
        }
    }

    /**
     * Wait for a method until it returns true. Only allow methods with Simple Type Parameters. e.x. allow m(int i) but
     * NOT m(Integer i). However, for types with no corresponding simple type available, complex type is also allowed.
     * e.x. m(Hashmap h) is allowed.
     * 
     * @param obj
     *            The Object where the method relies on.
     * @param method
     *            Method name
     * @param args
     *            Arguments. An Object array. If the method does not need any argument, please send in an empty Object
     *            array or null
     * @param checkInterval
     *            Time interval
     * @param timeoutSecond
     *            Timeout in second
     * @param stopOnFailure
     *            Stop waiting when receiving exceptions from method.
     * @return true if the method in argument returns true before timeout.
     * @throws OmpLibraryException
     */
    public static boolean waitUntilTrue(final Object obj, final String method, final Object[] args, int checkInterval,
            int timeoutSecond, final boolean stopOnFailure) throws OmpLibraryException {
        return waitUntilTrue(obj, method, args, checkInterval, timeoutSecond, stopOnFailure, false);
    }

    /**
     * Wait for a method until it returns true. Only allow methods with Simple Type Parameters. e.x. allow m(int i) but
     * NOT m(Integer i). However, for types with no corresponding simple type available, complex type is also allowed.
     * e.x. m(Hashmap h) is allowed.
     * 
     * Due to artf270550: If InvocationTargetException occur and stopOnFailure is false, do a printout don't throw
     * exception
     * 
     * @param obj
     *            The Object where the method relies on.
     * @param method
     *            Method name
     * @param args
     *            Arguments. An Object array. If the method does not need any argument, please send in an empty Object
     *            array or null
     * @param checkInterval
     *            Time interval
     * @param timeoutSecond
     *            Timeout in second
     * @param stopOnFailure
     *            Stop waiting when receiving exceptions from method.
     * @param reduceChecks
     *            Reduce number of checks
     * @return true if the method in argument returns true before timeout.
     * @throws OmpLibraryException
     */
    public static boolean waitUntilTrue(final Object obj, final String method, final Object[] args, int checkInterval,
            int timeoutSecond, final boolean stopOnFailure, boolean reduceChecks) throws OmpLibraryException {
        return waitUntilTrue(new Waitable() {
            public String getDescription() {
                return "Waiting for method: " + method + " in class " + obj.getClass() + " to return true";
            }

            public boolean getCheckResult() throws WaitTerminationException, WaitCriticalException {
                try {
                    return (Boolean) MethodUtils.invokeMethod(obj, method, args);
                } catch (NoSuchMethodException e) {
                    throw new RuntimeException("Cannot find matching method in " + obj.getClass() + ". "
                            + Arrays.toString(args), e);
                } catch (IllegalAccessException e) {
                    throw new RuntimeException("Cannot invoke method. Code error! ", e);
                } catch (ClassCastException e) {
                    throw new RuntimeException("Cannot invoke method. Code error! Method does not return boolean! ", e);
                } catch (InvocationTargetException e) {
                    logger.warn("Caught exception from method! " + e.getTargetException());
                    logger.debug("Exception", e);
                    if (stopOnFailure) {
                        throw new WaitCriticalException("Got exception from method", e);
                    } else {
                        logger.warn("Exception ignored");
                        return false;
                        // artf270550 : ROB_PROCESS_005: TC timeout fails due to omp.util.Tools exception
                        // throw new WaitTerminationException("Got exception from method", e);
                    }
                }
            }
        }, checkInterval, (float) timeoutSecond, reduceChecks);
    }

    /**
     * Wait until true using new waitable interface
     * 
     * @param w
     * @param checkInterval
     * @param timeoutSecond
     * @param reduceChecks
     * @return
     * @throws OmpLibraryException
     */
    public static boolean waitUntilTrue(Waitable w, int checkInterval, float timeoutSecond, boolean reduceChecks)
            throws OmpLibraryException {
        try {
            logger.info(w.getDescription());
            // Calculate end time
            long endTime = Calendar.getInstance().getTimeInMillis() + (long) (timeoutSecond * 1000);
            // Invoke method and check
            while (!w.getCheckResult()) {
                long currentTime = Calendar.getInstance().getTimeInMillis();
                if (currentTime > endTime) {
                    logger.warn("TIMEOUT: " + w.getDescription());
                    return false;
                }
                // Below is to reduce the number of checks during waiting
                int timeLeft = (int) ((endTime - currentTime) / 1000);
                int sleepTime = timeLeft / 6;
                if (!reduceChecks || sleepTime < checkInterval) {
                    sleepTime = checkInterval;
                }
                logger.info("Timeout in " + timeLeft + " seconds. Wait for " + sleepTime + " sec and try again");
                Thread.sleep(sleepTime * 1000);
            }
            // If while loop can be terminated by itself, return true
            return true;
        } catch (InterruptedException e) {
            logger.error("Sleep has been interrupted! " + e.getMessage());
            return false;
        } catch (WaitTerminationException e) {
            logger.info("Wait terminated. " + e.getMessage());
            return false;
        } catch (WaitCriticalException e) {
            logger.error("Wait terminated by critical exception.");
            throw new OmpLibraryException("Wait terminated by critical exception.", e);
        }
    }

    /**
     * Execute command locally, via Runtime.exec() method
     * 
     * @param command
     *            Command to be executed
     * @param dir
     *            Directory where the command should be executed in
     * @return CommandExecutionResult
     * @throws IOException
     * @throws InterruptedException
     */
    public static CommandExecutionResult runCommandLocal(String command, String dir) throws IOException,
            InterruptedException {
        return runCommandLocal(command, dir, -1);// Wait forever
    }

    /**
     * Execute command locally, via Runtime.exec() method
     * 
     * @param command
     *            Command to be executed
     * @param timeoutInMilliseconds
     *            Max waiting time until it aborts.
     * @return CommandExecutionResult
     * @throws IOException
     * @throws InterruptedException
     */
    public static CommandExecutionResult runCommandLocal(String command, int timeoutInMilliseconds) throws IOException,
            InterruptedException {
        return runCommandLocal(command, null, timeoutInMilliseconds);
    }

    /**
     * Execute command locally, via Runtime.exec() method
     * 
     * @param command
     *            Command to be executed
     * @param dir
     *            Directory where the command should be executed in
     * @param timeoutInMilliseconds
     *            Max waiting time until it aborts.
     * @return CommandExecutionResult
     * @throws IOException
     * @throws InterruptedException
     */
    public static CommandExecutionResult runCommandLocal(String command, String dir, int timeoutInMilliseconds)
            throws IOException, InterruptedException {
        String[] commands = { "/bin/sh", "-c", command };
        Process p = null;
        if (dir == null) {
            p = Runtime.getRuntime().exec(commands);
        } else {
            p = Runtime.getRuntime().exec(commands, new String[] {}, new File(dir));
        }
        String[] output = readTextFromStream(p, timeoutInMilliseconds);
        if (!output[1].equals("")) {
            output[1] = " (Error : " + output[1] + ")";
        }
        return new CommandExecutionResult(p.exitValue(), output[0] + output[1]);
    }

    /**
     * Read text from InputStream
     * 
     * @param is
     *            InputStream
     * @return text
     * @throws IOException
     */
    public static String[] readTextFromStream(Process p) throws IOException {
        return readTextFromStream(p, -1);
    }

    /**
     * Read text from InputStream
     * 
     * @param is
     *            InputStream
     * @param timeoutInMilliseconds
     *            . Max waiting time until it aborts.
     * @return text
     * @throws IOException
     */
    public static String[] readTextFromStream(Process p, int timeoutInMilliseconds) throws IOException {
        BufferedReader br_in = new BufferedReader(new InputStreamReader(p.getInputStream()));
        BufferedReader br_err = new BufferedReader(new InputStreamReader(p.getErrorStream()));

        long endTime = System.currentTimeMillis() + timeoutInMilliseconds;
        StringBuilder out = new StringBuilder();
        StringBuilder err = new StringBuilder();

        while (isProcessRunning(p)) {
            if (timeoutInMilliseconds >= 0 && System.currentTimeMillis() > endTime) {
                logger.error("Timeout occured after " + timeoutInMilliseconds + " milliseconds.");
                try {
                    p.destroy();
                    // need to wait a bit after destroy, we assume the destroy will always be successful...
                    p.waitFor();
                } catch (Exception e) {
                    e.printStackTrace();
                }
                break;
            }
            try {
                Thread.sleep(100);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            out.append(readNewText(br_in));
            err.append(readNewText(br_err));
        }
        out.append(readNewText(br_in));
        err.append(readNewText(br_err));
        return new String[] { out.toString(), err.toString() };
    }

    /**
     * This method does the same logic as unix grep command when matching a local file against regular expression
     * 
     * @param filename
     *            - String - filename of the local file
     * @param reg
     *            - String - java regular expression, to be matched against each line in the specified file
     * @return String - all matched lines seperated by "\n"
     * @throws OmpLibraryException
     */
    public static String localFileGrep(String filename, String reg) throws OmpLibraryException {
        BufferedReader reader = null;
        StringBuilder result = new StringBuilder();
        try {
            reader = new BufferedReader(new FileReader(filename));
            Pattern p = Pattern.compile(reg);
            String line = null;
            while ((line = reader.readLine()) != null) {
                Matcher m = p.matcher(line);
                if (m.matches()) {
                    result.append(line).append("\n");
                }
            }
        } catch (FileNotFoundException e) {
            throw new OmpLibraryException(e.getMessage());
        } catch (IOException e) {
            throw new OmpLibraryException(e.getMessage());
        } finally {
            if (reader != null) {
                try {
                    reader.close();
                } catch (IOException e) {
                    throw new OmpLibraryException(e.getMessage());
                }
            }
        }

        return result.toString();
    }

    private static String readNewText(BufferedReader r) {
        try {
            StringBuilder out = new StringBuilder();
            while (r.ready()) {
                char[] buf = new char[10000];
                int count = r.read(buf);
                String str = new String(buf, 0, count);
                logger.debug("Read : " + str);
                out.append(str);
            }
            return out.toString();
        } catch (IOException e) {
            e.printStackTrace();
            return "";
        }
    }

    private static boolean isProcessRunning(Process p) {
        try {
            p.exitValue();
            return false;
        } catch (IllegalThreadStateException e) {
            return true;
        }
    }

    /**
     * Execute command locally, via Runtime.exec() method
     * 
     * @param command
     *            Command to be executed
     * @return CommandExecutionResult
     * @throws IOException
     * @throws InterruptedException
     */
    public static CommandExecutionResult runCommandLocal(String command) throws IOException, InterruptedException {
        return runCommandLocal(command, null);
    }

    /**
     * Execute command remotely, via ssh
     * 
     * @param ssh
     *            sshLib instance
     * @param command
     *            Command to be executed
     * @param subrack
     *            subrack
     * @param slot
     *            slot
     * @return CommandExecutionResult
     * @throws OmpLibraryException
     */
    public static CommandExecutionResult runCommandRemote(SshLib ssh, String command, int subrack, int slot)
            throws OmpLibraryException {
        String extendedCommand = command + " ; echo $?";
        String output = "";
        if (subrack == -10 || slot == -10) {
            output = ssh.sendCommand(extendedCommand, true);
        } else {
            output = ssh.sendCommand(extendedCommand, subrack, slot, true);
        }
        String[] parsedOutput = parseOutput(output);
        int r = 1;
        try {
            r = Integer.parseInt(parsedOutput[0]);
        } catch (NumberFormatException e) {
            throw new OmpLibraryException("Cannot get exitValue from: " + parsedOutput[0]);
        }
        return new CommandExecutionResult(r, parsedOutput[1]);
    }

    private static String[] parseOutput(String text) {
        String[] outputArray = text.split("\\n");
        String errorCode = outputArray[outputArray.length - 1];
        String output = text.substring(0, text.length() - errorCode.length());
        if (output.endsWith("\n")) {
            output = output.substring(0, output.length() - "\n".length());
        }
        return new String[] { errorCode, output };
    }

    /**
     * Execute command remotely, via ssh.The method will decide where the command should be sent to (SC1 or SC2), basing
     * on the connectivity of SSH port.
     * 
     * @param ssh
     *            sshLib instance
     * @param command
     *            Command to be executed
     * @return CommandExecutionResult
     * @throws OmpLibraryException
     */
    public static CommandExecutionResult runCommandRemote(SshLib ssh, String command) throws OmpLibraryException {
        if (!ssh.setConfig(ssh.getUseVipOam())) {
            throw new OmpLibraryException("Cannot send command! None of the SCs is available");
        }
        return runCommandRemote(ssh, command, -10, -10);
    }

    /**
     * Get a String representing current time.
     * 
     * @param format
     *            Format string. e.x. yyyyddMM-HHmmss
     * @return
     */
    public static String getCurrentTimeString(String format) {
        SimpleDateFormat dateFormat = new SimpleDateFormat(format);
        return dateFormat.format(new Date());
    }

    /**
     * Get a String representing current time.
     * 
     * Format: yyyyddMM-HHmmss
     * 
     * @return
     */
    public static String getCurrentTimeString() {
        return getCurrentTimeString("yyyyddMM-HHmmss");
    }

    public static class WaitInterruptedException extends Exception {
        private static final long serialVersionUID = 1L;

        public WaitInterruptedException(String m) {
            super(m);
        }
    }

    /**
     * Extract file from resource to temp location. The source file can be standard-alone or inside a jar.
     * 
     * <B>RUNTIME EXCEPTION WILL BE SENT IF THE OPERATION FAILED DUE TO ANY REASON! </B>
     * 
     * @param sourceFile
     *            The file to extracted. If the file should be on the root of the classloader path, DO NOT write '/' at
     *            the beginning. e.g. "file.ext" or "python/code.ext" are valid, "/file.ext" is NOT.
     * @param c
     *            The class where to get the classloader
     * @param newFile
     *            The new temp file, which is a copy of the source
     * @param runnable
     *            runnable is this new file executable
     */
    public static void extractResourceFile(String sourceFile, Class<?> c, File newFile, boolean runnable) {
        URL sourceFileUrl = getResourceFileUrl(sourceFile, c);
        try {
            FileUtils.copyURLToFile(sourceFileUrl, newFile);
            newFile.setExecutable(runnable);
            newFile.deleteOnExit();
        } catch (IOException e) {
            throw new RuntimeException("File " + sourceFile + " can not be extracted from ClassLoader of " + c, e);
        }
    }

    private static URL getResourceFileUrl(String sourceFile, Class<?> c) {
        URL sourceFileUrl = c.getClassLoader().getResource(sourceFile);
        if (sourceFileUrl == null) {
            throw new RuntimeException("File " + sourceFile + " can not be found via ClassLoader of " + c);
        }
        return sourceFileUrl;
    }

    /**
     * Extract resource file and read its content
     * 
     * @param sourceFile
     * @param c
     *            The class where to get the classloader
     * @return the content of the resource file
     */
    public static String extractResourceFileAndReadContent(String sourceFile, Class<?> c) {
        URL sourceFileUrl = getResourceFileUrl(sourceFile, c);
        try {
            return IOUtils.toString(sourceFileUrl);
        } catch (IOException e) {
            throw new RuntimeException("File " + sourceFile + " can not be extracted from ClassLoader of " + c, e);
        }
    }

    /**
     * Extract resource file and read its content
     * 
     * @param sourceFile
     * @param c
     *            The class where to get the classloader
     * @param tmpFile
     *            tmp file
     * @return the content of the resource file
     */
    public static String extractResourceFileAndReadContent(String sourceFile, Class<?> c, File tmpFile) {
        return extractResourceFileAndReadContent(sourceFile, c);
    }

    /**
     * Read a file and return its content as a string
     * 
     * @param file
     * @return
     * @throws IOException
     */
    public static String readFileToString(File file) throws IOException {
        return FileUtils.readFileToString(file);
    }

    /**
     * Force delete a file or directory
     * 
     * @param fileOrDir
     * @return
     */
    public static boolean deleteQuietly(File fileOrDir) {
        return FileUtils.deleteQuietly(fileOrDir);
    }

    /**
     * Force delete a file or directory when JVM exit
     * 
     * @param fileOrDir
     * @return
     */
    public static void forceDeleteOnExit(File fileOrDir) {
        try {
            FileUtils.forceDeleteOnExit(fileOrDir);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    /**
     * Get relative path to the base dir
     * 
     * @param from
     *            the base dir / file
     * @param path
     * @return
     */
    public static String getRelativePath(String from, String to) {
        return getRelativePath(new File(from), new File(to));
    }

    /**
     * Get relative path to the base dir
     * 
     * @param from
     *            the base dir / file
     * @param to
     * @return
     */
    public static String getRelativePath(File from, File to) {
        return getRelativePath(from, to, File.separatorChar);
    }

    /**
     * Get relative path to the base dir
     * 
     * @param from
     *            the base dir / file
     * @param to
     * @param separatorChar
     * @return
     */
    public static String getRelativePath(File from, File to, char separatorChar) {
        String fromPath = from.getAbsolutePath();
        String toPath = to.getAbsolutePath();
        boolean isDirectory = from.isDirectory();
        return relativePath(fromPath, toPath, isDirectory, separatorChar);
    }

    /**
     * Get relative path to the base dir
     * 
     * @param fromPath
     *            the base dir / file
     * @param toPath
     * @param fromIsDirectory
     * @param separatorChar
     * @return
     */
    public static String relativePath(String fromPath, String toPath, boolean fromIsDirectory, char separatorChar) {
        ArrayList<String> fromElements = splitPath(fromPath);
        ArrayList<String> toElements = splitPath(toPath);
        while (!fromElements.isEmpty() && !toElements.isEmpty()) {
            if (!(fromElements.get(0).equals(toElements.get(0)))) {
                break;
            }
            fromElements.remove(0);
            toElements.remove(0);
        }

        StringBuffer result = new StringBuffer();
        for (int i = 0; i < fromElements.size() - (fromIsDirectory ? 0 : 1); i++) {
            result.append("..");
            result.append(separatorChar);
        }
        for (String s : toElements) {
            result.append(s);
            result.append(separatorChar);
        }
        if (result.length() == 0) {
            // means from and to are the same
            // return . if to is a dir, or file name if to is a file
            File toFile = (new File(toPath));
            return toFile.isDirectory() ? "." : (new File(toPath)).getName();
        } else {
            return result.substring(0, result.length() - 1);
        }
    }

    private static ArrayList<String> splitPath(String path) {
        ArrayList<String> pathElements = new ArrayList<String>();
        for (StringTokenizer st = new StringTokenizer(path, File.separator); st.hasMoreTokens();) {
            String token = st.nextToken();
            if (token.equals(".")) {
                // do nothing
            } else if (token.equals("..")) {
                if (!pathElements.isEmpty()) {
                    pathElements.remove(pathElements.size() - 1);
                }
            } else {
                pathElements.add(token);
            }
        }
        return pathElements;
    }

    public static String getRelativeMacAddress(String firstMacAddress, long offset) {

        String relativeMacAddress = "";
        long longMacAddress = Long.parseLong((firstMacAddress.replace(":", "").toLowerCase()), 16);
        String hexSumValue = Long.toHexString(longMacAddress + offset);
        int hexSumValueSize = hexSumValue.length();
        if (hexSumValueSize < 12) {
            String hexZeros = "000000000000";
            hexSumValue = (hexZeros.substring(0, 12 - hexSumValueSize)) + hexSumValue;
        } else if (hexSumValueSize > 12) {
            hexSumValue = hexSumValue.substring(hexSumValueSize - 12);
        }
        for (int i = 0; i < 10; i = i + 2) {
            relativeMacAddress = relativeMacAddress + hexSumValue.substring(i, i + 2) + ":";
        }
        relativeMacAddress = relativeMacAddress + hexSumValue.substring(10);
        return relativeMacAddress;
    }
}
