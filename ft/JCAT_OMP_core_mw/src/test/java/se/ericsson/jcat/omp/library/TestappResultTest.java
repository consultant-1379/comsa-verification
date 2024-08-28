package se.ericsson.jcat.omp.library;

import java.util.HashMap;
import java.util.Map;

import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;

public class TestappResultTest {

    private Map<String, String> data1 = new HashMap<String, String>();
    private Map<String, String> data2 = new HashMap<String, String>();

    @Before
    public void createDatas() {

        data1.put("fail", "0");
        data1.put("recv", "1000");
        data1.put("timeout", "0");
        data1.put("send", "1000");
        data1.put("unknown", "0");

        data2.put("fail", "100");
        data2.put("recv", "2000");
        data2.put("timeout", "100");
        data2.put("send", "2000");
        data2.put("unknown", "100");
    }

    @Test
    public void constructorTest() {
        TestappResult result1 = new TestappResult(data1);
        Assert.assertTrue(result1.getSend() == 1000);
        Assert.assertTrue(result1.getRecv() == 1000);
        Assert.assertTrue(result1.getFail() == 0);
        Assert.assertTrue(result1.getTimeout() == 0);
        Assert.assertTrue(result1.getUnknown() == 0);
    }

    @Test
    public void calculationTest() {
        TestappResult result1 = new TestappResult(data1);
        Assert.assertTrue(result1.getRealFail() == 0);
        Assert.assertTrue(result1.getRealLoss() == 0);
        Assert.assertTrue(result1.getRealTimeout() == 0);
        TestappResult result2 = new TestappResult(data2);
        Assert.assertTrue(result2.getRealFail() == 5);
        Assert.assertTrue(result2.getRealLoss() == 0);
        Assert.assertTrue(result2.getRealTimeout() == 5);
        TestappResult diff = new TestappResult(result1, result2);
        Assert.assertTrue(diff.getRealFail() == 10);
        Assert.assertTrue(diff.getRealLoss() == 0);
        Assert.assertTrue(diff.getRealTimeout() == 10);
        Assert.assertTrue(diff.getSend() == 1000);
        Assert.assertTrue(diff.getRecv() == 1000);
        Assert.assertTrue(diff.getFail() == 100);
        Assert.assertTrue(diff.getTimeout() == 100);
        Assert.assertTrue(diff.getUnknown() == 100);
    }
}
