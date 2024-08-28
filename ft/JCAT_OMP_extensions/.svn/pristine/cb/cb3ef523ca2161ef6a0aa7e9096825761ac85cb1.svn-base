package se.ericsson.jcat.omp.library;

import java.util.HashMap;
import java.util.Map;

import org.easymock.EasyMock;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.powermock.api.easymock.PowerMock;

import se.ericsson.jcat.omp.fw.OmpLibraryException;
import se.ericsson.jcat.omp.fw.OmpSut;
import se.ericsson.jcat.omp.library.OsLib.DrbdState;
import se.ericsson.jcat.omp.util.Tools;

public class OsLibTest {

    private OsLibImpl os;
    private SshLib ssh;

    @Before
    public void setUp() throws NoSuchMethodException, SecurityException, OmpLibraryException {
        ssh = PowerMock.createMock(SshLibImpl.class,
                                   SshLibImpl.class.getMethod("sendCommand", String.class, int.class, int.class),
                                   SshLibImpl.class.getMethod("sendCommand", String.class));
        EasyMock.expect(ssh.sendCommand("hostname")).andReturn("SC-2-1").anyTimes();
        EasyMock.expect(ssh.sendCommand("hostname", 2, 1)).andReturn("SC-2-1").anyTimes();
        EasyMock.expect(ssh.sendCommand("hostname", 2, 2)).andReturn("SC-2-2").anyTimes();
        EasyMock.expect(ssh.sendCommand("hostname", 2, 3)).andReturn("PL-2-3").anyTimes();
        EasyMock.expect(ssh.sendCommand("hostname", 2, 4)).andReturn("PL-2-4").anyTimes();

        OmpSut sut = PowerMock.createMock(OmpSut.class, OmpSut.class.getMethod("getLibrary", String.class));
        EasyMock.expect(sut.getLibrary("SshLib")).andReturn((SshLibImpl) ssh).anyTimes();
        PowerMock.replay(sut);
        ssh = (SshLib) sut.getLibrary("SshLib");
        os = new OsLibImpl(sut);
    }

    private String readResource(String file) {
        return Tools.extractResourceFileAndReadContent(file, this.getClass());
    }

    @Test
    public void testHostname() throws OmpLibraryException {
        PowerMock.replay(ssh);
        Assert.assertTrue("hostname is not correct", os.getHostname(2, 1).equals(ssh.getHostname(2, 1)));
    }

    @Test
    public void testDrbdState() throws OmpLibraryException {
        EasyMock.expect(ssh.sendCommand("cat /proc/drbd", 2, 1)).andReturn(readResource("sc1drbd.txt")).anyTimes();
        EasyMock.expect(ssh.sendCommand("cat /proc/drbd", 2, 2)).andReturn(readResource("sc2drbd.txt")).anyTimes();
        PowerMock.replay(ssh);
        Map<String, DrbdState> stateMap = new HashMap<String, DrbdState>();
        String firstController = ssh.getHostname(2, 1);
        String secondController = ssh.getHostname(2, 2);
        stateMap.put(firstController, DrbdState.PRIMARY_SECONDARY);
        stateMap.put(secondController, DrbdState.SECONDARY_PRIMARY);
        Assert.assertTrue("DRBD status not ready", os.waitFordrbdState(stateMap, 2));
    }

    @Test
    public void testLiveNodes() throws OmpLibraryException {
        EasyMock.expect(ssh.sendCommand("tipc-config -n")).andReturn(readResource("tipc.txt")).anyTimes();
        PowerMock.replay(ssh);
        String[] nodes = os.getLiveNodes();
        Assert.assertTrue("not 4 nodes alive", nodes.length == 4);
    }

    @Test
    public void testConfiguredNodes() throws OmpLibraryException {
        EasyMock.expect(ssh.sendCommand("cat /cluster/etc/cluster.conf | grep \"^ *node\"")).andReturn(readResource("livenodes.txt")).anyTimes();
        PowerMock.replay(ssh);
        Map<String, Integer> nodes = os.getConfiguredNodes2();
        Assert.assertTrue("not 4 nodes found", nodes.size() == 4);
    }
}
