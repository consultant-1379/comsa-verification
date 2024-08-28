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

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Hashtable;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.Vector;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.apache.log4j.Logger;
import org.python.core.PyException;
import org.python.core.PyObject;
import org.python.core.PyTuple;
import org.python.util.PythonInterpreter;

import se.ericsson.jcat.fw.jython.Jythonizer;
import se.ericsson.jcat.fw.utils.TestInfo;
import se.ericsson.jcat.omp.fw.OmpLibrary;
import se.ericsson.jcat.omp.fw.OmpLibraryException;
import se.ericsson.jcat.omp.fw.OmpSut;
import se.ericsson.jcat.omp.util.Tools;

/**
 * The purpose of this class is ... TODO javadoc for class LoggerLibImpl
 */
public class SafLibImpl extends OmpLibrary implements SafLib {
    private static Logger logger = Logger.getLogger(SshLibImpl.class);

    enum State {
        GET_CSI_COMP, GET_CSI_STATE
    }

    public static enum CampaignType {
        INSTALL, REMOVAL, UPGRADE
    }

    private PythonInterpreter interp = null;

    OmpSut sut = null;

    SshLib ssh = null;
    OsLib os = null;

    /**
     * Creates a new instance of <code>SshLib</code>.
     * 
     * @param sut
     * @throws Exception
     */
    public SafLibImpl(final OmpSut sut) throws Exception {
        this.sut = sut;
        this.interp = Jythonizer.getInstance();
    }

    /**
     * Returns the unique name of this library.
     */
    @Override
    public String getName() {
        return "SafLib";
    }

    /**
     * Method called by LibraryBroker to set the Sut of the library
     */
    @Override
    public void setSut(final OmpSut sut) {
        this.sut = sut;
    }

    /**
     * TODO - Comment me
     */
    @Override
    public void setUp() {
        ssh = (SshLib) sut.getLibrary("SshLib");
        os = (OsLib) sut.getLibrary("OsLib");
        // Do imports
        interp.exec("import coremw.saf_lib as saf_lib");
        interp.exec("if(hasattr(saf_lib, 'setUp')): saf_lib.setUp()");
        interp.set("sut", sut);
        interp.exec("saf_lib.setSut(sut)");
    }

    /**
     * TODO - Comment me
     */
    @Override
    public void tearDown() {
        interp.exec("if(hasattr(saf_lib, 'tearDown')): saf_lib.tearDown()");
    }

    /**
     * Returns LoggerLib as runtime dependency.
     */
    @Override
    public String[] getRuntimeDependencies() {
        return new String[] { "SshLib", "LoggerLib", "OsLib" };
    }

    /**
     * Returns LoggerLib as setup dependency.
     */
    @Override
    public String[] getSetupDependencies() {
        return new String[] { "LoggerLib", "SshLib", "OsLib" };
    }

    public String getAmfNodeName(int subrack, int slot) {
        return getType(subrack, slot) + getSeparator() + slot;
    }

    public int getSubrack(String amfNodeName) {
        String[] tmp = amfNodeName.split(getSeparator());
        int result = 2; // if we get a hostname called PL-3 like it is in CBA,
                        // for example
        if (tmp.length == 3) { // if we get a hostname like the old style PL-2-3
            return Integer.parseInt(tmp[1]); // Array [PL,2,3], tmp[1] = 2
        }
        return result;
    }

    public int getSlot(String amfNodeName) {
        String[] tmp = amfNodeName.split(getSeparator());
        return Integer.parseInt(tmp[tmp.length - 1]);
    }

    public boolean isPL(int subrack, int slot) {
        return getType(subrack, slot).equals(getPL());
    }

    public boolean isSC(int subrack, int slot) {
        return getType(subrack, slot).equals(getSC());
    }

    public Map<String, String> getAmfNodeAdminState() throws OmpLibraryException {

        logger.info("Getting amfNodeAdminState");
        boolean state = true;
        String node = "";
        String adminState;
        Map<String, String> nodeAdminStates = new HashMap<String, String>();

        for (String line : cmwStatusWithDetail("node").split("\n")) {
            if (state) {
                Pattern p1 = Pattern.compile("safAmfNode=(\\S*),safAmfCluster=(\\S*)");
                Matcher m = p1.matcher(line);
                if (m.matches()) {
                    state = false;
                    node = m.group(1);
                }
            } else {
                Pattern p2 = Pattern.compile(".*AdminState=(\\S*)\\(.*");
                Matcher m = p2.matcher(line);
                if (m.matches()) {
                    state = true;
                    adminState = m.group(1);
                    nodeAdminStates.put(node, adminState);
                }
            }
        }
        logger.info("Current amfNodeAdminState is: " + nodeAdminStates.toString());
        return nodeAdminStates;
    }

    public Map<String, String> getAmfNodeOperState() throws OmpLibraryException {

        logger.info("Getting amfNodeOperState");
        boolean state = true;
        String node = "";
        String operState;
        Map<String, String> nodeOperStates = new HashMap<String, String>();

        for (String line : cmwStatusWithDetail("node").split("\n")) {
            if (state) {
                Pattern p1 = Pattern.compile("safAmfNode=(\\S*),safAmfCluster=(\\S*)");
                Matcher m = p1.matcher(line);
                if (m.matches()) {
                    state = false;
                    node = m.group(1);
                }
            } else {
                Pattern p2 = Pattern.compile(".*OperState=(\\S*)\\(.*");
                Matcher m = p2.matcher(line);
                if (m.matches()) {
                    state = true;
                    operState = m.group(1);
                    nodeOperStates.put(node, operState);
                }
            }
        }
        logger.info("Current amfNodeAdminState is: " + nodeOperStates.toString());
        return nodeOperStates;
    }

    public Map<String, String> getWantedAmfNodeAdminState() {
        Map<String, String> wantedAdminState = new HashMap<String, String>();
        final String s = sut.getConfigDataString("physical_size");
        final int size = Integer.parseInt(s);

        for (int i = 1; i <= size; i++) {
            String amfNode = getAmfNodeName(2, i);
            wantedAdminState.put(amfNode, "UNLOCKED");
        }
        return wantedAdminState;
    }

    public Map<String, String> getWantedAmfNodeOperState() {
        Map<String, String> wantedOperState = new HashMap<String, String>();
        final String s = sut.getConfigDataString("physical_size");
        final int size = Integer.parseInt(s);

        for (int i = 1; i <= size; i++) {
            String amfNode = getAmfNodeName(2, i);
            wantedOperState.put(amfNode, "ENABLED");
        }
        return wantedOperState;
    }

    public boolean isAmfNodeAdminState(Map<String, String> wantedState) throws OmpLibraryException {
        Map<String, String> actualState = getAmfNodeAdminState();
        return wantedState.equals(actualState);
    }

    public boolean isAmfNodeOperState(Map<String, String> wantedState) throws OmpLibraryException {
        Map<String, String> actualState = getAmfNodeOperState();
        return wantedState.equals(actualState);
    }

    public boolean isNodesInServiceState(Map<String, String> wantedState) throws OmpLibraryException {
        Map<String, String> actualState = getNodesInServiceState();
        return wantedState.equals(actualState);
    }

    public Map<String, String> updateAmfNodeAdminState(int subrack, int slot, String state,
            Map<String, String> amfNodeState) throws OmpLibraryException {
        Map<String, String> returnValue = new HashMap<String, String>(amfNodeState);
        String amfNode = getAmfNodeName(subrack, slot);
        if (returnValue.containsKey(amfNode)) {
            returnValue.put(amfNode, state);
        } else {
            throw new OmpLibraryException("Node not found: " + amfNode);
        }
        return returnValue;
    }

    @Override
    public Map<String, Map<String, String>> getSafAppHAState(String safAppName) throws OmpLibraryException {
        return getSafAppHAState(safAppName, getCompleteHAStateInRawFormat());
    }

    @Override
    public Map<String, Map<String, String>> getSafAppHAState(String safAppName, String cachedHAStateInRawFormat)
            throws OmpLibraryException {
        String node = "";
        String csi = "";
        String csiState = "";
        State state;

        state = State.GET_CSI_COMP;

        logger.info("Getting HA state");
        logger.debug("Cached HA state: " + cachedHAStateInRawFormat);

        Map<String, Map<String, String>> nodeAmfCSICompHaStates = new HashMap<String, Map<String, String>>();
        for (String line : cachedHAStateInRawFormat.split("\n")) {
            if (state == State.GET_CSI_COMP) {
                Pattern p1 = Pattern.compile(".*safCSIComp.*safSu=(\\S*)\\\\,.*safSg.*safApp=" + safAppName
                        + ".*safCsi=(\\S*)\\,.*safSi.*");
                Matcher m = p1.matcher(line);
                if (m.matches()) {
                    node = m.group(1);
                    csi = m.group(2);
                    // if this is the first time we get a record for this node,
                    // create a new csi hashmap.
                    if (nodeAmfCSICompHaStates.get(node) == null) {
                        Map<String, String> amfCSICompHaStates = new HashMap<String, String>();
                        nodeAmfCSICompHaStates.put(node, amfCSICompHaStates);
                    }
                    state = State.GET_CSI_STATE;
                }
            } else {
                Pattern p2 = Pattern.compile(".*HAState=(\\S*)\\(.*");
                Matcher m = p2.matcher(line);
                if (m.matches()) {
                    state = State.GET_CSI_COMP;
                    csiState = m.group(1);
                    // get the node hashmap, and insert the csi + its state
                    Map<String, String> nodeCSIStatesMap = nodeAmfCSICompHaStates.get(node);
                    nodeCSIStatesMap.put(csi, csiState);
                }
            }
        }
        logger.info("Current HA state is: " + nodeAmfCSICompHaStates);
        return nodeAmfCSICompHaStates;
    }

    @Override
    public String getCompleteHAStateInRawFormat() throws OmpLibraryException {
        return cmwStatusWithDetail("csiass");
    }

    public Map<String, Map<String, String>> getHAState() throws OmpLibraryException {
        return getSafAppHAState(".*");// Will take all SafApp's.
    }

    public Map<String, Map<String, String>> getHAState(int subrack, int slot) throws OmpLibraryException {

        String node = getAmfNodeName(subrack, slot);
        List<String> nonAssociatedNodes = new Vector<String>();
        Map<String, Map<String, String>> amfCSICompHaStates = getHAState();
        Iterator<String> nodeMapIterator = amfCSICompHaStates.keySet().iterator();

        while (nodeMapIterator.hasNext()) {
            String key = nodeMapIterator.next();
            if (!key.equals(node)) {
                nonAssociatedNodes.add(key);
            }
        }
        Iterator<String> iterator = nonAssociatedNodes.iterator();
        while (iterator.hasNext()) {
            String key = iterator.next();
            amfCSICompHaStates.remove(key);
        }
        return amfCSICompHaStates;
    }

    public Map<String, String> getHAState(String siName) throws OmpLibraryException {
        Map<String, Map<String, String>> states = getHAState();
        Map<String, String> result = new HashMap<String, String>();
        Iterator<String> it = states.keySet().iterator();
        while (it.hasNext()) {
            String node = it.next();
            if (states.get(node).get(siName) != null) {
                result.put(node, states.get(node).get(siName));
            }
        }

        return result;
    }

    public Map<String, Map<String, String>> getComponentHAState(String[] csiList) throws OmpLibraryException {

        List<String> nonAssociatedCSIs = new Vector<String>();
        List<String> emptyNodes = new Vector<String>();
        Map<String, Map<String, String>> componentStatusMap = getHAState();

        for (String key : componentStatusMap.keySet()) {
            Map<String, String> csiMap = componentStatusMap.get(key);
            for (String csi : csiMap.keySet()) {
                boolean foundMatch = false;
                for (String component : csiList) {
                    // compare all csi in the subset (belonging to the specific
                    // component, eg. CoreMW)
                    // to the ones in the complete list.
                    if (csi.equals(component)) {
                        foundMatch = true;
                    }
                }
                if (!foundMatch) {
                    // in case we do not find a csi in the subset list, put it
                    // in the
                    // nonAssociatedCSIs vector for removal later
                    nonAssociatedCSIs.add(csi);
                }
            }
            if (nonAssociatedCSIs.size() != 0) {
                for (String comp : nonAssociatedCSIs) {
                    // remove the csi:s that are not associated to this
                    // component
                    csiMap.remove(comp);
                }
                if (csiMap.isEmpty()) {
                    emptyNodes.add(key);
                }
            }
        }

        for (String emptyNode : emptyNodes) {
            componentStatusMap.remove(emptyNode);
        }
        logger.info("Returning component HA state map: " + componentStatusMap);
        return componentStatusMap;
    }

    public Map<String, Map<String, String>> getCMWHAState() throws OmpLibraryException {

        logger.debug("Enter getCMWHAState()");

        String[] application = { "OpenSAF", "ERIC-CoreMW", "OSAlarmBridge", "AaService1" };
        String[] csis = getComponents(application);
        return getComponentHAState(csis);
    }

    public boolean isHAState(boolean exactMatch, Map<String, Map<String, String>> actualState,
            Map<String, Map<String, String>> wantedState, Map<String, Map<String, String>> redundancyMap)
            throws OmpLibraryException {

        boolean result = true;

        if (exactMatch) {
            // if exactMatch is true, we care about which SC is standby and
            // which is active.
            // This means we need an exact match to the state, even on the SC:s
            if (!actualState.equals(wantedState)) {
                logger.warn("Actual and Wanted state HashMaps are not equal");
                logger.warn("Actual: " + actualState);
                logger.warn("Wanted: " + wantedState);
                return false;
            }
        } else {
            // if exactMatch is false, we don't care which SC is active and
            // which is standby
            if (actualState.keySet().equals(wantedState.keySet())) {
                // nodes are the same, let's continue...
                Iterator<String> it = actualState.keySet().iterator();
                // for each node...
                while (it.hasNext()) {
                    String node = it.next();
                    // check if the components are the same for all nodes
                    if (!(wantedState.get(node).keySet()).equals(actualState.get(node).keySet())) {
                        logger.warn("Node " + node + " does not hold expected components.");
                        logger.warn("Wanted  : " + wantedState.get(node).keySet());
                        logger.warn("Actual: " + actualState.get(node).keySet());
                        return false;
                    }
                    // operate on the component hashmaps.
                    Map<String, String> actualComponents = actualState.get(node);
                    Map<String, String> wantedComponents = wantedState.get(node);
                    Iterator<String> compIt = actualComponents.keySet().iterator();
                    while (compIt.hasNext()) {
                        String component = compIt.next();
                        String model = redundancyMap.get(node).get(component);
                        if (model == null) {
                            throw new OmpLibraryException("Could not find model for component " + component);
                        }
                        if (model.contains("NoRed")) {
                            // expect both maps to be equal
                            if (!actualComponents.get(component).equals(wantedComponents.get(component))) {
                                logger.warn("NoRed component " + component + " does not hold expected state.");
                                logger.warn("Expected: " + wantedComponents.get(component));
                                logger.warn("Found   : " + actualComponents.get(component));
                                return false;
                            }
                        } else if (model.contains("2N")) {
                            // find the matching component (2N should have two
                            // nodes including this component.
                            // some application also have single components with
                            // 2N
                            List<String> twoN = findComponent(component, actualState);
                            if (twoN.size() == 2) {
                                String node1WantedState = wantedState.get(twoN.get(0)).get(component);
                                String node1ActualState = actualState.get(twoN.get(0)).get(component);
                                String node2WantedState = wantedState.get(twoN.get(1)).get(component);
                                String node2ActualState = actualState.get(twoN.get(1)).get(component);

                                if (node1WantedState.equals(node2WantedState)) {
                                    logger.warn("Wanted States does not comply to 2N model.");
                                    logger.warn("Expected: ACTIVE,STANDBY or STANDBY,ACTIVE");
                                    logger.warn("Found   : " + node1WantedState + "," + node2WantedState);
                                    return false;
                                }
                                if (node1ActualState.equalsIgnoreCase("ACTIVE")) {
                                    if (!node2ActualState.equalsIgnoreCase("STANDBY")) {
                                        logger.warn("2N Components " + component + " on nodes " + twoN.get(0) + ","
                                                + twoN.get(1) + " does not match");
                                        logger.warn("Found   : " + twoN.get(0) + node1ActualState + "," + twoN.get(1)
                                                + node2ActualState);
                                        logger.warn("Expected:  ACTIVE,STANDBY");
                                        return false;
                                    }
                                } else if (node1ActualState.equalsIgnoreCase("STANDBY")) {
                                    if (!node2ActualState.equalsIgnoreCase("ACTIVE")) {
                                        logger.warn("2N Components " + component + " on nodes " + twoN.get(0) + ","
                                                + twoN.get(1) + " does not match");
                                        logger.warn("Found   : " + twoN.get(0) + node1ActualState + "," + twoN.get(1)
                                                + node2ActualState);
                                        logger.warn("Expected: STANDBY,ACTIVE");
                                        return false;
                                    }
                                } else {
                                    // no match
                                    logger.warn("Could not find expected state for component " + component
                                            + " on nodes " + twoN.get(0) + "," + twoN.get(1));
                                    logger.warn("Found   : " + node1ActualState + "," + node2ActualState);
                                    logger.warn("Expected: " + node1WantedState + "," + node2WantedState);
                                    return false;
                                }
                            } else if (twoN.size() == 1) {
                                if (!actualState.get(twoN.get(0)).equals(wantedComponents.get(twoN.get(0)))) {
                                    logger.warn("Single 2N component " + component + " states are not equal");
                                    logger.warn("Wanted : " + wantedComponents.get(twoN.get(0)));
                                    logger.warn("Found  : " + actualComponents.get(twoN.get(0)));
                                    return false;
                                }
                            } else {
                                throw new OmpLibraryException("Unexpected number of component " + component
                                        + " found, " + twoN.size());
                            }
                            // make sure one is active and one is standby
                        } else if (model.contains("NWay")) {
                            // TODO: currently the NWay model assumes all
                            // components to be in active state
                            // thus, expected both maps to be equal
                            // the code is duplicated from 2N, might need to
                            // change when preconditions for
                            // NWay changes
                            if (!actualComponents.get(component).equals(wantedComponents.get(component))) {
                                logger.warn("NWay component " + component + " does not hold expected state.");
                                logger.warn("Wanted : " + wantedComponents.get(component));
                                logger.warn("Found  : " + actualComponents.get(component));
                                return false;
                            }
                        } else {
                            throw new OmpLibraryException("Could not recognize redundancy model " + model);
                        }

                    }

                }
            } else {
                logger.warn("Nodes differ from expected.");
                logger.warn("Actual nodes: " + actualState.keySet() + " Wanted nodes: " + wantedState.keySet());
                return false;
            }
        }
        return result;
    }

    public Map<String, String> getCompRedundancyModel() throws OmpLibraryException {
        Map<String, String> sgMap = new HashMap<String, String>();
        String comp = "";
        String sg = "";
        for (String line : cmwStatusWithDetail("csiass").split("\n")) {
            Pattern p1 = Pattern.compile(".*safCSIComp=safComp=(\\S*)\\\\,safSu=.*safSg=(\\S*)\\\\,safApp=(\\S*),.*");
            Matcher m = p1.matcher(line);
            if (m.matches()) {
                comp = m.group(1);
                sg = m.group(2);
            }
            Pattern p2 = Pattern.compile(".*HAState=(\\S*)\\.*");
            Matcher m1 = p2.matcher(line);
            if (m1.matches()) {

            }
            sgMap.put(comp, sg);
        }
        // Returns a map with all redundancy models for all components
        return sgMap;
    }

    public Map<String, String> getCompRedundancyModel(String model) throws OmpLibraryException {
        Map<String, String> map = getCompRedundancyModel();
        List<String> notAssociatedModel = new Vector<String>();
        for (String key : map.keySet()) {
            if (!(map.get(key)).equals(model)) {
                notAssociatedModel.add(key);
            }
        }
        Iterator<String> i = notAssociatedModel.iterator();
        while (i.hasNext()) {
            map.remove(i.next());
        }
        // Returns a map with matching components for a specific redundancy
        // model
        return map;
    }

    public Map<String, Map<String, String>> getCMWWantedHAState() throws OmpLibraryException {

        final String[] CMW_APPLICATION = { "OpenSAF", "ERIC-CoreMW", "OSAlarmBridge", "AaService1" };
        final Map<String, List<String>> standby2N = new HashMap<String, List<String>>();
        final List<String> sc2 = new Vector<String>();
        sc2.add("SC-2N");
        standby2N.put(getAmfNodeName(2, 2), sc2);
        final Map<String, List<String>> standbyNway = new HashMap<String, List<String>>();

        return getWantedHAState(CMW_APPLICATION, standby2N, standbyNway);
    }

    public Map<String, Map<String, String>> getWantedHAState(String[] application, Map<String, List<String>> standby2N,
            Map<String, List<String>> standbyNway) throws OmpLibraryException {

        final String MODEL_2N = "2N";
        final String MODEL_NO_REDUNDANCY = "NoRed";
        final String MODEL_NWAY_ACTIVE = "NWay";
        final String STATE_ACTIVE = "ACTIVE";
        final String STATE_STANDBY = "STANDBY";

        Map<String, Map<String, String>> modelMap = null;
        Map<String, String> compMap = new HashMap<String, String>();
        Map<String, Map<String, String>> wantedStates = new HashMap<String, Map<String, String>>();

        // get the redundancy information from imm
        modelMap = getAppRedundancyImmData(application);
        String node = "";
        String comp = "";
        String model = "";
        Iterator<String> nodeIt = modelMap.keySet().iterator();
        while (nodeIt.hasNext()) {
            node = nodeIt.next();
            Map<String, String> wantedCompMap = new HashMap<String, String>();
            compMap = modelMap.get(node);
            Iterator<String> compIt = compMap.keySet().iterator();
            while (compIt.hasNext()) {
                comp = compIt.next();
                model = compMap.get(comp);
                if (model.contains(MODEL_NO_REDUNDANCY)) {
                    wantedCompMap.put(comp, STATE_ACTIVE);
                } else if (model.contains(MODEL_2N)) {
                    List<String> tmp = standby2N.get(node);
                    if (tmp != null) {
                        Iterator<String> tmpIter = tmp.iterator();
                        // go through the vector, if component matches, set it
                        // to standby
                        while (tmpIter.hasNext()) {
                            String si = tmpIter.next();
                            if (si.contains(comp) || si.equalsIgnoreCase("SC-2N")) {
                                wantedCompMap.put(comp, STATE_STANDBY);
                            }
                        }
                    } else {
                        wantedCompMap.put(comp, STATE_ACTIVE);
                    }
                } else if (model.contains(MODEL_NWAY_ACTIVE)) {
                    List<String> tmp = standbyNway.get(node);
                    if (tmp != null) {
                        Iterator<String> tmpIter = tmp.iterator();
                        // go through the vector, if component matches, set it
                        // to standby
                        while (tmpIter.hasNext()) {
                            String si = tmpIter.next();
                            if (si.contains(comp)) {
                                wantedCompMap.put(comp, STATE_STANDBY);
                            }
                        }
                    } else {
                        wantedCompMap.put(comp, STATE_ACTIVE);
                    }
                } else {
                    throw new OmpLibraryException("Can't find the expected redundancy model, " + model);
                }
            }
            wantedStates.put(node, wantedCompMap);

        }
        logger.info("Returning Wanted States: " + wantedStates);
        return wantedStates;
    }

    public Map<String, Map<String, String>> getCMWRedundancyModel() throws OmpLibraryException {

        String[] safApps = { "OpenSAF", "ERIC-CoreMW", "OSAlarmBridge", "AaService1" };
        return this.getAppRedundancyImmData(safApps);
    }

    public Map<String, Map<String, String>> updateWantedHAState(int subrack, int slot, String state,
            Map<String, Map<String, String>> redundancyModel, Map<String, Map<String, String>> wantedState)
            throws OmpLibraryException {

        Map<String, Map<String, String>> newState = new HashMap<String, Map<String, String>>(wantedState);
        Map<String, String> values = new HashMap<String, String>();
        String amfNode = this.getAmfNodeName(subrack, slot);

        if (state.equals("ACTIVE") || state.equals("STANDBY")) {

            if (newState.keySet().contains(amfNode)) {
                values = newState.get(amfNode);
            } else {
                throw new OmpLibraryException("Unknown node, " + amfNode);
            }
            // compare the value map (all components for this node)
            // with the redundancy model map.
            // for each component that is 2N, change the state.
            Map<String, String> redValues = redundancyModel.get(amfNode);
            Iterator<String> it = values.keySet().iterator();
            while (it.hasNext()) {
                String comp = it.next();
                ;
                String model = redValues.get(comp);
                if (model != null) {
                    if (model.contains("2N")) {
                        values.put(comp, state);
                    }
                } else {
                    throw new OmpLibraryException("Cannot find component " + comp + " in redundancy model map.");
                }
            }

            newState.put(amfNode, values);
        } else {
            throw new OmpLibraryException("Unknown state, " + state);
        }

        return newState;
    }

    public Map<String, Map<String, String>> removeNodeFromWantedHAState(int subrack, int slot,
            Map<String, Map<String, String>> wantedState) throws OmpLibraryException {

        Map<String, Map<String, String>> newState = new HashMap<String, Map<String, String>>(wantedState);
        String amfNode = this.getAmfNodeName(subrack, slot);

        if (wantedState.containsKey(amfNode)) {
            Iterator<String> it = wantedState.keySet().iterator();
            while (it.hasNext()) {
                if (it.next().equals(amfNode)) {
                    newState.remove(amfNode);
                }
            }
            logger.info("Returning new state with node " + amfNode + " removed. " + newState);
            return newState;
        } else {
            throw new OmpLibraryException("Node " + amfNode + " not recognized in state map ");
        }
    }

    public boolean isCmwHAState(Map<String, Map<String, String>> wantedState) throws OmpLibraryException {
        logger.debug("Enter isCmwHAState()");
        String[] cmwApps = { "OpenSAF", "ERIC-CoreMW", "OSAlarmBridge", "AaService1" };
        return isHAState(false, this.getCMWHAState(), wantedState, getAppRedundancyImmData(cmwApps));
    }

    public boolean waitForCmwHAState(Map<String, Map<String, String>> wantedState, int timeout) {
        logger.debug("Enter waitForCmwHAState()");
        return Tools.waitUntilTrue(this, "isCmwHAState", new Object[] { wantedState }, 10, timeout);
    }

    public Map<String, String> getNodesInServiceState() throws OmpLibraryException {
        logger.debug("Enter getNodesInServiceState()");

        Map<String, String> states = new HashMap<String, String>();
        String node = "";
        String readistate = "";
        boolean foundCpnd = false;

        for (String line : cmwStatusWithDetail("comp").split("\n")) {
            Pattern p1 = Pattern.compile("safComp=CPND,.*safSu=(\\S*),safSg.*safApp.*");
            Matcher m = p1.matcher(line);
            if (m.matches()) {
                node = m.group(1);
                foundCpnd = true;
            }
            Pattern p2 = Pattern.compile(".*ReadinessState=(\\S*)\\(.*");
            Matcher m2 = p2.matcher(line);
            if (m2.matches() && foundCpnd) {
                readistate = m2.group(1);
                states.put(node, readistate);
                foundCpnd = false;
            }
        }
        return states;
    }

    public Map<String, String> getWantedNodesInServiceState() throws OmpLibraryException {
        Map<String, String> states = new HashMap<String, String>();

        final String s = sut.getConfigDataString("physical_size");
        final int size = Integer.parseInt(s);

        for (int i = 1; i <= size; i++) {
            String amfNode = getAmfNodeName(2, i);
            states.put(amfNode, "IN-SERVICE");
        }

        return states;
    }

    public Map<String, String> updateNodesInServiceState(int subrack, int slot, String state,
            Map<String, String> nodeState) throws OmpLibraryException {

        if (!(state.equals("IN-SERVICE") || state.equals("OUT-OF-SERVICE"))) {
            throw new OmpLibraryException("Invalid state, " + state);
        } else {
            Map<String, String> states = getNodesInServiceState();
            String downNode = this.getAmfNodeName(subrack, slot);
            boolean found = false;
            for (String node : states.keySet()) {
                if (node.equals(downNode)) {
                    states.put(node, state);
                    found = true;
                }
            }
            if (found) {
                return states;
            } else {
                throw new OmpLibraryException("Does not recognize expected node, " + downNode + ".");
            }
        }
    }

    public boolean waitForNodesInService(Map<String, String> wantedState, int timeout) throws OmpLibraryException {
        logger.debug("Enter waitForNodesInService()");
        return Tools.waitUntilTrue(this, "isNodesInServiceState", new Object[] { wantedState }, 10, timeout);
    }

    public boolean waitForAdministrativeState(Map<String, String> wantedState, int timeout) {
        logger.debug("Enter waitForAdministrativeState()");
        return Tools.waitUntilTrue(this, "isAmfNodeAdminState", new Object[] { wantedState }, 10, timeout);
    }

    public boolean waitForOperationalState(Map<String, String> wantedState, int timeout) {
        logger.debug("Enter waitForOperationalState()");
        return Tools.waitUntilTrue(this, "isAmfNodeOperState", new Object[] { wantedState }, 10, timeout);
    }

    /**
     * Get the list of SAF cluster nodes.
     * 
     * @return the list of node names as a Set of Strings
     * @throws OmpLibraryException
     *             on command error
     */
    public String[] getClusterNodes() throws OmpLibraryException {
        logger.debug("Enter getClusterNodes()");
        Set<String> keySet = getAmfNodeAdminState().keySet();
        Object[] objNodes = keySet.toArray();
        String[] strNodes = new String[objNodes.length];
        for (int i = 0; i < objNodes.length; i++) {
            strNodes[i] = objNodes[i].toString();
        }
        return strNodes;
    }

    /**
     * Get the list of SAF payload cluster nodes.
     * 
     * @return the list of node names as a Set of Strings
     * @throws OmpLibraryException
     *             on command error
     */
    public String[] getClusterNodesPL() throws OmpLibraryException {
        logger.debug("Enter getClusterNodesPL()");
        final String[] allNodes = getClusterNodes();
        final List<String> plNodes = new Vector<String>();
        String[] plNodesArray = new String[1];
        int subrack, slot;

        for (int i = 0; i < allNodes.length; i++) {
            subrack = getSubrack(allNodes[i]);
            slot = getSlot(allNodes[i]);
            if (isPL(subrack, slot)) {
                plNodes.add(allNodes[i]);
            }
        }
        plNodesArray = plNodes.toArray(plNodesArray);
        return plNodesArray;
    }

    /**
     * Get the list of SAF SC cluster nodes.
     * 
     * @return the list of node names as a Set of Strings
     * @throws OmpLibraryException
     *             on command error
     */
    public String[] getClusterNodesSC() throws OmpLibraryException {
        logger.debug("Enter getClusterNodesSC()");
        final String[] allNodes = getClusterNodes();
        final List<String> scNodes = new Vector<String>();
        String[] scNodesArray = new String[1];
        int subrack, slot;

        for (int i = 0; i < allNodes.length; i++) {
            subrack = getSubrack(allNodes[i]);
            slot = getSlot(allNodes[i]);
            if (isSC(subrack, slot)) {
                scNodes.add(allNodes[i]);
            }
        }
        scNodesArray = scNodes.toArray(scNodesArray);
        return scNodesArray;
    }

    public String getScStatus(int subrack, int slot) throws OmpLibraryException {
        logger.debug("Enter getScStatus()");
        String result = null;
        Map<String, String> siStates = getScInfo();
        String amfNode = getAmfNodeName(subrack, slot);

        if (siStates.containsKey(amfNode)) {
            result = siStates.get(amfNode);
        } else {
            throw new OmpLibraryException("No SC status for  " + amfNode + " found.");
        }
        return result;
    }

    // ----------------------------------------------------------

    // Specification: saf.getActiveSc()
    // 1) SC-1 Active & SC-2 DOWN => return SC-1
    // 2) SC-1 DOWN & SC-2 Active => return SC-2
    // 3) SC-1 Active & SC-2 Standby => return SC-1
    // 4) SC-1 Standby & SC-2 Active => return SC-2
    // 5) SC-1 Standby & SC-2 Standby => OmpLibraryException(No SC report Active
    // state)
    // 6) SC-1 Active & SC-2 Active => OmpLibraryException (Both SCs report
    // Active state)

    public String getActiveSc() throws OmpLibraryException {
        return getActiveSc(".*");
    }

    public String getActiveSc(String app) throws OmpLibraryException {
        logger.debug("Enter getActiveSc()");
        Boolean sc1_Active = false;
        Boolean sc2_Active = false;
        Map<String, String> siStates = getScInfo(app);

        // SC-1 Executing? Check SC state
        if (siStates.containsKey(getAmfNodeName(2, 1))) {
            logger.info(getAmfNodeName(2, 1) + ": " + siStates.get(getAmfNodeName(2, 1)));
            if ((siStates.get(getAmfNodeName(2, 1))).equalsIgnoreCase("ACTIVE")) {
                sc1_Active = true;
            }
        } else {
            logger.info(getAmfNodeName(2, 1) + ": DOWN");
        }

        // SC-2 Executing? Check SC state
        if (siStates.containsKey(getAmfNodeName(2, 2))) {
            logger.info(getAmfNodeName(2, 2) + ": " + siStates.get(getAmfNodeName(2, 2)));
            if ((siStates.get(getAmfNodeName(2, 2))).equalsIgnoreCase("ACTIVE")) {
                sc2_Active = true;
            }
        } else {
            logger.info(getAmfNodeName(2, 2) + ": DOWN");
        }

        // Return
        if (sc1_Active && !sc2_Active) { // SC-2-1 Active only. OK!
            return getAmfNodeName(2, 1);
        } else if (!sc1_Active && sc2_Active) { // SC-2-2 Active only. OK!
            return getAmfNodeName(2, 2);
        } else if (!sc1_Active && !sc2_Active) { // No Active SC. Not OK!
            throw new OmpLibraryException("No SC report Active state: " + siStates);
        } else if (sc1_Active && sc2_Active) { // Both SCs Active. Not OK!
            throw new OmpLibraryException("Both SCs report Active state: " + siStates);
        }

        return null;
    }

    // ----------------------------------------------------------

    public String getStandbySc() throws OmpLibraryException {
        return getStandbySc(".*");
    }

    public String getStandbySc(String app) throws OmpLibraryException {
        logger.debug("Enter getStandbySc()");
        String result = null;
        Map<String, String> siStates = getScInfo(app);

        if (siStates.containsKey(getAmfNodeName(2, 1))) {
            if ((siStates.get(getAmfNodeName(2, 1))).equalsIgnoreCase("STANDBY")) {
                result = getAmfNodeName(2, 1);
            }
        }
        if (siStates.containsKey(getAmfNodeName(2, 2))) {
            if ((siStates.get(getAmfNodeName(2, 2))).equalsIgnoreCase("STANDBY")) {
                result = getAmfNodeName(2, 2);
            }
        } else {
            throw new OmpLibraryException("No standby SAF SC found: " + siStates);
        }
        if (result == null) {
            throw new OmpLibraryException("No standby SAF SC found: " + siStates);
        }
        return result;
    }

    // Get the components associated with a specific application. Argument
    // 'application' is IMM safApp data
    public String[] getComponents(String[] application) throws OmpLibraryException {
        HashSet<String> compSet = new HashSet<String>();
        String comp = "";

        // Export IMM config to file if needed and get the file name of the file
        // to fetch.
        String[] localImmFileToFetch = exportImmConfig("/home/", "immdata.xml");
        String localImmFile = transfferBackFile(localImmFileToFetch[0], localImmFileToFetch[1]);
        for (String component : application) {
            String command = "cat " + localImmFile + " | grep \'\\<dn>safComp=' | grep " + component;
            String immList = localFileOperate(command);
            for (String line : immList.split("\n")) {
                Pattern p = Pattern.compile(".*safComp=(\\S*),safSu=(\\S*),safSg=(\\S*),safApp=(\\S*)<.*");
                Matcher m = p.matcher(line);
                if (m.matches()) {
                    comp = m.group(1);
                } else {

                }
                compSet.add(comp);
            }
        }
        return compSet.toArray(new String[0]);
    }

    public boolean installApplication(String campaignSdp, int timeout) throws OmpLibraryException {
        return modifyApplication(campaignSdp, timeout, CampaignType.INSTALL);
    }

    public boolean upgradeApplication(String campaignSdp, int timeout) throws OmpLibraryException {
        return modifyApplication(campaignSdp, timeout, CampaignType.UPGRADE);
    }

    public boolean removeApplication(String campaignSdp, int timeout) throws OmpLibraryException {
        return modifyApplication(campaignSdp, timeout, CampaignType.REMOVAL);
    }

    private boolean modifyApplication(String campaignSdp, int timeout, CampaignType type) throws OmpLibraryException {
        String campaignId = importSwBundleFromLocal(campaignSdp);
        logger.info("Starting campaign " + campaignId);
        // Execute campaign:
        this.upgradeStart(campaignId);

        // Wait until campaign execution has completed
        boolean result = waitForCampaignCompleted(campaignId, timeout);
        if (!result) {
            throw new OmpLibraryException("Campaign " + campaignId + " did not complete in time, interrupting...");
        }
        // Commit the campaign, but wait a while before doing so,
        // Stated in 2/1553-APR 901 0444/1 Uen A2 that when scripting this one
        // might get
        // error codes from imm if not sleeping.
        sleep(3);

        // don't commit if its a removal campaign
        if (!type.equals(CampaignType.REMOVAL)) {
            this.upgradeCommit(campaignId);
        }

        // should wait a while to remove sw bundle after commitment of campaign
        // otherwise it is very likely to failed to remove sdp
        sleep(3);
        // Remove the campaign SDP
        // TODO: on UPDATE, also remove the old application SDP
        this.removeSwBundle(campaignId);

        // Take a backup
        if (!this.backupCreate(campaignId + "_After_" + type + "_" + Tools.getCurrentTimeString())) {
            throw new OmpLibraryException("Could not create backup. Interrupting...");
        }
        return true;
    }

    private void sleep(int numOfSeconds) {
        try {
            logger.debug("Sleeping " + numOfSeconds + " seconds...");
            Thread.sleep(numOfSeconds * 1000);
        } catch (InterruptedException e) {
            logger.error("Interrupted while sleeping", e);
        }
    }

    // ==============================================================================New
    // CMW!

    public String install(String fileName) throws OmpLibraryException {
        logger.info("Installing " + fileName);
        interp.exec("result = saf_lib.install('" + fileName + "')");
        final PyTuple result = (PyTuple) interp.get("result");
        return parseJythonResult(result);
    }

    // New CMW!
    public String rebootCluster() throws OmpLibraryException {
        logger.info("Going to reboot cluster");
        interp.exec("result = saf_lib.clusterReboot()");
        final PyTuple result = (PyTuple) interp.get("result");
        return parseJythonResult(result);
    }

    public String rebootNode(int subrack, int slot) throws OmpLibraryException {
        logger.info("Rebooting node with subrack " + subrack + " and slot " + slot);
        interp.exec("result = saf_lib.clusterRebootNode(" + subrack + "," + slot + ")");
        final PyTuple result = (PyTuple) interp.get("result");
        return parseJythonResult(result);
    }

    public boolean backupCreate(String backupName, int timeout) throws OmpLibraryException {
        logger.info("Creating backup with name " + backupName);
        String res;
        String to = Integer.toString(timeout);
        interp.exec("result = saf_lib.backupCreate('" + backupName + "," + to + "')");
        final PyTuple result = (PyTuple) interp.get("result");
        res = parseJythonResult(result);
        if (res.contains("failed")) {
            return false;
        } else {
            return true;
        }
    }

    public boolean backupCreate(String backupName) throws OmpLibraryException {
        // default timeout = 2400
        logger.info("Creating backup with name " + backupName);
        String res;
        interp.exec("result = saf_lib.backupCreate('" + backupName + "')");
        final PyTuple result = (PyTuple) interp.get("result");
        res = parseJythonResult(result);
        if (res.contains("failed")) {
            return false;
        } else {
            return true;
        }

    }

    public boolean backupRestore(String backupName, int timeout) throws OmpLibraryException {
        logger.info("Restoring backup with name " + backupName);
        String res;
        String to = Integer.toString(timeout);
        interp.exec("result = saf_lib.backupRestore(" + backupName + "," + to + ")");
        final PyTuple result = (PyTuple) interp.get("result");
        res = parseJythonResult(result);
        if (res.contains("failed")) {
            return false;
        } else {
            return true;
        }
    }

    public boolean backupRestore(String backupName) throws OmpLibraryException {
        logger.info("Restoring backup with name " + backupName);
        // default timeout = 2400
        String res;
        interp.exec("result = saf_lib.backupRestore('" + backupName + "')");
        final PyTuple result = (PyTuple) interp.get("result");
        res = parseJythonResult(result);
        if (res.contains("failed")) {
            return false;
        } else {
            return true;
        }
    }

    public String backupList() throws OmpLibraryException {
        interp.exec("result = saf_lib.backupList()");
        final PyTuple result = (PyTuple) interp.get("result");
        return parseJythonResult(result);
    }

    public String backupRemove(String backupName) throws OmpLibraryException {
        logger.info("Removing backup with name " + backupName);
        interp.exec("result = saf_lib.backupRemove('" + backupName + "')");
        final PyTuple result = (PyTuple) interp.get("result");
        return parseJythonResult(result);
    }

    public String getInstalledSwOnRepository() throws OmpLibraryException {
        interp.exec("result = saf_lib.getInstalledSwOnRepository()");
        final PyTuple result = (PyTuple) interp.get("result");
        return parseJythonResult(result);
    }

    public String getInstalledSwOnNode(String nodeType, int subrack, int slot) throws OmpLibraryException {
        interp.exec("result = saf_lib.getInstalledSwOnNode('" + nodeType + "," + subrack + "," + slot + "')");
        final PyTuple result = (PyTuple) interp.get("result");
        return parseJythonResult(result);
    }

    public Map<String, List<String>> getInstalledSwOnAllNodes() throws OmpLibraryException {
        interp.exec("result = saf_lib.getInstalledSwOnAllNodes()");
        final PyTuple result = (PyTuple) interp.get("result");

        Map<String, List<String>> hash = new HashMap<String, List<String>>();
        String[] list = parseJythonResult(result).split("\n");
        for (int i = 0; i < list.length; i++) {
            String[] node = list[i].split(" ");
            if (node.length != 2) {
                throw new OmpLibraryException("Error parsing node software: " + list[i]);
            }

            if (hash.containsKey(node[0])) {
                hash.get(node[0]).add(node[1]);
            } else {
                ArrayList<String> array = new ArrayList<String>();
                array.add(node[1]);
                hash.put(node[0], array);
            }
        }

        return hash;
    }

    public String copySwPackageToSystem(String[] filePaths) throws OmpLibraryException {
        interp.exec("result = saf_lib.copySwPackageToSystem('" + filePaths + "')");
        final PyTuple result = (PyTuple) interp.get("result");
        return parseJythonResult(result);
    }

    public String importSwBundle(String swBundleFileName) throws OmpLibraryException {
        // Since python lib only accepts sdps be put in /home/coremw/incoming/
        // dir,
        // we should do a fix here.
        String sdpName = "";
        boolean fullPath = false;
        if (swBundleFileName.replaceFirst("/home/coremw/incoming/", "").contains("/")) {
            // swBundleFileName is a full path and not in /home/coremw/incoming/
            ssh.sendCommand("mkdir -p /home/coremw/incoming");
            ssh.sendCommand("cp " + swBundleFileName + " /home/coremw/incoming/");
            fullPath = true;
        }
        sdpName = (new File(swBundleFileName)).getName();
        interp.exec("result = saf_lib.importSwBundle('" + sdpName + "')");
        final PyTuple result = (PyTuple) interp.get("result");
        final String id = parseJythonResult(result);
        if (fullPath) {
            // Remove the copied file
            ssh.sendCommand("rm -f /home/coremw/incoming/" + sdpName);
        }
        return id;
    }

    public String importSwBundleFromLocal(String swBundleLocalPath) throws OmpLibraryException {
        logger.info("Copy file " + swBundleLocalPath + " to remote");
        ssh.sendCommand("rm -rf /home/coremw/incoming");
        ssh.sendCommand("mkdir -p /home/coremw/incoming");
        ssh.remoteCopy(swBundleLocalPath, "/home/coremw/incoming/", 120, 3);
        String filename = (new File(swBundleLocalPath)).getName();
        logger.info("Import sdp " + filename);
        return importSwBundle(filename);
    }

    public String checkCampaignStatus(String campaignId) throws OmpLibraryException {
        String line = Tools.runCommandRemote(ssh, "cmw-campaign-status " + campaignId).output;
        String statusLine = line.split("\n")[0];
        return statusLine.replace(campaignId + "=", "");
    }

    public String removeSwBundle(String swBundlePackageId) throws OmpLibraryException {
        logger.info("Removing SW bundle " + swBundlePackageId);
        interp.exec("result = saf_lib.removeSwBundle('" + swBundlePackageId + "')");
        final PyTuple result = (PyTuple) interp.get("result");
        return parseJythonResult(result);
    }

    public String removeAllSwFromCluster() throws OmpLibraryException {
        interp.exec("result = saf_lib.removeAllSwFromCluster()");
        final PyTuple result = (PyTuple) interp.get("result");
        return parseJythonResult(result);
    }

    public String upgradeStart(String campaignName) throws OmpLibraryException {
        interp.exec("result = saf_lib.upgradeStart('" + campaignName + "')");
        final PyTuple result = (PyTuple) interp.get("result");
        return parseJythonResult(result);
    }

    public String upgradeStatusCheck(String campaignName) throws OmpLibraryException {
        interp.exec("result = saf_lib.upgradeStatusCheck('" + campaignName + "')");
        final PyTuple result = (PyTuple) interp.get("result");
        return parseJythonResult(result);
    }

    public String upgradeCommit(String campaignName) throws OmpLibraryException {
        logger.info("Committing campaign " + campaignName);
        interp.exec("result = saf_lib.upgradeCommit('" + campaignName + "')");
        final PyTuple result = (PyTuple) interp.get("result");
        return parseJythonResult(result);
    }

    public boolean immSave() throws OmpLibraryException {
        return Tools.runCommandRemote(ssh, "cmw-immSave").returnValue == 0;
    }

    // ===========================PRIVATE
    // METHODS==========================================
    private String parseJythonResult(final PyTuple pt) throws OmpLibraryException {
        PyObject pyVerdict;
        PyObject pyMessage;
        try {
            pyVerdict = pt.__getitem__(0);
            logger.debug("Parsing PyTuple arg0: " + pyVerdict.toString());
            pyMessage = pt.__getitem__(1);
            logger.debug("Parsing PyTuple arg1: " + pyMessage.toString());
        } catch (final PyException pe) {
            throw new OmpLibraryException("Parsing error, PyTyple key not found: " + pe.toString());
        }

        // Do we need null checks on these?
        final String verdict = pyVerdict.toString();
        final String message = pyMessage.toString();

        if (!verdict.equalsIgnoreCase("SUCCESS")) {
            throw new OmpLibraryException(message);
        }

        return message;
    }

    private String getType(int subrack, int slot) {
        String result = getSC();
        if (slot > 2) {
            result = getPL();
        }
        return result;
    }

    private String getSeparator() {
        return "-";
    }

    private String getPL() {
        return "PL";
    }

    private String getSC() {
        return "SC";
    }

    private String cmwStatusWithDetail(String command) throws OmpLibraryException {
        String remotePath = "/home/";
        String tmpFile = "cmw-status.tmp";
        cmwStatus(" -v " + command + " > " + remotePath + tmpFile);
        String localfile = transfferBackFile(remotePath, tmpFile);
        return localFileOperate("cat " + localfile);
    }

    private String cmwStatus(String command) throws OmpLibraryException {
        int timeout = Integer.parseInt(ssh.getTimeout(0, 0));
        ssh.setTimeout(3000);
        String output = ssh.sendCommand("cmw-status " + command);
        ssh.setTimeout(timeout);
        return output;
    }

    private Map<String, String> getScInfo() throws OmpLibraryException {
        return getScInfo(".*");
    }

    /**
     * General method to get the HA state for SC-2N SG
     * 
     * @return a hashmap with the SC:s as keys and their HA state as values
     */
    // private Map<String, String> getScInfo(String app) throws OmpLibraryException {
    //
    // Map<String, String> siStates = new HashMap<String, String>();
    // String node = "";
    // String state = "";
    // String si = "";
    //
    // for (String line : cmwStatusWithDetail("siass").split("\n")) {
    // Pattern p1 = Pattern.compile("safSISU=safSu=(\\S*)\\\\.*safSg.*safSi=(\\S*),safApp=" + app);
    // Matcher m = p1.matcher(line);
    // if (m.matches()) {
    // node = m.group(1);
    // si = m.group(2);
    // }
    // Pattern p2 = Pattern.compile(".*HAState=(\\S*)\\(.*");
    // Matcher m2 = p2.matcher(line);
    // if (m2.matches()) {
    // state = m2.group(1);
    // }
    // if (si.equals("SC-2N")) {
    // System.out.println(line);
    // System.out.println("GGGGGGGGGGGGGGGGGGGGGGGGGGG node = " + node + " si = " + si);
    // System.out.println("GGGGGGGGGGGGGGGGGGGGGGGGGGG state = " + state);
    // System.out.println("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX node = " + node + " si = " + si + " state = "
    // + state + "\n");
    // siStates.put(node, state);
    // }
    // Pattern p3 = Pattern.compile(".*HAReadinessState=(\\S*)\\(.*");
    // Matcher m3 = p3.matcher(line);
    // if (m3.matches()) {
    // // we don't save ReadiState at this point
    // }
    // }
    //
    // return siStates;
    // }

    private Map<String, String> getScInfo(String app) throws OmpLibraryException {
        Map<String, String> siStates = new HashMap<String, String>();
        String node = "";
        String state = "";
        String si = "";

        for (String line : cmwStatusWithDetail("siass").split("\n")) {
            Pattern p1 = Pattern.compile("safSISU=safSu=(\\S*)\\\\.*safSg.*safSi=(\\S*),safApp=" + app);
            Matcher m = p1.matcher(line);
            if (m.matches()) {
                node = m.group(1);
                si = m.group(2);
                if (!si.equals("SC-2N")) {
                    si = "";
                    si = "";
                    state = "";
                    node = "";
                }
            }
            Pattern p2 = Pattern.compile(".*HAState=(\\S*)\\(.*");
            Matcher m2 = p2.matcher(line);
            if (m2.matches()) {
                state = m2.group(1);
                // }
                // if (si.equals("SC-2N")) {
                // System.out.println(line);
                // System.out.println("GGGGGGGGGGGGGGGGGGGGGGGGGGG node = " + node + " si = " + si);
                // System.out.println("GGGGGGGGGGGGGGGGGGGGGGGGGGG state = " + state);
                // System.out.println("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX node = " + node + " si = " + si + " state = "
                // + state + "\n");
                siStates.put(node, state);
                si = "";
                state = "";
                node = "";
            }
            Pattern p3 = Pattern.compile(".*HAReadinessState=(\\S*)\\(.*");
            Matcher m3 = p3.matcher(line);
            if (m3.matches()) {
                // we don't save ReadiState at this point
            }
        }

        return siStates;
    }

    public boolean isCampaignExecutionComplete(String campaignId) throws OmpLibraryException {
        String status = "";
        try {
            status = checkCampaignStatus(campaignId);
        } catch (OmpLibraryException e) {
            return false;
        }
        if (status.contains("COMPLETED")) {
            return true;
        } else if (status.contains("FAILED")) {
            logger.warn("Campaign execution failed! " + campaignId);
            throw new OmpLibraryException("Campaign " + campaignId + " failed!");
        } else {
            return false;
        }
    }

    private boolean waitForCampaignCompleted(String campaignId, int timeout) throws OmpLibraryException {
        return Tools.waitUntilTrue(this, "isCampaignExecutionComplete", new Object[] { campaignId }, 15, timeout, true);
    }

    private Map<String, Map<String, String>> getAppRedundancyImmData(String[] safApps) throws OmpLibraryException {
        logger.debug("Enter getAppRedundancyImmData()");
        String node = "";
        String comp = "";
        String redModel = "";
        String app = "";
        Map<String, String> compMap = new HashMap<String, String>();
        Map<String, Map<String, String>> nodeMap = new HashMap<String, Map<String, String>>();

        // Export IMM config to file if needed and get the file name of the file
        // to fetch.
        String[] localImmFileToFetch = exportImmConfig("/home/", "immdata.xml");
        // SCP the IMM file to local directory
        String localImmFile = transfferBackFile(localImmFileToFetch[0], localImmFileToFetch[1]);
        for (String safApp : safApps) {
            String command = "cat " + localImmFile + " | grep \'\\<dn>safComp='";
            String immList = localFileOperate(command);
            for (String line : immList.split("\n")) {
                Pattern p = Pattern.compile(".*safComp=(\\S*),safSu=(\\S*),safSg=(\\S*),safApp=(\\S*)<.*");
                Matcher m = p.matcher(line);
                if (m.matches()) {
                    comp = m.group(1);
                    node = m.group(2);
                    redModel = m.group(3);
                    app = m.group(4);
                    // get the correct redundancy model (SI)
                    if (app.equalsIgnoreCase(safApp)) {
                        if (nodeMap.get(node) == null) {
                            compMap = new HashMap<String, String>();
                        } else {
                            compMap = nodeMap.get(node);
                        }
                        compMap.put(comp, redModel);
                        nodeMap.put(node, compMap);
                    }
                } else {
                    throw new OmpLibraryException("Unrecognized string output, could not parse IMM data");
                }
            }
            // get all unique components that exist for the current application
            Map<String, String> redundancy = new HashMap<String, String>();
            HashSet<String> unique = new HashSet<String>();
            Iterator<String> it = nodeMap.keySet().iterator();
            while (it.hasNext()) {
                Set<String> components = nodeMap.get(it.next()).keySet();
                Iterator<String> compIt = components.iterator();
                while (compIt.hasNext()) {
                    unique.add(compIt.next());
                }
            }
            // get all the unique components and put them in the component-model
            // hashmap
            it = unique.iterator();
            while (it.hasNext()) {
                redundancy.put(it.next(), "");
            }

            // get the SI redundancy model for each component
            // we do these hashmap operations to reduce the number of ssh
            // commands needed.
            Iterator<String> i = unique.iterator();
            while (i.hasNext()) {
                comp = i.next();
                String imm = localFileOperate("cat " + localImmFile + "  | grep \'\\<dn>safCsi=" + comp + "\'");
                String tmp = imm.split("\n")[0];
                Pattern p2 = Pattern.compile(".*safCsi=(\\S*),safSi=(\\S*),safApp=(\\S*)<.*");
                Matcher m2 = p2.matcher(tmp);
                if (m2.matches()) {
                    redModel = m2.group(2);
                    // fix the redundancy models for AAService and
                    // OSAlarmBridge, these are
                    // not represented in the IMM in the same way as OpenSAF
                    // components.
                    if (redModel.equals("OSAlarmBridge")) {
                        redModel = "NoRed";
                    } else if (redModel.equals("AaService")) {
                        redModel = "2N";
                    }
                    redundancy.put(comp, redModel);
                } else {
                    throw new OmpLibraryException("Can't find the correct redundancy model, could not parse IMM data.");
                }
            }

            // go through the original nodeMap, for each component, add the
            // redundancy model
            it = nodeMap.keySet().iterator();
            while (it.hasNext()) {
                node = it.next();
                compMap = nodeMap.get(node);
                Iterator<String> redIt = redundancy.keySet().iterator();
                while (redIt.hasNext()) {
                    comp = redIt.next();
                    if (compMap.containsKey(comp)) {
                        compMap.put(comp, redundancy.get(comp));
                    }
                }
                nodeMap.put(node, compMap);
            }
        }
        logger.info("Returning Map with IMM Data: " + nodeMap);
        return nodeMap;
    }

    private String transfferBackFile(String remotePath, String targetFile) throws OmpLibraryException {
        String localPath = TestInfo.getLogDir() + "/";
        String tmpTar = targetFile + ".tgz";
        (new File(localPath + targetFile)).delete();
        (new File(localPath + tmpTar)).delete();
        ssh.sendCommand("pushd " + remotePath + "; rm -f " + tmpTar + "; tar czf " + tmpTar + " " + targetFile
                + "; popd");
        ssh.remoteCopyFrom(remotePath + tmpTar, localPath, 120);
        try {
            Tools.runCommandLocal("tar xzf " + tmpTar, localPath);
        } catch (Exception e) {
            e.printStackTrace();
            throw new OmpLibraryException(e.getMessage());
        }
        (new File(localPath + tmpTar)).deleteOnExit();
        (new File(localPath + targetFile)).deleteOnExit();
        return localPath + targetFile;
    }

    private String localFileOperate(String command) throws OmpLibraryException {
        try {
            return Tools.runCommandLocal(command).output;
        } catch (IOException e) {
            throw new OmpLibraryException(e.getMessage());
        } catch (InterruptedException e) {
            throw new OmpLibraryException(e.getMessage());
        }
    }

    private List<String> findComponent(String component, Map<String, Map<String, String>> map) {
        List<String> tmp = new Vector<String>();
        Iterator<String> it = map.keySet().iterator();
        while (it.hasNext()) {
            String node = it.next();
            if (map.get(node).containsKey(component)) {
                tmp.add(node);
            }
        }

        return tmp;
    }

    /**
     * It the version of CoreMW is R2B01 or higher, the IMM config data must be exported to ensure that we get the valid
     * IMM data. If an older version is used, imm_basic.xml will be returned as the valid file to fetch.
     * 
     * @param localOuputFilePath
     *            The path of the output file used to export IMM configuration data if needed.
     * @param localOutputFileName
     *            The name of the output file.
     * @return an array with two elements. The file path of the file containing the IMM data is found in position 0 and
     *         the file name of the same file is found in position 1.
     * @throws OmpLibraryException
     */
    private String[] exportImmConfig(String localOuputFilePath, String localOutputFileName) throws OmpLibraryException {
        if (ssh.sendCommand("which cmw-immconfig-export").contains("Command not found")) {
            return new String[] { "/home/coremw/etc/", "imm_basic.xml" };
        } else {
            ssh.sendCommand("cmw-immconfig-export " + localOuputFilePath + localOutputFileName);
            return new String[] { localOuputFilePath, localOutputFileName };
        }
    }

    /*
     * (non-Javadoc)
     * 
     * @see se.ericsson.jcat.omp.library.SafLib#isCmwStatusOk()
     */
    public boolean isCmwStatusOk() throws OmpLibraryException {
        String status = cmwStatus("app csiass comp node sg si siass su");
        if (status.contains("Status OK")) {
            return true;
        } else {
            logger.warn("Status is not OK.");
            logger.warn(status);
            return false;
        }
    }

    // ===============================================old methods removed since
    // they not apply to CMW
    @Deprecated
    public Hashtable<String, String> getHaState(String csiName) throws OmpLibraryException {
        return new Hashtable<String, String>();
    }

    // Replaced by new methods getNodesInServiceState,
    // getWantedNodesInServiceState
    @Deprecated
    public boolean checkNodesAmfState(final String[] nodes, final String state) throws OmpLibraryException {
        logger.debug("Enter checkNodesAmfState()");
        String node = "";
        String readistate = "";
        boolean isState = true;
        HashMap<String, String> nodeAmfReadiStates = new HashMap<String, String>();

        for (String line : cmwStatus("-v comp").split("\n")) {
            Pattern p1 = Pattern.compile("safComp=CPND,.*safSu=(\\S*),safSg.*safApp.*");
            Matcher m = p1.matcher(line);
            if (m.matches()) {
                node = m.group(1);
            }
            Pattern p2 = Pattern.compile(".*ReadinessState=(\\S*)\\(.*");
            Matcher m2 = p2.matcher(line);
            if (m2.matches()) {
                readistate = m2.group(1);
                nodeAmfReadiStates.put(node, readistate);
            }
        }
        logger.info("MAP:::" + nodeAmfReadiStates);

        // if CPND does not have the wanted state
        // (which should be IN-SERVICE or OUT-OF-SERVICE),
        // break and return false.
        for (String currentnode : nodes) {
            logger.info("Get " + state + " for node" + currentnode + ".");
            if (!nodeAmfReadiStates.keySet().contains(currentnode)) {
                throw new OmpLibraryException("Amf node " + currentnode + " does not exist on this system");
            }
            if (!nodeAmfReadiStates.get(currentnode).equalsIgnoreCase(state)) {
                logger.warn("Component CPND, node " + currentnode + ", expected " + state + ", got "
                        + nodeAmfReadiStates.get(currentnode));
                return false;
            }

        }
        return isState;
    }
}
