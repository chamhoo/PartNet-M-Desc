import os
import sys
sys.path.append('/home/leech/3d/code/PartRules')
from tqdm import tqdm

from partnet_m import PartNetM
from utils import trimesh_render, normalize_trimesh




# Partnet-M Path
path = "/home/leech/3d/data/dataset"
shapepath = "/home/leech/3d/code/PartNet-M-Desc/shapes/"
os.mkdir(shapepath)

# Traver this dir and generate images and mask of each parts
for idx in tqdm(os.listdir(path)):
    data = PartNetM(idx, path)
    datamesh = data.trimesh()
    datamesh = normalize_trimesh(datamesh)
    camera = trimesh_render(datamesh, shapepath + f"{idx}.png")