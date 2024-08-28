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
package se.ericsson.jcat.omp.library;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.Map;

import se.ericsson.jcat.omp.fw.OmpLibraryException;

/**
 * The purpose of this class is to define the Java API methods for Python library ssh_lib.
 */
public interface TestappLib {
    String setConfiguration(String instance, String profile, int intensity, String logLevel, int tcpConn, int tcpTime)
            throws OmpLibraryException;

    String setConfigurationString(String instance, String profile) throws OmpLibraryException, FileNotFoundException,
            IOException;

    String setConfigurationFile(String instance, String fileName) throws OmpLibraryException, FileNotFoundException,
            IOException;

    String setConfiguration() throws OmpLibraryException;

    String getConfiguration(String instance) throws OmpLibraryException;

    String getConfiguration() throws OmpLibraryException;

    String getStatistics(String instance) throws OmpLibraryException;

    String getStatistics() throws OmpLibraryException;

    Map<String, String> getTotalStatistics(String instance) throws OmpLibraryException;

    Map<String, String> getTotalStatistics() throws OmpLibraryException;

    String getActualIntensity(String instance, int interval) throws OmpLibraryException;

    String getActualIntensity() throws OmpLibraryException;

    String getConfiguredIntensity(String instance) throws OmpLibraryException;

    String getConfiguredIntensity() throws OmpLibraryException;

    String resetStatistics(String instance) throws OmpLibraryException;

    String resetStatistics() throws OmpLibraryException;

    String stopTraffic() throws OmpLibraryException;

    boolean isTrafficOk(Map<String, String> tblStart, Map<String, String> tblEnd, double proc, double timeout,
            double fail);

    boolean isStable();

    boolean isStable(int intensity);

    boolean isStable(int intensity, double intensityDeviation);

    boolean isStable(double loss, double timeout, double fail);

    boolean isStable(double loss, double timeout, double fail, int intensity);

    boolean isStable(final double loss, final double timeout, final double fail, final int intensity, int sleep);

    boolean waitUntilStable(int timeoutSeconds);

    boolean waitUntilStable(int timeoutSeconds, int intensity);

    boolean waitUntilStable(int timeoutSeconds, int intensity, double intensityDeviation);

    boolean isTrafficStopped(int sleepTime);

    Map<String, Map<String, String>> getTestAppHAState() throws OmpLibraryException;

    Map<String, Map<String, String>> getTestAppHAState(String currentHAState) throws OmpLibraryException;

}
