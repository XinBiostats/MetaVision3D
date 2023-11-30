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
![MetaVision3D](https://github.com/XinBiostats/MetaVision3D/assets/136360597/e239688c-8b0e-4f84-ba35-08a0d1a7fa1b)

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
1. Download data from [Dropbox](https://www.dropbox.com/scl/fi/5lc4sjudy1eby0ns80imq/3d_lipid.csv?rlkey=3e8yzh7gva8kzliwnc3xa2mt3&dl=0) and put downloaded data into data folder.
2. We created a demo ([demo.ipynb](https://github.com/XinBiostats/MetaVision3D/blob/main/demo.ipynb)) to demonstrate how to use MetaVision3D. The results will be displayed inline or saved by users.
