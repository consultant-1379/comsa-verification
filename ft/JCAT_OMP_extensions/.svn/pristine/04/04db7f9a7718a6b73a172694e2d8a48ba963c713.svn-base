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

import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Enumeration;
import java.util.Hashtable;
import java.util.List;

import se.ericsson.jcat.fw.jython.Jythonizer;
import se.ericsson.jcat.omp.fw.OmpLibrary;
import se.ericsson.jcat.omp.fw.OmpSut;
import se.ericsson.jcat.omp.fw.OmpTestInfo;

/**
 * <strong> IMPORTANT!</strong>
 * This LibraryBroker has being @deprecated, it is still available for 
 * backward compatibility. Please use the new LibraryBroker 
 * {@link se.ericsson.commonlibrary.LibraryBroker} </br>
 *  </br>
 * A broker for all pluggable Omp libraries (implemented in either Java or
 * Python) This class manages the list of libraries, providing access to them
 * (given a unique name), and calls setUp and tearDown on all of them at
 * appropriate times. To configure a library for loading by the library broker,
 * one must set a system property before the LibraryBroker is created. To
 * specify a Java library for loading called
 * se.ericsson.jcat.fw.test.TestJavaLibrary, set the following System Property
 * se.ericsson.jcat.omp.fw.JavaLibrary:se.ericsson.jcat.fw.test.TestJavaLibrary
 * (to anything) - i.e. it is the fact that this system property is set that
 * loads the library, not what it is set to that matters. Similarly for a Python
 * library called test.TestPythonLibrary, set the following System Property
 * se.ericsson.jcat.omp.fw.PythonLibrary:test.TestPythonLibrary (to anything).
 * 
 */
@Deprecated
public class LibraryBroker {

    private final Hashtable<String, OmpLibrary> libraries;

    private final OmpSut sut;

//    private static String LIBRARY_BROKER_JAVA_PREFIX =
//            "se.ericsson.jcat.omp.fw.JavaLibrary:";
//
//    private static String LIBRARY_BROKER_PYTHON_PREFIX =
//            "se.ericsson.jcat.omp.fw.PythonLibrary:";

    /**
     * Constructor for LibraryBroker, which loads the pluggable libraries from a
     * list (taken from system properties in the future), and calls setUp on all
     * of them.
     * 
     * @param sut The System under test which will be passed to all libraries
     *        when they are created
     */
    @Deprecated
    public LibraryBroker(final OmpSut sut) {
        this.sut = sut;
        libraries = new Hashtable<String, OmpLibrary>(10, 10);
        final Object[] libraryConfig = readLibraryConfiguration();
        for(int i = 0; i < libraryConfig.length; i++) {
            final LibraryConfig lf = (LibraryConfig) libraryConfig[i];
            OmpLibrary library = null;
            if(lf.getLanguage() == LibraryConfig.JAVA) {
                library = loadAndInstantiateJava(lf.getClassOrModule());
            }
            else if(lf.getLanguage() == LibraryConfig.PYTHON) {
                library = loadAndInstantiatePython(lf.getClassOrModule());
            }
            if(library != null) libraries.put(library.getName(), library);
        }

        checkRuntimeDependencies();
    }

    /**
     * Dispose for LibraryBroker, which calls tearDown on all the pluggable
     * libraries
     */
    @Deprecated
    public void dispose() {
        final Enumeration<OmpLibrary> libraryEnumeration = libraries.elements();

        while(libraryEnumeration.hasMoreElements()) {
            libraryEnumeration.nextElement().tearDown();
        }
        libraries.clear();

    }

    /**
     * private implementation method for reading the configuration of which
     * libraries to instantiate
     * 
     * @return An array of LibraryConfig containing the data that has been read
     */
    private Object[] readLibraryConfiguration() {
        final List<LibraryConfig> libraryArray = new ArrayList<LibraryConfig>();

        final String[] javaLibraries = OmpTestInfo.getJavaLibraries();
        for(int i = 0; i < javaLibraries.length; i++) {
            libraryArray.add(new LibraryConfig(LibraryConfig.JAVA,
                    javaLibraries[i]));
        }
        final String[] pythonLibraries = OmpTestInfo.getPythonLibraries();
        for(int i = 0; i < pythonLibraries.length; i++) {
            libraryArray.add(new LibraryConfig(LibraryConfig.PYTHON,
                    pythonLibraries[i]));
        }

        return libraryArray.toArray();
    }

    /**
     * private implementation method for checking all the runtime dependencies
     * between libraries. If any library expresses a dependency to another
     * library that has not been loaded, then a RuntimeException will be thrown,
     * and the initialization of the system interrupted.
     */
    private void checkRuntimeDependencies() {
        final List<String> errors = new ArrayList<String>();
        final Enumeration<OmpLibrary> libraryEnumeration = libraries.elements();
        while(libraryEnumeration.hasMoreElements()) {
            final OmpLibrary l = libraryEnumeration.nextElement();
            final String[] dependencies = l.getRuntimeDependencies();
            for(int i = 0; i < dependencies.length; i++) {
                if(libraries.get(dependencies[i]) == null) {
                    errors.add(new String("Error : Library " + l.getName()
                            + " missing dependency " + dependencies[i] + "\r"));
                }
            }

        }
        if(errors.size() > 0) {
            throw new RuntimeException(
                    "LibraryBroker:Unresolved Library Dependencies : \r"
                            + errors.toString());
        }
    }

    /**
     * private implementation method for calling setUp in turn on all the
     * configured libraries.
     */
    @Deprecated
    public void setUp() {
        final Collection<OmpLibrary> libraryColl = libraries.values();
        final OmpLibrary[] sortedOrder =
                new LibraryDependencySorter().sort(libraryColl
                        .toArray(new OmpLibrary[0]));

        for(int i = 0; i < sortedOrder.length; i++) {
            sortedOrder[i].setUp();
        }
    }

    /**
     * private implementation method for instantiating a given Java pluggable
     * library .
     * 
     * @param className The fully qualified path of the class implementing the
     *        library
     * @return A new instance of the given library
     */
    @SuppressWarnings("unchecked")
    private OmpLibrary loadAndInstantiateJava(final String className) {
        String error = null;
        try {
            final Class<OmpLibrary> libraryClass =
                    (Class<OmpLibrary>) Class.forName(className);
            final Constructor<OmpLibrary> constructor =
                    libraryClass.getConstructor(OmpSut.class);
            final Object instance = constructor.newInstance(sut);
            final OmpLibrary library = (OmpLibrary) instance;
            return library;
        }
        catch(final ClassNotFoundException n) {
            // TODO redirect to logger
            error = ("Java Library Class " + className + " not found");
        }
        catch(final NoSuchMethodException n) {
            // TODO redirect to logger
            error =
                    ("Java Library Class " + className + " has no constructor taking an OmpSut");
        }
        catch(final IllegalAccessException n) {
            // TODO redirect to logger
            error =
                    ("Java Library of class " + className + " cannot be created (IllegalAccess)");
        }
        catch(final InstantiationException n) {
            // TODO redirect to logger
            error =
                    ("Java Library of class " + className + " cannot be created (InstantiationException)");
        }
        catch(final InvocationTargetException n) {
        	n.printStackTrace();
            // TODO redirect to logger
            error =
                    ("Java Library of class " + className + " cannot be created (InvocationTargetException)");
        }
        if(error != null) {
            System.out.println("Throwing " + error);
            throw new RuntimeException(
                    "LibraryBroker:Unresolved Library Dependencies : " + error);
        }
        return null;
    }

    /**
     * private implementation method for instantiating a given Python pluggable
     * library T.
     * 
     * @param className The fully qualified path of the class implementing the
     *        library
     * @return A new instance of the given library
     */
    private OmpLibrary loadAndInstantiatePython(final String moduleAndClassName) {
        String error = null;
        Exception rootCause = null;
        try {
            final int index = moduleAndClassName.lastIndexOf('.');
            final String module = moduleAndClassName.substring(0, index);
            final String className = moduleAndClassName.substring(index + 1);
            System.out.println("module is " + module + " and class is "
                    + className);
            final Object instance =
                    Jythonizer.toJavaInstance(module, className,
                            OmpLibrary.class);

            final OmpLibrary library = (OmpLibrary) instance;
            library.setSut(sut);
            return library;
        }
        catch(final Exception n) {
            rootCause = n;
            n.printStackTrace();
            // TODO redirect to logger'
            error =
                    ("Python interpreter could not be created or library "
                            + moduleAndClassName + " could not be created : ");
        }
        if(error != null) {
            System.out.println("Throwing " + error);
            throw new RuntimeException(
                    "LibraryBroker:Unresolved Library Dependencies : " + error,
                    rootCause);
        }
        return null;
    }

    /**
     * Gets a given library instance, given its unique library name
     * 
     * @param name The unique name of the library
     * @return The (already instantiated and setUp) instance of the library
     */
    @Deprecated
    public OmpLibrary get(final String name) {
        return libraries.get(name);
    }

}
