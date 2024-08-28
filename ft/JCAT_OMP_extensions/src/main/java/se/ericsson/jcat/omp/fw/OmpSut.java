package se.ericsson.jcat.omp.fw;

import java.io.DataInputStream;
import java.io.IOException;
import java.net.Socket;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.apache.commons.configuration.ConfigurationException;
import org.apache.commons.configuration.ConversionException;
import org.apache.commons.configuration.SystemConfiguration;
import org.apache.commons.configuration.XMLConfiguration;
import org.apache.log4j.Logger;

import se.ericsson.jcat.fw.SUT;
import se.ericsson.jcat.fw.jython.Jythonizer;
import se.ericsson.jcat.fw.utils.Ssh2Session;
import se.ericsson.jcat.omp.util.LibraryBroker;

/**
 * To configure a library for loading by the library broker, one must set a system property before the Sut is created.
 * To specify a Java library for loading called se.ericsson.jcat.fw.test.TestJavaLibrary, set the following System
 * Property se.ericsson.jcat.omp.fw.JavaLibrary:se.ericsson.jcat.fw.test. TestJavaLibrary (to anything) - i.e. it is the
 * fact that this system property is set that loads the library, not what it is set to that matters. Similary for a
 * Python library called test.TestPythonLibrary, set the following System Property
 * se.ericsson.jcat.omp.fw.PythonLibrary:test.TestPythonLibrary (to anything).
 */
public class OmpSut extends SUT {
    @SuppressWarnings("unused")
    private String safSutName = null;
    // Holds the target_data strucure
    private XMLConfiguration xmlConfiguration = null;
    private final LibraryBroker libraryBroker;
    private String hostnameSeparator = null;
    private static OmpSut sut = null;
    private static final Logger logger = Logger.getLogger(OmpSut.class);

    /**
     * Just for unit test
     */
    protected static void removeSut() {
        sut = null;
        OmpTestInfo.resetInitializedFlag();
        se.ericsson.commonlibrary.LibraryBroker.reloadLibraries();
    }

    /**
     * Just for unit test
     */
    protected OmpSut() {
        libraryBroker = null;
    }

    /**
     * Constructor save the ip address
     * 
     * @param sutName
     */
    public OmpSut(final String sutName) {
        super(""); // Create a SUT with no name. Why? We only have one SUT and makes the events look better.
        sut = this;
        this.safSutName = sutName;
        libraryBroker = new LibraryBroker(this);
        libraryBroker.setUp();
        try {
            se.ericsson.commonlibrary.LibraryBroker.setPythonInterpreter(Jythonizer.getInstance());
        } catch (Exception e) {
            throw new RuntimeException("Cannot get Python intepretor!", e);
        }
        se.ericsson.commonlibrary.LibraryBroker.initializeLibraries();

    }

    /**
     * Creates a new instance of <code>OmpSut</code>.
     * 
     * @param sutName
     * @param xmlConfiguration
     */
    public OmpSut(final String sutName, final XMLConfiguration xmlConfiguration) {
        super(""); // Create a SUT with no name. Why? We only have one SUT and makes the events look better.
        sut = this;
        this.safSutName = sutName;
        this.xmlConfiguration = xmlConfiguration;
        libraryBroker = new LibraryBroker(this);
        libraryBroker.setUp();
        try {
            se.ericsson.commonlibrary.LibraryBroker.setPythonInterpreter(Jythonizer.getInstance());
        } catch (Exception e) {
            throw new RuntimeException("Cannot get Python intepretor!", e);
        }
        se.ericsson.commonlibrary.LibraryBroker.initializeLibraries();
    }

    /**
     * @deprecated
     * @param logfilePath
     * @return
     */
    @Deprecated
    public String fetchLogs(final String logfilePath) {
        // implement something to fetch a bunch of logs from the SUT
        // fetchlogs is called when a testcase fails.
        // the logs should include enough information to attach this
        // logfile to a Trouble report
        return "aLogFile.tar.gz";
    }

    /**
     * Gets a given library instance, given its unique library name
     * 
     * @param name
     *            The unique name of the library
     * @return The (already instantiated and setUp) instance of the library
     */
    public OmpLibrary getLibrary(final String name) {
        return libraryBroker.get(name);
    }

    /**
     * Gets a given library instance. Example: sut.getLibrary(OsLib.class);
     * 
     * @param <T>
     *            Library class
     * @param t
     * @return Library instance
     */
    @SuppressWarnings("unchecked")
    public <T> T getLibrary(final Class<T> t) {
        String name = t.getSimpleName();
        return (T) libraryBroker.get(name);
    }

    /**
     * Disposes the SUT
     */
    public void dispose() {
        libraryBroker.dispose();
    }

    /**
     * Return the XMLConfiguration.
     * 
     * @return xml configuration
     */
    public XMLConfiguration getXmlConfiguration() {
        return xmlConfiguration;
    }

    /**
     * Returns the associated string value for the given key value as defined in the SUT configuration XML file. If no
     * configuration xml file is defined or the key does not map null is returned.
     * 
     * @param key
     *            The configuration key.
     * @return The associated string.
     */
    public String getConfigDataString(String key) {
        if (xmlConfiguration != null) {
            return xmlConfiguration.getString(key);
        } else {
            return null;
        }
    }

    /**
     * Returns the associated string value for the given key value as defined in the SUT configuration XML file. If no
     * configuration xml file is defined or the key does not map null is returned. Lists are defined with ',' as
     * delimiter char in the conf file.
     * 
     * @param key
     *            The configuration key.
     * @return The associated string.
     */
    public String[] getConfigDataStringArray(String key) {
        if (xmlConfiguration != null) {
            try {
                return xmlConfiguration.getStringArray(key);
            } catch (ConversionException ce) {
                System.err.println("Key does not map to a String/List of Strings: " + ce.toString());
                return null;
            }
        } else {
            return null;
        }
    }

    @Deprecated
    /**
     * A blade in the system can be represented in 3 ways:
     * 
     * Get the subrack from the string representing a blade/hostname
     * 
     * @param blade
     * @return subrack
     * @deprecated for CBA 2010-08-12, use methods in libraries instead, will be removed 2012-01-01
     */
    public int getSubrack(final String blade) {
        final String[] parts = parseName(blade);
        final int subrack = new Integer(parts[1]).intValue();
        return subrack;
    }

    @Deprecated
    /**
     * Get the slot from the string representing a blade/hostname
     * 
     * @param blade
     * @return slot 
     * @deprecated for CBA 2010-08-12, use methods in libraries instead, will be removed 2012-01-01
     */
    public int getSlot(final String blade) {
        final String[] parts = parseName(blade);
        final int slot = new Integer(parts[2]).intValue();
        return slot;
    }

    @Deprecated
    /**
     * Get the type from the string representing a blade/hostname
     * Until we ask the system about this it is only relevant with a
     * hostname as parameter
     * @param blade
     * @return slot 
     * @deprecated for CBA 2010-08-12, use methods in libraries instead, will be removed 2012-01-01
     */
    public String getType(final String blade) {
        final String[] parts = parseName(blade);
        final String type = parts[0].toString();
        return type;
    }

    private String[] parseName(String node) {
        String[] result = new String[4];
        result[3] = "-";
        Pattern p = Pattern.compile("(\\D+)[_|-](\\d+)([_|-])(\\d+)");
        Matcher m = p.matcher(node);
        if (m.matches()) {
            result[0] = m.group(1);
            result[1] = m.group(2);
            result[2] = m.group(4);
            result[3] = m.group(3);
        }
        return result;
    }

    @Deprecated
    /**
     * Get the type from the subrack/slot
     * @param bsubrack
     * @param slot
     * @return "SC" or "PL" 
     * @deprecated for CBA 2010-08-12, use methods in libraries instead, will be removed 2012-01-01
     */
    public String getType(final int subrack, final int slot) {
        String type = getSc();
        if (slot > 2) {
            type = getPl();
        }
        return type;
    }

    @Deprecated
    /**
     * Get the 'other SC' string representing a blade/hostname
     * 
     * @param blade
     * @return 'other sc'
     * @deprecated for CBA 2010-08-12, use methods in libraries instead, will be removed 2012-01-01
     */
    public String getOtherSc(final String blade) {

        String type = getType(blade);
        int subrack = getSubrack(blade);
        int slot = getSlot(blade);
        if (slot == 1) {
            slot = 2;
        } else {
            slot = 1;
        }
        final String result = type + getSeparator() + subrack + getSeparator() + slot;
        return result;
    }

    @Deprecated
    /**
     * Get the 'blade' string from the subrack and slot
     * 
     * @param subrack
     * @param slot
     * @return "blade_x_y"
     * @deprecated for CBA 2010-08-12, use methods in libraries instead, will be removed 2012-01-01
     */
    public String getBlade(int subrack, int slot) {
        return "blade" + getSeparator() + subrack + getSeparator() + slot;
    }

    @Deprecated
    /**
     * Get the hostname string from the subrack and slot
     * 
     * @param subrack
     * @param slot
     * @return "SC_x_y" or "PL_x_y"
     * @deprecated for CBA 2010-08-12, use methods in libraries instead, will be removed 2012-01-01
     */
    public String getHostname(int subrack, int slot) {
        String type = getSc();
        if (slot > 2) {
            type = getPl();
        }
        return type + getSeparator() + subrack + getSeparator() + slot;
    }

    @Deprecated
    /**
     * Get the hostname string from the blade
     * 
     * @param blade_x_y
     * @return "SC_x_y" or "PL_x_y"
     * @deprecated for CBA 2010-08-12, use methods in libraries OsLib located in JCAT_OMP_extensions instead, will be removed 2012-01-01
     */
    public String getHostname(String blade) {
        String type = getSc();
        if (getSlot(blade) > 2) {
            type = getPl();
        }

        return type + getSeparator() + getSubrack(blade) + getSeparator() + getSlot(blade);
    }

    @Deprecated
    /**
     * Is the blade a PL
     * 
     * @param subrack
     * @param slot
     * @return true if blade is a PL
     * @deprecated for CBA 2010-08-12, use methods in libraries instead, will be removed 2012-01-01
     */
    public boolean isPL(int subrack, int slot) {
        boolean result = false;
        if (slot > 2) {
            result = true;
        }

        return result;
    }

    @Deprecated
    /**
     * Is the blade a SC
     * 
     * @param subrack
     * @param slot
     * @return true if blade is a SC
     * @deprecated for CBA 2010-08-12, use methods in libraries instead, will be removed 2012-01-01
     */
    public boolean isSC(int subrack, int slot) {
        return !isPL(subrack, slot);
    }

    @Deprecated
    /**
     * Reread the hostname separator from server.
     * @deprecated for CBA 2010-08-12, use methods in libraries instead, will be removed 2012-01-01
     */
    public void resetSeparator() {
        this.hostnameSeparator = getSeparatorFromCluster();
    }

    @Deprecated
    /**
     * Return the blade/hostname separator. If hostnameSeparator flag is set
     * when starting JVM, its value will be used. Otherwise this class will go
     * into the server and get the separator automatically.
     * 
     * @return the value of hostnameSeparator flag or the one currently used in
     *         the system
     * @deprecated for CBA 2010-08-12, use methods in libraries instead, will be removed 2012-01-01
     */
    public String getSeparator() {
        String separator = System.getProperty("hostnameSeparator");
        if (separator != null) {
            return separator;
        } else {
            if (this.hostnameSeparator == null) {
                resetSeparator();
            }
            return this.hostnameSeparator;
        }
    }

    @Deprecated
    public String getSc() {
        return "SC";
    }

    @Deprecated
    public String getPl() {
        return "PL";
    }

    /**
     * Get the size of the SUT. (number of blades)
     * 
     * @return size
     */
    public int getSutSize() {
        return Integer.parseInt(this.getConfigDataString("physical_size"));
    }

    /**
     * Read the hostname separator from server.
     * 
     * @return Hostname separator(- or _)
     */
    private String getSeparatorFromCluster() {
        final String username = getConfigDataString("user");
        final String password = getConfigDataString("pwd");
        String ip1full = getConfigDataString("ipAddress.ctrl.ctrl1");
        String ip2full = getConfigDataString("ipAddress.ctrl.ctrl2");
        String ip1 = ip1full;
        String ip2 = ip2full;
        int ip1Port = 22;
        int ip2Port = 22;

        System.out.println("Controller IP addresses: " + ip1 + " " + ip2);

        if (ip1.contains(":")) {
            ip1 = ip1.split(":")[0];
            ip1Port = Integer.parseInt(ip1full.split(":")[1]);
        }
        if (ip2.contains(":")) {
            ip2 = ip2.split(":")[0];
            ip2Port = Integer.parseInt(ip2full.split(":")[1]);
        }

        String ip = null;
        int port = 0;

        System.out.println("Trying ip address: " + ip1full);
        if (ip1 != null && isPortOpen(ip1, ip1Port)) {
            ip = ip1;
            port = ip1Port;
        } else {
            System.out.println("Trying ip address: " + ip2full);
            if (ip2 != null && isPortOpen(ip2, ip2Port)) {
                ip = ip2;
                port = ip2Port;
            }
        }

        if (ip == null) {
            System.err.println("Cannot get separator! No controller is available!");
            return null;
        }

        Ssh2Session s = new Ssh2Session(ip, port, username, password);
        s.setRawOutput(false);
        s.openSshShell();
        String command = "hostname";
        String separator = null;
        try {
            String result = s.sendCommand(command);
            String[] parts = parseName(result);
            separator = parts[3];
            System.out.println("Hostname (" + result + ") separator read from server: " + separator);
        } catch (IOException e) {
            System.err.println("Cannot get separator! " + e.getMessage());
        }
        s.disconnect();
        return separator;
    }

    private boolean isPortOpen(final String ip, final int port) {
        Socket myClient;
        DataInputStream input;
        boolean isOpen = false;

        try {
            myClient = new Socket(ip, port);
            input = new DataInputStream(myClient.getInputStream());
            input.close();
            myClient.close();
            isOpen = true;
        } catch (final Exception e) {
            isOpen = false;
        }
        return isOpen;
    }

    public static OmpSut getOmpSut() {
        if (sut == null) {
            sut = readOmpSut();
        }
        return sut;
    }

    private static OmpSut readOmpSut() {
        XMLConfiguration xmlConfiguration = null;
        SystemConfiguration systemConfiguration = new SystemConfiguration();

        OmpTestInfo.parseProperties(systemConfiguration);

        // Read SUT configuration from file and populate SUT
        if (OmpTestInfo.getSutConfigurationFile() != null) {
            try {
                xmlConfiguration = new XMLConfiguration(OmpTestInfo.getSutConfigurationFile());
            } catch (final ConfigurationException cex) {
                logger.info("SUT configuration data not readable", cex);
            }
        }

        OmpSut ompSut = new OmpSut("OMP Sut", xmlConfiguration);
        return ompSut;
    }
}
