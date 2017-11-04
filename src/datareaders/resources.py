from os.path import join, dirname

def get_data_resource(rel_path):
    energy_comps_dir = dirname(dirname(dirname(__file__))) # energy-analytics-comps/
    data_file = join(energy_comps_dir, 'data', rel_path) # energy-analytics-comps/data/rel_path
    return data_file
