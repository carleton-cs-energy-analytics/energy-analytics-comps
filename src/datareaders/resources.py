from os.path import join, dirname

def get_data_resource(rel_path):
    '''
    Rel_path should not start with a slash
    :param rel_path: Str of folder/file.extension that we want, can also just be folder!
    :return: Path to data/rel_path
    '''
    energy_analytics_comps_path = dirname(dirname(dirname(__file__))) # energy-analytics-comps/
    data_file = join(energy_analytics_comps_path, 'data', rel_path) # energy-analytics-comps/data/rel_path
    return data_file
