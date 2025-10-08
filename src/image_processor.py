"""
Image processing utilities for PNG sprite loading and alpha channel extraction.
"""

from typing import Optional, Tuple
import numpy as np
import cv2
from PIL import Image
import logging

logger = logging.getLogger(__name__)


class ImageProcessor:
    """
    Process PNG sprite images for collision polygon generation.
    
    Handles loading PNG images, extracting alpha channels, and detecting
    opaque regions for collision shape generation.
    """
    
    def __init__(self, alpha_threshold: int = 128) -> None:
        """
        Initialize image processor.
        
        Args:
            alpha_threshold: Alpha value threshold (0-255). Pixels with alpha
                           greater than this are considered opaque.
                           
        Raises:
            ValueError: If alpha_threshold is not in valid range
        """
        if not 0 <= alpha_threshold <= 255:
            raise ValueError(f"Alpha threshold must be 0-255, got {alpha_threshold}")
        
        self.alpha_threshold = alpha_threshold
    
    def load_image(self, filepath: str) -> Image.Image:
        """
        Load PNG image with alpha channel.
        
        Args:
            filepath: Path to PNG file
            
        Returns:
            PIL Image in RGBA mode
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file is not a valid image
        """
        try:
            img = Image.open(filepath)
        except FileNotFoundError:
            logger.error(f"Image file not found: {filepath}")
            raise
        except Exception as e:
            logger.error(f"Failed to load image {filepath}: {e}")
            raise ValueError(f"Invalid image file: {filepath}") from e
        
        # Convert to RGBA if needed
        if img.mode != 'RGBA':
            logger.info(f"Converting image from {img.mode} to RGBA")
            img = img.convert('RGBA')
        
        logger.info(f"Loaded image: {filepath}, size: {img.size}, mode: {img.mode}")
        return img
    
    def extract_alpha_mask(self, img: Image.Image) -> np.ndarray:
        """
        Extract binary alpha mask from image.
        
        Args:
            img: PIL Image in RGBA mode
            
        Returns:
            Binary numpy array (uint8) where 255 = opaque, 0 = transparent
        """
        # Get alpha channel
        if img.mode != 'RGBA':
            raise ValueError("Image must be in RGBA mode")
        
        alpha = np.array(img)[:, :, 3]
        
        # Apply threshold to create binary mask
        mask = np.where(alpha > self.alpha_threshold, 255, 0).astype(np.uint8)
        
        opaque_pixels = np.sum(mask == 255)
        total_pixels = mask.size
        coverage = (opaque_pixels / total_pixels) * 100
        
        logger.debug(f"Alpha mask created: {opaque_pixels}/{total_pixels} "
                    f"opaque pixels ({coverage:.1f}%)")
        
        return mask
    
    def find_contours(self, mask: np.ndarray) -> Tuple[list, np.ndarray]:
        """
        Find contours in binary mask using OpenCV.
        
        Args:
            mask: Binary mask array (uint8)
            
        Returns:
            Tuple of (contours, hierarchy) from cv2.findContours
            
        Raises:
            ValueError: If no contours found
        """
        if mask.dtype != np.uint8:
            raise ValueError("Mask must be uint8 type")
        
        # Find contours - external only (outermost boundaries)
        contours, hierarchy = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )
        
        if not contours:
            logger.warning("No contours found in image")
            raise ValueError("No contours found - image may be fully transparent")
        
        logger.info(f"Found {len(contours)} contour(s)")
        
        # Log contour sizes
        for i, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            logger.debug(f"Contour {i}: {len(contour)} points, area: {area:.1f}")
        
        return contours, hierarchy
    
    def process_image(self, filepath: str) -> Tuple[Image.Image, list, np.ndarray]:
        """
        Complete image processing pipeline.
        
        Args:
            filepath: Path to PNG file
            
        Returns:
            Tuple of (original_image, contours, mask)
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If image processing fails
        """
        logger.info(f"Processing image: {filepath}")
        
        # Load image
        img = self.load_image(filepath)
        
        # Extract alpha mask
        mask = self.extract_alpha_mask(img)
        
        # Find contours
        contours, _ = self.find_contours(mask)
        
        logger.info(f"Image processing complete: {len(contours)} contour(s) detected")
        
        return img, contours, mask


def get_image_dimensions(filepath: str) -> Tuple[int, int]:
    """
    Get image dimensions without loading full image.
    
    Args:
        filepath: Path to image file
        
    Returns:
        (width, height) tuple
    """
    with Image.open(filepath) as img:
        return img.size


def validate_image_file(filepath: str) -> bool:
    """
    Validate that file is a valid PNG image with alpha channel.
    
    Args:
        filepath: Path to image file
        
    Returns:
        True if valid, False otherwise
    """
    try:
        with Image.open(filepath) as img:
            # Check if PNG
            if img.format != 'PNG':
                logger.warning(f"Image is not PNG format: {img.format}")
                return False
            
            # Check if has alpha
            if img.mode not in ('RGBA', 'LA', 'PA'):
                logger.warning(f"Image does not have alpha channel: {img.mode}")
                return False
            
            return True
    except Exception as e:
        logger.error(f"Image validation failed: {e}")
        return False
