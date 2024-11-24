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

## Implement
MetaVision3D can be run through two different ways:

### 1. Using Docker (Recommended):
We have pre-configured the environment for you using Docker, which ensures a consistent and reliable environment and make it easy to get started.

#### Steps:
- Clone MetaVision3D from Github Repository:
```bash
git clone https://github.com/XinBiostats/MetaVision3D
```
- Download [dataset](https://www.dropbox.com/scl/fo/qjdk94golwij84xfii15b/h?rlkey=etrdydm1iw86ntcprbem2wivn&dl=1) from Zenodo and put it in "./MetaVision3D/data/".
- Download Docker desktop from [Docker website](https://www.docker.com), and install it on your machine.
- Open Docker Tesktop first, then open the Terminal or PowerShell(Windows),and run below command with your MetaVision3D path:
```bash
docker run -it --rm --user root -e GRANT_SUDO=yes -p 8888:8888 -v "YOUR_SAMI_PATH:/home/jovyan/work" xinbiostats/metavision3d:latest

example: docker run -it --rm --user root -e GRANT_SUDO=yes -p 8888:8888 -v "/Users/xin.ma/Desktop/MetaVision3D:/home/jovyan/work" xinbiostats/metavision3d:latest
```

- Find the highlighted link in your terminal and copy it to your browser. The link will not be the exactly same, but will show up at same place.
![docker_link](https://github.com/XinBiostats/SAMI/blob/main/figures/docker_link.png)
- All set! You can play with our Demo now. ([demo](https://github.com/XinBiostats/SAMI/blob/main/demo)) 

### 2. Using Conda:
Create your own environment for MetaVision3D.(Due to potential incompatibility issues caused by different operating systems and versions, it is recommended to use Docker.）

#### Steps:
- Clone MetaVision3D from Github Repository:
```bash
git clone https://github.com/XinBiostats/MetaVision3D
```
- Download [dataset](https://www.dropbox.com/scl/fo/qjdk94golwij84xfii15b/h?rlkey=etrdydm1iw86ntcprbem2wivn&dl=1) from Zenodo and put it in "./MetaVision3D/data/".

- Open the Terminal or PowerShell(Windows), then install requirements:
```bash
conda env create -f environment.yml
```

-  Activate SAMI environment, find your R installation's home directory.
```bash
conda activate SAMI
```
We created a demo ([demo.ipynb](https://github.com/XinBiostats/MetaVision3D/blob/main/demo.ipynb)) to demonstrate how to use MetaVision3D. The results will be displayed inline or saved by users.
