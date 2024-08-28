package se.ericsson.jcat.omp.fw;

import se.ericsson.jcat.omp.library.MockSshLib;

public class MockSut extends OmpSut {

    public OmpLibrary getLibrary(final String name) {
        if (name.equalsIgnoreCase("sshlib")) {
            return new MockSshLib();
        }
        return null;
    }

    public String getConfigDataString(String key) {
        if (key.equals("physical_size")) {
            return "4";
        }
        return null;
    }

}
