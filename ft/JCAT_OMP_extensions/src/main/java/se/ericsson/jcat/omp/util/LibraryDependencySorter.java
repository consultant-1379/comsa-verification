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
import java.util.Enumeration;
import java.util.Hashtable;
import java.util.Iterator;
import java.util.List;

import se.ericsson.jcat.omp.fw.OmpLibrary;

/**
 * A Utility class for sorting the order in which setup should be called on
 * libraries. More complex than perhaps one would have liked, but there do not
 * seem to be good utilities in Java Collections to do this kind of thing (the
 * general Comparator etc dont work since our "list" is not a well behaved list
 * according to the definitions in Java Collections).
 */
public class LibraryDependencySorter {

    public LibraryDependencySorter() {
    }

    /**
     * Private class used to store relations between one library and another
     * during the ordering process.
     */
    class OmpLibraryDependencyInfo {
        List<OmpLibraryDependencyInfo> forwards;

        List<OmpLibraryDependencyInfo> backwards;

        OmpLibrary library;

        public OmpLibraryDependencyInfo(final OmpLibrary library) {
            this.library = library;
            forwards = new ArrayList<OmpLibraryDependencyInfo>();
            backwards = new ArrayList<OmpLibraryDependencyInfo>();
        }
    }

    /**
     * The only method in this utility class that is used externally. Providing
     * a list of OmpLibrary this method will return them ordered according to
     * dependency (ascending), and will throw RuntimeException in case either a
     * dependency is declared to an unknown library, or if there are circular
     * dependencies amongst the libraries.
     * 
     * @param arr The array of OmpLibrary to sort
     * @return The sorted array
     */
    public OmpLibrary[] sort(final OmpLibrary[] arr) {
        final Hashtable<String, OmpLibraryDependencyInfo> libraries =
                new Hashtable<String, OmpLibraryDependencyInfo>();

        // First populate our hashtable of OmpLibraryDependencyInfos
        for(int i = 0; i < arr.length; i++) {
            libraries.put(arr[i].getName(),
                    new OmpLibraryDependencyInfo(arr[i]));
        }

        // Now we go through them one at a time, connecting up the dependencies,
        // in both directions
        final Enumeration<OmpLibraryDependencyInfo> en = libraries.elements();
        while(en.hasMoreElements()) {
            final OmpLibraryDependencyInfo next = en.nextElement();
            final String[] deps = next.library.getSetupDependencies();
            for(int i = 0; i < deps.length; i++) {
                final OmpLibraryDependencyInfo info = libraries.get(deps[i]);
                if(info == null) {
                    throw new RuntimeException("LibraryBroker : Library "
                            + next.library.getName()
                            + " has dependency to unknown library " + deps[i]);
                }
                next.forwards.add(info);
                info.backwards.add(next);
            }

        }

        // Now we have to traverse the relationships to check that none are
        // circular

        final Enumeration<OmpLibraryDependencyInfo> elements =
                libraries.elements();
        while(elements.hasMoreElements()) {
            final OmpLibraryDependencyInfo thisOne = elements.nextElement();
            if(checkForRecursion(thisOne, thisOne)) {
                throw new RuntimeException(
                        "There are circular dependencies involving library "
                                + thisOne.library.getName());
            }

        }

        // And now we have to extract the relationships in backwards order, i.e.
        // removing any
        // that do not have any dependencies to other libraries, and then when
        // we remove them
        // we also remove the dependencies from libraries which have a
        // dependency to the one
        // being removed.
        final ArrayList<OmpLibrary> answer = new ArrayList<OmpLibrary>();
        while(libraries.size() > 0) {
            final Enumeration<OmpLibraryDependencyInfo> e =
                    libraries.elements();
            while(e.hasMoreElements()) {
                final OmpLibraryDependencyInfo thisOne = e.nextElement();
                if(thisOne.forwards.size() == 0) {
                    libraries.remove(thisOne.library.getName());
                    answer.add(thisOne.library);
                    final Iterator<OmpLibraryDependencyInfo> iter =
                            thisOne.backwards.iterator();
                    while(iter.hasNext()) {
                        iter.next().forwards.remove(thisOne);
                    }
                }
            }

        }

        return answer.toArray(arr);

    }

    private boolean checkForRecursion(final OmpLibraryDependencyInfo thisOne,
            final OmpLibraryDependencyInfo toCheckFor) {
        final Iterator<OmpLibraryDependencyInfo> iter =
                thisOne.forwards.iterator();
        while(iter.hasNext()) {
            final OmpLibraryDependencyInfo next = iter.next();
            if(next == toCheckFor) return true;
            if(checkForRecursion(next, toCheckFor)) return true;
        }
        return false;

    }
}
