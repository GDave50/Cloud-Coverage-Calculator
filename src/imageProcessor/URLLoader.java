package imageProcessor;

import java.awt.image.BufferedImage;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.net.MalformedURLException;
import java.net.URL;
import java.nio.file.FileSystems;
import java.util.ArrayList;
import java.util.Scanner;

import javax.imageio.ImageIO;
import javax.swing.JFileChooser;
import javax.swing.JOptionPane;
import javax.swing.filechooser.FileFilter;
import javax.swing.filechooser.FileNameExtensionFilter;

import intravenous.display.LookNFeel;
import intravenous.tools.Timer;

/**
 * The goal of this program is to download images from about 1400 URLs, store
 * those images in a folder, prompt the user to crop each image, and then prompt
 * the user to categorize each image based on the cloud type it contains.
 * @author Gage Davidson
 */
class URLLoader {
    
    /**
     * Filepath delimiter (i.e. "/" "//" "\\")
     */
    static final String DELIM = FileSystems.getDefault().getSeparator();
    
    /**
     * String path to a directory which holds the images.
     */
    static String imagesDir;
    
    /**
     * Default folder for images. Any folder can be used, however.
     */
    private static final String DEFAULT_IMAGES_DIR =
            "C:/Users/" + System.getProperty("user.name") + "/Desktop/images/".replaceAll("//", DELIM);
    
    /**
     * File which holds the ~1400 URLs.
     */
    private static File urlFile;
    
    /**
     * @param args command line arguments; unused
     */
    public static void main(String[] args) {
        LookNFeel.setLookNFeel("Nimbus");
        
        int opt =
                JOptionPane.showConfirmDialog(null, "Do you have a full image folder?", "", JOptionPane.YES_NO_OPTION);
        
        /* if the user does not already have all the images */
        if (opt == JOptionPane.NO_OPTION) {
            urlFile = getURLsFile();
            imagesDir = getImagesFolder();
            
            ArrayList<URL> urls = loadURLs(urlFile);
            writeImageURLs(urls);
        } else {
            imagesDir = getImagesFolder();
        }
        
        Organizer org = new Organizer();
        org.runOrganizer();
    }
    
    /**
     * Prompts the user to select a folder which will hold or already does hold
     * images.
     * @return filepath to the folder
     */
    private static String getImagesFolder() {
        JFileChooser chooser = new JFileChooser();
        chooser.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY);
        chooser.setDialogTitle("Choose an images folder");
        chooser.setSelectedFile(new File(DEFAULT_IMAGES_DIR));
        
        if (chooser.showOpenDialog(null) == JFileChooser.CANCEL_OPTION)
            System.exit(0);
        
        String path = chooser.getSelectedFile().getPath();
        
        if (!path.endsWith(DELIM))
            path += DELIM;
        
        return path;
    }
    
    /**
     * Prompts the user to select a text file which contains a list of URLs.
     * @return text file containing a list of URLs
     */
    private static File getURLsFile() {
        JFileChooser chooser = new JFileChooser();
        
        FileFilter textFileFilter = new FileNameExtensionFilter("Text files", new String[] {
                "txt"
        });
        chooser.setFileFilter(textFileFilter);
        chooser.setDialogTitle("Choose a URLs File");
        
        if (chooser.showOpenDialog(null) == JFileChooser.CANCEL_OPTION)
            System.exit(0);
        
        return chooser.getSelectedFile();
    }
    
    /**
     * Creates a list of URLs based on a given text file containing a list of
     * URLs
     * @param urlList text file containing a list of URLs
     * @return list of URLs loaded
     */
    private static ArrayList<URL> loadURLs(File urlList) {
        ArrayList<URL> urls = new ArrayList<>(1450);
        
        try (Scanner scan = new Scanner(urlList)) {
            for (String line = scan.nextLine(); scan.hasNextLine(); line = scan.nextLine()) {
                try {
                    URL url = new URL(line);
                    urls.add(url);
                } catch (MalformedURLException ex) {
                    System.err.println("failed to create URL: " + ex.getMessage());
                }
            }
        } catch (FileNotFoundException ex) {
            System.err.println("file not found: " + ex.getMessage());
            System.exit(1);
            return null;
        }
        
        System.out.println("Done loading URLs");
        
        return urls;
    }
    
    /**
     * Iterate through all the URLs in a given list, download the image, and
     * save the image to images folder.
     * @param urls list of URLS
     */
    private static void writeImageURLs(ArrayList<URL> urls) {
        Timer timer = new Timer();
        final String format = "Done writing image %d (%dms)\n";
        int count = 1;
        
        for (URL url : urls) {
            try {
                timer.start();
                
                BufferedImage image = ImageIO.read(url);
                
                String filepath = imagesDir + "image" + count + ".jpg";
                ImageIO.write(image, "jpg", new File(filepath));
                
                System.out.printf(format, count, (int) timer.time());
                
                ++count;
            } catch (IOException | IllegalArgumentException ex) {
                System.err.println("failed to read/write image" + count + ", skipping");
            }
        }
        
        System.out.println("Done writing all images");
    }
}
