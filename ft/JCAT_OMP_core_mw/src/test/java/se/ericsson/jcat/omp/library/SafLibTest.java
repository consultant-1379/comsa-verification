package se.ericsson.jcat.omp.library;

import java.io.File;
import java.util.Map;

import org.junit.AfterClass;
import org.junit.Assert;
import org.junit.BeforeClass;
import org.junit.Test;

import se.ericsson.jcat.fw.utils.TestInfo;
import se.ericsson.jcat.omp.fw.MockSut;
import se.ericsson.jcat.omp.fw.OmpLibraryException;

/**
 * The test expect the following commandline output files: <br />
 * cmw-immconfig-export.txt : the output of cmw-immconfig-export command <br />
 * cmw-status-comp.txt : the output of cmw-status -v comp command, while PL-3 missing (rebooting) and SC-2 is active <br />
 * cmw-status-csiass.txt : the output of cmw-status -v csiass command, while PL-3 missing (rebooting) and SC-2 is active <br />
 * cmw-status-node.txt : the output of cmw-status -v node command, while PL-3 is disabled <br />
 * cmw-status-siass.txt : the output of cmw-status -v siass command, while PL-3 missing (rebooting) and SC-2 is active <br />
 */
public class SafLibTest {

    private static SafLibImpl saf;
    private static Map<String, Map<String, String>> redundencyMap;

    @BeforeClass
    public static void setUp() throws Exception {
        File target = new File("target");
        TestInfo.setLogDir(target.getAbsolutePath());
        saf = new SafLibImpl(new MockSut());
        saf.setUp();
        redundencyMap = saf.getCMWRedundancyModel();
    }

    @AfterClass
    public static void tearDown() {
        saf.tearDown();
        TestInfo.setLogDir(null);
    }

    @Test
    public void nodeAmfAdminStatusTest() throws OmpLibraryException {
        Map<String, String> nodes = saf.getAmfNodeAdminState();
        Assert.assertTrue(nodes.get("SC-1").equals("UNLOCKED"));
        Assert.assertTrue(nodes.get("SC-2").equals("UNLOCKED"));
        Assert.assertTrue(nodes.get("PL-3").equals("LOCKED"));
        Assert.assertTrue(nodes.get("PL-4").equals("UNLOCKED"));
    }

    @Test
    public void nodeAmfOperStatusTest() throws OmpLibraryException {
        Map<String, String> nodes = saf.getAmfNodeOperState();
        Assert.assertTrue(nodes.get("SC-1").equals("ENABLED"));
        Assert.assertTrue(nodes.get("SC-2").equals("ENABLED"));
        Assert.assertTrue(nodes.get("PL-3").equals("DISABLED"));
        Assert.assertTrue(nodes.get("PL-4").equals("ENABLED"));
    }

    @Test
    public void nodeWantedAmfAdminStatusTest() throws OmpLibraryException {
        Map<String, String> nodes = saf.getWantedAmfNodeAdminState();
        nodes = saf.updateAmfNodeAdminState(2, 3, "LOCKED", nodes);
        Assert.assertTrue("Admin status not correct", saf.isAmfNodeAdminState(nodes));
    }

    @Test
    public void nodeWantedAmfOperStatusTest() throws OmpLibraryException {
        Map<String, String> nodes = saf.getWantedAmfNodeOperState();
        nodes.put("PL-3", "DISABLED");
        Assert.assertTrue("Oper status not correct", saf.isAmfNodeOperState(nodes));
    }

    @Test
    public void nodesInServiceStateTest() throws OmpLibraryException {
        Map<String, String> nodes = saf.getNodesInServiceState();
        Assert.assertTrue(nodes.get("SC-1").equals("IN-SERVICE"));
        Assert.assertTrue(nodes.get("SC-2").equals("IN-SERVICE"));
        Assert.assertTrue(nodes.get("PL-3").equals("OUT-OF-SERVICE"));
        Assert.assertTrue(nodes.get("PL-4").equals("IN-SERVICE"));
    }

    @Test
    public void wantedNodesInServiceStateTest() throws OmpLibraryException {
        Map<String, String> nodes = saf.getWantedNodesInServiceState();
        nodes = saf.updateNodesInServiceState(2, 3, "OUT-OF-SERVICE", nodes);
        Assert.assertTrue("wantedNodesInService status not correct", saf.isNodesInServiceState(nodes));
    }

    @Test
    public void safAppHaStateTest() throws OmpLibraryException {
        Map<String, Map<String, String>> mw = saf.getSafAppHAState("ERIC-CoreMW");
        Assert.assertTrue(mw.get("SC-1").get("MdfImmCC").equals("STANDBY"));
        Assert.assertTrue(mw.get("SC-1").get("OSAlarmBridge").equals("ACTIVE"));
        Assert.assertTrue(mw.get("SC-1").get("EcimSwm").equals("STANDBY"));
        Assert.assertTrue(mw.get("SC-1").get("MdfGCC").equals("ACTIVE"));
        Assert.assertTrue(mw.get("SC-1").get("ClusterMonitor").equals("STANDBY"));
        Assert.assertTrue(mw.get("SC-2").get("MdfImmCC").equals("ACTIVE"));
        Assert.assertTrue(mw.get("SC-2").get("OSAlarmBridge").equals("ACTIVE"));
        Assert.assertTrue(mw.get("SC-2").get("EcimSwm").equals("ACTIVE"));
        Assert.assertTrue(mw.get("SC-2").get("MdfGCC").equals("ACTIVE"));
        Assert.assertTrue(mw.get("SC-2").get("ClusterMonitor").equals("ACTIVE"));
        Assert.assertTrue(mw.get("PL-3") == null);
        Assert.assertTrue(mw.get("PL-4").get("OSAlarmBridge").equals("ACTIVE"));
        Assert.assertTrue(mw.get("PL-4").get("MdfGCC").equals("ACTIVE"));

        Map<String, String> monitor = saf.getHAState("ClusterMonitor");
        Assert.assertTrue(monitor.get("SC-1").equals("STANDBY"));
        Assert.assertTrue(monitor.get("SC-2").equals("ACTIVE"));

        Map<String, Map<String, String>> node2 = saf.getHAState(2, 2);
        Assert.assertTrue(node2.get("SC-2").get("MdfImmCC").equals("ACTIVE"));
        Assert.assertTrue(node2.get("SC-2").get("OSAlarmBridge").equals("ACTIVE"));
        Assert.assertTrue(node2.get("SC-2").get("EcimSwm").equals("ACTIVE"));
        Assert.assertTrue(node2.get("SC-2").get("MdfGCC").equals("ACTIVE"));
    }

    @Test
    public void wantedSafAppHaStateTest() throws OmpLibraryException {
        Map<String, Map<String, String>> mw = saf.getCMWWantedHAState();
        mw = saf.removeNodeFromWantedHAState(2, 3, mw);
        Assert.assertTrue(saf.isCmwHAState(mw));
    }

    @Test
    public void updateSafAppHaStateTest() throws OmpLibraryException {
        Map<String, Map<String, String>> mw = saf.getSafAppHAState("ERIC-CoreMW");
        Assert.assertTrue(mw.get("SC-1").get("ClusterMonitor").equals("STANDBY"));
        Assert.assertTrue(mw.get("SC-2").get("ClusterMonitor").equals("ACTIVE"));
        mw = saf.updateWantedHAState(2, 1, "ACTIVE", redundencyMap, mw);
        mw = saf.updateWantedHAState(2, 2, "STANDBY", redundencyMap, mw);
        Assert.assertTrue(mw.get("SC-1").get("ClusterMonitor").equals("ACTIVE"));
        Assert.assertTrue(mw.get("SC-2").get("ClusterMonitor").equals("STANDBY"));
    }

    @Test
    public void isHaStateTest() throws OmpLibraryException {
        Map<String, Map<String, String>> mw1 = saf.getSafAppHAState("ERIC-CoreMW");
        Map<String, Map<String, String>> mw2 = saf.getSafAppHAState("ERIC-CoreMW");
        Assert.assertTrue(saf.isHAState(true, mw1, mw2, redundencyMap));
        Assert.assertTrue(saf.isHAState(true, mw2, mw1, redundencyMap));
        // Switch Active SC and Standby SC
        mw2 = saf.updateWantedHAState(2, 1, "ACTIVE", redundencyMap, mw2);
        mw2 = saf.updateWantedHAState(2, 2, "STANDBY", redundencyMap, mw2);
        Assert.assertTrue(saf.isHAState(false, mw1, mw2, redundencyMap));
        Assert.assertTrue(saf.isHAState(false, mw2, mw1, redundencyMap));
        Assert.assertFalse(saf.isHAState(true, mw1, mw2, redundencyMap));
        Assert.assertFalse(saf.isHAState(true, mw2, mw1, redundencyMap));
        // Change status of component
        mw2.get("SC-1").put("ClusterMonitor", "STANDBY");
        Assert.assertFalse(saf.isHAState(false, mw1, mw2, redundencyMap));
        Assert.assertFalse(saf.isHAState(false, mw2, mw1, redundencyMap));
        // Remove on node
        mw2 = saf.removeNodeFromWantedHAState(2, 2, mw2);
        Assert.assertFalse(saf.isHAState(false, mw1, mw2, redundencyMap));
        Assert.assertFalse(saf.isHAState(false, mw2, mw1, redundencyMap));
        Assert.assertFalse(saf.isHAState(true, mw1, mw2, redundencyMap));
        Assert.assertFalse(saf.isHAState(true, mw2, mw1, redundencyMap));
    }

    @Test
    public void getComponentRedundencyModelTest() throws OmpLibraryException {
        Map<String, String> cw = saf.getCompRedundancyModel("2N");
        Assert.assertTrue(cw.get("ClusterMonitor").equals("2N"));
    }

    @Test
    public void getClusterNodesTest() throws OmpLibraryException {
        Assert.assertTrue("Cluster nodes size not correct", saf.getClusterNodes().length == 4);
        Assert.assertTrue("Number of PL nodes not correct", saf.getClusterNodesPL().length == 2);
        Assert.assertTrue("Number of SC nodes not correct", saf.getClusterNodesSC().length == 2);
    }

    @Test
    public void getScTest() throws OmpLibraryException {
        Assert.assertTrue("SC-1 should be standby SC", saf.getStandbySc().equals("SC-1"));
        Assert.assertTrue("SC-2 should be active SC", saf.getActiveSc().equals("SC-2"));
        Assert.assertTrue("SC-1 should be standby", saf.getScStatus(2, 1).equals("STANDBY"));
        Assert.assertTrue("SC-2 should be active", saf.getScStatus(2, 2).equals("ACTIVE"));
    }
}
