package se.ericsson.jcat.omp.util.runtime;

import java.io.BufferedReader;
import java.io.InputStreamReader;

import org.apache.log4j.Logger;

public class CommandExecutor {

    private static Logger logger = Logger.getLogger(CommandExecutor.class);

    public static void execute(CommandResultParser parser) throws Exception {
        String s;
        Runtime rt = Runtime.getRuntime();

        logger.debug("Start exec");
        Process proc = rt.exec(parser.getCommands());
        logger.debug("Create streams");

        BufferedReader stdInput = new BufferedReader(new InputStreamReader(proc.getInputStream()));

        BufferedReader stdError = new BufferedReader(new InputStreamReader(proc.getErrorStream()));

        logger.debug("Start parsing");
        // read the output from the command
        while ((s = stdInput.readLine()) != null) {
            logger.debug(s);
            parser.newLine(s);
        }

        logger.debug("Errors:");
        // read any errors from the attempted command
        while ((s = stdError.readLine()) != null) {
            logger.debug(s);
            parser.newErrorLine(s);
        }
    }

}
