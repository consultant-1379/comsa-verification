package se.ericsson.jcat.omp.fw;

import java.util.ArrayList;
import java.util.Iterator;

import org.apache.commons.configuration.Configuration;
import org.apache.log4j.Logger;

import se.ericsson.jcat.fw.utils.TestInfo;

/**
 * The purpose of this class is ... TODO javadoc for class OmpTestInfo
 */
public class OmpTestInfo extends TestInfo {
    /* Create logger */
    private static final Logger logger = Logger.getLogger(OmpTestInfo.class);

    /* Fields holding OMP specific framework info */
    private static String sutConfigurationFile = null;
    private static String versionsConfigFile   = null;

    private static ArrayList<String> javaLibraries = new ArrayList<String>();

    private static ArrayList<String> pythonLibraries = new ArrayList<String>();
    
    private static boolean isInitialized = false;
    
    /**
     * Only for unit test
     */
    protected static void resetInitializedFlag(){
        isInitialized = false;
    }
    
    @SuppressWarnings("unchecked")
    public static void parseProperties(final Configuration configuration) {
    	
    	if (isInitialized) {
    		logger.info("OmpTestInfo has already been initialized. Skip parsing");
    		return;
    	}
    	
        // Parse JCAT Framework Properties

        final String dbProperties = configuration.getString("dbprop");
        if(dbProperties != null) {
            TestInfo.setDbProperties(dbProperties);
        }

        final String groupID = configuration.getString("groupID");
        if(groupID != null) {
            TestInfo.setGroupId(groupID);
        }

        final String testType = configuration.getString("testType");
        if(testType != null) {
            TestInfo.setTestType(testType);
        }

        final String versionMajor = configuration.getString("SutVersionMajor");
        if(versionMajor != null) {
            TestInfo.setSutVersionMajor(versionMajor);
        }

        final String versionMinor = configuration.getString("SutVersionMinor");
        if(versionMinor != null) {
            TestInfo.setSutVersionMinor(versionMinor);
        }

        // General JCAT properties that might be set in a properties file, or in
        // system property,
        // but which must be readable in System property

        final String name = configuration.getString("name");
        if(name != null) {
            System.setProperty("name", name);
        }

        final String python_path = configuration.getString("python.path");
        if(python_path != null) {
            System.setProperty("python.path", python_path);
        }

        final String catroot = configuration.getString("catroot");
        if(catroot != null) {
            System.setProperty("catroot", catroot);
        }

        final String log4j_configuration =
                configuration.getString("log4j.configuration");
        if(log4j_configuration != null) {
            System.setProperty("log4j.configuration", log4j_configuration);
        }

        final String logdir = configuration.getString("logdir");
        if(logdir != null) {
            System.setProperty("logdir", logdir);
        }

        final String extroot = configuration.getString("extroot");
        if(extroot != null) {
            System.setProperty("extroot", extroot);
        }

        // Parse OMP Framework Properties
        sutConfigurationFile = configuration.getString("sutConfigurationFile");

        // Parse Products/Versions fileversionsConfigFile
        versionsConfigFile = configuration.getString("versionsConfigFile");

        // Parse properties for Java & Python libraries
        final Configuration javalibconfig =
                configuration.subset("se.ericsson.jcat.omp.fw");
        final Iterator<String> fwKeys = javalibconfig.getKeys();
        while(fwKeys.hasNext()) {
            final String next = fwKeys.next();
            if(next.startsWith("JavaLibrary:"))
                javaLibraries.add(next.substring(new String("JavaLibrary;")
                        .length(), next.length()));
            if(next.startsWith("PythonLibrary:"))
                pythonLibraries.add(next.substring(new String("PythonLibrary;")
                        .length(), next.length()));
        }

        isInitialized = true;
    }

    /**
     * Gets the list of configured java libraries
     * 
     * @return
     */
    public static String[] getJavaLibraries() {
        return javaLibraries.toArray(new String[0]);
    }

    /**
     * Gets the list of configured java libraries
     * 
     * @return
     */
    public static String[] getPythonLibraries() {
        return pythonLibraries.toArray(new String[0]);
    }

    public static void clearLibraries() {
        javaLibraries = new ArrayList<String>();
        pythonLibraries = new ArrayList<String>();
    }

    /**
     * Sets the sutConfigurationFile property.
     * 
     * @param value state
     */
    public static void setSutConfigurationFile(final String value) {
        sutConfigurationFile = value;
    }

    /**
     * Gets the value of boolean.
     * 
     * @return sutConfigurationFile path
     */
    public static String getSutConfigurationFile() {
        return sutConfigurationFile;
    }
    
    /**
     * Gets the value of boolean.
     * 
     * @return sutConfigurationFile path
     */
    public static String getVersionsConfigFile() {
        return versionsConfigFile;
    }
}
