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

import java.util.ArrayList;
import java.util.Iterator;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.apache.commons.configuration.ConfigurationException;
import org.apache.commons.configuration.HierarchicalConfiguration.Node;
import org.apache.commons.configuration.XMLConfiguration;
import org.apache.commons.configuration.tree.ConfigurationNode;
import org.apache.log4j.Logger;

/**
 * The purpose of this class is to parse the XMLconfiguration given as input in the constructor. It is not a general
 * parser of configurations but rather a specific implementation designed to parse a versions file.
 */

public class VersionParser {

    static private Logger logger = Logger.getLogger(VersionParser.class.getName());

    static private VersionParser vp = new VersionParser();
    static private XMLConfiguration versions;
    static private Pattern ericssonRevFinder = Pattern.compile("([PRpr]\\d+[a-zA-Z]+\\d+)");
    static private Pattern ericssonRevMatcher = Pattern.compile("^([PRpr])(\\d+)([a-zA-Z]+)(\\d+)$");

    static public VersionParser getInstance() {
        return vp;
    }

    private VersionParser() {
        final String fn = System.getProperty("versionsConfigFile");
        try {
            setVersions(new XMLConfiguration(fn));
        } catch (ConfigurationException e) {
            logger.error("Versions config data not readable", e);
        }
    }

    /**
     * 
     * @return the product Ids that matches the product name
     */
    public ArrayList<String> getProductIds(String productName) {
        ArrayList<String> productIds = new ArrayList<String>();
        String[] products = getProductIds();
        for (int j = 0; j < products.length; j++) {
            String prodId = products[j];
            if (getName(prodId).equals(productName)) {
                productIds.add(prodId);
            }
        }
        return productIds;
    }

    /**
     * 
     * @return An ordered array with the product identities found in the file
     */
    public String[] getProductIds() {
        Node[] products = getProducts();
        String[] productIds = new String[products.length];
        for (int j = 0; j < products.length; j++) {
            productIds[j] = products[j].getAttribute(0).getValue().toString();
        }

        return productIds;
    }

    /**
     * 
     * @param id
     *            , product identity
     * @return true if the product can be found, otherwise false
     */
    public boolean isMemberOf(String id) {
        return (getProduct(id) != null);
    }

    /**
     * 
     * @param id
     *            , product identity
     * @return the version of the product, null if not found
     */
    public String getVersion(String id) {
        return getValue(id, "version");
    }

    /**
     * Look for ericsson revision number in String
     * 
     * @param stringToLook
     * @return null if not found
     */
    public static String findEricssonRev(String stringToLook) {
        Matcher m = ericssonRevFinder.matcher(stringToLook);
        if (m.find()) {
            return m.group();
        } else {
            logger.warn("Cannot find version number in string: " + stringToLook);
            return null;
        }
    }

    /**
     * 
     * @param id
     *            , product identity
     * @return the name of the product, null if not found
     */
    public String getName(String id) {
        return getValue(id, "name");
    }

    /**
     * 
     * @param id
     *            , product identity
     * @return The value of the extension property
     */
    public String getExtension(String id) {
        return getValue(id, "extension");
    }

    /**
     * 
     * @param id
     *            , product identity
     * @return The value of the binary property
     */
    public String getBinary(String id) {
        return getValue(id, "binary");
    }

    /**
     * 
     * @param id
     *            , product identity
     * @return The value of the generator property
     */
    public String getGenerator(String id) {
        return getValue(id, "generator");
    }

    public boolean hasBinary(String id) {
        boolean returnValue = false;
        String bin = getBinary(id);
        if (bin != null && !(bin.equalsIgnoreCase("no"))) {
            returnValue = true;
        }
        return returnValue;
    }

    /**
     * 
     * @param id
     *            , product identity
     * @return true if the product has a jcat_omp_extensions subproject false otherwise
     */
    public boolean hasExtension(String id) {
        boolean returnValue = false;
        if (!(getExtension(id).equalsIgnoreCase("no"))) {
            returnValue = true;
        }
        return returnValue;
    }

    /**
     * 
     * @param id
     *            , product identity
     * @return true if the product has a jcat_omp_extensions subproject false otherwise
     */
    public boolean hasGenerator(String id) {
        boolean returnValue = false;
        if (!(getGenerator(id).equalsIgnoreCase("no"))) {
            returnValue = true;
        }
        return returnValue;
    }

    /**
     * 
     * @param rev
     *            , product rev
     * @return true if the rev is an Ericsson standard revision p = Pattern.compile("target_(.*).xml"); m =
     *         p.matcher(sutconf); if(m.find()) {
     */
    public boolean isEricssonRev(String rev) {
        boolean result = false;
        Matcher m = ericssonRevMatcher.matcher(rev);
        if (m.find()) {
            result = true;
        }
        return result;
    }

    /**
     * 
     * @param id
     * @param rev
     * @return true if product has higher version than the argument
     */
    public boolean isHigherOrEqualVersion(String id, String rev) {
        String version = getVersion(id);
        if (version == null) {
            logger.warn("Product " + id + " is not in product map");
            return false;
        }
        if (!isEricssonRev(rev) || !isEricssonRev(version)) {
            logger.warn("Cannot parse rev: " + rev + " . Not valid");
            return false;
        }
        if (isVersion(id, rev)) {
            return true;
        } else {
            String revOnNode = getVersion(id);
            if (!isPrefixEqual(parseRevPrefix(revOnNode), parseRevPrefix(rev))) {
                logger.warn("Prefix is not equal! " + revOnNode + " " + rev);
            }
            Matcher mRevOnNode = ericssonRevMatcher.matcher(revOnNode);
            Matcher mRev = ericssonRevMatcher.matcher(rev);
            if (mRevOnNode.find() && mRev.find()) {
                // Compare each section
                for (int i = 2; i <= mRevOnNode.groupCount(); i++) {
                    // upper and lower cases
                    String sOnNode = mRevOnNode.group(i).toUpperCase();
                    String sRev = mRev.group(i).toUpperCase();
                    // when the rev is in complete (R13 vs R13B01)
                    if (sOnNode.length() == 0 && sRev.length() != 0) {
                        sOnNode = sRev;
                    } else if (sRev.length() == 0 && sOnNode.length() != 0) {
                        sRev = sOnNode;
                    }
                    // change the strings into same length (R10 vs R9, change R9 to R09)
                    int lengthDifference = sOnNode.length() - sRev.length();
                    if (lengthDifference > 0) {
                        for (int a = 0; a < lengthDifference; a++) {
                            sRev = "0" + sRev;
                        }
                    } else if (lengthDifference < 0) {
                        for (int a = 0; a < 0 - lengthDifference; a++) {
                            sOnNode = "0" + sOnNode;
                        }
                    }
                    // compare each char in the string.
                    for (int a = 0; a < sOnNode.length(); a++) {
                        if (sRev.charAt(a) < sOnNode.charAt(a)) {
                            return true;
                        } else if (sRev.charAt(a) > sOnNode.charAt(a)) {
                            return false;
                        }
                    }
                }
                return true;
            } else {
                logger.error("Unexpected error! " + revOnNode + " " + rev);
                return false;
            }
        }
    }

    /**
     * 
     * @param id
     *            , product identity
     * @param rev
     *            , version
     * @return true if versions of product is equal to argument
     */
    public boolean isVersion(String id, String rev) {
        return getVersion(id).equalsIgnoreCase(rev);
    }

    /**
     * 
     * @param rev
     * @return the prefix of an Ericsson revision
     */
    public static String parseRevPrefix(String rev) {
        return getIndex(rev, 1);
    }

    /**
     * 
     * @param rev
     * @return the major number from an Ericsson revision
     */
    public static int parseRevMajor(String rev) {
        return Integer.parseInt(getIndex(rev, 2));
    }

    /**
     * 
     * @param rev
     * @return the minor number from an Ericsson revision
     */
    public static String parseRevMinor(String rev) {
        return getIndex(rev, 3);
    }

    /**
     * 
     * @param rev
     * @return the amendment level from an Ericsson revision
     */
    public static int parseRevAmendment(String rev) {
        return Integer.parseInt(getIndex(rev, 4));
    }

    /**
     * 
     * @param pref1
     * @param pref2
     * @return true if prefix1 is greater than prefix2
     */
    private boolean isPrefixEqual(String pref1, String pref2) {
        return pref1.equalsIgnoreCase(pref2);
    }

    /**
     * 
     * @param rev
     * @param i
     * @return group(i) from an Ericsson revision
     */
    private static String getIndex(String rev, int i) {
        String result = null;
        Matcher m = ericssonRevMatcher.matcher(rev);
        if (m.find()) {
            result = m.group(i);
        }
        return result;

    }

    /*
     * 
     * @param id, product identity
     * 
     * @param item, sub node to get value for
     */
    private String getValue(String id, String item) {
        String value = null;

        if (isMemberOf(id)) {
            Node product = getProduct(id);
            for (int i = 0; i < product.getChildrenCount(); i++) {
                ConfigurationNode n = product.getChild(i);
                if (item.equals(n.getName())) {
                    value = n.getValue().toString();
                    break;
                }

            }
        }

        return value;
    }

    /*
     * 
     * @return An array with all product nodes
     */
    @SuppressWarnings("unchecked")
    private Node[] getProducts() {
        Node[] products = new Node[getVersions().getRoot().getChildrenCount()];
        Iterator<Node> i = getVersions().getRoot().getChildren().iterator();
        for (int j = 0; j < products.length; j++) {
            products[j] = i.next();
        }

        return products;
    }

    /*
     * 
     * @param id, product identity
     * 
     * @return The node with matching product id
     */
    private Node getProduct(String id) {
        Node product = null;
        Node[] products = getProducts();

        for (int i = 0; i < products.length; i++) {
            if (id.equals(products[i].getAttribute(0).getValue().toString())) {
                product = products[i];
                break;
            }
        }
        return product;
    }

    /*
     * 
     * @return the versions configuration structure
     */
    private XMLConfiguration getVersions() {
        return versions;
    }

    /**
     * 
     * @param conf
     *            , The versions configuration structure
     */
    private void setVersions(XMLConfiguration conf) {
        versions = conf;
    }
}
