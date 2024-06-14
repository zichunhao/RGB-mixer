# RGB Mixer
This is a python script that takes an image and mixes the RGB channels pixel-wise to create a new image. 

## Usage
```bash
python3 main.py --yamls <list of yaml files to process>
``` 
Example:
```bash
python main.py --yamls example.yml
```

## Configuration
The RGB Mixer script uses YAML configuration files to specify the input images, output path, and mixing functions for each color channel. Here's an example YAML configuration file:
```yaml
inputs:
  - inputs/image1.jpg
  - inputs/image2.jpg
output: outputs/mixed_image.jpg
R_path: functions/func1.py
G_path: functions/func2.py
B_path: functions/func3.py
```
- `inputs`: A list of input $N$ image paths relative to the project directory.
- `output`: The output path for the generated mixed image, relative to the project directory.
- `R_path`, `G_path`, `B_path`: Paths to the Python files containing the mixing functions for the red, green, and blue channels, respectively. The paths are relative to the project directory.
- The mixing function files should be a python script that defines `func`, `func_min`, and `func_max`.
    - `func`: The mixing function that takes $N$ pixel values and returns the mixed pixel value.
    - `func_min`: The minimum value that the mixed pixel can take. It does not need to be the actual minimum.
    - `func_max`: The maximum value that the mixed pixel can take. 
    - The `func_min` and `func_max` will be used to normalize the pixel values before mixing:
    $$
    \tilde{P} = \frac{P - \mathtt{func\_min}}{\mathtt{func\_max} - \mathtt{func\_min}} \times 255
    $$
    They do not need to be the actual minimum and maximum values of the pixel values. 