package se.ericsson.jcat.omp.util;

public class CommandExecutionResult {
	/**
	 * The return value of the command. 0 means success
	 */
	public int returnValue;
	/**
	 * The output of the command
	 */
	public String output;

	protected CommandExecutionResult(int returnValue, String output) {
		this.returnValue = returnValue;
		this.output = output;
	}
	
	public String toString() {
		return output;
	}
}
