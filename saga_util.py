'''
Wrapper for command-line SAGA tools
'''
import os

SAGA_DIR = 'C:\\Users\\ganzk\\Documents\\waterspout\\saga-7.3.0_x64\\saga_cmd.exe'

class Saga_cmd(object):
    def __init__(self, cmd_dir=SAGA_DIR):
        self.saga_dir = cmd_dir

    def execute(self, tool, params):
        '''
        Given tool ID and parameters, execute sys call for the tool.
        '''
        cmd_str = " ".join(key + " " + params[key] for key in params)
        cmd_str = " ".join([self.saga_dir, tool, cmd_str])

        return os.system(cmd_str)
        if __name__ == "__main__":
            print(cmd_str)

    def upslope_area(self, target_x, target_y, dem, output, method=2, conv=1.1):
        tool = "ta_hydrology 4"
        params_dict = {"-TARGET_PT_X": str(float(target_x)),
                       "-TARGET_PT_Y": str(float(target_y)),
                       "-ELEVATION": dem,
                       "-AREA": output,
                       "-METHOD": str(method),
                       "-CONVERGE": str(conv)}
        
        self.execute(tool, params_dict)
    
    def grid_to_image(self, grid, filepath, kml=0, coloring=1, col_palette=8):
        tool = "io_grid_image 0"
        params_dict = {"-GRID": grid,
                       "-FILE": filepath,
                       "-FILE_KML": str(kml),
                       "-COLOURING": str(coloring),
                       "-COL_PALETTE": str(col_palette)}
        
        self.execute(tool, params_dict)
    
    def reclassify_grid(self, grid, output, method=1, rmin=0, rmax=10, rnew=1, rop=1):
        tool = "grid_tools 15"
        params_dict = {"-INPUT": grid,
                       "-RESULT": output,
                       "-METHOD": str(method),
                       "-MIN": str(rmin),
                       "-MAX": str(rmax),
                       "-RNEW": str(rnew),
                       "-ROPERATOR": str(rop)}
        self.execute(tool, params_dict)
    
    def vectorize_grid_class(self, grid, polys, class_all=0, class_id=1, split=0, allverts=0):
        tool = "shapes_grid 6"
        params_dict = {"-GRID": grid,
                       "-POLYGONS": polys,
                       "-CLASS_ALL": str(class_all),
                       "-SPLIT": str(split),
                       "-ALLVERTICES": str(allverts)}
        self.execute(tool, params_dict)

    def simplify_lines(self, shapes, out, tolerance=3):
        tool = "shapes_lines 4"
        params_dict = {"-LINES": shapes,
                       "-OUTPUT": out,
                       "-TOLERANCE": str(tolerance)}
        
        self.execute(tool, params_dict)
    
    def polygon_to_points(self, shapes, points):
        tool = "shapes_polygons 6"
        params_dict = {"-SHAPES": shapes,
                       "-POINTS": points}
        
        self.execute(tool, params_dict)
    
    def add_coords_points(self, shapes, out, x=0, y=0, z=0, m=0, lat=1, lon=1):
        tool = "shapes_points 6"
        params_dict = {"-INPUT": shapes,
                       "-OUTPUT": out,
                       "-X": str(x),
                       "-Y": str(y),
                       "-Z": str(z),
                       "-M": str(m),
                       "-LAT": str(lat),
                       "-LON": str(lon)}
        self.execute(tool, params_dict)
    
    def shp_to_txt(self, shapes, txt, header=1, sep=0, fields="3;7;8", precisions="0;4;4"):
        tool = "io_shapes 18"
        params_dict = {"-POINTS": shapes,
                       "-FILE": txt,
                       "-WRITE_HEADER": str(header),
                       "-FIELDSEP": str(sep),
                       "-FIELDS": fields,
                       "-PRECISIONS": precisions}
        
        self.execute(tool, params_dict)