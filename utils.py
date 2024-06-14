import yaml
from typing import Dict, List, Tuple
from rgb_mixer import RGBMixer
from importlib import import_module
import inspect
from pathlib import Path


def parse_yaml(yaml_file: str) -> Tuple[RGBMixer, str, str]:
    """
    Parse a YAML file and create an RGBMixer object.

    Args:
        yaml_file: Path to the YAML file.

    Returns:
        A tuple containing an instance of RGBMixer, the input paths, and the output path.

    Raises:
        ValueError: If the number of input images is insufficient for the R, G, B functions.
    """
    # Load the YAML file
    with open(yaml_file, "r") as file:
        config = yaml.safe_load(file)

    # Extract the necessary fields from the YAML config
    input_paths: List[str] = config["inputs"]
    output_path: str = config["output"]
    function_paths: Dict[str, str] = {
        "R": config["R_path"],
        "G": config["G_path"],
        "B": config["B_path"],
    }
    num_images = len(input_paths)
    rescale_target = config.get("rescale_target", 0)
    # Load the R, G, B functions and min/max values from separate Python files
    functions = {}
    min_max_values = {}
    for channel, path in function_paths.items():
        module_name = path.replace(".py", "").replace("/", ".")
        module = import_module(module_name)
        func = getattr(module, "func")
        func_args = inspect.getfullargspec(func).args
        # Check if there are enough input images
        if len(func_args) > num_images:
            raise ValueError(
                f"Insufficient number of input images for {channel} function."
            )
        functions[channel] = func
        min_max_values[f"{channel}_min"] = getattr(module, "func_min", None)
        min_max_values[f"{channel}_max"] = getattr(module, "func_max", None)

    # Create an instance of RGBMixer
    rgb_mixer = RGBMixer(
        R_func=functions["R"],
        G_func=functions["G"],
        B_func=functions["B"],
        **min_max_values,
    )

    return rgb_mixer, rescale_target, input_paths, output_path


def get_proj_dir():
    return Path(__file__).resolve().parent
