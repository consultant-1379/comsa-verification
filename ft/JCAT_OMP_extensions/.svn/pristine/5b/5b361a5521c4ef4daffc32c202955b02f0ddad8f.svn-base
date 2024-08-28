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
package se.ericsson.jcat.omp.library;

import java.io.IOException;

import org.apache.log4j.Level;
import org.apache.log4j.Logger;
import org.python.core.PyDictionary;
import org.python.core.PyList;
import org.python.core.PyString;
import org.python.util.PythonInterpreter;
import org.w3c.dom.Document;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.w3c.dom.Text;

import se.ericsson.jcat.fw.jython.Jythonizer;
import se.ericsson.jcat.omp.fw.OmpLibrary;
import se.ericsson.jcat.omp.fw.OmpSut;

/**
 * 
 * The purpose of this class is ... TODO javadoc for class TargetDataLibImpl
 */
public class TargetDataLibImpl extends OmpLibrary implements TargetDataLib {
    private static Logger logger = Logger.getLogger(TargetDataLibImpl.class);

    private PythonInterpreter interp = null;

    OmpSut sut = null;

    /**
     * Creates a new instance of <code>TargetDataLibImpl</code>.
     * 
     * @param sut
     * @throws Exception
     */
    public TargetDataLibImpl(OmpSut sut) throws Exception {
        this.sut = sut;
        this.interp = Jythonizer.getInstance();
        logger.setLevel(Level.INFO);
    }

    /**
     * Returns the unique name of this library.
     */
    public String getName() {
        return "TargetDataLib";
    }

    /**
     * Method called by LibraryBroker to set the Sut of the library
     */
    public void setSut(final OmpSut sut) {
        this.sut = sut;
    }

    public void setUp() {
        // Do imports
        interp.exec("import omp.target.target_data as target_data");
        // Do setups

        logger.info("TargetDataLib: Initiating");
        if (sut.getXmlConfiguration() != null) {

            try {
                setTargetData(sut.getXmlConfiguration().getDocument());
            } catch (IOException ioe) {
                logger.error("Failed to parse XML configuration data", ioe);
            }
        }
    }

    public void tearDown() {

    }

    /**
     * Returns LoggerLib as runtime dependency.
     */
    public String[] getRuntimeDependencies() {
        return new String[] { "LoggerLib" };
    }

    /**
     * Returns LoggerLib as setup dependency.
     */
    public String[] getSetupDependencies() {
        return new String[] { "LoggerLib" };
    }

    public PyDictionary getTargetData() {
        interp.exec("result = target_data.getTargetHwData()");
        final PyDictionary targetData = (PyDictionary) interp.get("result");
        return targetData;
    }

    public PyDictionary setTargetData(Document doc) throws IOException {
        logger.info("Creating target_data dictionary from XML data");

        /*
         * Verify that the top level only have one child.
         */
        NodeList children = doc.getChildNodes();
        if (children.getLength() != 1) {
            throw new IOException("Malformed config data");
        }

        /*
         * The first child becomes top node and should not be part in the resulting structure.
         */
        Node root = children.item(0);
        logger.debug("Top node = " + root.getNodeName());

        /* Create top dictionary instance */
        PyDictionary dict = new PyDictionary();

        /* Remove any whitespace nodes */
        cleanWhitespace(root);
        /* Traverse document and populate dictionary */
        traverseNodes(root, dict);

        logger.debug("Result dictionary = " + dict.toString());

        /* Set the created dictionary to be active in target_data */
        interp.exec("result = target_data.setTargetXmlData(" + dict + ")");

        return dict;
    }

    /*
     * Traverse the document tree from top and populate the Python dictionary structure.
     */
    private void traverseNodes(Node n, PyDictionary dict) throws IOException {
        PyDictionary newDict = null;
        NodeList children = n.getChildNodes();

        if (children != null) {
            for (int i = 0; i < children.getLength(); i++) {
                Node childNode = children.item(i);

                if (childNode.getNodeType() == Node.ELEMENT_NODE) {
                    logger.debug("Processing element node = " + childNode.getNodeName());
                    NodeList grandChildren = childNode.getChildNodes();
                    if (grandChildren.getLength() <= 0) {
                        throw new IOException("Malformed config data");
                    }
                    Node grandChild = grandChildren.item(0);
                    if (grandChild.getNodeType() == Node.ELEMENT_NODE) {
                        newDict = new PyDictionary();
                        dict.__setitem__(new PyString(childNode.getNodeName()), newDict);
                    }
                } else if (childNode.getNodeType() == Node.TEXT_NODE) {
                    String text = ((Text) childNode).getData();
                    logger.debug("Processing text node = " + text);
                    if (text.startsWith("[") && text.endsWith("]")) {
                        String subText = text.substring(1, text.length() - 1);
                        String[] list = subText.split("\\\\,");
                        PyString[] pList = new PyString[list.length];
                        for (int j = 0; j < list.length; j++) {
                            pList[j] = new PyString(list[j]);
                        }
                        dict.__setitem__(new PyString(childNode.getParentNode().getNodeName()), new PyList(pList));
                    } else {
                        dict.__setitem__(new PyString(childNode.getParentNode().getNodeName()), new PyString(text));
                    }
                } else {
                    throw new IOException("Malformed config data");
                }

                if (newDict == null) {
                    traverseNodes(childNode, dict);
                } else {
                    traverseNodes(childNode, newDict);
                }
            }
        }
    }

    /*
     * Remove any text nodes only containing whitespace characters from the document.
     */
    private void cleanWhitespace(Node n) {
        NodeList children = n.getChildNodes();
        if (children != null) {
            for (int i = 0; i < children.getLength(); i++) {
                Node childNode = children.item(i);
                if (childNode.getNodeType() == Node.TEXT_NODE && (!((Text) childNode).getData().matches("\\S+"))) {
                    logger.debug("Removing text node = " + ((Text) childNode).getData());
                    n.removeChild(children.item(i));
                    i--;
                }
                cleanWhitespace(childNode);
            }
        }
    }
}
