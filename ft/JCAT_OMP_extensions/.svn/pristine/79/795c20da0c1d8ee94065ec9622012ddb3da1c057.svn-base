/*------------------------------------------------------------------------------
 *******************************************************************************
 * COPYRIGHT Ericsson 2009
 *
 * The copyright to the computer program(s) herein is the property of
 * Ericsson Inc. The programs may be used and/or copied only with written
 * permission from Ericsson Inc. or in accordance with the terms and
 * conditions stipulated in the agreement/contract under which the
 * program(s) have been supplied.
 *******************************************************************************
 *----------------------------------------------------------------------------*/
package se.ericsson.jcat.omp.util.chart;

import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartUtilities;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.axis.DateAxis;
import org.jfree.chart.axis.ValueAxis;
import org.jfree.chart.plot.Marker;
import org.jfree.chart.plot.ValueMarker;
import org.jfree.chart.plot.XYPlot;
import org.jfree.data.time.Second;
import org.jfree.data.time.TimeSeries;
import org.jfree.data.time.TimeSeriesCollection;
import org.jfree.data.xy.XYDataset;
import org.jfree.ui.RectangleAnchor;
import org.jfree.ui.TextAnchor;

import java.awt.*;
import java.io.File;
import java.io.IOException;
import java.io.OutputStream;
import java.util.ArrayList;
import java.util.Collection;

public class TimeSeriesChart {
    private final String title;
    private final Collection<DataSeries> dataSerieses;
    private final Collection<TimeMarker> timeMarkers;

    public TimeSeriesChart(String title) {
        this.title = title;
        dataSerieses = new ArrayList<DataSeries>();
        timeMarkers = new ArrayList<TimeMarker>();
    }

    public void write(OutputStream out) throws IOException {
        ChartUtilities.writeChartAsJPEG(out, plot(), 500, 270);
    }

    public void write(File file) throws IOException {
        ChartUtilities.saveChartAsJPEG(file, plot(), 500, 270);
    }

    private JFreeChart plot() {
        TimeSeriesCollection data = new TimeSeriesCollection();
        for (DataSeries dataSeries : dataSerieses) {
            data.addSeries(createTimeSeries(dataSeries));
        }
        JFreeChart chart = createChart(data, title);
        setMargin(chart);
        for (TimeMarker timeMarker : timeMarkers) {
            chart.getXYPlot().addDomainMarker(createMarker(timeMarker));
        }
        return chart;
    }

    private TimeSeries createTimeSeries(DataSeries dataSeries) {
        TimeSeries series = new TimeSeries(dataSeries.getTitle(), Second.class);
        for (DataPoint point : dataSeries.getDataPoints()) {
            series.add(new Second(point.getTimestamp()), point.getValue());
        }
        return series;
    }

    private Marker createMarker(TimeMarker timeMarker) {
        Marker marker = new ValueMarker(timeMarker.getTimestamp().getTime());
        marker.setPaint(Color.blue);
        marker.setLabel(timeMarker.getText());
        marker.setLabelAnchor(RectangleAnchor.TOP_RIGHT);
        marker.setLabelTextAnchor(TextAnchor.TOP_LEFT);
        return marker;
    }

    private JFreeChart createChart(XYDataset data, String title) {
        return ChartFactory.createTimeSeriesChart(title, "X", "Y", data, true, true, false);
    }

    private void setMargin(JFreeChart chart) {
        XYPlot plot = chart.getXYPlot();

        DateAxis domainAxis = new DateAxis("Time");
        domainAxis.setUpperMargin(0.50);
        plot.setDomainAxis(domainAxis);

        ValueAxis rangeAxis = plot.getRangeAxis();
        rangeAxis.setUpperMargin(0.30);
        rangeAxis.setLowerMargin(0.50);
    }

    public void addTimeMarker(TimeMarker timeMarker)  {
        timeMarkers.add(timeMarker);
    }

    public void addDataSeries(DataSeries dataSeries) {
        dataSerieses.add(dataSeries);
    }
}
