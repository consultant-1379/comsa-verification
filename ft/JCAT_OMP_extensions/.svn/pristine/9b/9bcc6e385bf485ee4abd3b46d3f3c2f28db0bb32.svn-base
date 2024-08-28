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

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import org.apache.log4j.Logger;

import se.ericsson.commonlibrary.CommonLibrary;
import se.ericsson.commonlibrary.CommonLibraryDataProvider;
import se.ericsson.jcat.fw.utils.Ssh2Session;
import se.ericsson.jcat.omp.fw.OmpLibraryException;
import se.ericsson.jcat.omp.util.Tools;

/**
 * Implements the Java API methods for Python library HpNetwork_lib.
 */
public class HpNetworkLibImpl implements HpNetworkLib {

    private static Logger logger = Logger.getLogger(HpNetworkLibImpl.class);

    private List<Class<? extends CommonLibrary>> l;
    private HpNetworkLibDataProvider data;

    public HpNetworkLibImpl() {
        l = new ArrayList<Class<? extends CommonLibrary>>();
    }

    /**
     * Return runtime dependencies.
     */
    public String[] getRuntimeDependencies() {
        return new String[] { "LoggerLib", "TargetDataLib" };
    }

    /**
     * Return setup dependencies.
     */
    public String[] getSetupDependencies() {
        return new String[] { "LoggerLib", "TargetDataLib" };
    }

    /**
     * Return information of which VC is Active VC.
     * 
     * @param target
     *            - VC address
     * @return Result message, True or False.
     * @throws OmpLibraryException
     * @throws IOException
     */
    public boolean getActiveVcStatus() throws OmpLibraryException {
        boolean status = false;
        Ssh2Session vCSession = null;
        vCSession = Tools.getSshSession(data.getVcAddressArray()[0], data.getVcUserName(), data.getVcPassword());
        if (vCSession.getSessionData().contains("not found")) {
            logger.info("Unable to get session from " + data.getVcAddressArray()[0]
                    + ". Not a valid Virtual Connect IP address.");
        } else {

            String result;
            try {
                result = vCSession.sendCommand("show interconnect");

                logger.info("The result of command: " + result);
                for (String line : result.split("\n")) {
                    if (line.contains("Primary")) {
                        String[] results = vCSession.sendCommand("show interconnect "
                                                                         + line.substring(0, line.indexOf(":") + 2)).split("\n");
                        if (results[0].contains(line.subSequence(0, line.indexOf(":") + 2))
                                && results[5].contains("Primary")) {
                            logger.info("IP address of Active VC is "
                                    + results[12].substring(results[12].indexOf(":") + 1).trim());
                        }
                    }
                }

                status = true;
            } catch (IOException e) {
                logger.info("Unable to get Active VC");
                e.printStackTrace();
            }

        }
        return status;

    }

    public boolean virtualConnectDown() throws OmpLibraryException {
        return false;
    }

    public boolean virtualConnectReset() throws OmpLibraryException {
        return false;
    }

    public boolean virtualConnectUp() throws OmpLibraryException {
        return false;
    }

    public boolean onboadAdminShutdown() throws OmpLibraryException {
        return false;
    }

    public boolean onboadAdminReset() throws OmpLibraryException {
        return false;
    }

    public boolean onboadAdminUp() throws OmpLibraryException {
        return false;
    }

    public HpNetworkLibDataProvider getLibraryDataProvider() {
        return data;
    }

    @Override
    public Class<? extends CommonLibrary> getLibraryInterface() {
        return HpNetworkLib.class;
    }

    @Override
    public String getUniqueIdentifier() {
        return "RDA HP Network lib";
    }

    @Override
    public void initialize() {
    }

    @Override
    public void shutdown() {
    }

    @Override
    // OMPLib and CommonLib
    public List<Class<? extends CommonLibrary>> getRuntimeDependencyList() {
        return l;
    }

    @Override
    public List<Class<? extends CommonLibrary>> getSetupDependencyList() {
        return l;
    }

    @Override
    public void setLibraryDataProvider(CommonLibraryDataProvider data) {
        this.data = (HpNetworkLibDataProvider) data;
    }

}
