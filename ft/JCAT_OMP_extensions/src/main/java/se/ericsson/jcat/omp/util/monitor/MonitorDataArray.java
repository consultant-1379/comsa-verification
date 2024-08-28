package se.ericsson.jcat.omp.util.monitor;

import java.util.List;

/**
 * Represents a group of MonitorData
 */
public class MonitorDataArray {
    private List<MonitorData> dataArray;

    public MonitorDataArray(List<MonitorData> dataArray) {
        this.dataArray = dataArray;
    }

    public List<MonitorData> getDataArray() {
        return dataArray;
    }
}
