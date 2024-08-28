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

import org.apache.log4j.Logger;

import se.ericsson.jcat.fw.utils.Ssh2Session;
import se.ericsson.jcat.omp.fw.OmpExtendedFetchLogs;

public class SafLogFetcher extends OmpExtendedFetchLogs {
	private static Logger logger = Logger.getLogger(SafLogFetcher.class);
	
    public SafLogFetcher(final String ip1, final String ip2, final String username,
            final String password) {
        super("cmw-collect-info /home/collect_info_cmw.tgz", "SAF_Logs", ip1, ip2, username, password);
    }

    /**
     * @see se.ericsson.jcat.omp.fw.OmpExtendedFetchLogs#getFilePath(java.lang.String)
     */
    @Override
    public String[] getFilePath(final String info) {
        return new String[] {"/home/", "collect_info_cmw.tgz"};
    }
    
protected boolean isInstalledOnSystem()	{
	logger.info("Checking if SAF is installed before running fetchlogs");
		boolean isInstalled = false;
		Ssh2Session ssh;
		try {
			ssh = getSshSession();
			ssh.openSshShell();
			ssh.setRawOutput(false);
			ssh.setTimeout(30000);
			String result = ssh.sendCommand("which cmw-collect-info;echo $?");
			ssh.closeSshShell();
			if (result.endsWith("0")) {
				isInstalled = true;
			}
		} catch (Exception e) {
			logger.error(e.toString(), e);
			isInstalled = false;
		}
		return isInstalled;
	}
}
