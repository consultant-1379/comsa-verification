package se.ericsson.jcat.omp.library;

import java.util.HashMap;
import java.util.Map;

import se.ericsson.jcat.omp.util.monitor.Pollable;

public class TestappResult implements Pollable {
    private int fail;
    private int recv;
    private int timeout;
    private int send;
    private int unknown;
    private double realLoss;
    private double realFail;
    private double realTimeout;
    private double actualIntensity;

    public TestappResult(Map<String, String> data) {
        init(Integer.parseInt(data.get("fail")), Integer.parseInt(data.get("recv")),
             Integer.parseInt(data.get("timeout")), Integer.parseInt(data.get("send")),
             Integer.parseInt(data.get("unknown")));
    }

    public TestappResult(Map<String, String> startData, Map<String, String> endData) {
        init(Integer.parseInt(endData.get("fail")) - Integer.parseInt(startData.get("fail")),
             Integer.parseInt(endData.get("recv")) - Integer.parseInt(startData.get("recv")),
             Integer.parseInt(endData.get("timeout")) - Integer.parseInt(startData.get("timeout")),
             Integer.parseInt(endData.get("send")) - Integer.parseInt(startData.get("send")),
             Integer.parseInt(endData.get("unknown")) - Integer.parseInt(startData.get("unknown")));
    }

    public TestappResult(TestappResult startData, TestappResult endData) {
        init(endData.getFail() - startData.getFail(), endData.getRecv() - startData.getRecv(), endData.getTimeout()
                     - startData.getTimeout(), endData.getSend() - startData.getSend(),
             endData.getUnknown() - startData.getUnknown());
    }

    public TestappResult(int fail, int recv, int timeout, int send, int unknown) {
        init(fail, recv, timeout, send, unknown);
    }

    private void init(int fail, int recv, int timeout, int send, int unknown) {
        this.fail = fail;
        this.recv = recv;
        this.timeout = timeout;
        this.send = send;
        this.unknown = unknown;
        caculateReals();
    }

    private void caculateReals() {
        if (recv == 0) {
            realLoss = 100;
        } else {
            realLoss = (double) ((fail + timeout + unknown) / recv) * 100;
        }
        realFail = ((double) fail / send) * 100;
        realTimeout = ((double) timeout / send) * 100;
    }

    public int getFail() {
        return fail;
    }

    public int getRecv() {
        return recv;
    }

    public int getTimeout() {
        return timeout;
    }

    public int getSend() {
        return send;
    }

    public int getUnknown() {
        return unknown;
    }

    public double getRealLoss() {
        return realLoss;
    }

    public double getRealFail() {
        return realFail;
    }

    public double getRealTimeout() {
        return realTimeout;
    }

    public void setActualIntensity(double actualIntensity) {
        this.actualIntensity = actualIntensity;
    }

    public double getActualIntensity() {
        return actualIntensity;
    }

    public String toString() {
        return "Fail " + this.getFail() + " ::: Recv " + this.getRecv() + " ::: Timeout " + this.getTimeout()
                + " ::: Send " + this.getSend() + " ::: Unknown " + this.getUnknown();
    }

    @Override
    public Map<String, Double> getPollData() {
        Map<String, Double> data = new HashMap<String, Double>();
        data.put("Intensity", (double) actualIntensity);
        return data;
    }
}
