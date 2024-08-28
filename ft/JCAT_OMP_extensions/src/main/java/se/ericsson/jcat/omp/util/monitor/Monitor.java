package se.ericsson.jcat.omp.util.monitor;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.ScheduledFuture;
import java.util.concurrent.TimeUnit;

import org.apache.log4j.Logger;

import se.ericsson.jcat.omp.util.LogWriterHelper;
import se.ericsson.jcat.omp.util.chart.DataPoint;
import se.ericsson.jcat.omp.util.chart.DataSeries;
import se.ericsson.jcat.omp.util.chart.TimeMarker;
import se.ericsson.jcat.omp.util.chart.TimeSeriesChart;

/**
 * Singleton Monitor to collect MonitorData from Monitorable and plot
 */
public class Monitor {
    private final static Logger LOGGER = Logger.getLogger(Monitor.class);

    private final static Monitor INSTANCE = new Monitor();

    private final Map<String, MonitorDataArray> dataMap;
    private final Map<String, MonitorDataArray> failuresDataMap;
    private final ScheduledExecutorService executorService;
    private final Map<String, ScheduledFuture<?>> executorMap;

    private final List<TimeMarker> timeMarkers;

    /**
     * Returns the global Monitor instance.
     * 
     * @return
     */
    public static Monitor getInstance() {
        return INSTANCE;
    }

    private Monitor() {
        executorMap = new HashMap<String, ScheduledFuture<?>>();
        dataMap = new HashMap<String, MonitorDataArray>();
        failuresDataMap = new HashMap<String, MonitorDataArray>();
        executorService = Executors.newScheduledThreadPool(5);
        timeMarkers = Collections.synchronizedList(new ArrayList<TimeMarker>());
    }

    public void addMonitorable(Monitorable monitorable) {
        addMonitorable(monitorable, null);
    }

    /**
     * Register a Monitorable into Monitor and starts to collect MonitorData
     * 
     * @param monitorable
     */
    public void addMonitorable(Monitorable monitorable, StatusAnalyzer analyzer) {
        if (executorMap.get(monitorable.getMonitorableName()) != null) {
            executorMap.get(monitorable.getMonitorableName()).cancel(true);
        }
        executorMap.put(monitorable.getMonitorableName(),
                        executorService.scheduleWithFixedDelay(new Collector(monitorable, analyzer),
                                                               monitorable.getStartupDelay(),
                                                               monitorable.getPollDataDelay(), TimeUnit.SECONDS));
    }

    public void removeMonitorable(Monitorable monitorable) {
        if (executorMap.get(monitorable.getMonitorableName()) != null) {
            executorMap.get(monitorable.getMonitorableName()).cancel(true);
        }
    }

    public void addTimeMarker(String text) {
        timeMarkers.add(new TimeMarker(text));
    }

    /**
     * Terminate Monitor, all registered Monitorables will be discarded.
     */
    public void terminate() {
        executorService.shutdown();
    }

    public void reset() {
        synchronized (dataMap) {
            dataMap.clear();
        }
        synchronized (failuresDataMap) {
            failuresDataMap.clear();
        }
        synchronized (timeMarkers) {
            timeMarkers.clear();
        }
    }

    /**
     * Plot time series charts based on the collected MonitorData, and return the paths to the images.
     * 
     * @return
     */
    public List<ImagePath> plot() {
        Map<String, DataSeries> chartMap = createChartMap();
        return createImagePaths(chartMap);
    }

    private List<ImagePath> createImagePaths(Map<String, DataSeries> chartMap) {
        List<ImagePath> imagePaths = new ArrayList<ImagePath>();

        for (Map.Entry<String, DataSeries> series : chartMap.entrySet()) {
            TimeSeriesChart chart = new TimeSeriesChart(series.getKey());
            chart.addDataSeries(series.getValue());
            addTimeMarkers(chart);
            try {
                File imageFile = LogWriterHelper.createImageFile();
                chart.write(imageFile);
                imagePaths.add(new ImagePath(series.getKey(), imageFile.getAbsolutePath()));
            } catch (IOException e) {
                e.printStackTrace();
                LOGGER.error(e.getMessage());
            }
        }
        return imagePaths;
    }

    private void addTimeMarkers(TimeSeriesChart chart) {
        synchronized (timeMarkers) {
            for (TimeMarker marker : timeMarkers) {
                chart.addTimeMarker(marker);
            }
        }
    }

    private Map<String, DataSeries> createChartMap() {
        Map<String, DataSeries> chartMap = new HashMap<String, DataSeries>();

        synchronized (dataMap) {
            for (Map.Entry<String, MonitorDataArray> instance : dataMap.entrySet()) {
                for (MonitorData data : instance.getValue().getDataArray()) {
                    for (Map.Entry<String, Double> sample : data.getData().getPollData().entrySet()) {
                        String key = String.format("%s-%s", instance.getKey(), sample.getKey());
                        DataSeries series = chartMap.get(key);
                        if (series == null) {
                            series = new DataSeries(key);
                        }
                        series.addDataPoint(new DataPoint(data.getTimestamp(), sample.getValue()));
                        chartMap.put(key, series);
                    }
                }
            }
        }
        return chartMap;
    }

    /**
     * Returns a list of MonitorDataArray of a maximal size of 2, the greater the index, the later the MonitorData, or
     * empty list if monitorable is not registered.
     * 
     * @param monitorable
     * @return
     */
    public MonitorDataArray getLastMonitorData(Monitorable monitorable) {
        MonitorDataArray lists = dataMap.get(monitorable.getMonitorableName());
        if (lists == null) {
            return new MonitorDataArray(Collections.synchronizedList(new ArrayList<MonitorData>()));
        }
        return lists;
    }

    /**
     * Returns the failures in a MonitorDataArray, the smaller the index, the most recent the MonitorData is, or empty
     * list if monitorable is not registered.
     * 
     * @param monitorable
     * @return MonitorDataArray
     */
    public MonitorDataArray getLastMonitorFailuresData(Monitorable monitorable) {
        MonitorDataArray lists = failuresDataMap.get(monitorable.getMonitorableName());
        if (lists == null) {
            return new MonitorDataArray(Collections.synchronizedList(new ArrayList<MonitorData>()));
        }
        return lists;
    }

    class Collector implements Runnable {
        private Monitorable monitorable;
        private StatusAnalyzer analyzer;

        Collector(Monitorable monitorable, StatusAnalyzer analyzer) {
            this.monitorable = monitorable;
            this.analyzer = analyzer;
        }

        @Override
        public void run() {
            Pollable pollableData = null;

            try {
                pollableData = monitorable.pollData();
            } catch (Exception e) {
                LOGGER.warn("Cannot pull data now in " + monitorable.getMonitorableName());
            }

            if (pollableData == null) {
                return;
            }
            // adding the MonitorData to the monitorable dataMap
            MonitorDataArray dataArray = dataMap.get(monitorable.getMonitorableName());
            if (dataArray == null) {
                dataArray = new MonitorDataArray(Collections.synchronizedList(new ArrayList<MonitorData>()));
            }
            dataArray.getDataArray().add(0, new MonitorData(pollableData));

            dataMap.put(monitorable.getMonitorableName(), dataArray);

            // if the collected MonitorData is considered as a failure, add the MonitorData to the monitorable
            // failuresDataMap
            if (analyzer != null && !analyzer.analyzeStatus(pollableData)) {
                MonitorDataArray failuresDataArray = failuresDataMap.get(monitorable.getMonitorableName());
                if (failuresDataArray == null) {
                    failuresDataArray = new MonitorDataArray(Collections.synchronizedList(new ArrayList<MonitorData>()));
                }
                failuresDataArray.getDataArray().add(0, new MonitorData(pollableData));

                failuresDataMap.put(monitorable.getMonitorableName(), failuresDataArray);
            }
        }
    }
}
