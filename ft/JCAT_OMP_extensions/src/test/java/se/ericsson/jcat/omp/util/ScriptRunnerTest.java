package se.ericsson.jcat.omp.util;

import java.io.File;

import org.junit.Assert;
import org.junit.Test;

public class ScriptRunnerTest {

    @Test
    public void testRunner() {
        File file = new File("runner");
        Tools.extractResourceFile("gethostname.sh", this.getClass(), file, true);
        ScriptRunner sr = new ScriptRunner(new String[] { file.getAbsolutePath(), "arg" });
        sr.run();
        Assert.assertTrue("File name check failed", sr.getScenarioFilename().equals(file.getAbsolutePath()));
        Assert.assertTrue("Script failed", sr.getExitValue() == 0);
        Assert.assertFalse("Script should not fail", sr.hasFailures());
        Assert.assertFalse("Script should not contain error", sr.hasError());
    }

    @Test
    public void testRunnerFail() {
        File file = new File("error_runner");
        Tools.extractResourceFile("errorscript.sh", this.getClass(), file, true);
        ScriptRunner sr = new ScriptRunner(new String[] { file.getAbsolutePath(), "arg" });
        sr.run();
        Assert.assertTrue("Script should fail", sr.hasFailures());
    }

    @Test
    public void testRunnerError() {
        ScriptRunner sr = new ScriptRunner(new String[] { "not_existing_file", "arg" });
        sr.run();
        Assert.assertTrue("Script should return error", sr.hasError());
        Assert.assertTrue("Script should have failure message", sr.getFailures() != null);
    }

    @Test
    public void testFactory() {
        Runner runner = RunnerFactory.createScriptRunner(new String[] { "not_existing_file", "arg" });
        runner.init();
        runner.run();
        Assert.assertTrue("Script failed", runner.hasError());
    }
}
