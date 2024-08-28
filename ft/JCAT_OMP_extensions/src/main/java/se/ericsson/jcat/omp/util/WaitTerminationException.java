package se.ericsson.jcat.omp.util;

public class WaitTerminationException extends Exception {

    private static final long serialVersionUID = 1L;

    public WaitTerminationException(String s) {
        super(s);
    }

    public WaitTerminationException(String s, Exception e) {
        super(s, e);
    }

}
