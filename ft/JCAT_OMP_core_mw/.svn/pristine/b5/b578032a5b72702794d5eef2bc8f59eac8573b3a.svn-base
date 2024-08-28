package se.ericsson.jcat.omp.library;

import java.util.Map;

import se.ericsson.jcat.omp.fw.OmpLibrary;
import se.ericsson.jcat.omp.fw.OmpLibraryException;
import se.ericsson.jcat.omp.fw.OmpSut;

public class MockOsLib extends OmpLibrary implements OsLib {

    @Override
    public Map<String, DrbdState> getDrbdState() throws OmpLibraryException {
        return null;
    }

    @Override
    public boolean isDrbdState(Map<String, DrbdState> preferdStateMap) throws OmpLibraryException {
        return false;
    }

    @Override
    public Map<String, DrbdState> getUpStateDrbd() throws OmpLibraryException {
        return null;
    }

    @Override
    public boolean waitForDrbdSynch(int subrack, int blade, int timeoutSec) throws OmpLibraryException {
        return false;
    }

    @Override
    public String[] getLiveNodes() throws OmpLibraryException {
        return null;
    }

    @Override
    public Map<String, Integer> getConfiguredNodes2() throws OmpLibraryException {
        return null;
    }

    @Override
    public int getSubrack(String hostname) throws OmpLibraryException {
        return 0;
    }

    @Override
    public int getSlot(String hostname) throws OmpLibraryException {
        return 0;
    }

    @Override
    public String getHostname(int subrack, int slot) throws OmpLibraryException {
        return null;
    }

    @Override
    public int getPid(int subrack, int slot, String process) throws OmpLibraryException {
        return 0;
    }

    @Override
    public int[] getPids(int subrack, int slot, String process) throws OmpLibraryException {
        return null;
    }

    @Override
    public boolean killProcess(int subrack, int slot, int pid) throws OmpLibraryException {
        return false;
    }

    @Override
    public boolean isProcessAlive(int subrack, int slot, String process) throws OmpLibraryException {
        return false;
    }

    @Override
    public void backup(String ip, String user, String password, String scriptPath, String storageUser,
            String storagePassword, String backupIp, String backupStorage) throws OmpLibraryException {

    }

    @Override
    public String[] getCoreDumps() throws OmpLibraryException {
        return null;
    }

    @Override
    public boolean waitFordrbdState(Map<String, DrbdState> preferredDrbdState, int maxTimeSecond)
            throws OmpLibraryException {
        return false;
    }

    @Override
    public String[] getNodeHostnames() throws OmpLibraryException {
        return null;
    }

    @Override
    public String[] getConfiguredNodes() throws OmpLibraryException {
        return null;
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
