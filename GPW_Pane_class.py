class GPW_Pane:
    def __init__(self, gridded_data, header_data):
        self.grid = gridded_data
        self.nrows = header_data['nrows']
        self.ncols = header_data['ncols']
        self.origin = (float(header_data['xllcorner']), float(header_data['yllcorner']))
        self.resolution = float(header_data['cellsize'])
        self.bad_data_flag = float(header_data['NODATA_value'])