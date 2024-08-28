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
package se.ericsson.jcat.omp.util;

import java.io.File;
import java.util.HashMap;
import java.util.Map;
import java.util.Vector;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;

import org.apache.log4j.Logger;
import org.w3c.dom.Document;
import org.w3c.dom.NamedNodeMap;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;

import se.ericsson.jcat.omp.fw.OmpLibraryException;
import se.ericsson.jcat.omp.fw.OmpSut;
import se.ericsson.jcat.omp.library.SshLib;

public class AppConfigStringReader {

    private static Logger logger = Logger.getLogger(AppConfigStringReader.class);

    private static boolean ready = false;

    private static Document appConfigDocument = null;
    private static Vector<String> safCompList = new Vector<String>();
    private static Vector<String> csiPrototypeList = new Vector<String>();
    private static Vector<String> suPrototypeList = new Vector<String>();
    private static Vector<String> siInstanceList = new Vector<String>();
    private static Vector<String> sgInstanceList = new Vector<String>();
    private static Vector<String> nodePrototypeList = new Vector<String>();
    private static Vector<String> nodeInstanceList = new Vector<String>();
    private static HashMap<String, String> mmasInstanceMap = new HashMap<String, String>();
    private static String hostnameSeparator = null;

    public static void readAppConfig(OmpSut sut) {
        logger.debug("Reading AppConfig.");
        if (!isReady()) {
            logger.info("Read AppConfig.");
            try {
                SshLib ssh = (SshLib) sut.getLibrary("SshLib");
                String result = ssh.sendCommand("ls /home/tspsaf/etc/AppConfig.xml", true);
                if (result.equals("/home/tspsaf/etc/AppConfig.xml")) {
                    deleteTmpFile("/tmp/AppConfig.xml");
                    hostnameSeparator = sut.getSeparator();
                    ssh.remoteCopyFrom("/home/tspsaf/etc/AppConfig.xml", "/tmp/", 10);
                    appConfigDocument = readFile("/tmp/AppConfig.xml");
                    deleteTmpFile("/tmp/AppConfig.xml");
                    if (appConfigDocument != null) {
                        logger.info("Read success");
                        parseContent();
                        ready = true;
                    } else {
                        logger.info("Read failed");
                        ready = false;
                    }
                } else {
                    logger.info("Cannot find AppConfig file!");
                    ready = false;
                }
            } catch (OmpLibraryException e) {
                logger.error("Cannot read AppConfig file! " + e.getMessage());
                deleteTmpFile("/tmp/AppConfig.xml");
                ready = false;
            }

        } else {
            logger.info("AppConfig already read in previous testcase.");
            return;
        }
    }

    private static void deleteTmpFile(String file) {
        File f = new File(file);
        if (f.exists()) {
            f.delete();
        }
    }

    private static void parseContent() {
        prepareList("componentPrototype", safCompList);
        prepareList("CSIPrototype", csiPrototypeList);
        prepareList("SUPrototype", suPrototypeList);
        prepareList("SIInstance", siInstanceList);
        prepareList("SGInstance", sgInstanceList);
        prepareList("nodePrototype", nodePrototypeList);
        prepareList("nodeInstance", nodeInstanceList);
    }

    private static void prepareList(String tagName, Vector<String> list) {
        logger.info("Searching for: " + tagName);
        list.clear();
        NodeList nodes = appConfigDocument.getElementsByTagName(tagName);
        for (int i = 0; i < nodes.getLength(); i++) {
            Node node = nodes.item(i);
            NamedNodeMap map = node.getAttributes();
            if (map != null) {
                Node nameItem = map.getNamedItem("name");
                if (nameItem != null) {
                    String content = nameItem.getTextContent();
                    list.add(content);
                    logger.info("added: " + content);
                    if (tagName.equals("SGInstance") && content.contains("MMAS")
                            && (content.contains("TRAFFIC") || content.contains("OAM"))) {
                        try {
                            Node redundancyModel = getNode(node, "redundancyModel");
                            Node suRankList = getNode(redundancyModel.getFirstChild().getNextSibling(), "SURankList");
                            Node rank = suRankList.getFirstChild();
                            while (rank != null) {
                                if (rank.getNodeName().equals("SU")) {
                                    NamedNodeMap m = rank.getAttributes();
                                    if (m != null) {
                                        Node su = m.getNamedItem("SUName");
                                        if (su != null) {
                                            String name = su.getTextContent();
                                            name = name.replace("safSu=", "").replace("safNode=", "");
                                            String[] part = name.split(",");
                                            part[0] = part[0].contains("OAM") ? part[0].substring(part[0].lastIndexOf("OAM"))
                                                    : part[0].substring(part[0].lastIndexOf("TRAFFIC"));
                                            getMmasInstanceMap().put(part[1], part[0]);
                                        }
                                    }
                                }
                                rank = rank.getNextSibling();
                            }
                        } catch (Exception e) {
                            logger.error("Error while reading AppConfig!");
                        }
                    }
                }
            }
        }
    }

    private static Node getNode(Node parentNode, String name) throws Exception {
        Node child = parentNode.getFirstChild();
        while (child != null && !child.getNodeName().equals(name)) {
            child = child.getNextSibling();
        }
        if (child == null) {
            logger.error("Error in AppConfig! Cannot find " + name);
            throw new Exception();
        }
        return child;
    }

    private static Document readFile(String appConfig) {
        logger.info("File: " + appConfig);
        try {
            File file = new File(appConfig);
            DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
            DocumentBuilder db = dbf.newDocumentBuilder();
            Document doc = db.parse(file);
            doc.getDocumentElement().normalize();
            return doc;
        } catch (Exception e) {
            logger.error("Cannot read file " + appConfig + "! " + e.getMessage());
            return null;
        }
    }

    public static Vector<String> getSafCompList() {
        return safCompList;
    }

    public static Vector<String> getCsiPrototypeList() {
        return csiPrototypeList;
    }

    public static Vector<String> getSuPrototypeList() {
        return suPrototypeList;
    }

    public static Vector<String> getSiInstanceList() {
        return siInstanceList;
    }

    public static Vector<String> getSgInstanceList() {
        return sgInstanceList;
    }

    public static Vector<String> getNodePrototypeList() {
        return nodePrototypeList;
    }

    public static Vector<String> getNodeInstanceList() {
        return nodeInstanceList;
    }

    public static Map<String, String> getMmasInstanceMap() {
        return mmasInstanceMap;
    }

    public static boolean isReady() {
        return ready;
    }

    private static String getString(Vector<String> list, String matchingString, int subrack, int slot) {
        if (list == null) {
            return null;
        }
        final Pattern p = Pattern.compile(matchingString);
        final String node = slot <= 2 ? "SC" + hostnameSeparator + "2" + hostnameSeparator + slot : "PL"
                + hostnameSeparator + "2" + hostnameSeparator + slot;
        Vector<String> tmpList = new Vector<String>();
        for (int i = 0; i < list.size(); i++) {
            String name = list.get(i);
            final Matcher m = p.matcher(name);
            if (m.matches()) {
                tmpList.add(name);
            }
        }
        if (tmpList.size() == 0) {
            return "NotFound";
        } else if (tmpList.size() == 1) {
            return tmpList.get(0);
        } else {
            for (int i = 0; i < tmpList.size(); i++) {
                String name = tmpList.get(i);
                String cluster = mmasInstanceMap.get(node);
                if (cluster == null) {
                    return "NotFound";
                } else if (name.endsWith(cluster)) {
                    return name;
                }
            }
            logger.warn("Cannot find matching string!");
            return "NotFound";
        }
    }

    public static String getMmasTrafficSafSu(int subrack, int slot) {
        return getString(suPrototypeList, ".*MMAS.*TRAFFIC.*", subrack, slot);
    }

    public static String getMmasOamSafSu(int subrack, int slot) {
        return getString(suPrototypeList, ".*MMAS.*OAM.*", subrack, slot);
    }

    public static String getMmasTrafficSafComp(int subrack, int slot) {
        return getString(safCompList, ".*MMAS.*(INSTANCE|TRAFFIC).*", subrack, slot);
    }

    public static String getMmasOamSafComp(int subrack, int slot) {
        return getString(safCompList, ".*MMAS.*(INSTANCE|OAM).*", subrack, slot);
    }

    public static String getMmasTrafficSafSi(int subrack, int slot) {
        return getString(siInstanceList, ".*MMAS.*TRAFFIC.*", subrack, slot);
    }

    public static String getMmasOamSafSi(int subrack, int slot) {
        return getString(siInstanceList, ".*MMAS.*OAM.*", subrack, slot);
    }

    public static Map<String, String> getMmasTrafficInstanceMap() {
        HashMap<String, String> trafficMap = new HashMap<String, String>();
        for (String node : mmasInstanceMap.keySet()) {
            String cluster = mmasInstanceMap.get(node);
            if (cluster.contains("TRAFFIC")) {
                trafficMap.put(node, cluster);
            }
        }
        return trafficMap;
    }
}
