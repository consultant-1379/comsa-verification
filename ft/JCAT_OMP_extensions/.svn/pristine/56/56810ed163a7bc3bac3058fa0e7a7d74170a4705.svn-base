package se.ericsson.jcat.omp.util;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import org.apache.log4j.Logger;

import se.ericsson.jcat.fw.logging.LogWriter;
import se.ericsson.jcat.fw.logging.writers.LogWriterHolder;
import se.ericsson.jcat.fw.utils.TestInfo;

public class LogWriterHelper {

    public static void setTestSubStep(String text) {
        setTestStep("[sub] " + text);
    }

    private static void setTestStep(String step) {
        ArrayList<LogWriter> logWriters = LogWriterHolder.getInstance().getLogWriters();

        for (LogWriter logWriter : logWriters) {
            logWriter.setTestStep(step);
        }
    }

    public static void setTestInfoInFile(Logger logger, String description, String... text) {
        setTestInfo(setTestTextInFile(logger, description, text));
    }

    private static void setTestFailureInFile(Logger logger, String description, String... text) {
        setTestFailure(setTestTextInFile(logger, description, text));
    }

    private static void setTestFailureInFile(Logger logger, String description, Throwable t) {
        String error = t.getCause() + "\t" + t.getMessage() + "\n";
        for (StackTraceElement s : t.getStackTrace()) {
            error += s.toString() + "\n";
        }
        setTestFailure(setTestTextInFile(logger, description, error));
    }

    private static String setTestTextInFile(Logger logger, String description, String... text) {
        String filename = "trace_files/" + "trace-" + Tools.getCurrentTimeString("yyyyddMM-HHmmss-SSS") + ".txt";
        File logfile = createFileInLogDir(filename);
        try {
            BufferedWriter bw = new BufferedWriter(new FileWriter(logfile));
            for (String t : text) {
                bw.write(Tools.getCurrentTimeString("yyyyddMM-HHmmss-SSS") + "\t");
                bw.write(t + "\n");
            }
            bw.flush();
            bw.close();
            return description + " ... " + buildHyperLink("Detailed info", filename);
        } catch (IOException e) {
            logger.warn("Cannot write logs to file " + logfile.getAbsolutePath() + ", please check! " + e.getMessage());
            return description + " ... (detail is missing)";
        }
    }

    private static File createFileInLogDir(String filename) {
        File file = new File(TestInfo.getLogDir() + "/" + filename);
        file.getParentFile().mkdirs();
        return file;
    }

    public static File createImageFile() {
        String filename = "image_files/" + "image-" + Tools.getCurrentTimeString("yyyyddMM-HHmmss-SSS") + ".ipeg";
        return createFileInLogDir(filename);
    }

    public static void writeImageToLog(Logger logger, String imagePath) {
        logger.info(createImageTag(imagePath));
    }

    private static String createImageTag(String imagePath) {
        return String.format("<img src=\"%s\" alt=\"%s\"/>", imagePath, "image missing");
    }

    private static String buildHyperLink(String text, String url) {
        return "<a href=\"" + url + "\" target=\"_blank\">" + text + "</a>";
    }

    public static void setTestInfoMultipleLines(Logger logger, String info) {
        logger.info(newStyledText(info).multipleLines().toString());
    }

    private static void setTestInfo(String info) {
        ArrayList<LogWriter> logWriters = LogWriterHolder.getInstance().getLogWriters();

        for (LogWriter logWriter : logWriters) {
            logWriter.setTestInfo(info);
        }
    }

    private static void setTestFailure(String info) {
        ArrayList<LogWriter> logWriters = LogWriterHolder.getInstance().getLogWriters();

        for (LogWriter logWriter : logWriters) {
            logWriter.setTestFailure(info);
        }
    }

    public static StyledText newStyledText(String text) {
        return new StyledText(text);
    }

    public static Table newTable(String caption) {
        return new Table(caption);
    }

    public static class StyledText {
        private String self = null;

        private StyledText(String text) {
            self = text;
        }

        public StyledText(String text, String hyperLink) {
            self = "<a href=\"" + hyperLink + "\" target=\"_blank\">" + text + "</a>";
        }

        public StyledText red() {
            self = "<font color=\"red\">" + self + "</font>";
            return this;
        }

        public StyledText blue() {
            self = "<font color=\"blue\">" + self + "</font>";
            return this;
        }

        public StyledText green() {
            self = "<font color=\"green\">" + self + "</font>";
            return this;
        }

        public StyledText color(String color) {
            self = "<font color=\"" + color + "\">" + self + "</font>";
            return this;
        }

        public StyledText bold() {
            self = "<b>" + self + "</b>";
            return this;
        }

        public StyledText multipleLines() {
            self = self.replaceAll("\n", "<br/>\n");
            return this;
        }

        /**
         * Define a preformatted block using html pre tag. Don't use together with multipleLines()
         * 
         * @return
         */
        public StyledText formatedBlock() {
            self = "<pre>" + self + "</pre>";
            return this;
        }

        public String toString() {
            return self;
        }
    }

    public static class Table {
        private String caption = null;
        private List<String> header = null;
        private List<Integer> headerSpan = null;
        private List<List<String>> data = null;
        private List<List<Integer>> dataSpan = null;
        private List<List<String>> dataColor = null;
        private int width = 770;

        private Table(String caption) {
            this.caption = caption;
            header = new ArrayList<String>();
            headerSpan = new ArrayList<Integer>();
            data = new ArrayList<List<String>>();
            data.add(new ArrayList<String>());
            dataSpan = new ArrayList<List<Integer>>();
            dataSpan.add(new ArrayList<Integer>());
            dataColor = new ArrayList<List<String>>();
            dataColor.add(new ArrayList<String>());
        }

        public Table setWidth(int width) {
            this.width = width;
            return this;
        }

        public Table appendHeader(String header) {
            return this.appendHeader(header, 1);
        }

        public Table appendHeader(String header, int colSpan) {
            this.header.add(header);
            this.headerSpan.add(colSpan);
            return this;
        }

        public Table appendData(String text) {
            return appendData(text, 1, "default");
        }

        public Table appendData(String text, int colSpan, String color) {
            this.data.get(this.data.size() - 1).add(text);
            this.dataSpan.get(this.dataSpan.size() - 1).add(colSpan);
            this.dataColor.get(this.dataColor.size() - 1).add(color);
            return this;
        }

        public Table newDataRow() {
            data.add(new ArrayList<String>());
            dataSpan.add(new ArrayList<Integer>());
            dataColor.add(new ArrayList<String>());
            return this;
        }

        public String toString() {
            StringBuilder output = new StringBuilder();
            output.append("<table border=\"1\" style=\"width:").append(width).append("px;\">").append("\n");
            output.append("<tr><th colspan=\"100%\" style=\"text-align:center;\">").append(this.caption).append("</th></tr>").append("\n");
            output.append("<tr>");
            for (int i = 0; i < header.size(); i++) {
                output.append("<th colspan=\"" + headerSpan.get(i) + "\">" + header.get(i) + "</th>");
            }
            output.append("</tr>").append("\n");
            for (int i = 0; i < data.size(); i++) {
                output.append("<tr>");
                for (int j = 0; j < data.get(i).size(); j++) {
                    if (dataColor.get(i).get(j).equalsIgnoreCase("default")) {
                        output.append("<td colspan=\"" + dataSpan.get(i).get(j) + "\">" + data.get(i).get(j) + "</td>");
                    } else {
                        output.append("<td colspan=\"" + dataSpan.get(i).get(j) + "\" bgcolor=\""
                                + dataColor.get(i).get(j) + "\">" + data.get(i).get(j) + "</td>");
                    }
                }
                output.append("</tr>").append("\n");
            }
            output.append("</table>").append("\n");
            return output.toString();
        }
    }
}
