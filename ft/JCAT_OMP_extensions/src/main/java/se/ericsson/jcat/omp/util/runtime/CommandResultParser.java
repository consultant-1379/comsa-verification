package se.ericsson.jcat.omp.util.runtime;

public interface CommandResultParser {

    public String[] getCommands();

    public void newLine(String line);

    public void newErrorLine(String line);

}
