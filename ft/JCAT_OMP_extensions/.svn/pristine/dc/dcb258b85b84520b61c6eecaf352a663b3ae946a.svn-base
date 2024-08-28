package se.ericsson.jcat.omp.fw;

import java.io.File;
import java.text.Format;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Iterator;

import junit.framework.Test;

import org.apache.commons.configuration.ConfigurationException;
import org.apache.commons.configuration.PropertiesConfiguration;
import org.apache.commons.configuration.SystemConfiguration;
import org.apache.commons.configuration.XMLConfiguration;
import org.apache.log4j.Logger;

import se.ericsson.jcat.fw.NonUnitFrameworkTestSetup;
import se.ericsson.jcat.fw.SUTHolder;
import se.ericsson.jcat.fw.utils.TestInfo;

/**
 * The purpose of this class is ... TODO javadoc for class OmpTestSetup
 */
@Deprecated
@SuppressWarnings("unchecked")
public class OmpTestSetup extends NonUnitFrameworkTestSetup {
    private static final Logger logger = Logger.getLogger(OmpTestSetup.class);

    private static String PROPERTIES_FILENAME = "jcat_omp_extensions.properties";

    static {
        try {
            // Check all properties in the properties file to see if they are
            // already "overridden"
            final SystemConfiguration systemConfiguration = new SystemConfiguration();

            final PropertiesConfiguration propertiesConfiguration = new PropertiesConfiguration(PROPERTIES_FILENAME);
            final Iterator<String> keyIterator = propertiesConfiguration.getKeys();
            while (keyIterator.hasNext()) {
                final String key = keyIterator.next();
                if (systemConfiguration.getProperty(key) != null) {
                    propertiesConfiguration.clearProperty(key);
                }
            }
            SystemConfiguration.setSystemProperties(propertiesConfiguration);
        } catch (final ConfigurationException ce) {
            // Assume the file not found, and thats ok - all properties are
            // presumably set via System Properties instead
        }

    }

    public OmpTestSetup(final Test testName) {
        // TODO - Implement getIsDumpName private static method
        super(testName, getSoftwareName());
        /*
         * The line below is removed according to teamforge tracker artf21169.
         * Logger.getRootLogger().setLevel(Level.INFO);
         */
    }

    public void setUp() {
        // eanmatt - Where do we want to do this, here?
        // move the created info.out to the proper directory

        // Properties already read from Properties file when class loaded, and
        // converted to System Properties

        // Read System Properties using Commons Configuration and populate
        // OmpTestInfo. System properties read after properties file, so that
        // System properties override.

        SUTHolder.getInstance().zones = new OmpSut[1];
        SUTHolder.getInstance().zones[0] = OmpSut.getOmpSut();

        moveInfoFile();

        // eanmatt - Moved this to last.
        super.setUp();
    }

    private void moveInfoFile() {
        final File info_file = new File(TestInfo.getOriginalLogDir() + "/info.out");
        final File destination_dir = new File(TestInfo.getLogDir());
        final boolean success_move = info_file.renameTo(new File(destination_dir, info_file.getName()));
        if (!success_move) {
            System.out.println("Error: Could not move " + info_file.getAbsolutePath() + " to "
                    + destination_dir.getAbsolutePath());
        }
    }

    /**
     * 
     */
    public void setXMLConfiguration() {

        @SuppressWarnings("unused")
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

        moveInfoFile();
    }

    public void superSetup() {
        super.setUp();
    }

    public void tearDown() {

        logger.info("OmpTestSetup::tearDown");
        OmpTestInfo.clearLibraries();

        // Call tear down in super
        super.tearDown();

    }

    /*
     * Fetches the software name
     */
    private static String getSoftwareName() {
        String dump = "Dump";

        Format formatter;
        formatter = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        final Date date = new Date();

        dump = dump + " " + formatter.format(date);

        return dump;
    }

}
