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

import org.python.core.PyDictionary;
import org.w3c.dom.Document;

/**
 * The purpose of this class is to define the Java API methods for Python module
 * target_data.
 */
public interface TargetDataLib {
    
    /**
     * Returns the active Python dictionary from the target_data module.
     * 
     * @return
     */
    public PyDictionary getTargetData();
    
    /**
     * Populate the Python target_data module with data in the specified
     * document tree.
     * 
     * @param document
     * @return
     * @throws IOException
     */
    public PyDictionary setTargetData(Document document) throws IOException;
}
