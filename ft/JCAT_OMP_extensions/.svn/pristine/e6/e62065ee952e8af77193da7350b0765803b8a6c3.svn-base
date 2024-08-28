package se.ericsson.jcat.omp.util.monitor;

/**
 *
 */
public interface Monitorable {
    /**
     * Returns a collection of MonitorData
     * 
     * @return
     */
    Pollable pollData();

    String getMonitorableName();

    /**
     * Define the delay before the first collection of MonitorData
     * 
     * @return
     */
    int getStartupDelay();

    /**
     * Define the delay between each collection of MonitorData
     * 
     * @return
     */
    int getPollDataDelay();
}