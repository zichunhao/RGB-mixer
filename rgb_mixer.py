import numpy as np
from PIL import Image
from typing import Callable, List, Optional


class RGBMixer:
    def __init__(
        self,
        R_func: Callable,
        G_func: Callable,
        B_func: Callable,
        R_min: Optional[float] = None,
        R_max: Optional[float] = None,
        G_min: Optional[float] = None,
        G_max: Optional[float] = None,
        B_min: Optional[float] = None,
        B_max: Optional[float] = None,
    ):
        """
        Initialize the RGBMixer.

        Args:
            R_func: Function to apply to the red channel.
            G_func: Function to apply to the green channel.
            B_func: Function to apply to the blue channel.
            R_min: Minimum value for red channel normalization.
                If None, the minimum value of the channel will be used.
            R_max: Maximum value for red channel normalization.
                If None, the maximum value of the channel will be used.
            G_min: Minimum value for green channel normalization.
                If None, the minimum value of the channel will be used.
            G_max: Maximum value for green channel normalization.
                If None, the maximum value of the channel will be used.
            B_min: Minimum value for blue channel normalization.
                If None, the minimum value of the channel will be used.
            B_max: Maximum value for blue channel normalization.
                If None, the maximum value of the channel will be used.
        """
        self.R = R_func
        self.G = G_func
        self.B = B_func
        self.R_min = R_min
        self.R_max = R_max
        self.G_min = G_min
        self.G_max = G_max
        self.B_min = B_min
        self.B_max = B_max

    def process(
        self, images: List[Image.Image], rescale_target: int = 0
    ) -> Image.Image:
        """
        Process the input images and generate a new image using the specified R, G, B functions.

        Args:
            images: List of input images.
            rescale_target: Index of the target image for rescaling.

        Returns:
            The generated image after applying the R, G, B functions and normalization.
        """
        # Get the dimensions of the target image
        target_width, target_height = images[rescale_target].size

        # Resize all images to match the target image size
        resized_images = [img.resize((target_width, target_height)) for img in images]

        # Convert images to numpy arrays
        image_arrays = [np.array(img) for img in resized_images]

        # Extract R, G, B channels from each image
        r_channels = [arr[:, :, 0] for arr in image_arrays]
        g_channels = [arr[:, :, 1] for arr in image_arrays]
        b_channels = [arr[:, :, 2] for arr in image_arrays]

        # Apply the R, G, B functions to the respective channels
        mixed_r = self.R(*r_channels)
        mixed_g = self.G(*g_channels)
        mixed_b = self.B(*b_channels)

        # Normalize the mixed channels
        mixed_r = self._normalize(mixed_r, self.R_min, self.R_max)
        mixed_g = self._normalize(mixed_g, self.G_min, self.G_max)
        mixed_b = self._normalize(mixed_b, self.B_min, self.B_max)

        # Stack the mixed channels to create the final image
        mixed_image = np.dstack((mixed_r, mixed_g, mixed_b)).astype(np.uint8)

        return Image.fromarray(mixed_image)

    def _normalize(
        self,
        arr: np.ndarray,
        min_val: Optional[float] = None,
        max_val: Optional[float] = None,
    ) -> np.ndarray:
        """
        Normalize the input array to the range [0, 255].

        Args:
            arr: Input array to normalize.
            min_val: Minimum value for normalization. If None, the minimum value of the array will be used.
            max_val: Maximum value for normalization. If None, the maximum value of the array will be used.

        Returns:
            The normalized array.
        """
        if min_val is None:
            min_val = np.min(arr)
        if max_val is None:
            max_val = np.max(arr)
        return ((arr - min_val) * 255 / (max_val - min_val)).astype(np.uint8)
