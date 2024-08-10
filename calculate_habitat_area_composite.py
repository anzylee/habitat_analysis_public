from fun import *
from raster import Raster
from config import *

def calculate_habitat_area(layer): #, epsg):
    """
    Calculate the usable habitat area
    :param layer: osgeo.ogr.Layer
    :param epsg: int (Authority code drives area units)
    :return: None
    """
    # retrieve units
    srs = geo.osr.SpatialReference()
    #srs.ImportFromEPSG(epsg)
    area_unit = "square %s" % str(srs.GetLinearUnitsName())
    #pass
    # add area field
    layer.CreateField(geo.ogr.FieldDefn("area", geo.ogr.OFTReal))

    # create list to store polygon sizes
    poly_size = []

    # iterate through geometries (polygon features) of the layer
    for feature in layer:
        # retrieve polygon geometry
        polygon = feature.GetGeometryRef()
        # add polygon size if field "value" is one (determined by chsi_treshold)
        if int(feature.GetField(0)) == 1:
            poly_size.append(polygon.GetArea())
        # write area to area field
        feature.SetField("area", polygon.GetArea())
        # add the feature modifications to the layer
        layer.SetFeature(feature)

    # calculate and print habitat area

    print(sum(poly_size))
    print("The total habitat area is %5.2f " % sum(poly_size) + area_unit)

def main():
    """
    Calculate the usable physical habitat area based on a previously created chsi raster.
    Use the create_hsi_rasters.py script first to create a chsi raster.
    > uses chsi_ras_name: string (directory and file name ending on ".tif")
    > uses chsi_threshold_value: float (min=0.0, max=1.0)
    """
    chsi_raster = Raster(chsi_raster_name)
    # extract pixels where the physical habitat quality is higher than the user threshold value
    habitat_pixels = np.greater_equal(chsi_raster.array, chsi_threshold) * 1
    # write the habitat pixels to a binary array (0 -> no habitat, 1 -> usable habitat)
    geo.create_raster(os.path.abspath("") + "\\habitat\\habitat-pixels.tif",
                      raster_array=habitat_pixels,
                      #epsg=chsi_raster.epsg,
                      geo_info=chsi_raster.geo_transformation) #(create habitat pixels raster)

    # convert the raster with usable pixels to polygon (must be an integer raster!)
    tar_shp_file_name = os.path.abspath("") + "\\habitat\\habitat-area.shp"
    habitat_polygons = geo.raster2polygon(os.path.abspath("") + "\\habitat\\habitat-pixels.tif",
                                          tar_shp_file_name)

    # calculate the habitat area (will be written to the attribute table)
    calculate_habitat_area(habitat_polygons.GetLayer()) #, chsi_raster.epsg)
    #pass


if __name__ == '__main__':


    curve_name = 'composite'    ## SHOULD HAVE THE SAME UNIT AS V AND D
                                # Hampton or CDFW or composite

    percentiles = ['50', '40', '30', '20', '10']  # should be str


    chsi_threshold = 0.6

    if curve_name == 'composite':
        for perc_ind in range(len(percentiles)):
            # launch main function
            hsi_output_dir = os.path.abspath("") + "\\habitat_" + curve_name + "_" + percentiles[perc_ind] + "\\"
            chsi_raster_name = hsi_output_dir + "chsi.tif"
            main()
