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

import java.util.ArrayList;
import java.util.List;

import org.apache.log4j.Logger;
import org.python.core.PyException;
import org.python.core.PyList;
import org.python.core.PyObject;
import org.python.util.PythonInterpreter;

import se.ericsson.commonlibrary.CommonLibrary;
import se.ericsson.commonlibrary.CommonLibraryDataProvider;
import se.ericsson.jcat.fw.jython.Jythonizer;
import se.ericsson.jcat.omp.fw.OmpLibrary;
import se.ericsson.jcat.omp.fw.OmpLibraryException;
import se.ericsson.jcat.omp.fw.OmpSut;

/**
 * Implements the Java API methods for Python library ethswitch_lib.
 */
public class EthSwitchLibImpl extends OmpLibrary implements EthSwitchLib {

    private static Logger logger = Logger.getLogger(EthSwitchLibImpl.class);

    private PythonInterpreter interp = null;
    private List<Class<? extends CommonLibrary>> l;
    private CommonLibraryDataProvider data;
    
    OmpSut sut = null;

	
    
    public EthSwitchLibImpl() {
    	l = new ArrayList<Class<? extends CommonLibrary>>();
	}

    /**
     * Creates a new instance of <code>EthSwitchLib</code>.
     * 
     * @param sut
     * @throws Exception
     */
    public EthSwitchLibImpl(final OmpSut sut) throws Exception {
        this.sut = sut;
        this.interp = Jythonizer.getInstance();
    }

    /**
     * Returns the unique name of this library.
     */
    public String getName() {
        return "EthSwitchLib";
    }

    /**
     * Method called by LibraryBroker to set the Sut of the library.
     */
    public void setSut(final OmpSut sut) {
        this.sut = sut;
    }

    /**
     * Imports the python lib and executes the setup method.
     */
    public void setUp() {
        interp.exec("import omp.tf.ethswitch_lib as ethswitch_lib");
        interp
                .exec("if(hasattr(ethswitch_lib, 'setUp')): ethswitch_lib.setUp()");
    }

    /**
     * Executes teardown method in python lib.
     */
    public void tearDown() {
        interp
                .exec("if(hasattr(ethswitch_lib, 'tearDown')): ethswitch_lib.tearDown()");
    }

    /**
     * Return runtime dependencies.
     */
    public String[] getRuntimeDependencies() {
        return new String[] { "LoggerLib", "TargetDataLib", "SnmpLib" };
    }

    /**
     * Return setup dependencies.
     */
    public String[] getSetupDependencies() {
        return new String[] { "LoggerLib", "TargetDataLib", "SnmpLib" };
    }
    
    public String portDown(final String target, final String port)
    throws OmpLibraryException {
        interp.exec("result = ethswitch_lib.portDown('" + target + "', '"
        + port + "')");
        final PyList result = (PyList) interp.get("result");
        String cmdRes = parseJythonListResult(result);
        logger.info(cmdRes);    
        return result.toString();
     }   

    public String portUp(final String target, final String port)
            throws OmpLibraryException {
        interp.exec("result = ethswitch_lib.portUp('" + target + "', '" + port
                + "')");
        final PyList result = (PyList) interp.get("result");
        String cmdRes = parseJythonListResult(result);
        logger.info(cmdRes);
        return result.toString();
    }

    public String checkAndFixAllPortToDown(final String target)
            throws OmpLibraryException {
        interp.exec("result = ethswitch_lib.checkAndFixAllPortToDown('"
                + target + "')");
        final PyList result = (PyList) interp.get("result");
        String cmdRes = parseJythonListResult(result);
        logger.info(cmdRes);
        return result.toString();
    }

    public String checkAndFixAllPortToUp(final String target)
            throws OmpLibraryException {
        interp.exec("result = ethswitch_lib.checkAndFixAllPortToUp('" + target
                + "')");
        final PyList result = (PyList) interp.get("result");
        String cmdRes = parseJythonListResult(result);
        logger.info(cmdRes);
        return result.toString();
    }

    public String checkAndFixAllListedPortsToUp(final String target, final String[] ports)
            throws OmpLibraryException {
        PyList pyPorts = new PyList();
        for (int i=0; i<ports.length; i++){
            pyPorts.add(ports[i]);
        }        
        interp.exec("result = ethswitch_lib.checkAndFixAllListedPortsToUp('" + target
                + "', " + pyPorts + ")");
        final PyList result = (PyList) interp.get("result");
        return result.toString();
    }
   
    public String checkAndFixAllListedPortsToDown(final String target, final String[] ports)
            throws OmpLibraryException {
        PyList pyPorts = new PyList();
        for (int i=0; i<ports.length; i++){
            pyPorts.add(ports[i]);
        }        
        interp.exec("result = ethswitch_lib.checkAndFixAllListedPortsToDown('" + target
                + "', " + pyPorts + ")");
        final PyList result = (PyList) interp.get("result");
        return result.toString();
        
    }

    public String getListIfUpOperStatus(final String target)
            throws OmpLibraryException {

        interp.exec("result = ethswitch_lib.getListIfUpOperStatus('" + target
                + "')");
        final PyList result = (PyList) interp.get("result");
        return parseJythonListResult(result);
    }
    
	public String getPortState(String switchName, int port )
		throws OmpLibraryException{
		PyObject pyVerdict;
        PyObject pyMessage;
        PyObject pyCommand;
        String portStatus="down";

		interp.exec("result = ethswitch_lib.getListIfUpOperStatus('" + switchName
           + "')");
		final PyList result = (PyList) interp.get("result");
//		String resultString = parseJythonListForaPort(result, port);
        try {
            pyVerdict = result.__getitem__(0);
            logger.debug("Parsing PyList arg0: " + pyVerdict.toString());
            pyMessage = result.__getitem__(1);
            logger.debug("Parsing PyList arg1: " + pyMessage.toString());
            pyCommand = result.__getitem__(2);
            logger.debug("Parsing PyList arg2: " + pyCommand.toString());
        }
        catch(final PyException pe) {
            throw new OmpLibraryException(
        			"Parsing error, PyList key not found. PyException was: " + pe.toString());
        }

        if(!(pyVerdict.toString()).equalsIgnoreCase("SUCCESS")) {
            throw new OmpLibraryException(pyMessage.toString());
        }
        
        String pyMessageString = pyMessage.toString().replace("[", "");
        pyMessageString= pyMessageString.replace("]", "");
        pyMessageString= pyMessageString.replace("'", "");
        String[] ports = pyMessageString.split(",");

        String pyCommandString = pyCommand.toString().replace("[", "");
        pyCommandString = pyCommandString.replace("]", "");
        pyCommandString = pyCommandString.replace("'", "");
        String[] status = pyCommandString.toString().split(",");
        
        if(ports.length != status.length){
        	throw new OmpLibraryException("Status of all ports is not available. Kindly check again.");
        }
        for (int i=0; i<ports.length; i++){
         	if (Integer.parseInt(ports[i].trim()) == port)
        	{
        		portStatus=status[i].trim();
        		logger.info("Port"+ ports[i]+" Status is" + status[i]);
        		break;
        	}
        	
        }
        return portStatus;
    }
	 

    public String getListIfUpAdminStatus(final String target)
            throws OmpLibraryException {
        interp.exec("result = ethswitch_lib.getListIfUpAdminStatus('" + target
                + "')");
        final PyList result = (PyList) interp.get("result");
        return result.toString();
    }

    public String getListIfNotUpOperStatus(final String target)
            throws OmpLibraryException {
        interp.exec("result = ethswitch_lib.getListIfNotUpOperStatus('"
                + target + "')");
        final PyList result = (PyList) interp.get("result");
        return result.toString();
    }

    public String getListIfNotUpAdminStatus(final String target)
            throws OmpLibraryException {
        interp.exec("result = ethswitch_lib.getListIfNotUpAdminStatus('"
                + target + "')");
        final PyList result = (PyList) interp.get("result");
        return result.toString();
    }

    /*
     * Parse the PyTuple result structure returned from the Jython API method.
     * TODO: Throw OmpLibraryException if PyTuple parse fails?
     */
    private String parseJythonListResult(final PyList pl)
            throws OmpLibraryException {
        PyObject pyVerdict;
        PyObject pyMessage;
        PyObject pyCommand;
        try {
            pyVerdict = pl.__getitem__(0);
            logger.debug("Parsing PyList arg0: " + pyVerdict.toString());
            pyMessage = pl.__getitem__(1);
            logger.debug("Parsing PyList arg1: " + pyMessage.toString());
            pyCommand = pl.__getitem__(2);
            logger.debug("Parsing PyList arg2: " + pyCommand.toString());
        }
        catch(final PyException pe) {
            throw new OmpLibraryException(
        			"Parsing error, PyList key not found. PyException was: " + pe.toString());
        }

        // Do we need null checks on these?
        final String verdict = pyVerdict.toString();
        final String message = pyMessage.toString();

        if(!verdict.equalsIgnoreCase("SUCCESS")) {
            throw new OmpLibraryException(message);
        }

        return message;
    }
    
    
     
	@Override
	public void setLibraryDataProvider(CommonLibraryDataProvider data) {
		this.data = data;
	}

	@Override
	public CommonLibraryDataProvider getLibraryDataProvider() {
		return data;
	}

	@Override
	public Class<? extends CommonLibrary> getLibraryInterface() {
		return  EthSwitchLib.class;
	}

	@Override
	public String getUniqueIdentifier() {
		return "RDA ETH Switch lib";
	}

	@Override
	public void initialize() {
		this.setUp();
	}

	@Override
	public void shutdown() {
		this.tearDown();
		
	}

	@Override // OMPLib and CommonLib
	public List<Class<? extends CommonLibrary>> getRuntimeDependencyList() {
		return l;
	}

	@Override
	public List<Class<? extends CommonLibrary>> getSetupDependencyList() {
		return l;
	}
 }
