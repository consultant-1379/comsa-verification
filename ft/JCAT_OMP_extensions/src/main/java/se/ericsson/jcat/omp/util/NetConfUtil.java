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

import java.io.IOException;

import org.apache.log4j.Logger;
import org.apache.xmlbeans.XmlException;
import org.apache.xmlbeans.XmlObject;
import se.ericsson.jcat.omp.fw.OmpSut;
import se.ericsson.jcat.omp.library.SshLibImpl;
import x0.ietfParamsXmlNsNetconfBase1.EditConfigDocument;
import x0.ietfParamsXmlNsNetconfBase1.EditConfigType;
import x0.ietfParamsXmlNsNetconfBase1.FilterInlineType;
import x0.ietfParamsXmlNsNetconfBase1.FilterType;
import x0.ietfParamsXmlNsNetconfBase1.GetDocument;
import x0.ietfParamsXmlNsNetconfBase1.HelloDocument;
import x0.ietfParamsXmlNsNetconfBase1.RpcDocument;
import x0.ietfParamsXmlNsNetconfBase1.RpcReplyDocument;
import x0.ietfParamsXmlNsNetconfBase1.RpcType;
import x0.ietfParamsXmlNsNetconfBase1.RunningDocument;

@Deprecated
public class NetConfUtil {

    private static Logger logger = Logger.getLogger(SshLibImpl.class);
	
    private static final String NETCONF_MESASGE_END = "]]>]]>";
    private static final String XML_START =
            "\n<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n";
    private static int msgCount = 0;

    private static RpcDocument constructRpcDocument(final XmlObject rpcTypeDocument) {
        final RpcDocument rpc = RpcDocument.Factory.newInstance();
        final RpcType rpcType = rpc.addNewRpc();
        rpcType.set(rpcTypeDocument);
        rpcType.setMessageId(String.valueOf(++msgCount));
        return rpc;
    }

    private static EditConfigDocument constructEditConfigDocument(
            final XmlObject meDocument) {
        final EditConfigDocument edit =
                EditConfigDocument.Factory.newInstance();
        final EditConfigType editType = edit.addNewEditConfig();
        final RunningDocument running = RunningDocument.Factory.newInstance();
        running.addNewRunning();
        editType.addNewConfig().set(meDocument);
        editType.addNewTarget().set(running);
        return edit;
    }

    private static GetDocument constructGetDocument(final XmlObject filterDoc) {
        final GetDocument get = GetDocument.Factory.newInstance();
        final FilterInlineType filter = get.addNewGet().addNewFilter();
        filter.set(filterDoc);
        filter.setType(FilterType.SUBTREE);
        return get;
    }
    
    private static HelloDocument constructHelloDocument() {
        final HelloDocument hello = HelloDocument.Factory.newInstance();
        hello.addNewHello().addNewCapabilities().addCapability(
                "urn:ietf:params:netconf:base:1.0");
        return hello;
    }

    private static RpcReplyDocument destructRpcReply(final String reply) {
        final String[] responses = reply.split(NETCONF_MESASGE_END);
        RpcReplyDocument rpcReply = null;
        try {
            rpcReply =
                    RpcReplyDocument.Factory
                            .parse(responses[responses.length - 1]);
        }
        catch(final XmlException e) {
        	logger.error("Cannot parse Rpc-Reply Document!", e);
            logger.error("Exception message: " +e.getMessage());
            logger.error(reply.replaceAll("<", "&lt;").replaceAll(">","&gt;"));
            
            return null;
        }
        return rpcReply;
    } 

    private static boolean verifyRpcReplyOk(final RpcReplyDocument rpcReply) {
        final XmlObject ok = rpcReply.getRpcReply().getOk();
        return ok != null;
    }

    private static String getDataFromRpcReply(final RpcReplyDocument rpcReply) {
        if (rpcReply == null) {
            logger.error("Cannot get data from null! (getDataFromRpcReply())");
            return null;
        }
        return rpcReply.getRpcReply().getData().toString();
    }
    
    private static Ssh2sessionUtil getConnection(OmpSut sut) {

        final String username = sut.getConfigDataString("user");
        final String password = sut.getConfigDataString("pwd");
        final String ip1 = sut.getConfigDataString("ipAddress.ctrl.ctrl1");
        final String ip2 = sut.getConfigDataString("ipAddress.ctrl.ctrl2");
        String ip = null;

        if(Tools.isPortOpen(ip1, 2022)) {
            ip = ip1;
        }
        else if(Tools.isPortOpen(ip2, 2022)) {
            ip = ip2;
        }
        else {
            logger.error("Cannot connect to 2022 port on both SC1 and SC2!");
            return null;
        }

        final Ssh2sessionUtil ssh2SessionUtil =
                new Ssh2sessionUtil("Netconf Ssh2sessionUtil");
        try {
            ssh2SessionUtil.startNetconfSession(ip, 2022, username, password,
                    10 * 1000, 0);
        }
        catch(final IOException e) {
            logger.error("Error!");
            return null;
        }
        return ssh2SessionUtil;
    }

    private static String sendRpcCommand(final RpcDocument rpc, final OmpSut sut) {
        final HelloDocument hello = constructHelloDocument();
        final Ssh2sessionUtil connection = getConnection(sut);
        final String xml =
                XML_START + hello.toString() + NETCONF_MESASGE_END + XML_START
                        + rpc.toString() + NETCONF_MESASGE_END;
        logger.debug("Sending xml to netconf: \n" + xml);
        if (connection == null) {
            logger.error("NetConf is not running on SUT!");
            return null;
        }
        final String out = connection.sendNetconfMsg(xml);
        connection.closeSession();
        return out;
    }
    
    public static boolean sendEditCommand(final XmlObject doc, final OmpSut sut) {
        EditConfigDocument edit = constructEditConfigDocument(doc);
        RpcDocument rpc = constructRpcDocument(edit);
        String out = sendRpcCommand(rpc, sut);
        RpcReplyDocument reply = destructRpcReply(out);
        if(verifyRpcReplyOk(reply)) {
            return true;
        }
        else {
            logger.error("Could complete edit call!\n" + out);
            return false;
        }
    }
    
    public static String sendGetCommand(final XmlObject doc, final OmpSut sut) {
    	 final GetDocument get = constructGetDocument(doc);
         final RpcDocument rpc = constructRpcDocument(get);
         final String out = sendRpcCommand(rpc, sut);
         final RpcReplyDocument reply = destructRpcReply(out);
         return getDataFromRpcReply(reply);
    }
    
}
