package se.ericsson.jcat.omp.util;

import junit.framework.Assert;

import org.junit.Test;

import se.ericsson.jcat.omp.util.LogWriterHelper.Table;

public class LogWriterHelperTest {
    @Test
    public void testStyledText() {
        Assert.assertEquals("<font color=\"green\">demo</font>",
                            LogWriterHelper.newStyledText("demo").green().toString());
        Assert.assertEquals("<font color=\"red\">demo</font>", LogWriterHelper.newStyledText("demo").red().toString());
        Assert.assertEquals("<font color=\"blue\">demo</font>", LogWriterHelper.newStyledText("demo").blue().toString());
        Assert.assertEquals("<b>demo</b>", LogWriterHelper.newStyledText("demo").bold().toString());
        Assert.assertEquals("demo<br/>\ndemo", LogWriterHelper.newStyledText("demo\ndemo").multipleLines().toString());
        Assert.assertEquals("<pre>demo\tdemo</pre>",
                            LogWriterHelper.newStyledText("demo\tdemo").formatedBlock().toString());
    }

    @Test
    public void testTable() {
        Table t = LogWriterHelper.newTable("table");
        t.appendHeader("header1");
        t.appendHeader("header2", 2);
        t.appendData("sdsd", 2, "red");
        t.appendData("ssss");
        t.newDataRow();
        t.appendData("sdsd");
        t.appendData("sdsd");
        t.appendData("sdsd");
        String result = t.setWidth(500).toString().replace("\n", "");
        String expected = Tools.extractResourceFileAndReadContent("tableTestResult.txt", this.getClass()).replace("\n",
                                                                                                                  "");
        Assert.assertEquals(expected, result);
    }
}
