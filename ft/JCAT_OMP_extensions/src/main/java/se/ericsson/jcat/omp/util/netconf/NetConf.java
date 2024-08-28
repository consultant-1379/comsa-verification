package se.ericsson.jcat.omp.util.netconf;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.Reader;
import java.io.StringReader;
import java.util.Stack;

import org.apache.log4j.Level;
import org.apache.log4j.Logger;
import org.apache.xmlbeans.XmlAnySimpleType;
import org.apache.xmlbeans.XmlException;
import org.apache.xmlbeans.XmlObject;

import se.ericsson.jcat.fw.utils.Ssh2Session;
import se.ericsson.jcat.omp.fw.OmpLibraryException;
import se.ericsson.jcat.omp.fw.OmpSut;
import se.ericsson.jcat.omp.util.LogWriterHelper;
import x0.ietfParamsXmlNsNetconfBase1.CandidateDocument;
import x0.ietfParamsXmlNsNetconfBase1.CloseSessionDocument;
import x0.ietfParamsXmlNsNetconfBase1.CommitDocument;
import x0.ietfParamsXmlNsNetconfBase1.ConfigInlineType;
import x0.ietfParamsXmlNsNetconfBase1.CopyConfigDocument;
import x0.ietfParamsXmlNsNetconfBase1.CopyConfigType;
import x0.ietfParamsXmlNsNetconfBase1.DefaultOperationType;
import x0.ietfParamsXmlNsNetconfBase1.DeleteConfigDocument;
import x0.ietfParamsXmlNsNetconfBase1.DeleteConfigType;
import x0.ietfParamsXmlNsNetconfBase1.DiscardChangesDocument;
import x0.ietfParamsXmlNsNetconfBase1.EditConfigDocument;
import x0.ietfParamsXmlNsNetconfBase1.EditConfigType;
import x0.ietfParamsXmlNsNetconfBase1.ErrorOptionType;
import x0.ietfParamsXmlNsNetconfBase1.FilterInlineType;
import x0.ietfParamsXmlNsNetconfBase1.FilterType;
import x0.ietfParamsXmlNsNetconfBase1.GetConfigDocument;
import x0.ietfParamsXmlNsNetconfBase1.GetConfigType;
import x0.ietfParamsXmlNsNetconfBase1.GetDocument;
import x0.ietfParamsXmlNsNetconfBase1.GetType;
import x0.ietfParamsXmlNsNetconfBase1.HelloDocument;
import x0.ietfParamsXmlNsNetconfBase1.KillSessionDocument;
import x0.ietfParamsXmlNsNetconfBase1.LockDocument;
import x0.ietfParamsXmlNsNetconfBase1.RpcDocument;
import x0.ietfParamsXmlNsNetconfBase1.RpcErrorType;
import x0.ietfParamsXmlNsNetconfBase1.RpcOperationSourceType;
import x0.ietfParamsXmlNsNetconfBase1.RpcOperationTargetType;
import x0.ietfParamsXmlNsNetconfBase1.RpcReplyDocument;
import x0.ietfParamsXmlNsNetconfBase1.RpcType;
import x0.ietfParamsXmlNsNetconfBase1.RunningDocument;
import x0.ietfParamsXmlNsNetconfBase1.TestOptionType;
import x0.ietfParamsXmlNsNetconfBase1.UnlockDocument;
import x0.ietfParamsXmlNsNetconfBase1.ValidateDocument;

import com.trilead.ssh2.Connection;
import com.trilead.ssh2.Session;
import com.trilead.ssh2.StreamGobbler;

/*
 * TODO A server receiving a <session-id> element MUST NOT continue the NETCONF session. Similarly, a client that does
 * not receive a <session-id> element in the server's <hello> message MUST NOT continue the NETCONF session. In both
 * cases, the underlying transport should be closed.
 */

public class NetConf {
    private static Logger logger = Logger.getLogger("NetConf");

    private OmpSut sut;

    private InputStream stdout;
    private Connection conn = null;
    private Session sess = null;
    private long sessionID = 0;
    private int messageCounter = 1;

    private String connectedHost = null;
    private int port;

    private ServerCapabilities serverCapabilities = null;

    private DefaultOperationType.Enum defaultOperation = null;
    private ErrorOptionType.Enum errorOption = ErrorOptionType.ROLLBACK_ON_ERROR;
    private TestOptionType.Enum testOption = TestOptionType.TEST_THEN_SET;

    private static final long timeoutForNetconfReply = 10;

    // Netconf capabilities
    /** The writable-running capability */
    public static final String WRITABLE_RUNNING = "urn:ietf:params:netconf:capability:writable-running:1.0";
    /** The candidate capability */
    public static final String CANDIDATE = "urn:ietf:params:netconf:capability:candidate:1.0";
    /** The confirmed-commit capability */
    public static final String CONFIRMED_COMMIT = "urn:ietf:params:netconf:capability:confirmed-commit:1.0";
    /** The rollback-on-error capability */
    public static final String ROLLBACK_ON_ERROR = "urn:ietf:params:netconf:capability:rollback-on-error:1.0";
    /** The validate capability */
    public static final String VALIDATE = "urn:ietf:params:netconf:capability:validate:1.0";
    /** The startup capability */
    public static final String STARTUP = "urn:ietf:params:netconf:capability:startup:1.0";
    /** The url capability */
    public static final String URL = "urn:ietf:params:netconf:capability:url:1.0";
    /** The xpath capability */
    public static final String XPATH = "urn:ietf:params:netconf:capability:xpath:1.0";

    /**
     * The string that will be added at the end of all netcon messages.
     */
    public static final String NETCONF_MESSAGE_END = "\n]]>]]>";

    private boolean useRawMessage = false;
    private Level rawLogLevel = Level.DEBUG;

    /**
     * Creates a new instance, use startNetConfSession to get a connection to a netconf server.
     */
    public NetConf(OmpSut sut, int port) {
        serverCapabilities = new ServerCapabilities();
        this.sut = sut;
        this.port = port;
    }

    public void setUseRawMessage(boolean useRawMessage) {
        this.useRawMessage = useRawMessage;
    }

    public void setRawMsgLogLevel(Level level) {
        rawLogLevel = level;
    }

    /**
     * Starts a netconf session using values for user, password and port from properties.
     * 
     * @param hostname
     *            ip address of netconf server
     * @return a Session object that holds the connection can be used to get "raw" access to the input and output
     *         streams
     */
    public Session startNetConfSession() {

        String userid = sut.getConfigDataString("user");
        String password = sut.getConfigDataString("pwd");
        String hostname = sut.getConfigDataString("ipAddress.vip.vip_2");

        if (userid == null || password == null || port == 0 || hostname == null) {
            logger.error("Unable to obtain property(ies) for netconf");
            logger.error("user = " + userid);
            logger.error("pwd = " + password);
            logger.error("ipAddress.vip.vip_2 = " + hostname);
            return null;
        }

        startNetConfSession(hostname, port, userid, password);
        return sess;
    }

    public long getSessionID() {
        return sessionID;
    }

    /**
     * Method used to get a netconf session, this method must be called before anything else can be don or sent via the
     * netconf channnel, since there won't be a connection until after the call of this method.
     * 
     * @param hostname
     *            ip address of netconf server
     * @param netConfPort
     *            port to connect to
     * @param username
     *            user on netconf server
     * @param password
     *            password for user on netconf server
     * @return a HelloDocument object that is the answer from the server when starting a netconf session
     */
    public HelloDocument startNetConfSession(String hostname, int netConfPort, String username, String password) {

        sess = null;
        sessionID = 0;

        logger.info("Starting netconf over SSH connection on " + hostname + ", port " + netConfPort);
        try {

            Ssh2Session ssh = new Ssh2Session(hostname, netConfPort, username, password);

            conn = ssh.getSshClient();
            if (conn == null)
                return null;

            /* Create a session */

            sess = conn.openSession();
            logger.info("Session opened");

            stdout = new StreamGobbler(sess.getStdout());
            InputStream stderr = new StreamGobbler(sess.getStderr());

            BufferedReader br = new BufferedReader(new InputStreamReader(stdout));
            BufferedReader stderrReader = new BufferedReader(new InputStreamReader(stderr));

            sess.startSubSystem("netconf");

            logger.info("Subsystem \"netconf\" started");

            String helloMessage = receiveNetconfMessage(br);

            this.sendHello();

            logger.debug("after sendHello");

            HelloDocument hello = null;
            try {
                hello = parseHelloDocument(helloMessage);
                String[] capabilities = hello.getHello().getCapabilities().getCapabilityArray();
                for (String capability : capabilities) {

                    serverCapabilities.addCapability(capability);
                }
                sessionID = hello.getHello().getSessionId();

                // host is connected save hostname
                connectedHost = hostname;

                if (stderr.available() > 0) {
                    logger.info("Got indication of data on stderr:");

                    while (true) {
                        String line = stderrReader.readLine();
                        if (line == null) {
                            break;
                        }
                        printNiceLog(Level.WARN, "NETCONF MSG SENT:", new String(line));
                    }
                    logger.info("End of stderr \n---------------------------------------");
                }
            } catch (Exception e) {
                logger.warn("Did not get a valid hello from server");
            } finally {
                if (stderrReader != null) {
                    try {
                        stderrReader.close();
                    } catch (IOException e) {
                        logger.warn("Could not close error input stream", e);
                    }
                }
            }
            return hello;

        } catch (IOException e) {
            e.printStackTrace();
            if (hostname == null) {
                logger.info("Could not connect to " + hostname + " , check host name");
            }
            logger.info("Could not connect to " + hostname + " on port: " + netConfPort);
            logger.info(e);
            return null;
        }
    }

    private static String readBufferLine(BufferedReader br) throws IOException {
        StringBuilder line = new StringBuilder(1024);
        int element;
        int charCount = 0;
        while (br.ready() && (element = br.read()) != -1) {
            char character = (char) element;
            logger.trace("Got:" + character);
            charCount++;
            line.append(character);
            if (character == '\n' || character == '\r')
                break;
        }
        return line.toString();
    }

    private boolean readToEndOfNetconfReply(BufferedReader br, StringBuilder reply) throws IOException {
        // String readLine = br.readLine(); // can hang!
        String readLine = readBufferLine(br);
        if (readLine == null)
            return true;
        String netconfEndOfMsg = "]]>]]>";
        int end;
        logger.trace("Got:" + readLine);
        if ((end = readLine.indexOf(netconfEndOfMsg)) != -1) {
            reply.append(readLine.substring(0, end));
            return true;
        } else {
            reply.append(readLine);
            return false;
        }
    }

    private void readNetconfReplyBuffer(BufferedReader br, StringBuilder reply) throws IOException, OmpLibraryException {

        // Limit to break from read loop to avoid out of memory
        final int CHAR_LIMIT = 325000;

        logger.debug("starting to read netconf message");
        boolean foundEndOfMessage = false;
        while ((br.ready() || waitForReadBuffer(br)) && !(foundEndOfMessage = readToEndOfNetconfReply(br, reply))) {
            if (reply.length() > CHAR_LIMIT) {
                String msg = "Has not revieved any xml tags the last " + reply.length() + " characters read.";
                logger.error(msg + " Could not receive a valid netconf message!! Aborting read of netconf message!");
                logger.info(reply);
                throw new OmpLibraryException(msg);
            }
        }
        if (!foundEndOfMessage) {
            logger.error(reply.toString());
            throw new OmpLibraryException("Incomplete message in buffer.");
        }
    }

    private boolean waitForReadBuffer(BufferedReader br) throws IOException {
        double currentWaitTime = 0;
        long interval = 10;
        while (!br.ready()) {
            if (currentWaitTime > timeoutForNetconfReply)
                throw new IOException("Input stream cannot be read.");
            try {
                Thread.sleep(interval);
            } catch (InterruptedException e) {
            }
            currentWaitTime += interval / 1000.0;
        }
        return true;

    }

    private String receiveRawNetconfMessage(BufferedReader br) throws IOException, XmlException {

        // ArrayList<String> lines = new ArrayList<String>();
        StringBuilder reply = new StringBuilder(12096);

        try {
            readNetconfReplyBuffer(br, reply);
        } catch (Exception e) {
            logger.error("Error", e);
            return null;
        }

        logger.debug("done reading net conf message");

        // log result/reply to protocol logger
        try {
            // NetConfReply netConfReply = new NetConfReply(reply.toString());
            // logger.info(netConfReply.toString());
            LogWriterHelper.setTestInfoInFile(logger, "Message received", formattedNetconfMessage(reply.toString()));
        } catch (OutOfMemoryError e) {
            logger.error("java out of memory increase [java -Xms<initial heap size> -Xmx<maximum heap size>]");
            logger.info("<font size=\"2\"><pre><netconfJCAT>Java.lang.OutOfMemoryError: Java heap space</netconfJCAT></pre></font>");
        }

        return reply.toString();
    }

    public String formattedNetconfMessage(String input) throws IOException {
        Reader br = new StringReader(input);

        StringBuilder reply = new StringBuilder(12096);
        String currentTag = null;
        int startOfTagIndex = -1;
        boolean parsingStartTag = false, parsingEndTag = false;
        Stack<String> tagStack = new Stack<String>();
        char character;
        int readElement;
        int charCount = 0;
        int indentation = 0;
        boolean increaseInd = true;
        boolean endCharacterReceived = false;
        boolean newLineApplied = true;

        while (br.ready() && (readElement = br.read()) != -1) {
            character = (char) readElement;
            logger.trace("Got:" + character);
            charCount++;

            // Remove whitespaces
            if (character == ' ') {
                while ((character = (char) br.read()) == ' ') {
                    logger.debug("In while got a whitespace");
                }
                logger.debug("Appending that whitespace, character is now: " + character);
                reply.append(' ');
            }

            // Ignoring end of line characters
            if (character == '\n') {
                logger.trace("end of line");
                charCount = 0;
                // reply.append(character);
                // Ignoring carage returns
            } else if (character == '\r') {
                logger.trace("carrige return");
                charCount = 0;
                // reply.append(character);
                // Ignoring tab
            } else if (character == '\t') {
                logger.trace("tab");
                charCount = 0;

                // If we have a end of xml tag we will apply a new line
            } else if (character == '>') {
                charCount = 0;
                endCharacterReceived = true;
                if (parsingStartTag && startOfTagIndex >= 0) {
                    currentTag = tagStack.push(reply.substring(startOfTagIndex, reply.length()));
                } else if (parsingEndTag) {
                    ;
                } else {
                    endCharacterReceived = false;
                    // logger.error("XML end tag found without start tag.");
                }
                if (endCharacterReceived) {
                    if (increaseInd) {
                        // logger.debug("end of starting xml tag");
                        reply.append(character);
                        reply.append('\n');
                        // We want the next lines indentation increased
                        indentation += 2;
                    } else {
                        // We want the indentation to be the same
                        // logger.debug("end of ending xml tag");
                        reply.append(character);
                        reply.append('\n');
                    }
                    parsingStartTag = false;
                    parsingEndTag = false;
                    newLineApplied = true;
                } else {
                    parseOrdinaryChar(currentTag, character, parsingStartTag, parsingEndTag, reply);
                }
                // If we have the start of an xml tag we will check if it is a starting or closing tag
            } else if (character == '<') {
                charCount = 0;
                endCharacterReceived = false;
                if (!newLineApplied) {
                    reply.append('\n');
                }
                if ((character = (char) br.read()) == '/') {
                    // We want indentation to be the same at next tag and decreased for this tag
                    increaseInd = false;
                    indentation -= 2;
                    for (int i = 0; i < indentation; i++) {
                        reply.append(" ");
                    }
                    reply.append('<');
                    reply.append(character);
                    tagStack.pop();
                    if (tagStack.size() > 0)
                        currentTag = tagStack.peek();
                    else
                        currentTag = null;
                    parsingEndTag = true;
                    // logger.debug("beginning of closing tag");
                } else {
                    // logger.debug("beginning of xml tag");
                    // We want to increase the indentation at the next tag
                    increaseInd = true;
                    for (int i = 0; i < indentation; i++) {
                        reply.append(" ");
                    }
                    reply.append('<');
                    parsingStartTag = true;
                    startOfTagIndex = reply.length();
                    reply.append(character);
                }
                newLineApplied = false;
                // Check if it is a tag without content or just a '/'
            } else if (character == '/') {
                charCount = 0;
                // Closing of tag without content we want the indentation to stay the same
                if ((character = (char) br.read()) == '>') {
                    endCharacterReceived = true;
                    reply.append('/');
                    reply.append(character);
                    reply.append('\n');
                    newLineApplied = true;
                    parsingStartTag = false;
                } else {
                    if (endCharacterReceived) {
                        for (int i = 0; i < indentation; i++) {
                            reply.append(" ");
                        }
                    }
                    reply.append('/');
                    reply.append(character);
                    newLineApplied = false;
                    endCharacterReceived = false;
                }
            } else {
                if (endCharacterReceived) {
                    for (int i = 0; i < indentation; i++) {
                        reply.append(" ");
                    }
                }
                parseOrdinaryChar(currentTag, character, parsingStartTag, parsingEndTag, reply);
                endCharacterReceived = false;
                newLineApplied = false;

            }

        }

        return reply.toString();

    }

    /**
     * Reads a netconf message until end of message(]]>]]>) is received. Formats the input and writes to protocol log
     */
    private String receiveNetconfMessage(BufferedReader br) {
        String rawMessage = validateNetconfMessage(br);
        if (useRawMessage) {
            printNiceLog(rawLogLevel, "NETCONF MSG RECEIVED: ", rawMessage);
            return rawMessage;
        } else {
            try {
                String formattedMessage = formattedNetconfMessage(rawMessage);
                try {
                    LogWriterHelper.setTestInfoInFile(logger, "Message received", formattedMessage);
                } catch (OutOfMemoryError e) {
                    logger.error("java out of memory increase [java -Xms<initial heap size> -Xmx<maximum heap size>]");
                    logger.info("<font size=\"2\"><pre><netconfJCAT>Java.lang.OutOfMemoryError: Java heap space</netconfJCAT></pre></font>");
                }
                return formattedMessage;
            } catch (Exception e) {
                logger.info("<font size=\"2\"><pre><netconfJCAT>" + e.getMessage() + "</netconfJCAT></pre></font>");
                return null;
            }
        }
    }

    private String validateNetconfMessage(BufferedReader br) {
        StringBuilder reply = new StringBuilder(12096);
        StringBuilder line = new StringBuilder(20);
        char character;
        int charCount = 0;
        // Limit to break from read loop to avoid out of memory
        final int CHAR_LIMIT = 325000;

        try {
            logger.debug("starting to read netconf message");

            while ((character = (char) br.read()) != -1) {
                logger.trace("Got:" + character);
                charCount++;
                if (charCount > CHAR_LIMIT) {
                    logger.error("Has not revieved any xml tags the last "
                            + charCount
                            + " characters read. Could not receive a valid netconf message!! Aborting read of netconf message!");
                    logger.info(reply);
                    return null;
                }

                // Checking if we have a end of netconf message
                if (character == ']') {
                    line.append(character);
                    charCount = 0;
                    // logger.debug("Got a ]");
                    if ((character = (char) br.read()) == ']') {
                        line.append(character);
                        // logger.debug("Got another ]");
                        if ((character = (char) br.read()) == '>') {
                            line.append(character);
                            // logger.debug("Got a >");
                            if ((character = (char) br.read()) == ']') {
                                // logger.debug("Got yet another ]");
                                line.append(character);
                                if ((character = (char) br.read()) == ']') {
                                    line.append(character);
                                    if ((character = (char) br.read()) == '>') {
                                        logger.debug("End of netconf message reached");
                                        break;
                                    } else {
                                        // line.append(character);
                                        logger.debug("appending :" + line);
                                        reply.append(line);
                                        line.setLength(0);
                                    }
                                } else {
                                    // line.append(character);
                                    logger.debug("appending :" + line);
                                    reply.append(line);
                                    line.setLength(0);
                                }
                            } else {
                                // line.append(character);
                                logger.debug("appending :" + line);
                                reply.append(line);
                                line.setLength(0);
                            }
                        } else {
                            // line.append(character);
                            logger.trace("appending :" + line);
                            reply.append(line);
                            line.setLength(0);
                        }
                    } else {
                        // line.append(character);
                        // logger.debug("appending :" + line);
                        reply.append(line);
                        line.setLength(0);
                    }
                } else {
                    reply.append(character);
                }
            }
        } catch (IOException e) {
            logger.error("Error", e);
        }
        logger.debug("done reading net conf message");
        return reply.toString();

    }

    private void parseOrdinaryChar(String parentTag, char character, boolean parsingStartTag, boolean parsingEndTag,
            StringBuilder reply) {

        if (parsingStartTag)
            formatTagChar(parentTag, character, reply);
        else if (parsingEndTag)
            formatTagChar(parentTag, character, reply);
        else
            formatContentChar(parentTag, character, reply);
    }

    /**
     * Format the characters between < and >.
     */
    private void formatTagChar(String parentTag, char character, StringBuilder reply) {
        reply.append(character);
    }

    /**
     * Format the character based on the tag. This is used for special formatting of contents, such as not displaying
     * passwords.
     */
    private void formatContentChar(String parentTag, char character, StringBuilder reply) {
        if (parentTag != null && parentTag.contains("password")) {
            reply.append('X');
        } else {
            reply.append(character);
        }
    }

    /**
     * Sends the bytes in the array on stdout stream, and waits for a reply.
     * 
     * @param data
     *            the netconf message encoded as a byte[]
     * @return the message received as a reply
     * @throws IOException
     *             on send exceptions
     * @throws NoSessionException
     *             if the netconf session is closed or not started
     * @throws XmlException
     */
    public String sendBytes(byte[] data) throws IOException, OmpLibraryException, XmlException {
        if (sess == null) {
            throw new OmpLibraryException("A netconf session must be started before anything can be sent");
        }

        BufferedReader br = new BufferedReader(new InputStreamReader(stdout, "UTF-8"));

        sendBytesNoResult(data);
        logger.debug("Done sending starting to receive");

        String temp = receiveNetconfMessage(br);

        // Something wrong when waiting for netconf reply
        if (temp == null) {

            // Debug printout from Erlang
            // Erlang erlang = new Erlang(connectedHost, sisSidUser, sisSidPass, sisSidPrompt);
            // erlang.printLocks();

            // sleep before retry
            try {
                Thread.sleep(10000);
            } catch (InterruptedException e) {
                // Ignored
            }

            // restart netconf session
            this.startNetConfSession();

            // sleep before resend
            try {
                Thread.sleep(5000);
            } catch (InterruptedException e) {
                // Ignored
            }

            // send message again
            sendBytesNoResult(data);
            temp = receiveNetconfMessage(br);

            // Debug printout from erlang
            // erlang.printLocks();
            // erlang.exitErlang();
        }
        return temp;
        // return waitForPrompt(br);
    }

    public String sendBytesRawResult(byte[] data) throws IOException, OmpLibraryException, XmlException {
        if (sess == null) {
            throw new OmpLibraryException("A netconf session must be started before anything can be sent");
        }

        BufferedReader br = new BufferedReader(new InputStreamReader(stdout, "UTF-8"));

        sendBytesNoResult(data);

        logger.debug("Done sending starting to receive");

        String temp = receiveRawNetconfMessage(br);
        return temp;
    }

    /**
     * Sends the bytes in the array on stdout stream.
     * 
     * @param data
     *            the netconf message encoded as a byte[]
     * @throws IOException
     *             if an IO error occurs
     * @throws OmpLibraryException
     *             if no netconf session exist
     * @throws XmlException
     */
    private void sendBytesNoResult(byte[] data) throws IOException, OmpLibraryException, XmlException {
        if (sess == null) {
            throw new OmpLibraryException("A netconf session must be started before anything can be sent");
        }
        logger.trace(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>");
        logger.trace("Sending to netconf channel");
        logger.trace(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>");

        if (logger.getLevel() == Level.TRACE) {
            logger.trace(this.removeXmlTagsAndFormat(data));
        }
        logger.trace(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>");

        OutputStream os = sess.getStdin();

        logger.debug("Data length: " + data.length);
        os.write(data, 0, data.length);
        os.flush();
        // log sent data to protocol logger
        // TODO - REMOVE printXml(Level.DEBUG, formattedNetconfMessage(new String(data)));
        printNiceLog(rawLogLevel, "NETCONF MSG SENT:", new String(data));

        // logger.info(new String(data));
        // os.close();
        os = null;
    }

    // Returns the contents of the file in a byte array.
    /**
     * Parses an xml file and returns it as a byte[], does NOT add the netconf end sequence "[[>[[>".
     * 
     * @param file
     *            file that contains a netconf message in xml format
     * @return the file as a byte[]
     * @throws IOException
     *             if there s an error reading the file
     */
    public byte[] parseXmlFile(File file) throws IOException {
        logger.debug("Getting bytes from file");
        InputStream is = new FileInputStream(file);

        // Get the size of the file
        long length = file.length();

        // You cannot create an array using a long type.
        // It needs to be an int type.
        // Before converting to an int type, check
        // to ensure that file is not larger than Integer.MAX_VALUE.
        if (length > Integer.MAX_VALUE) {
            logger.error("File " + file.getCanonicalPath() + " is too large! " + length);
            closeInputStream(is);
            return new byte[0];
        }

        // Create the byte array to hold the data
        byte[] bytes = new byte[(int) length];

        // Read in the bytes
        int offset = 0;
        int numRead = 0;
        while (offset < bytes.length && (numRead = is.read(bytes, offset, bytes.length - offset)) >= 0) {
            offset += numRead;
        }

        // Ensure all the bytes have been read in
        if (offset < bytes.length) {
            closeInputStream(is);
            throw new IOException("Could not completely read file " + file.getName());
        }

        closeInputStream(is);

        // messageCounter ++;
        return bytes;
    }

    /**
     * Creates a valid rpc message if the XmlObject is correct.
     * 
     * @param xmlObject
     *            the object to be embedded in the RPC message
     * @return the xml message encoded ad a byte[]
     */
    public byte[] constructRpcMessage(XmlObject xmlObject) {

        RpcDocument rpc = RpcDocument.Factory.newInstance();

        RpcType type = rpc.addNewRpc();

        type.set(xmlObject);
        type.setMessageId("" + messageCounter++);

        logger.debug("RPC::::\n" + rpc);

        // return (fixIs20NameSpaceError(rpc.toString() + NETCONF_MESASGE_END).getBytes());
        return (rpc.toString() + NETCONF_MESSAGE_END).getBytes();
    }

    /**
     * Creates a valid RPC-get message if the xmlObject is valid.
     * 
     * @param xmlObject
     *            the object to be embedded in the get message
     * @return the xml message encoded ad a byte[]
     */
    public byte[] constructGetMessage(XmlObject xmlObject) {

        GetDocument get = GetDocument.Factory.newInstance();

        GetType getType = get.addNewGet();
        FilterInlineType filter = getType.addNewFilter();

        filter.set(xmlObject);
        filter.setType(FilterType.SUBTREE);

        return constructRpcMessage(get);
    }

    public byte[] constructGetXpathMessage(String expression) {
        GetDocument get = GetDocument.Factory.newInstance();

        GetType getType = get.addNewGet();
        FilterInlineType filter = getType.addNewFilter();

        filter.setType(FilterType.XPATH);
        XmlAnySimpleType select = XmlAnySimpleType.Factory.newInstance();
        select.setStringValue(expression);
        filter.setSelect(select);

        return constructRpcMessage(get);
    }

    /**
     * NOT implemented yet.
     * 
     * @param xmlObject
     *            the object to be embedded in the get message
     */
    public byte[] constructGetConfigMessage(XmlObject xmlObject) {
        GetConfigDocument getconfDoc = GetConfigDocument.Factory.newInstance();
        GetConfigType getconfType = getconfDoc.addNewGetConfig();
        FilterInlineType filter = getconfType.addNewFilter();

        RunningDocument runningDocument = RunningDocument.Factory.newInstance();
        runningDocument.addNewRunning();

        getconfType.addNewSource().set(runningDocument);// .setConfigName(ConfigNameType.Factory.newInstance());

        filter.set(xmlObject);
        filter.setType(FilterType.SUBTREE);

        // System.out.println("\n\n" + runningDocument + "\n\n");
        // System.out.println("\n\n" + xmlObject + "\n\n");
        // System.out.println(new String(constructRpcMessage(getconfDoc)));
        return constructRpcMessage(getconfDoc);
    }

    public byte[] constructGetConfigXpathMessage(String expression) {
        GetConfigDocument getconfDoc = GetConfigDocument.Factory.newInstance();
        GetConfigType getconfType = getconfDoc.addNewGetConfig();
        FilterInlineType filter = getconfType.addNewFilter();

        RunningDocument runningDocument = RunningDocument.Factory.newInstance();
        runningDocument.addNewRunning();

        getconfType.addNewSource().set(runningDocument);// .setConfigName(ConfigNameType.Factory.newInstance());

        filter.setType(FilterType.XPATH);
        XmlAnySimpleType select = XmlAnySimpleType.Factory.newInstance();
        select.setStringValue(expression);
        filter.setSelect(select);

        return constructRpcMessage(getconfDoc);
    }

    /**
     * Creates a valid RPC edit-config message if the xmlObject is valid.
     * 
     * @param xmlObject
     *            the object to be embedded in the edit message
     * @param defaultOperation
     *            Set default operation of edit-config message, null use default
     * @param errorOption
     *            Set error option, null will use default
     * @return the xml message encoded ad a byte[]
     */
    public byte[] constructEditMessage(XmlObject xmlObject, DefaultOperationType.Enum defaultOperation,
            ErrorOptionType.Enum errorOption, TestOptionType.Enum testOption) {

        EditConfigDocument editconfDoc = EditConfigDocument.Factory.newInstance();
        EditConfigType editType = editconfDoc.addNewEditConfig();

        RunningDocument runningDocument = RunningDocument.Factory.newInstance();
        runningDocument.addNewRunning();

        editType.addNewTarget().set(runningDocument);

        if (defaultOperation != null)
            editType.setDefaultOperation(defaultOperation);
        if (errorOption != null)
            editType.setErrorOption(errorOption);
        if (testOption != null)
            editType.setTestOption(testOption);

        ConfigInlineType configInline = editType.addNewConfig();
        configInline.set(xmlObject);

        // System.out.println(new String(constructRpcMessage(editconfDoc)));
        return constructRpcMessage(editconfDoc);
    }

    /**
     * Creates a RPC copy-config message.
     * 
     * @param targetType
     *            the target, running or url
     * @param xmlObject
     *            the source, running or url
     * @return the xml message encoded ad a byte[]
     */
    public byte[] constructCopyConfigMessage(XmlObject targetType, XmlObject xmlObject) {
        CopyConfigDocument copyConfDoc = CopyConfigDocument.Factory.newInstance();
        CopyConfigType copyType = copyConfDoc.addNewCopyConfig();

        copyType.addNewTarget().set(targetType);

        // ConfigInlineType configInline = copyType.addNewSource().addNewConfig();
        // configInline.set(xmlObject);

        copyType.addNewSource().set(xmlObject);

        return constructRpcMessage(copyConfDoc);
    }

    /**
     * Creates a valid RPC delete-config message if the xmlObject is valid.
     * 
     * @param xmlObject
     *            the object to be embedded in the get message
     * @return the xml message encoded ad a byte[]
     */
    public byte[] constructDeleteMessage(XmlObject xmlObject) {
        DeleteConfigDocument deleteconfDoc = DeleteConfigDocument.Factory.newInstance();
        DeleteConfigType deleteType = deleteconfDoc.addNewDeleteConfig();

        RunningDocument runningDocument = RunningDocument.Factory.newInstance();
        runningDocument.addNewRunning();

        deleteType.addNewTarget().set(xmlObject);

        return constructRpcMessage(deleteconfDoc);
    }

    /**
     * Creates a rpc lock message.
     * 
     * @return the xml message encoded ad a byte[]
     */
    public byte[] constructLockRunningMessage() {
        RunningDocument runningDocument = RunningDocument.Factory.newInstance();
        runningDocument.addNewRunning();

        return constructLockMessage(runningDocument);
    }

    /**
     * Creates a rpc lock message.
     * 
     * @return the xml message encoded ad a byte[]
     */
    private byte[] constructLockMessage(XmlObject targetType) {
        LockDocument lockDoc = LockDocument.Factory.newInstance();
        RpcOperationTargetType target = lockDoc.addNewLock().addNewTarget();

        target.set(targetType);

        return constructRpcMessage(lockDoc);
    }

    /**
     * Creates a rpc lock message.
     * 
     * @return the xml message encoded ad a byte[]
     */
    public byte[] constructUnLockRunningMessage() {
        RunningDocument runningDocument = RunningDocument.Factory.newInstance();
        runningDocument.addNewRunning();

        return constructUnLockMessage(runningDocument);
    }

    /**
     * Creates a rpc lock message.
     * 
     * @return the xml message encoded ad a byte[]
     */
    public byte[] constructUnLockCandidateMessage() {
        CandidateDocument candidateDocument = CandidateDocument.Factory.newInstance();
        candidateDocument.addNewCandidate();

        return constructUnLockMessage(candidateDocument);
    }

    public byte[] constructKillSessionMessage(long sessionId) {
        KillSessionDocument killSessionDocument = KillSessionDocument.Factory.newInstance();
        killSessionDocument.addNewKillSession().setSessionId(sessionId);

        return constructRpcMessage(killSessionDocument);

    }

    /**
     * Creates a rpc unlock message.
     * 
     * @param targetType
     *            the target, running or candidate
     * @return the xml message encoded ad a byte[]
     */
    private byte[] constructUnLockMessage(XmlObject targetType) {
        UnlockDocument lockDoc = UnlockDocument.Factory.newInstance();
        RpcOperationTargetType target = lockDoc.addNewUnlock().addNewTarget();

        target.set(targetType);

        return constructRpcMessage(lockDoc);
    }

    /**
     * Creates a rpc commit message.
     * 
     * @return the xml message encoded ad a byte[]
     */
    public byte[] constructCommitMessage() {
        // TODO: add check for the :candidate capability in hello message
        // which is required to be able to send a commit message
        CommitDocument commitDoc = CommitDocument.Factory.newInstance();
        commitDoc.addNewCommit();

        return constructRpcMessage(commitDoc);
    }

    /**
     * Creates a rpc validate candidate message.
     * 
     * @return the xml message encoded ad a byte[]
     */
    public byte[] constructValidateCandidateMessage() {
        ValidateDocument validateDoc = ValidateDocument.Factory.newInstance();
        RpcOperationSourceType source = validateDoc.addNewValidate().addNewSource();

        CandidateDocument canddateDoc = CandidateDocument.Factory.newInstance();
        canddateDoc.addNewCandidate();

        source.set(canddateDoc);

        return constructRpcMessage(validateDoc);
    }

    /**
     * Creates a rpc discard-changes message.
     * 
     * @return the xml message encoded ad a byte[]
     */
    public byte[] constructDiscardChangesMessage() {
        // TODO: add check for the :candidate capability in hello message
        // which is required to be able to send a commit message
        DiscardChangesDocument discardDoc = DiscardChangesDocument.Factory.newInstance();
        discardDoc.addNewDiscardChanges();

        return constructRpcMessage(discardDoc);
    }

    /**
     * Use this method to increase the message counter in the RPC messages if not the provided methods for creating RPC
     * messages are used or if using external XML files.
     * 
     * @return the current value of the message counter after the update
     */
    public int increaseMessageIdCounter() {
        return messageCounter++;
    }

    /**
     * Sends a Hello message on the netconf channel.
     * 
     * @return True if successful
     */
    public boolean sendHello() {
        boolean result = true;
        HelloDocument hello = HelloDocument.Factory.newInstance();
        hello.addNewHello().addNewCapabilities().addCapability("urn:ietf:params:netconf:base:1.0");

        byte[] cmd = null;

        cmd = (hello.toString() + NETCONF_MESSAGE_END).getBytes();

        try {
            sendBytesNoResult(cmd);
        } catch (Exception e) {
            result = false;
            e.printStackTrace();
        }
        return result;
    }

    /**
     * A method to parse a hello message.
     * 
     * @param netconfMessage
     *            the netconf message as a string
     * @return the parsed HelloDocument
     * @throws XmlException
     *             if there is a parse error
     * @throws EmptyDocumentException
     *             if there is no information in the message
     */
    public HelloDocument parseHelloDocument(String netconfMessage) throws XmlException, OmpLibraryException {
        HelloDocument helloReply = null;
        try {
            helloReply = HelloDocument.Factory.parse(netconfMessage);
        } catch (XmlException xe) {
            throw xe;
        }

        if (helloReply == null) {
            throw new OmpLibraryException("Hello message is empty");
        }

        return helloReply;
    }

    /**
     * Sends a Close message on the netconf channel.
     * 
     * @return True if successful otherwise False
     */
    public boolean sendClose() {
        boolean result = true;
        RpcDocument rpc = RpcDocument.Factory.newInstance();
        RpcType rpcType = rpc.addNewRpc();

        CloseSessionDocument close = CloseSessionDocument.Factory.newInstance();
        close.addNewCloseSession();

        rpcType.set(close);
        rpcType.setMessageId("" + messageCounter++);

        logger.debug("CLOSE::::\n" + rpc);
        try {
            String netconfResult = sendBytes((rpc.toString() + NETCONF_MESSAGE_END).getBytes());
            if (netconfResult != null && destructRpcOk(netconfResult) != null) {
                // Close response OK
            } else {
                logger.warn("Could not complete close call!\n" + netconfResult);
                result = false;
            }

        } catch (Exception e) {
            result = false;
            logger.warn(e);
        }
        rpc = null;
        close = null;
        return result;
    }

    /**
     * Sends a Kill session message on the netconf channel.
     * 
     * @param sessionId
     *            the id of session to kill
     * @return True if successful otherwise False
     */
    public boolean sendKillSession(long sessionId) {
        boolean result = true;
        RpcDocument rpc = RpcDocument.Factory.newInstance();
        RpcType rpcType = rpc.addNewRpc();

        KillSessionDocument kill = KillSessionDocument.Factory.newInstance();
        kill.addNewKillSession().setSessionId(sessionId);

        rpcType.set(kill);
        rpcType.setMessageId("" + messageCounter++);

        logger.debug("KILL::::\n" + rpc);
        try {
            sendBytesNoResult((rpc.toString() + NETCONF_MESSAGE_END).getBytes());
            // System.out.println("Reply::::");
            // for (int i = 0; i < netconfResult.length; i++) {
            // showResult(netconfResult);
            /* Verify that we got Ok back */
            // pcReplyDocument.Factory.parse(netconfResult).getRpcReply().getOk();
            // }
        } catch (Exception e) {
            result = false;
            logger.warn(e);
        }
        rpc = null;
        kill = null;
        return result;
    }

    /**
     * Method to get the errors out of a reply message.
     * 
     * @param reply
     *            the message gotten from the server
     * @return the rpc error as a xml bean
     * @throws XmlException
     *             if the String is not valid xml to be parsed as an error message
     */
    public static RpcErrorType[] getErrorFromReply(String reply) throws XmlException {
        RpcReplyDocument rpcReplyDoc = null;
        try {
            rpcReplyDoc = RpcReplyDocument.Factory.parse(reply);
        } catch (XmlException xe) {
            throw xe;// new IOException("Cannot parse the argument into a RpcReplyDocument");
        }

        return getErrorFromRpcReplyDocument(rpcReplyDoc);
    }

    /**
     * Return the IP address of this netconf seesion.
     * 
     * @return the IP address of the connected host.
     */
    public String getConnectedHost() {
        logger.info("The connected host is : " + connectedHost);
        return connectedHost;
    }

    /**
     * Returns the object holding the server capabilities.
     * 
     * @return object containing the status of servercapabilities included in netconf statndard.
     */
    public ServerCapabilities getServerCapabilities() {
        return serverCapabilities;
    }

    public DefaultOperationType.Enum getDefaultOperationForEditConfig() {
        return defaultOperation;
    }

    public void clearDefaultOperationForEditConfig() {
        defaultOperation = null;
    }

    /**
     * Set the default-operation parameter for edit-config Netconf messages.
     * 
     * @param defaultOperation
     *            Enumeration indicating the operation type.
     */
    public void setDefaultOperationForEditConfig(DefaultOperationType.Enum defaultOperation) {
        this.defaultOperation = defaultOperation;
    }

    public ErrorOptionType.Enum getErrorOptionForEditConfig() {
        return errorOption;
    }

    public void clearErrorOptionForEditConfig() {
        errorOption = null;
    }

    /**
     * Set error-option for edit-config messages.
     * 
     * @param errorOption
     *            Enumeration for error-options, see rfc4741
     */
    public void setErrorOptionForEditConfig(ErrorOptionType.Enum errorOption) {
        this.errorOption = errorOption;
    }

    public TestOptionType.Enum getTestOptionForEditConfig() {
        return testOption;
    }

    public void clearTestOptionForEditConfig() {
        testOption = null;
    }

    /**
     * Set test-option for edit-config messages.
     * 
     * @param errorOption
     *            Enumeration for test-options, see rfc4741
     */
    public void setTestOptionForEditConfig(TestOptionType.Enum testOption) {
        this.testOption = testOption;
    }

    /**
     * Method to get the the errors out of an RpcReplyDocument .
     * 
     * @param rpcReplyDoc
     *            the netconf answer gotten from the server
     * @return the errors in an array
     */
    public static RpcErrorType[] getErrorFromRpcReplyDocument(RpcReplyDocument rpcReplyDoc) {
        return rpcReplyDoc.getRpcReply().getRpcErrorArray();
    }

    /**
     * Closes stream sesssion and connection.
     */
    public void closeNetconfSession() {
        if (stdout != null) {
            try {
                stdout.close();
            } catch (IOException ioe) {

            }
        }

        logger.info("Closing the Netconf session");
        stdout = null;
        if (sess != null) {
            sess.close();
            sess = null;
        }

        if (conn != null) {
            conn.close();
            conn = null;
        }
        sessionID = 0;
    }

    public static void printXml(Level level, String xml) {
        logger.log(level, xml.replaceAll("<", "&lt;").replaceAll(">", "&gt;"));
    }

    private String removeXmlTagsAndFormat(byte[] data) {
        String stringWTags = new String(data);
        return removeXmlTagsAndFormat(stringWTags);
    }

    private String removeXmlTagsAndFormat(String stringWithTags) {
        // stringWoTags.replaceAll(">", "&gt;");

        try {

            String stringWoTags = stringWithTags.replaceAll("<", "&lt;");
            return "<font size=\"2\"><pre>" + stringWoTags.replaceAll(">", "&gt;") + "</pre></font>";
        } catch (OutOfMemoryError e) {
            logger.error("java out of memory increase [java -Xms<initial heap size> -Xmx<maximum heap size>]");
            return "<font size=\"2\"><pre><netconfJCAT>Java.lang.OutOfMemoryError: Java heap space</netconfJCAT></pre></font>";
        }
    }

    class ServerCapabilities {
        boolean hasWritableRunning = false;
        boolean hasCandidate = false;
        boolean hasConfirmedCommit = false;
        boolean hasRollbackOnError = false;
        boolean hasValidate = false;
        boolean hasStartup = false;
        boolean hasUrl = false;
        boolean hasXpath = false;

        // String[] standardCapabilities = null;

        public ServerCapabilities() {
            // standardCapabilities = new String[]{WRITABLE_RUNNING, CANDIDATE, CONFIRMED_COMMIT, ROLLBACK_ON_ERROR,
            // VALIDATE, STARTUP, URL, XPATH};
        }

        public boolean addCapability(String capability) {
            if (capability.equalsIgnoreCase(WRITABLE_RUNNING)) {
                hasWritableRunning = true;
                return true;
            }
            if (capability.equalsIgnoreCase(CANDIDATE)) {
                hasCandidate = true;
                return true;
            }
            if (capability.equalsIgnoreCase(CONFIRMED_COMMIT)) {
                hasConfirmedCommit = true;
                return true;
            }
            if (capability.equalsIgnoreCase(ROLLBACK_ON_ERROR)) {
                hasRollbackOnError = true;
                return true;
            }
            if (capability.equalsIgnoreCase(VALIDATE)) {
                hasValidate = true;
                return true;
            }
            if (capability.equalsIgnoreCase(STARTUP)) {
                hasStartup = true;
                return true;
            }
            if (capability.equalsIgnoreCase(URL)) {
                hasUrl = true;
                return true;
            }
            if (capability.equalsIgnoreCase(XPATH)) {
                hasXpath = true;
                return true;
            }
            return false;
        }

        public boolean hasWritableRunning() {
            return hasWritableRunning;
        }

        public boolean hasCandidate() {
            return hasCandidate;
        }

        public boolean hasConfirmedCommit() {
            return hasConfirmedCommit;
        }

        public boolean hasRollbackOnError() {
            return hasRollbackOnError;
        }

        public boolean hasValidate() {
            return hasValidate;
        }

        public boolean hasStartup() {
            return hasStartup;
        }

        public boolean hasUrl() {
            return hasUrl;
        }

        public boolean hasXpath() {
            return hasXpath;
        }
    }

    private void printNiceLog(Level level, String coverMsg, String msg) {
        logger.log(level, coverMsg);
        logger.log(level,
                   LogWriterHelper.newStyledText(msg.replaceAll("<", "&lt;").replace(">", "&gt;")).formatedBlock().toString());
    }

    private void closeInputStream(InputStream is) {
        // Close the input stream and return bytes
        if (is != null) {
            try {
                is.close();
            } catch (IOException e) {
                logger.warn("Failed to close input stream:", e);
            }
        }
    }

    /**
     * Split and parse RPC reply to validate if the transaction is completed OK without error.
     * 
     * @param reply
     *            the message received
     * @return the netconf answer gotten from the server
     */
    private RpcReplyDocument destructRpcOk(final String reply) {
        final String[] responses = reply.split(NETCONF_MESSAGE_END);
        for (String response : responses) {
            try {
                RpcReplyDocument rpcOk = RpcReplyDocument.Factory.parse(response);
                if (rpcOk.getRpcReply().getOk() != null) {
                    return rpcOk;
                }
            } catch (final XmlException e) {
                logger.debug("Message is not a valid RPC-Reply (OK): ");
                printNiceLog(rawLogLevel, "NETCONF RPC-REPLY ERROR: ", e.getMessage());
            }
        }
        logger.error("Cannot find any RPC-Reply (OK) in server response");
        return null;
    }
}
