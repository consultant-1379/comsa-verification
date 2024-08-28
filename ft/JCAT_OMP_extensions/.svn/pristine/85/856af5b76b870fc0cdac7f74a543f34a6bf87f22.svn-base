package se.ericsson.jcat.omp.library;

import java.io.File;
import java.util.ArrayList;
import java.util.List;

import org.apache.log4j.Logger;

import se.ericsson.jcat.omp.fw.OmpLibrary;
import se.ericsson.jcat.omp.fw.OmpLibraryException;
import se.ericsson.jcat.omp.fw.OmpSut;

public class ServletLibImpl extends OmpLibrary implements ServletLib {
    private static Logger logger = Logger.getLogger(ServletLibImpl.class);
    OmpSut sut = null;
    SshLib ssh = null;
    String user;
    String password;
    String ip;
    String tmpDirectory;

    /**
     * Creates a new instance of <code>ServletLib</code>.
     * 
     * @param sut
     * @throws Exception
     */
    public ServletLibImpl(OmpSut sut) throws Exception {
        setSut(sut);
    }

    /*
     * (non-Javadoc)
     * 
     * @see se.ericsson.jcat.omp.fw.OmpLibrary#setUp()
     */
    public void setUp() {
        ssh = (SshLib) sut.getLibrary("SshLib");
        user = sut.getConfigDataString("user");
        password = sut.getConfigDataString("pwd");
        ip = sut.getConfigDataString("ipAddress.ctrl.ctrl1");
        tmpDirectory = sut.getConfigDataString("MMAS.tmpDirectory");
    }

    /**
     * Returns the unique name of this library.
     */
    public String getName() {
        return "ServletLib";
    }

    /**
     * Method called by LibraryBroker to set the Sut of the library
     */
    public void setSut(OmpSut sut) {
        this.sut = sut;
    }

    /**
     * Returns ServletLib as runtime dependency.
     */
    public String[] getRuntimeDependencies() {
        return new String[] { "LoggerLib", "SshLib", "TargetDataLib" };
    }

    /**
     * Returns ServletLib as setup dependency.
     */
    public String[] getSetupDependencies() {
        return new String[] { "LoggerLib", "SshLib", "TargetDataLib" };
    }

    /**
     * Installs an application
     * 
     * @param applicationArchivePath
     *            path where archive can be found
     * @param applicationArchiveFile
     *            name of archive
     * @param cluster
     *            name of cluster where the application should be installed
     * @throws OmpLibraryException
     */
    public void install(File applicationArchive, String cluster) throws OmpLibraryException {
        String applicationName = applicationArchive.getName().substring(0, applicationArchive.getName().length() - 4);
        File targetApplicationArchive = new File(tmpDirectory + applicationArchive.getName());

        logger.info("Check to see if the application is already installed.");

        if (isInstalled(applicationName)) {
            throw new OmpLibraryException("Application is already installed.");
        }

        logger.info("Make a directory on the system.");

        ssh.sendCommand("mkdir -p " + tmpDirectory, true);

        String response = ssh.sendCommand("[ -d " + tmpDirectory + " ];echo $?");
        if (Integer.parseInt(response) != 0) {
            throw new OmpLibraryException("Failed to create directory" + tmpDirectory + ".");
        }

        logger.info("Copy the application archive.");

        ssh.sCopy(applicationArchive.getAbsolutePath(), ip, targetApplicationArchive.getAbsolutePath(), user, password,
                  1000);

        response = ssh.sendCommand("[ -f " + targetApplicationArchive.getAbsolutePath() + " ];echo $?", true);
        if (Integer.parseInt(response) != 0) {
            throw new OmpLibraryException("Copying " + applicationArchive.getAbsolutePath() + " to "
                    + targetApplicationArchive.getAbsolutePath() + " failed.");
        }

        logger.info("Install the SDP on the MMAS.");

        response = ssh.sendCommand("swm -i " + targetApplicationArchive.getAbsolutePath(), true);

        // TODO: Some kind of check here.

        if (!isInstalled(applicationName)) {
            throw new OmpLibraryException("Application " + applicationName + " has not been installed.");
        }

        logger.info("Install the files on all applicable MMAS nodes.");

        int numberOfNodes = 0;

        numberOfNodes = getNumberOfNodes();
        String sc = sut.getHostname(2, 1);
        ssh.setTimeout(300);
        response = ssh.sendCommand("swm -ai " + sc + " " + applicationName, true);

        if (!response.contains("installed on node")) {
            throw new OmpLibraryException(applicationName + " failed to install on node " + sc);
        }

        sc = sut.getHostname(2, 2);
        response = ssh.sendCommand("swm -ai " + sc + " " + applicationName, true);
        if (!response.contains("installed on node")) {
            throw new OmpLibraryException(applicationName + " failed to install on node " + sc);
        }

        // TODO: replace with one loop starting from slot 1
        for (int node = 3; node <= numberOfNodes; node++) {
            String pl = sut.getHostname(2, node);
            response = ssh.sendCommand("swm -ai " + pl + " " + applicationName, true);
            if (!response.contains("installed on node")) {
                throw new OmpLibraryException(applicationName + " failed to install on node " + pl);
            }

        }

        ArrayList<String> archiveFiles = (ArrayList<String>) getArchiveFiles(targetApplicationArchive);

        for (int i = 0; i < archiveFiles.size(); i++) {
            File file = new File(archiveFiles.get(i).trim());

            if (archiveFiles.get(i).contains("Counters")) {
                logger.info("Verify that the PM configuration files are copied to /home/MMAS/.pmcounters.");

                response = ssh.sendCommand("ls -l /home/mmas/.pmcounters | grep " + file.getName() + " | wc -l", true);
                if (Integer.parseInt(response) == 0) {
                    throw new OmpLibraryException("Counter " + file.getName() + " has not been copied.");
                }

            }

            if (archiveFiles.get(i).contains(".ear")) {
                logger.info("Verify that the ear files are copied to the correct cluster.");

                response = ssh.sendCommand("ls -l /home/mmas/.deploy/" + cluster + "| grep "
                        + file.getName().toString() + " | wc -l", true);
                if (Integer.parseInt(response) == 0) {
                    throw new OmpLibraryException("Earfile " + file.getName() + " has not been copied.");
                }
            }

            if (archiveFiles.get(i).contains("startup")) {
                logger.info("Verify that the startup hook files files are copied to /home/mmas/.startup_hooks/<cluster>.");

                response = ssh.sendCommand("ls -l /home/mmas/.startup_hooks/" + cluster + "| grep "
                        + file.getName().toString() + " | wc -l", true);
                if (Integer.parseInt(response) == 0) {
                    throw new OmpLibraryException("Hook " + file.getName() + " has not been copied.");
                }

            }
        }

        logger.info("Update and save the IMM.");

        response = ssh.sendCommand("immSave", true);

    }

    /**
     * @param applicationArchiveFile
     *            the name of the archive used to install this application
     * @param cluster
     *            the cluster to remove application from
     * @throws OmpLibraryException
     */
    public void remove(File applicationArchive, String cluster) throws OmpLibraryException {
        String applicationName = applicationArchive.getName().substring(0, applicationArchive.getName().length() - 4);

        File targetApplicationArchive = new File(tmpDirectory + applicationArchive.getName());

        logger.info("Check to see if the application archive is available in " + tmpDirectory);
        if (!isFileAvailable(targetApplicationArchive.getAbsolutePath())) {
            throw new OmpLibraryException(targetApplicationArchive.getAbsolutePath() + " is not available in "
                    + tmpDirectory);
        }

        logger.info("Check to see if the application is already installed.");
        if (!isInstalled(applicationName)) {
            throw new OmpLibraryException("Application " + applicationName + " has not been installed.");
        }

        logger.info("Remove the application from all applicable MMAS nodes");

        int numberOfNodes = getNumberOfNodes();
        ssh.setTimeout(300);
        String sc = sut.getHostname(2, 1);
        String response = ssh.sendCommand("swm -ar " + sc + " " + applicationName, true);
        if (!response.contains("installed on node")) {
            throw new OmpLibraryException(applicationName + " failed to install on node " + sc);

        }
        sc = sut.getHostname(2, 2);
        response = ssh.sendCommand("swm -ar " + sc + " " + applicationName, true);
        if (!response.contains("installed on node")) {
            throw new OmpLibraryException(applicationName + " failed to install on node " + sc);
        }

        for (int node = 3; node <= numberOfNodes; node++) {
            String pl = sut.getHostname(2, node);
            response = ssh.sendCommand("swm -ar " + pl + " " + applicationName, true);
            if (!response.contains("installed on node")) {
                throw new OmpLibraryException(applicationName + " failed to install on node " + pl);
            }

        }

        sleep(45);

        ArrayList<String> archiveFiles = (ArrayList<String>) getArchiveFiles(targetApplicationArchive);

        for (int i = 0; i < archiveFiles.size(); i++) {
            File file = new File(archiveFiles.get(i).trim());

            if (archiveFiles.get(i).contains("Counters")) {
                logger.info("Verify that the PM configuration files are removed from /home/MMAS/.pmcounters");

                response = ssh.sendCommand("ls -l /home/mmas/.pmcounters | grep " + file.getName().toString()
                        + " | wc -l", true);
                if (Integer.parseInt(response) != 0) {
                    throw new OmpLibraryException("Counter " + file.getName() + " has not been removed.");
                }
            }

            if (archiveFiles.get(i).contains(".ear")) {
                logger.info("Verify that the ear files are removed from the cluster");

                response = ssh.sendCommand("ls -l /home/mmas/.deploy/" + cluster + "| grep "
                        + file.getName().toString() + " | wc -l", true);
                if (Integer.parseInt(response) != 0) {
                    throw new OmpLibraryException("Earfile " + file.getName() + " has not been removed.");
                }
            }

            if (archiveFiles.get(i).contains("startup")) {
                logger.info("Verify that the startup hook files files are removed from /home/mmas/.startup_hooks/"
                        + cluster);
                response = ssh.sendCommand("ls -l /home/mmas/.startup_hooks/" + cluster + "| grep "
                        + file.getName().toString() + " | wc -l", true);
                if (Integer.parseInt(response) != 0) {
                    throw new OmpLibraryException("Hook " + file.getName() + " has not been removed.");
                }
            }
        }

        logger.info("Remove the SDP from the MMAS");
        ssh.sendCommand("swm -r " + applicationName, true);

        if (isInstalled(applicationName)) {
            throw new OmpLibraryException("Application " + applicationName + " has not been removed.");
        }

        logger.info("Remove the SDP package file from the MMAS target machine");
        ssh.sendCommand("rm " + targetApplicationArchive.getAbsolutePath(), true);
        if (isFileAvailable(targetApplicationArchive.getAbsolutePath())) {
            throw new OmpLibraryException(targetApplicationArchive.getAbsolutePath() + " is still available in "
                    + tmpDirectory + ". Removal failed.");
        }

        logger.info("Update and save the IMM");
        ssh.sendCommand("immSave");
    }

    /**
     * Checks to see whether the application is installed or not
     * 
     * @param applicationName
     *            the name of the application
     * @return true if the application is installed
     * @throws OmpLibraryException
     */
    public boolean isInstalled(String applicationName) throws OmpLibraryException {
        logger.info("Verify that the package is installed by listing installed files.");

        String response = ssh.sendCommand("swm -p| grep " + applicationName + "| wc -l", true);

        if (Integer.parseInt(response) > 0) {
            return true;
        } else {
            return false;
        }
    }

    /**
     * Checks to see if a certain file is on the system
     * 
     * @param filePath
     *            the path and the name of the file
     * @return true if the file is available
     * @throws OmpLibraryException
     */
    private boolean isFileAvailable(String filePath) throws OmpLibraryException {
        String response = ssh.sendCommand("[ -f " + filePath + " ];echo $?", true);

        if (Integer.parseInt(response) == 0) {
            return true;
        } else {
            return false;
        }
    }

    /**
     * Opens an archive and lists the files.
     * 
     * @param archivePath
     *            the path to the archive
     * @param archiveFileName
     *            the archive file
     * @return a list of files
     * @throws OmpLibraryException
     */
    private List<String> getArchiveFiles(File archive) throws OmpLibraryException {
        List<String> archiveFiles = new ArrayList<String>();
        ssh.setTimeout(300);
        String response = ssh.sendCommand("tar -tzf " + archive.getAbsolutePath(), true);

        String[] result = response.split("\\n");

        for (int x = 0; x < result.length; x++)
            archiveFiles.add(result[x]);

        return archiveFiles;
    }

    /**
     * Bad design, this helper is duplicated in MMASLibImpl. Reports the number of configured nodes.
     * 
     * @return The number of nodes this system consists of.
     * @throws OmpLibraryException
     */
    private int getNumberOfNodes() throws OmpLibraryException {
        int numberOfNodes = 0;

        try {
            numberOfNodes = Integer.valueOf(ssh.sendCommand("grep \\'^node .*\\' /cluster/etc/cluster.conf | wc -l",
                                                            true));
        } catch (NumberFormatException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }

        return numberOfNodes;
    }

    public static void sleep(int sec) {

        try {
            Thread.sleep(sec * 1000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

}
