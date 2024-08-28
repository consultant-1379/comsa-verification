package se.ericsson.jcat.omp.util.monitor;

import java.util.Date;

/**
 * Base data unit returned by Monitorable
 */
public class MonitorData {
    private final Date timestamp;
    private final Pollable data;

    public MonitorData(Pollable data) {
        this.data = data;
        timestamp = new Date();
    }

    public Pollable getData() {
        return data;
    }

    public Date getTimestamp() {
        return timestamp;
    }
}
