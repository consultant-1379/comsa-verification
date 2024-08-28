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

import java.util.Hashtable;
import java.util.List;
import java.util.Map;

import se.ericsson.jcat.omp.fw.OmpLibraryException;

/**
 * The purpose of this class is to define the Java API methods for Python library ssh_lib.
 */
public interface SafLib {

    /**
     * Get the amf node name for subrack/slot
     */
    String getAmfNodeName(int subrack, int slot);

    /**
     * Get the subrack number from an amf node name
     */
    int getSubrack(String amfNodeName);

    /**
     * Get the slot number from an amf node name
     */
    int getSlot(String amfNodeName);

    /**
     * Is the blade at subrack and slot a PL
     * 
     * @return true if the blade is a PL otherwise false
     */
    boolean isPL(int subrack, int slot);

    /**
     * Is the blade at subrack and slot a SC
     * 
     * @return true if the blade is a SC otherwise false
     */
    boolean isSC(int subrack, int slot);

    /**
     * Get the current amf nodes administrative state
     * 
     * @return a Map with the node names as keys and their state as value
     */
    Map<String, String> getAmfNodeAdminState() throws OmpLibraryException;

    /**
     * Get the current amf node name operating state
     * 
     * @return a Map with the node names as keys and their state as value
     */
    Map<String, String> getAmfNodeOperState() throws OmpLibraryException;

    /**
     * Get the hard coded amf nodes administrative state
     * 
     * @return a Map with the node names as keys and their state as value
     */
    Map<String, String> getWantedAmfNodeAdminState();

    /**
     * Get the hard coded amf nodes operating state
     * 
     * @return a Map with the node names as keys and their state as value
     */
    Map<String, String> getWantedAmfNodeOperState();

    /**
     * Is the actual state the same as the parameter
     * 
     * @return true if the states are the same false otherwise
     */
    boolean isAmfNodeAdminState(Map<String, String> wantedState) throws OmpLibraryException;

    /**
     * Is the actual state the same as the parameter
     * 
     * @return true if the states are the same false otherwise
     */
    boolean isAmfNodeOperState(Map<String, String> wantedState) throws OmpLibraryException;

    /**
     * Update the supplied state with the new value for the subrack and slot
     * 
     * @return A new updated state map with amf nodes as keys and states as values
     */
    Map<String, String> updateAmfNodeAdminState(int subrack, int slot, String state, Map<String, String> amfNodeState)
            throws OmpLibraryException;

    /**
     * 
     * Get the HaState for all nodes and CSIs in the cluster.
     * 
     * @return A nested Map with all nodes as keys and as value a Map using si as keys and haState as its value
     * @throws OmpLibraryException
     */
    Map<String, Map<String, String>> getHAState() throws OmpLibraryException;

    /**
     * Get the HA state for all nodes and CSIs in the cluster in raw format. In some cases the getHAState() method does
     * not give sufficient information, such as the SAF application name. This method makes it possible to retrieve such
     * information since nothing is filtered out.
     * 
     * @return
     * @throws OmpLibraryException
     */
    String getCompleteHAStateInRawFormat() throws OmpLibraryException;

    /**
     * Same as getHAState() method but returns the HA state for a specific SAF application.
     * 
     * @param safAppName
     * @return
     * @throws OmpLibraryException
     */
    Map<String, Map<String, String>> getSafAppHAState(String safAppName) throws OmpLibraryException;

    /**
     * Same as getSafAppHAState(String safAppName) but uses a cache of the HA state. This is a helper method that makes
     * it possible to extract all information specific for a certain SAF application.
     * 
     * @param safAppName
     * @param completeHAStateInRawFormat
     *            a string containing the complete HA state. See the getHAStateInRawFormat() method.
     * @return
     * @throws OmpLibraryException
     */
    Map<String, Map<String, String>> getSafAppHAState(String safAppName, String completeHAStateInRawFormat)
            throws OmpLibraryException;

    /**
     * 
     * Get the HaState for all CSIs on a given node.
     * 
     * @param subrack
     *            , slot
     * @return A nested Map with the given node as key and as value, a Map using si as keys and its haState as
     *         corresponding value
     * @throws OmpLibraryException
     */
    Map<String, Map<String, String>> getHAState(int subrack, int slot) throws OmpLibraryException;

    /**
     * Get the HAState for a specific CSI on all nodes where it exists
     * 
     * @param siName
     *            the CSI
     * @return A Map with the node(s) on which the CSI exist as key and the the HA state as value
     * @throws OmpLibraryException
     */
    Map<String, String> getHAState(String siName) throws OmpLibraryException;

    /**
     * 
     * Get the HaState for a component, given a list of its SI:s as a parameter.
     * 
     * @param a
     *            list of SI:s related to the component
     * @return A nested Map with all nodes as keys and as value a Map using csi as keys and haState as its value
     * @throws OmpLibraryException
     */
    Map<String, Map<String, String>> getComponentHAState(String[] csiList) throws OmpLibraryException;

    /**
     * 
     * Get the HaState for the CoreMW component, given a list of its SI:s as a parameter.
     * 
     * @param a
     *            list of SI:s related to CoreMW
     * @return A nested Map with all nodes as keys and as value a Map using csi as keys and haState as its value
     * @throws OmpLibraryException
     */
    Map<String, Map<String, String>> getCMWHAState() throws OmpLibraryException;

    /**
     * Run "cmw-status node su comp" command and check if everything is OK.
     * 
     * @return true if nothing if wrong.
     * @throws OmpLibraryException
     */
    boolean isCmwStatusOk() throws OmpLibraryException;

    /**
     * Compares the Map with expected with actual component states.
     * 
     * @param exactMatch
     *            , if this is true, SC-1 is expected to have its 2N-components in ACTIVE state whereas SC-2 is expected
     *            to have the 2N-components in STANDBY state. If exactMatch is false, it does not matter which SC
     *            component is considered active, as long as they are different.
     * @param wantedState
     *            , a nested Map describing the expected state of the system {node, {component, state}}
     * @return true if expected and actual states match, false if not.
     * @throws OmpLibraryException
     */
    boolean isHAState(boolean exactMatch, Map<String, Map<String, String>> actualState,
            Map<String, Map<String, String>> wantedState, Map<String, Map<String, String>> redundancyMap)
            throws OmpLibraryException;

    /**
     * Get each component on the cluster and its associated redundancy model.
     * 
     * @return a Map with component as key and its redundancy model as value
     */
    Map<String, String> getCompRedundancyModel() throws OmpLibraryException;

    /**
     * Get each component on the cluster associated with a specific redundancy model
     * 
     * @param model
     *            , The wanted redundancy model
     * @return a Map with component as key and its redundancy model as value
     */
    Map<String, String> getCompRedundancyModel(String model) throws OmpLibraryException;

    /**
     * Creates a nested Map with the expected states for a 'normal' setup of the CMW
     * 
     * @return a nested Map describing the expected state of the system {node, {CMWcomponent, state}}
     */
    Map<String, Map<String, String>> getCMWWantedHAState() throws OmpLibraryException;

    /**
     * Get the expected state for a specific application. The application information is used to search the
     * imm_basic.xml file to get the components associated with that specific application.
     * 
     * @param application
     *            The application that is searched for in the IMM file, represented by a String array in case several
     *            components are associated to the same application.
     * @param standby2N
     *            A Map describing which node is standby for a specific set of components, using 2N redundancy model
     * @param standbyNway
     *            A Map describing which node is standby for a specific set of components, using Nway Active redundancy
     *            model
     * @return a nested Map describing the expected state of the system {node, {CMWcomponent, state}}
     */
    Map<String, Map<String, String>> getWantedHAState(String[] application, Map<String, List<String>> standby2N,
            Map<String, List<String>> standbyNway) throws OmpLibraryException;

    /**
     * get the Redundancy model Map for Core MW
     * 
     * @return a nested Map describing the redundancy model for all CMW components {node,{component, redundancy model}}
     * @throws OmpLibraryException
     */
    Map<String, Map<String, String>> getCMWRedundancyModel() throws OmpLibraryException;

    /**
     * Update state Map, by changing the state on a node's 2N redundancy components
     * 
     * @param subrack
     * @param slot
     * @param state
     *            the new state, applied on all 2N components matching the node (subrack, slot)
     * @param redundancyModel
     *            the complete hash map for the product, e.g Testapp or CMW
     * @param wantedState
     *            the state map that needs an update
     * @return a new Map describing the updated state
     * @throws OmpLibraryException
     */
    Map<String, Map<String, String>> updateWantedHAState(int subrack, int slot, String state,
            Map<String, Map<String, String>> redundancyModel, Map<String, Map<String, String>> wantedState)
            throws OmpLibraryException;

    /**
     * Update a state Map by removing a node (matching subrack/slot)
     * 
     * @param subrack
     * @param slot
     * @param wantedState
     *            the state to be updated
     * @return a new state Map with the node matching (subrack/slot) removed.
     * @throws OmpLibraryException
     */
    Map<String, Map<String, String>> removeNodeFromWantedHAState(int subrack, int slot,
            Map<String, Map<String, String>> wantedState) throws OmpLibraryException;

    /**
     * Waits until the actual HA state of the system is the same as the wanted state.
     * 
     * @param wantedState
     * @param timeout
     *            , seconds it will wait before the method times out
     * @return true if states are stable before timeout.
     */
    boolean waitForCmwHAState(Map<String, Map<String, String>> wantedState, int timeout);

    /**
     * @param wantedState
     * @return
     * @throws OmpLibraryException
     */
    boolean isCmwHAState(Map<String, Map<String, String>> wantedState) throws OmpLibraryException;

    /**
     * Get the actual readiness state for the cluster
     * 
     * @return a Map with node as key and state ("IN-SERVICE" or "OUT-OF-SERVICE") as value
     * @throws OmpLibraryException
     */
    Map<String, String> getNodesInServiceState() throws OmpLibraryException;

    /**
     * Creates an expected readiness state for the cluster
     * 
     * @return a Map with node as key, and IN-SERVICE state as value (for all nodes)
     * @throws OmpLibraryException
     */
    Map<String, String> getWantedNodesInServiceState() throws OmpLibraryException;

    /**
     * Update the nodeStates Map with a new state for node matching node(subrack/slot)
     * 
     * @param subrack
     * @param slot
     * @param state
     *            new state for node, 'IN-SERVICE' or 'OUT-OF-SERVICE'
     * @param nodeStates
     *            state to be updated
     * @return a new Map with updated state for node (subrack/slot)
     * @throws OmpLibraryException
     */
    Map<String, String> updateNodesInServiceState(int subrack, int slot, String state, Map<String, String> nodeStates)
            throws OmpLibraryException;

    /**
     * Compare actual readiness state on the node with an expected state
     * 
     * @param wantedState
     *            the expected readiness state
     * @return true if equal, else false.
     * @throws OmpLibraryException
     */
    boolean isNodesInServiceState(Map<String, String> wantedState) throws OmpLibraryException;

    /**
     * Wait for expected and actual readiness state to match
     * 
     * @param wantedState
     *            the expected readiness state
     * @param maxTime
     *            seconds to wait before timeout
     * @return true if states match before maxTime, else false.
     * @throws OmpLibraryException
     */
    boolean waitForNodesInService(Map<String, String> wantedState, int maxTime) throws OmpLibraryException;

    /**
     * Waits until Administrative state is as expected
     * 
     * @param wantedState
     *            , the Administrative state to wait for
     * @param timeout
     * @return true if administrative states are stable before timeout.
     */
    boolean waitForAdministrativeState(Map<String, String> wantedState, int timeout);

    /**
     * Waits until Operational state is as expected
     * 
     * @param wantedState
     *            , the operational state to wait for
     * @param timeout
     * @return true if operational states are stable before timeout.
     */
    boolean waitForOperationalState(Map<String, String> wantedState, int timeout);

    /**
     * Get all nodes on the system
     * 
     * @return a Set of Strings including all amf node names
     * @throws OmpLibraryException
     */
    String[] getClusterNodes() throws OmpLibraryException;

    /**
     * Get all PL nodes on the system
     * 
     * @return a Set of Strings including all PL Amf node names
     * @throws OmpLibraryException
     */
    String[] getClusterNodesPL() throws OmpLibraryException;

    /**
     * Get all SC nodes on the system
     * 
     * @return a Set of Strings including all SC Amf node names
     * @throws OmpLibraryException
     */
    String[] getClusterNodesSC() throws OmpLibraryException;

    /**
     * Get the redundancy status of a specific SC node
     * 
     * @param subrack
     * @param slot
     * @return a String containing SC status
     * @throws OmpLibraryException
     */
    String getScStatus(int subrack, int slot) throws OmpLibraryException;

    /**
     * Get the Active System Controller
     * 
     * @return a String containing the ative SC
     * @throws OmpLibraryException
     */
    String getActiveSc() throws OmpLibraryException;

    /**
     * Get the Active System Controller
     * 
     * @param application
     * @return a String containing the ative SC
     * @throws OmpLibraryException
     */
    String getActiveSc(String app) throws OmpLibraryException;

    /**
     * Get the Standby System Controller
     * 
     * @return a String containing the Standby SC
     * @throws OmpLibraryException
     */
    String getStandbySc() throws OmpLibraryException;

    /**
     * Get the Standby System Controller
     * 
     * @param application
     * @return a String containing the Standby SC
     * @throws OmpLibraryException
     */
    String getStandbySc(String app) throws OmpLibraryException;

    /**
     * Get the components from imm_basic.xml for a specific application
     * 
     * @param application
     *            as named for safApp in IMM, represented as a String array for the case when an application is
     *            represented by several safApp/components.
     * @return a list of the components (safComp) used for that application
     */
    String[] getComponents(String[] application) throws OmpLibraryException;

    /**
     * Install an application, using CMW campaigns
     * 
     * @param runtime
     *            , the runtime.tar containing the SDP:s to be installed
     * @param app
     *            , the application to be installed
     * @return true if successful, false if not
     * @throws OmpLibraryException
     */
    boolean installApplication(String campaignSdp, int timeout) throws OmpLibraryException;

    boolean upgradeApplication(String campaignSdp, int timeout) throws OmpLibraryException;

    boolean removeApplication(String campaignSdp, int timeout) throws OmpLibraryException;

    // TODO: Remove this line!
    // ================================new py-wrappers
    /**
     * Install CMW on the cluster
     * 
     * @return true if the installation was successful otherwise false * @throws OmpLibraryException
     */
    String install(String fileName) throws OmpLibraryException;

    String rebootCluster() throws OmpLibraryException;

    String rebootNode(int subrack, int slot) throws OmpLibraryException;

    boolean backupCreate(String backupName) throws OmpLibraryException;

    boolean backupRestore(String backupName, int timeout) throws OmpLibraryException;

    boolean backupRestore(String backupName) throws OmpLibraryException;

    String backupList() throws OmpLibraryException;

    String backupRemove(String backupName) throws OmpLibraryException;

    String getInstalledSwOnRepository() throws OmpLibraryException;

    String getInstalledSwOnNode(String nodeType, int subrack, int slot) throws OmpLibraryException;

    Map<String, List<String>> getInstalledSwOnAllNodes() throws OmpLibraryException;

    String copySwPackageToSystem(String[] filePaths) throws OmpLibraryException;

    String importSwBundle(String swBundleFileName) throws OmpLibraryException;

    String importSwBundleFromLocal(String swBundleLocalPath) throws OmpLibraryException;

    String checkCampaignStatus(String campaignId) throws OmpLibraryException;

    String removeSwBundle(String swBundlePackageId) throws OmpLibraryException;

    String removeAllSwFromCluster() throws OmpLibraryException;

    String upgradeCommit(String campaignName) throws OmpLibraryException;

    String upgradeStart(String campaignName) throws OmpLibraryException;

    String upgradeStatusCheck(String campaignName) throws OmpLibraryException;

    boolean immSave() throws OmpLibraryException;

    // ==========METHODS FROM OLD TSPSAF=============DEPRECATED============================

    @Deprecated
    Hashtable<String, String> getHaState(String csiName) throws OmpLibraryException;

    @Deprecated
    /**
     * Get the readiness state for all components on a specific set of nodes
     * @param nodes an array of Amf node names
     * @param state expected state, IN-SERVICE or OUT-OF-SERVICE
     * @return true if all components for the nodes are in the expected state
     * @throws OmpLibraryException
     */
    boolean checkNodesAmfState(String[] nodes, String state) throws OmpLibraryException;
    // ==============================================================================

}
