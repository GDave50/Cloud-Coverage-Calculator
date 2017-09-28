package imageProcessor;

import java.awt.Graphics;
import java.awt.image.BufferedImage;

import javax.swing.JPanel;

/**
 * A JPanel which draws an image as its only content.
 * @author Gage Davidson
 */
class ImageDrawer extends JPanel {
    
    /**
     * Tracks the image that is drawn.
     */
    private BufferedImage image;
    
    ImageDrawer() {
    }
    
    /**
     * Paints the panel with the image.
     */
    @Override
    protected synchronized void paintComponent(Graphics g) {
        super.paintComponent(g);
        
        if (image == null) return;
        
        g.drawImage(image, 0, 0, getWidth(), getHeight(), null);
    }
    
    /**
     * Sets the image that the panel draws.
     * @param image new image to draw
     */
    synchronized void setImage(BufferedImage image) {
        this.image = image;
    }
}
