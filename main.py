import os

from image_util import make_transparent
from saga_util import Saga_cmd
import time

default_dem = "C:\\Users\\ganzk\\Documents\\waterspout\\data\\dem\\mosaic_filled.sgrd"
target_x = 607800
target_y = 4730000

path, filename = os.path.split(default_dem)

start = time.time()

s = Saga_cmd()
# Generate upslope area raster
s.upslope_area(target_x, target_y, default_dem, os.path.join(path, "upslope_area.sgrd"))

# Convert this to png
s.grid_to_image(os.path.join(path, "upslope_area.sgrd"), os.path.join(path, "upslope_area.png"))

# Make white cells transparent
print("\n\nRemoving white cells...")
make_transparent(os.path.join(path, "upslope_area.png"))

finish = time.time()

print("Processing finished in {:.2f} seconds".format(finish - start))