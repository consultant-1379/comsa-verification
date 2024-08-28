package se.ericsson.jcat.omp.library;

import java.io.File;
import java.io.IOException;
import java.util.List;

import org.python.core.PyDictionary;

import se.ericsson.commonlibrary.CommonLibrary;
import se.ericsson.commonlibrary.CommonLibraryDataProvider;
import se.ericsson.jcat.omp.fw.OmpLibrary;
import se.ericsson.jcat.omp.fw.OmpLibraryException;
import se.ericsson.jcat.omp.fw.OmpSut;
import se.ericsson.jcat.omp.util.Tools;

public class MockSshLib extends OmpLibrary implements SshLib {

    @Override
    public CommonLibraryDataProvider getLibraryDataProvider() {
        return null;
    }

    @Override
    public Class<? extends CommonLibrary> getLibraryInterface() {
        return null;
    }

    @Override
    public List<Class<? extends CommonLibrary>> getRuntimeDependencyList() {
        return null;
    }

    @Override
    public List<Class<? extends CommonLibrary>> getSetupDependencyList() {
        return null;
    }

    @Override
    public String getUniqueIdentifier() {
        return null;
    }

    @Override
    public void initialize() {

    }

    @Override
    public void setLibraryDataProvider(CommonLibraryDataProvider arg0) {

    }

    @Override
    public void shutdown() {

    }

    @Override
    public PyDictionary getTargetData() {
        return null;
    }

    @Override
    public String sendCommand(String command, int subrack, int blade) throws OmpLibraryException {
        if (command.startsWith("hostname")) {
            return this.getHostname(subrack, blade);
        }
        if (command.startsWith("cmw-status ")) {
            return cmwStatus(command);
        }
        if (command.contains("which cmw-immconfig-export")) {
            return "";
        }
        if (command.contains("cmw-immconfig-export")) {
            return cmwImmconfigExport();
        }
        return null;
    }

    private String cmwImmconfigExport() {
        createTmpTar("cmw-immconfig-export.txt", "immdata.xml");
        return "";
    }

    private String cmwStatus(String command) {
        if (command.contains("-v") && command.contains("node")) {
            createTmpTar("cmw-status-node.txt", "cmw-status.tmp");
        } else if (command.contains("-v") && command.contains("comp")) {
            createTmpTar("cmw-status-comp.txt", "cmw-status.tmp");
        } else if (command.contains("-v") && command.contains("csiass")) {
            createTmpTar("cmw-status-csiass.txt", "cmw-status.tmp");
        } else if (command.contains("-v") && command.contains("siass")) {
            createTmpTar("cmw-status-siass.txt", "cmw-status.tmp");
        }
        return "";
    }

    private void createTmpTar(String resourceFile, String tmpFile) {
        File target = new File("target");
        File f = new File(target.getAbsoluteFile() + "/" + tmpFile + ".tmp");
        if (f.exists())
            f.delete();
        Tools.extractResourceFile(resourceFile, this.getClass(), f, false);
        // File ftar = new File(target.getAbsoluteFile() + "/" + tmpFile + ".tgz");
        // if (ftar.exists())
        // ftar.delete();
        // try {
        // Tools.runCommandLocal("tar -C " + f.getParent() + " -czf " + ftar.getAbsolutePath() + " " + f.getName());
        // } catch (IOException e) {
        // e.printStackTrace();
        // } catch (InterruptedException e) {
        // e.printStackTrace();
        // }
        // ftar.deleteOnExit();
        f.deleteOnExit();
    }

    @Override
    public String sendCommand(String command) throws OmpLibraryException {
        return sendCommand(command, 2, 1);
    }

    @Override
    public String sendCommandNbi(String command) throws OmpLibraryException {
        return null;
    }

    @Override
    public String setTimeout(int timeout, int subrack, int slot) throws OmpLibraryException {
        return "";
    }

    @Override
    public String setTimeout(int timeout) throws OmpLibraryException {
        return "";
    }

    @Override
    public String getTimeout(int subrack, int slot) throws OmpLibraryException {
        return "1";
    }

    @Override
    public String sendRawCommand(String host, String command, String user, String password, int timeout)
            throws OmpLibraryException {
        return null;
    }

    @Override
    public String loginTest(int subrack, int slot, int attempts, String user, String pwd) throws OmpLibraryException {
        return null;
    }

    @Override
    public String bindAddresses(String blade, int localPort, int destinationPort) throws OmpLibraryException {
        return null;
    }

    @Override
    public String readFile(String blade, int localPort, String fileName, String request) throws OmpLibraryException {
        return null;
    }

    @Override
    public String remoteCopy(String file, String destination, int timeout, int numberOfRetries)
            throws OmpLibraryException {
        return null;
    }

    @Override
    public String remoteCopyFrom(String file, String destination, int timeout) throws OmpLibraryException {
        File target = new File("target");
        File[][] files = new File[][] {
                { new File(target.getAbsoluteFile() + "/cmw-status.tmp.tmp"),
                        new File(target.getAbsoluteFile() + "/cmw-status.tmp") },
                { new File(target.getAbsoluteFile() + "/immdata.xml.tmp"),
                        new File(target.getAbsoluteFile() + "/immdata.xml") } };
        try {
            for (File[] fset : files) {
                Tools.runCommandLocal("cp -f " + fset[0].getAbsolutePath() + " " + fset[1].getAbsolutePath());
                fset[0].deleteOnExit();
                fset[1].deleteOnExit();
            }
        } catch (IOException e) {
            e.printStackTrace();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        return "";
    }

    @Override
    public String sCopy(String file, String host, String destpath, String user, String passwd, int timeout)
            throws OmpLibraryException {
        return null;
    }

    @Override
    public void tearDownHandles() {

    }

    @Override
    public void setConfig(int subrack, int slot, int number) {

    }

    @Override
    public void setConfig(int subrack, int slot, int number, boolean useVipOam) {

    }

    @Override
    public boolean setConfig() {
        return false;
    }

    @Override
    public boolean setConfig(boolean useVipOam) {
        return false;
    }

    @Override
    public int[] getConfig() {
        return null;
    }

    @Override
    public boolean getUseVipOam() {
        return false;
    }

    @Override
    public boolean waitForConnection(int subrack, int slot, int timeout) {
        return false;
    }

    @Override
    public boolean waitForNoConnection(int subrack, int slot, int timeout) {
        return false;
    }

    @Override
    public String getHostname(int subrack, int blade) throws OmpLibraryException {
        return subrack + "-" + blade;
    }

    @Override
    public String getInternalConnectionCommand() {
        return null;
    }

    @Override
    public String getInternalBridgeCommand() {
        return null;
    }

    @Override
    public void resetInternalConnectionCommand() {

    }

    @Override
    public void determineInternalConnectionCommandNextTime() {

    }

    @Override
    public void setSut(OmpSut sut) {
    }

    @Override
    public String getName() {
        return null;
    }

    @Override
    public String[] getRuntimeDependencies() {
        return null;
    }

    @Override
    public String[] getSetupDependencies() {
        return null;
    }

}
