package se.ericsson.jcat.omp.util.monitor;

import java.io.File;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.junit.After;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;

import se.ericsson.jcat.fw.utils.TestInfo;

public class MonitorTest {

    @Before
    public void setUp() {
        File f = new File("target");
        TestInfo.setLogDir(f.getAbsolutePath());
    }

    @After
    public void tearDown() {
        TestInfo.setLogDir(null);
    }

    @Test
    public void monitorTest() {
        Monitor.getInstance().reset();
        MonitorableClass sthToMonitor = new MonitorableClass();
        StatusAnalyzer analyzer = new MonitorableClass();
        Monitor.getInstance().addMonitorable(sthToMonitor, analyzer);
        Monitor.getInstance().reset();
        try {
            Thread.sleep(2200);
        } catch (InterruptedException e) {
            Assert.assertTrue("Sleep interrupted!", false);
        }
        Monitor.getInstance().addTimeMarker("10");
        MonitorDataArray dataArray = Monitor.getInstance().getLastMonitorData(sthToMonitor);
        Assert.assertTrue("Should get back two results!", dataArray.getDataArray().size() >= 2);
        Assert.assertTrue("Each data should contain 3 results!",
                          dataArray.getDataArray().get(0).getData().getPollData().size() == 3);
        Assert.assertTrue("Each data should contain 3 results!",
                          dataArray.getDataArray().get(1).getData().getPollData().size() == 3);
        Map<String, Double> data1 = dataArray.getDataArray().get(0).getData().getPollData();
        Map<String, Double> data2 = dataArray.getDataArray().get(1).getData().getPollData();
        Assert.assertTrue("Check values 1D1, 1D2", data1.get("Data1") + 1 == data1.get("Data2"));
        Assert.assertTrue("Check values 1D2, 1D3", data1.get("Data2") + 1 == data1.get("Data3"));
        // Data2 is earlier than data1
        Assert.assertTrue("Check values 1D1, 2D1", data1.get("Data1") - 1 == data2.get("Data1"));
        Assert.assertTrue("Check values 2D1, 2D2", data2.get("Data1") + 1 == data2.get("Data2"));
        Assert.assertTrue("Check values 2D2, 2D3", data2.get("Data2") + 1 == data2.get("Data3"));
        List<ImagePath> pathList = Monitor.getInstance().plot();
        Assert.assertTrue("Should get 3 images", pathList.size() == 3);
        for (ImagePath i : pathList) {
            File f = new File(i.getPathToImage());
            Assert.assertTrue("Image file should exist: " + i.getKey(), f.exists());
            f.deleteOnExit();
        }
        Monitor.getInstance().removeMonitorable(sthToMonitor);
    }

    public class MonitorableClass implements Monitorable, StatusAnalyzer {

        private int data = 0;

        @Override
        public Pollable pollData() {
            data++;
            return new PollableClass(data);
        }

        @Override
        public String getMonitorableName() {
            return "MonitorDemo";
        }

        @Override
        public int getStartupDelay() {
            return 0;
        }

        @Override
        public int getPollDataDelay() {
            return 1;
        }

        @Override
        public String getAnalyzerName() {
            return "MonitorDemo";
        }

        @Override
        public boolean analyzeStatus(Pollable data) {
            return true;
        }

        @Override
        public StatusData getValidStatusData() {
            return new TrafficCharacteristics();
        }

        @Override
        public void setValidStatusData(StatusData status) {

        }
    }

    public class PollableClass implements Pollable {

        private Map<String, Double> result;

        private PollableClass(double data) {
            result = new HashMap<String, Double>();
            result.put("Data1", data);
            result.put("Data2", data + 1);
            result.put("Data3", data + 2);
        }

        @Override
        public Map<String, Double> getPollData() {
            return result;
        }

    }

    public class TrafficCharacteristics implements StatusData {

        @Override
        public String getData(String key) {
            return "test value";
        }

    }
}
