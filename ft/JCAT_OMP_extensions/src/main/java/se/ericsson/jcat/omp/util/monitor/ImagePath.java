package se.ericsson.jcat.omp.util.monitor;

public class ImagePath {
    private final String key;
    private final String pathToImage;

    public ImagePath(String key, String pathToImage) {
        this.key = key;
        this.pathToImage = pathToImage;
    }

    public String getKey() {
        return key;
    }

    public String getPathToImage() {
        return pathToImage;
    }
}
