
import sys
sys.path.append('/home/leech/3d/code/PartRules')

import os 
import json
import numpy as np
import trimesh
import torch 
from utils import load_trimesh_mesh, set_mesh_color, trimesh_render, normalize_trimesh

class PartNetM(object):
    def __init__(self, id, rootpath) -> None:
        self.id = id
        self.rootpath = rootpath
        self.objpath = os.path.join(self.rootpath, f"{id}")
        self.meshpart_path = os.path.join(self.objpath, "textured_objs")

    def trimesh(self):
        combined_mesh = []
        for filename in os.listdir(self.meshpart_path):
            if filename.endswith('.obj'):
                file_path = os.path.join(self.meshpart_path, filename)
                # load simge mesh
                current_mesh = load_trimesh_mesh(file_path)
                combined_mesh.append(current_mesh)
        return trimesh.util.concatenate(combined_mesh)
    

    

if __name__ == "__main__":
    # <trimesh.Scene(len(geometry)=3, name=`new-5.obj`)>
    dataset = PartNetM(156, "/home/leech/code/partnet_m")
