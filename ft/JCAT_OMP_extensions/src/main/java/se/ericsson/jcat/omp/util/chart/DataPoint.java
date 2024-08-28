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

import java.util.Date;

public class DataPoint {
    private final Date timestamp;
    private final double value;

    public DataPoint(Date timestamp, double value) {
        this.timestamp = timestamp;
        this.value = value;
    }

    public Date getTimestamp() {
        return timestamp;
    }

    public double getValue() {
        return value;
    }
}
