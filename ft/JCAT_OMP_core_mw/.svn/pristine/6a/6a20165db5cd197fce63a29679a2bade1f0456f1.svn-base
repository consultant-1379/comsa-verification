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

import se.ericsson.jcat.omp.fw.OmpLibraryException;
import org.python.core.PyList;
import org.python.core.PyDictionary;


/**
 * The purpose of this class is to define the Java API methods for Python
 * library opensaf_lib.
 */
public interface OpensafLib {
    public String getControllerState(int subrack, int slot) throws OmpLibraryException;

    public String getPayloadState(int subrack, int slot) throws OmpLibraryException;
    
    public String getServiceInstanceHaState(int subrack, int slot, final PyList serviceInstances) throws OmpLibraryException;
    
    public String getCompOpState(int subrack, int slot, final PyList comp) throws OmpLibraryException;
    
    public String getSuReadinessState(int subrack, int slot, final PyList serviceUnit) throws OmpLibraryException;
    
    public String getCompReadiState(int subrack, int slot, final PyList comp) throws OmpLibraryException;
    
    public String getControllerHAState(int subrack, int slot) throws OmpLibraryException;
    
    public PyDictionary getAllCompState() throws OmpLibraryException;
}
