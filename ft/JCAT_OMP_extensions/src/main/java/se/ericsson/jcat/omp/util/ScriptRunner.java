/*
 * Created on 2006-mar-20
 *
 */
package se.ericsson.jcat.omp.util;

import org.apache.log4j.Logger;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

import java.util.Arrays;


/**
 * This runner is used to run a script based on the java Runtime.exec() method. Any exceptions
 * thrown by the framework is reported as errors. If the script returns another value than the
 * expected value, it is reported as a failure.
 * @author xtsrrpn
 * @reviewed erafope 2008-apr-23
 */
public class ScriptRunner implements Runner {
    private static Logger logger = Logger.getLogger(ScriptRunner.class);
    private String[] cmdarray;
    private boolean hasFailures;
    private boolean hasError;
    private String failureString;
    private byte exitValue;

    ScriptRunner(String[] cmdArray) {
        this.cmdarray = cmdArray;
        exitValue = -1;
    }

    public void init() {
        if (!System.getProperty("os.name").endsWith("Linux")) {
            throw new RuntimeException(
                "This test case runs a script that requires the Linux OS. You are running at: " +
                System.getProperty("os.name"));
        } //Note: Could be extended in future to allow other OS than linux.
    }

    public boolean hasFailures() {
        return hasFailures;
    }

    public boolean hasError() {
        return hasError;
    }

    public String getFailures() {
        return failureString;
    }

    protected void setExitValue(byte value) {
        exitValue = value;
    }

    public byte getExitValue() {
        return exitValue;
    }

    /**
     * Returns the script name as scenario name.
     */
    public String getScenarioFilename() {
        return cmdarray[0];
    }

    public void run() {
        logger.info("Going to run script " + Arrays.toString(cmdarray));

        Runtime rtime = Runtime.getRuntime();
        Process child = null;
        byte value = -1;

        try {
            child = rtime.exec(cmdarray);

            InputStreamReader isr = new InputStreamReader(child.getInputStream());
            BufferedReader br = new BufferedReader(isr);
            String line = null;

            while ((line = br.readLine()) != null) {
                logger.info(line);
            }

            value = (byte) child.waitFor();
            setExitValue(value);

            if (value != 0) {
                byte[] b = new byte[child.getErrorStream().available()];
                child.getErrorStream().read(b);

                String errorMessage = new String(b);
                logger.info(errorMessage);
                logger.info("Script " + Arrays.toString(cmdarray) +
                    " failed. Value " + value + " was returned.");
                hasFailures = true;
            } else {
                logger.info("Script " + Arrays.toString(cmdarray) +
                    " successfully executed with exit value " + value);
            }
        } catch (InterruptedException e) {
            logger.info("InterruptedException " + e.getMessage());
        } catch (IOException e) {
            logger.info(e.getMessage());
            hasError = true;
            failureString = "IOException caught: " + e.getMessage();
        }
    }
}
