import pandas as pd
import json

def generate_json_fish_file(curve_name, fish_name, variables, life_stages,**kwargs):

    percentiles = kwargs.get('percentiles', None)
    perc_ind = kwargs.get('perc_ind', None)

    Dict = {}
    ind = 0

    for var in variables:
        for peri in life_stages:

            HSI = pd.read_excel('./hsc_'+curve_name+'/'+curve_name+'_'+fish_name+'.xlsx',
                                sheet_name= peri+'_'+var)
            dict_var_HSI = {}

            if curve_name == 'composite':
                col_ind = perc_ind + 1 # 1,2,3,4
            else:
                col_ind = 1

            for ii in range(0, len(HSI)):
                dict_var_HSI[ii] = {HSI.columns[0]: HSI[HSI.columns[0]][ii],
                                   'HSI': HSI[HSI.columns[col_ind]][ii]}

            Dict[var] = {peri: [*dict_var_HSI.values()]}
            ind = ind + 1

    # Serializing json
    json_object = json.dumps(Dict, indent=2)

    # Writing to sample.json
    with open('./hsc_'+curve_name+'/'+curve_name+'_'+fish_name+'_'+percentiles[perc_ind]+'.json', "w") as outfile:
        outfile.write(json_object)


curve_name = 'composite'  ## SHOULD HAVE THE SAME UNIT AS V AND D
percentiles = ['50', '40', '30', '20', '10'] # should be str

# Hampton or CDFW or composite
fish_names = ['Chinook', 'Coho', 'RainbowTrout', 'Steelhead']

# curve_name = 'CDFW'
# fish_name = 'Chinook'

variables = ["velocity", "depth"]
life_stages = ["Spawning"]

for fish_name in fish_names:
    for perc_ind in range(len(percentiles)):
        generate_json_fish_file(curve_name, fish_name, variables, life_stages,
                                    percentiles = percentiles, perc_ind = perc_ind)