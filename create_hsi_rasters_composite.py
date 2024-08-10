from fun import *
from raster_hsi import HSIRaster, Raster
from time import perf_counter


def combine_hsi_rasters(raster_list, method="geometric_mean"):
    """
    Combine HSI rasters into combined Habitat Suitability Index (cHSI) Rasters
    :param raster_list: list of HSIRasters (HSI)
    :param method: string (default="geometric_mean", alt="product)
    :return HSIRaster: contains float pixel values
    """
    if method == "geometric_mean":
        power = 1.0 / float(raster_list.__len__())
    else:
        # supposedly method is "product"
        power = 1.0

    chsi_raster = Raster(cache_folder + "chsi_start.tif",
                         raster_array=np.ones(raster_list[0].array.shape),
                         epsg=raster_list[0].epsg,
                         geo_info=raster_list[0].geo_transformation)
    for ras in raster_list:
        chsi_raster = chsi_raster * ras

    return chsi_raster ** power
    #pass


def get_hsi_curve(json_file, life_stage, parameters):
    """
    Retrieve HSI curves from fish json file for a specific life stage and a set of parameters
    :param fish_json: string (directory and name of json file containing HSI curves)
    :param life_stage: string (fish life stage, either "fry", "spawning", "juvenile", or "adult")
    :param parameters: list (may contain "velocity", "depth", and/or "grain_size")
    :return curve_data: dictionary of life stage specific HSI curves as pd.DataFrame for requested parameters;
                        for example: curve_data["velocity"]["HSI"]
    """
    # read the JSON file with fun.read_json
    file_info = read_json(json_file)
    # instantiate output dictionary
    curve_data = {}
    # iterate through parameter list (e.g., ["velocity", "depth"])
    for par in parameters:
        # create a void list to store pairs of parameter-HSI values as nested lists
        par_pairs = []
        # iterate through the length of parameter-HSI curves in the JSON file
        for i in range(0, file_info[par][life_stage].__len__()):
            # if the parameter is not empty (i.e., __len__ > 0), append the parameter-HSI (e.g., [u_value, HSI_value]) pair as nested list
            if str(file_info[par][life_stage][i]["HSI"]).__len__() > 0:
                try:
                    # only append data pairs if both parameter and HSI are numeric (floats)
                    par_pairs.append([float(file_info[par][life_stage][i][par_dict[par]]),
                                      float(file_info[par][life_stage][i]["HSI"])])
                except ValueError:
                    logging.warning("Invalid HSI curve entry for {0} in parameter {1}.".format(life_stage, par))
        # add the nested parameter pair list as pandas DataFrame to the curve_data dictionary
        curve_data.update({par: pd.DataFrame(par_pairs, columns=[par_dict[par], "HSI"])})
    return curve_data

    #pass


def get_hsi_raster(tif_dir, hsi_curve):
    """
    Calculate and return Habitat Suitability Index Rasters
    :param tif_dir: string of directory and name of  a tif file with parameter values (e.g., depth in m)
    :param hsi_curve: nested list of [[par-values], [HSI-values]], where
                            [par-values] (e.g., velocity values) and
                            [HSI-values] must have the same length.
    :return hsi_raster: Raster with HSI values
    """
    return HSIRaster(tif_dir, hsi_curve)
    #pass

def combine_hsi_rasters(raster_list, method="geometric_mean"):
    if method == "geometric_mean":
        power = 1.0 / float(raster_list.__len__())
    else:
        # supposedly method is "product"
        power = 1.0

    chsi_raster = Raster(cache_folder + "chsi_start.tif",
                         raster_array=np.ones(raster_list[0].array.shape),
                         epsg=raster_list[0].epsg,
                         geo_info=raster_list[0].geo_transformation)
    for ras in raster_list:
        chsi_raster = chsi_raster * ras

    return chsi_raster ** power
def get_fish_file(curve_name, fish_name, **kwargs):

    percentiles = kwargs.get('percentiles', None)
    perc_ind = kwargs.get('perc_ind', None)

    if curve_name == 'composite':
        fish_file = os.path.abspath("") + '/hsc_'+curve_name+'/'+curve_name+'_'+fish_name+'_'+percentiles[perc_ind]+'.json'

    else:
        fish_file = os.path.abspath("") + '/hsc_'+curve_name+'/' + curve_name + '_' + fish_name + '.json'

    return fish_file

@log_actions
@cache
def main():
    # get HSI curves as pandas DataFrames nested in a dictionary
    hsi_curve = get_hsi_curve(fish_file, life_stage=life_stage, parameters=parameters)

    # create HSI rasters for all parameters considered and store the Raster objects in a dictionary
    eco_rasters = {}
    for par in parameters:
        hsi_par_curve = [list(hsi_curve[par][par_dict[par]]),
                         list(hsi_curve[par]["HSI"])]
        eco_rasters.update({par: get_hsi_raster(tif_dir=tifs[par], hsi_curve=hsi_par_curve)})
        eco_rasters[par].save(hsi_output_dir + "hsi_%s.tif" % par)

    # get and save chsi raster
    chsi_raster = combine_hsi_rasters(raster_list=list(eco_rasters.values()),
                                      method="geometric_mean")
    chsi_raster.save(hsi_output_dir + "chsi.tif")


if __name__ == '__main__':
    # define global variables for the main() function

    curve_name = 'composite'    ## SHOULD HAVE THE SAME UNIT AS V AND D
                                # Hampton or CDFW or composite

    percentiles = ['50', '40', '30', '20', '10']  # should be str

    fish_name = 'Chinook'
    life_stage = "Spawning"  # either "fry", "juvenile", "adult", or "spawning"

    parameters = ["velocity", "depth"]

    if curve_name == 'composite':
        for perc_ind in range(len(percentiles)):
            fish_file = get_fish_file(curve_name, fish_name,
                                      percentiles=percentiles, perc_ind=perc_ind)

            tifs = {"velocity": os.path.abspath("") + "\\basement\\flow_velocity.tif",
                    "depth": os.path.abspath("") + "\\basement\\water_depth.tif"}
            hsi_output_dir = os.path.abspath("") + "\\habitat_"+curve_name+"_"+percentiles[perc_ind]+"\\"

            if not os.path.exists(hsi_output_dir):
                os.mkdir(hsi_output_dir)

            # run code and evaluate performance
            t0 = perf_counter()
            main()
            t1 = perf_counter()
            print("Time elapsed: " + str(t1 - t0))



