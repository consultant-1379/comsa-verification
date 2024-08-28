package se.ericsson.jcat.omp.library;

import java.util.HashMap;
import java.util.Map;

import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;

import se.ericsson.jcat.omp.util.monitor.Monitor;
import se.ericsson.jcat.omp.util.monitor.Monitorable;
import se.ericsson.jcat.omp.util.monitor.Pollable;

public class TestappLibTest {

    private Map<String, String> data1 = new HashMap<String, String>();
    private Map<String, String> data2 = new HashMap<String, String>();
    private TestappLibImpl testapp;

    @Before
    public void init() throws Exception {
        testapp = new TestappLibImpl(null);
    }

    @Before
    public void createDatas() {
        data1.put("fail", "0");
        data1.put("recv", "1000");
        data1.put("timeout", "0");
        data1.put("send", "1000");
        data1.put("unknown", "0");

        data2.put("fail", "100");
        data2.put("recv", "2000");
        data2.put("timeout", "100");
        data2.put("send", "2000");
        data2.put("unknown", "100");
    }

    @Test
    public void test() {
        Assert.assertFalse(testapp.isTrafficOk(data1, data2, 0, 0, 0));
        Assert.assertFalse(testapp.isTrafficOk(data1, data2, 11, 11, 0));
        Assert.assertTrue(testapp.isTrafficOk(data1, data2, 11, 11, 11));
        Assert.assertTrue(testapp.isTrafficOk(data1, data2, 0, 10, 10));
        // no traffic sent failure
        Assert.assertFalse(testapp.isTrafficOk(data1, data1, 11, 11, 11));
    }

    @Test
    public void monitorTest1() {
        Monitor.getInstance().reset();
        DummyDataPutter sthToMonitor = new DummyDataPutter(1);
        Monitor.getInstance().addMonitorable(sthToMonitor);
        Monitor.getInstance().reset();
        try {
            Thread.sleep(2200);
        } catch (InterruptedException e) {
            Assert.assertTrue("Sleep interrupted!", false);
        }
        testapp.setMonitorIndentifier(sthToMonitor);
        Assert.assertTrue(testapp.waitUntilStable(10));
        Monitor.getInstance().removeMonitorable(sthToMonitor);
    }

    @Test
    public void monitorTest2() {
        Monitor.getInstance().reset();
        DummyDataPutter sthToMonitor = new DummyDataPutter(2);
        Monitor.getInstance().addMonitorable(sthToMonitor);
        Monitor.getInstance().reset();
        try {
            Thread.sleep(2200);
        } catch (InterruptedException e) {
            Assert.assertTrue("Sleep interrupted!", false);
        }
        testapp.setMonitorIndentifier(sthToMonitor);
        Assert.assertFalse(testapp.isStable());
        Monitor.getInstance().removeMonitorable(sthToMonitor);
    }

    public class DummyDataPutter implements Monitorable {

        private int model;
        private boolean succ = true;

        private DummyDataPutter(int model) {
            this.model = model;
        }

        @Override
        public Pollable pollData() {
            switch (this.model) {
                case 1:
                    return new TestappResult(data1);
                case 2:
                    return new TestappResult(data2);
                case 3:
                    succ = !succ;
                    return succ ? new TestappResult(data1) : new TestappResult(data2);
            }
            return null;
        }

        @Override
        public String getMonitorableName() {
            return "TestApp";
        }

        @Override
        public int getStartupDelay() {
            return 0;
        }

        @Override
        public int getPollDataDelay() {
            return 1;
        }

    }
}
