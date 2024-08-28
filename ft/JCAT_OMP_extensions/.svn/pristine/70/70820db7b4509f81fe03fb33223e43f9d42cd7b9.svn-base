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

import java.util.ArrayList;
import java.util.List;

public class DataSeries {
    private final String title;
    private final List<DataPoint> dataPoints;

    public DataSeries(String title) {
        this.title = title;
        dataPoints = new ArrayList<DataPoint>();
    }

    public void addDataPoint(DataPoint dataPoint) {
        dataPoints.add(dataPoint);
    }

    public String getTitle() {
        return title;
    }

    public List<DataPoint> getDataPoints() {
        return dataPoints;
    }
}
