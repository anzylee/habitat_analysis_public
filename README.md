## Habitat analysis using composite habitat suitability curves

### Background
A set of python codes were developed to perform habitat analysis using composite habitat suitability curves with different percentile vales. The main python scripts and functions are based on this [Ecohydraulics repo](https://github.com/Ecohydraulics/Exercise-geco) and the in-depth description can be found in 'Python Programming for Water Resources Engineering and Research' below.

### Usage
This toolset is composed of two main python scripts.

#### 1. create_hsi_rasters_composite.py
This script creates HSI (habitat suitability index) rasters using velocity/depth rasters and HSC (habitat suitability curve).
The veolcotiy and depth rasters are stored in 'basement' folder and the composite HSCs are stored in 'hsc_composite' folder. This code only allows HSC in json format and you can use 'xlsx_to_json.py' to convert the HSC in xlsx to json format.
You can change the directories in the python script. Outputs are 'hsi_depth.tif' (depth HSI raster), 'hsi_velocity.tif' (velocity HSI raster), and 'chsi.tif' (combined HSI raster) in 'habitat_composite_XX' folder where XX denotes the percentile value.

#### 2. calculate_habitat_area_composite.py
This script calculates the habitat area whose HSI is greater than a certain threshold, which is defined in the code. Output is 'habitat-area.shp' (habitat area polygon) in 'habitat_composite_XX' folder where XX denotes the percentile value.
