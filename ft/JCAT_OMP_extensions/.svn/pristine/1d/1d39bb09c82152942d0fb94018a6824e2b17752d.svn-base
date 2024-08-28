package se.ericsson.jcat.omp.util.monitor;

public interface StatusAnalyzer {

    StatusData getValidStatusData();

    void setValidStatusData(StatusData status);

    String getAnalyzerName();

    /**
     * Analyze the reading
     * 
     * @return true if the status is ok
     */
    boolean analyzeStatus(Pollable trafficReading);

}
