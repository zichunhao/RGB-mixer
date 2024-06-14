import argparse
from typing import List
from tqdm import tqdm
from PIL import Image
from rgb_mixer import RGBMixer
from utils import parse_yaml
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)


def process_images(
    rgb_mixer: RGBMixer, input_paths: List[str], output_path: str
) -> None:
    """
    Process input images using the RGBMixer and save the generated image.

    Args:
        rgb_mixer: An instance of RGBMixer.
        input_paths: List of input image paths.
        output_path: Path to save the generated image.
    """
    images = [Image.open(path) for path in input_paths]
    mixed_image = rgb_mixer.process(images, rescale_target=0)
    mixed_image.save(output_path)


def main():
    parser = argparse.ArgumentParser(description="Process images using RGBMixer")
    parser.add_argument(
        "--yamls",
        nargs="+",
        required=True,
        help="Path(s) to the YAML configuration file(s)",
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Increase output verbosity"
    )
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    yaml_files = args.yamls

    for yaml_file in tqdm(yaml_files, desc="Processing YAML files"):
        try:
            rgb_mixer, input_paths, output_path = parse_yaml(yaml_file)
            input_images = [Image.open(path) for path in input_paths]
            output_path = Path(output_path)
            # make sure the output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)
            img = rgb_mixer.process(input_images)
            img.save(output_path)
            logging.debug(f"Generated image saved to: {output_path}")
        except FileNotFoundError as e:
            logging.error(f"Skipping {yaml_file} due to a FileNotFoundError: {e}")
            continue
        except ValueError as e:
            logging.error(f"Skipping {yaml_file} due to a ValueError: {e}")
            continue
        except Exception as e:
            logging.error(f"Skipping {yaml_file} due to an unexpected error: {e}")
            continue


if __name__ == "__main__":
    main()
