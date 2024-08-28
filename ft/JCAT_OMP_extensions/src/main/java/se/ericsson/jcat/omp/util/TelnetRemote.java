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
package se.ericsson.jcat.omp.util;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.Socket;
import java.net.SocketException;
import java.net.SocketTimeoutException;
import java.net.UnknownHostException;

import org.apache.log4j.Logger;

/**
 * Class for sending telnet commands.
 * 
 * @author ejieyuu
 * 
 */
public class TelnetRemote {
    private static Logger logger = Logger.getLogger(TelnetRemote.class);

    private final String address;
    private final int port;
    private final String prompt;
    private Socket sock = null;
    private BufferedReader in = null;
    private BufferedWriter out = null;
    private boolean started = false;
    private int delay = 200;

    public TelnetRemote(String address, int port, String prompt) {
        this.address = address;
        this.port = port;
        this.prompt = prompt;
        this.started = false;
    }

    public int getDelay() {
        return delay;
    }

    public void setDelay(int delayMilisec) {
        logger.info("Set command delay to " + delayMilisec);
        this.delay = delayMilisec;
    }

    public void startSession(int timeout) {
        try {
            sock = new Socket(address, port);
            sock.setSoTimeout(timeout);
            in = new BufferedReader(
                    new InputStreamReader(sock.getInputStream()));
            out = new BufferedWriter(new OutputStreamWriter(
                    sock.getOutputStream()));
            started = true;
        } catch (SocketException e) {
            logger.error("Error starting Telnet session! " + e.getMessage());
            e.printStackTrace();
            logger.error(e);
        } catch (UnknownHostException e) {
            logger.error("Error starting Telnet session! " + e.getMessage());
            e.printStackTrace();
            logger.error(e);
        } catch (IOException e) {
            logger.error("Error starting Telnet session! " + e.getMessage());
            e.printStackTrace();
            logger.error(e);
        }
    }

    public void endSession() {
        try {
            out.close();
            in.close();
            sock.close();
            sock = null;
            out = null;
            in = null;
        } catch (IOException e) {
            logger.error("Error closing Telnet session! " + e.getMessage());
            e.printStackTrace();
            logger.error(e);
        }
        started = false;
    }

    /**
     * Send command.
     * 
     * @param command
     * @param lastLineMatchPattern
     *            Regexp matching the last expected line.
     * @return Return values of the command.
     * @throws TelnetErrorException
     */
    public String executeCommand(String command) throws TelnetErrorException {
        if (!started) {
            throw new TelnetErrorException("Session must be started first!");
        }
        try {
            // Read initial prompt, if any
            this.doRecv(in);
            // Send command
            doSend(out, command);
            // Read reply
            return this.doRecv(in);
        } catch (Exception e) {
            logger.error("Error sending command! " + e.getMessage());
            e.printStackTrace();
            throw new TelnetErrorException(e.getMessage());
        }
    }

    private void doSend(BufferedWriter out, String command) throws IOException,
            InterruptedException {
        logger.info("Send: " + command);
        // "\r\n\" needed for telnet communication
        out.write(command + "\r\n");
        out.flush();
        Thread.sleep(delay);
    }

    private String doRecv(BufferedReader in) throws IOException,
            SocketTimeoutException, InterruptedException {
        String line = "";
        Thread.sleep(delay);
        if (!in.ready()) {
            return line;
        }

        while (true) {
            char[] buf = new char[1000];
            in.read(buf);
            logger.debug("Read : " + new String(buf));
            line = line + (new String(buf).trim());
            if (line.endsWith(prompt) && !in.ready()) {
                break;
            }
        }
        if (line.endsWith(prompt)) {
            // Remove last prompt
            line = line.substring(0, line.lastIndexOf(prompt));
            if (line.endsWith("\n")) {
                // Remove last line if it only contains prompt
                line = line.substring(0, line.lastIndexOf("\n"));
            }
        }
        logger.info("Reply: " + line);
        return line;
    }
}
