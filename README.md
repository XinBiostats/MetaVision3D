# MetaVision3D
©Nov 31, 2023 University of Florida Research Foundation, Inc. All Rights Reserved.

Shield: [![CC BY-NC-SA 4.0][cc-by-nc-sa-shield]][cc-by-nc-sa]

This work is licensed under a
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License][cc-by-nc-sa].

[![CC BY-NC-SA 4.0][cc-by-nc-sa-image]][cc-by-nc-sa]

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/
[cc-by-nc-sa-image]: https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png
[cc-by-nc-sa-shield]: https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg

We introduce __MetaVision3D__, a novel pipeline driven by computer vision techniques for the transformation of serial 2D MALDI mass spectrometry imaging sections into a high-resolution 3D spatial metabolome. Our framework employs advanced algorithms for image registration, normalization, and interpolation to enable the integration of serial 2D tissue sections, thereby generating a comprehensive 3D model of unique diverse metabolites across host tissues at mesoscale.
![MetaVision3D](https://github.com/XinBiostats/MetaVision3D/assets/136360597/4e87e94f-c738-47b1-900a-fa0e605ac808)

## Installation

1. Download MetaVision3D:
```bash
git clone https://github.com/XinBiostats/MetaVision3D
```
2. Requirements: MetaVision3D is implemented in Python. To install requirements
```bash
conda env create -f environment.yml
```
## Usage
1. Download data from [Dropbox](https://www.dropbox.com/scl/fo/tbsqj4d27zsqbkexxak8r/AI3TuR-k6zvliJTHWx8mF-c?rlkey=aznpybkek32cgg84mi9dvovtp&st=f6l50m6w&dl=0) and put downloaded data to "./MetaVision3D/data/"
2. We created a demo ([demo.ipynb](https://github.com/XinBiostats/MetaVision3D/blob/main/demo.ipynb)) to demonstrate how to use MetaVision3D. The results will be displayed inline or saved by users.
