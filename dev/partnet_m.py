
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
        self.pc10000_path = os.path.join(self.objpath, "point_sample", "pts-10000.txt")
        self.meshpart_path = os.path.join(self.objpath, "textured_objs")
        self.resultpath = os.path.join(self.objpath, "result.json")
        self.rulepath = os.path.join(self.objpath, "mobility_v2.json")
        self.plypath = os.path.join(self.objpath, "point_sample", "sample-points-all-pts-nor-rgba-10000.ply")
        self.ptspath = os.path.join(self.objpath, "point_sample", "pts-10000.pts")


    def _list_leaves(self, node):
        if 'children' not in node:
            # If there are no children, it's a leaf node, return its 'objs'
            return [node]
        else:
            # Otherwise, recursively process its children
            leaves = []
            for child in node.get('children', []):
                leaves += self._list_leaves(child)
            return leaves
    
    def trimesh(self):
        combined_mesh = []
        # 遍历指定文件夹下的所有文件
        for filename in os.listdir(self.meshpart_path):
            if filename.endswith('.obj'):
                file_path = os.path.join(self.meshpart_path, filename)
                # 加载单个网格文件
                current_mesh = load_trimesh_mesh(file_path)
                combined_mesh.append(current_mesh)
        return trimesh.util.concatenate(combined_mesh)
    
    # 递归遍历节点，并对含有objs的节点添加bbox
    def __add_bbox(self, node):
        if 'objs' in node:
            # 如果该节点有objs键，计算bbox并添加到节点中
            node['bbox'] = self.calculate_bbox(node['objs'])
        
        # 如果有子节点，继续递归处理
        if 'children' in node:
            for child in node['children']:
                self.__add_bbox(child)
                

    def addbbox(self, workdir):
        workspace = f"/home/leech/3d/code/PartRules/results/"
        with open(self.resultpath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for item in data:
            self.__add_bbox(item)
        # save
        with open(os.path.join(workspace, f"{self.id}.json"), 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


    def calculate_bbox(self, objs):
        combined_mesh = []
        for objpath in objs:
            file_path = os.path.join(self.meshpart_path, f"{objpath}.obj")
            current_mesh = load_trimesh_mesh(file_path)
            combined_mesh.append(current_mesh)
        completed_mesh = trimesh.util.concatenate(combined_mesh)
        bbox_oriented  = completed_mesh.bounding_box_oriented
        return bbox_oriented.vertices, bbox_oriented.primitive.transform

        
    def partsimg(self, workdir):
        # 创建新的文件夹
        workspace = f"/home/leech/3d/code/PartRules/{workdir}/{str(self.id)}/"
        os.mkdir(workspace)
        # 加载所有parts
        with open(self.resultpath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        leaves = []
        for item in data:
            leaves += self._list_leaves(item)
        # 获得所有obj的list
        obj_list = []
        for filename in os.listdir(self.meshpart_path):
            if filename.endswith('.obj'):
                obj_list.append(filename.split(".")[0])
        # 遍历所有parts，读取所需要的obj文件并绘图
        for part in leaves:
            part_name = part["name"]
            part_id = part["id"]
            red_list = part["objs"]
            # 绘制mesh
            combined_mesh = list()
            # 红色标记部分
            for part_path in red_list:
                file_path = os.path.join(self.meshpart_path, f"{part_path}.obj")
                current_mesh = load_trimesh_mesh(file_path)
                set_mesh_color(current_mesh, [1.,0.,0.,1.])
                combined_mesh.append(current_mesh)
            # 蓝色部分
            blue_list = list(set(obj_list) - set(red_list))
            for part_path in blue_list:
                file_path = os.path.join(self.meshpart_path, f"{part_path}.obj")
                current_mesh = load_trimesh_mesh(file_path)
                set_mesh_color(current_mesh,[0.,0.,1.,0.1])
                combined_mesh.append(current_mesh)
            # 合并并绘制
            completed_mesh = trimesh.util.concatenate(combined_mesh)
            completed_mesh = normalize_trimesh(completed_mesh)
            camera = trimesh_render(completed_mesh, workspace + f"{part_name}_{part_id}.png", title=f"{part_name}_{part_id}")

        # # 遍历指定文件夹下的所有文件
        # for filename in os.listdir(self.meshpart_path):
        #     if filename.endswith('.obj'):
        #         combined_mesh = []
        #         # 加载目标mesh
        #         file_path = os.path.join(self.meshpart_path, filename)
        #         current_mesh = load_trimesh_mesh(file_path)
        #         set_mesh_color(current_mesh, [1.,0.,0.,1.])
        #         combined_mesh.append(current_mesh)
        #         # 加载其他mesh
        #         for othesname in os.listdir(self.meshpart_path):
        #             if (othesname.endswith('.obj')) and (othesname != filename):
        #                 others_path = os.path.join(self.meshpart_path, othesname)
        #                 # 加载单个网格文件
        #                 current_other_mesh = load_trimesh_mesh(others_path)
        #                 set_mesh_color(current_other_mesh, [0.,0.,1.,0.1])
        #                 combined_mesh.append(current_other_mesh)
        #         completed_mesh = trimesh.util.concatenate(combined_mesh)
        #         camera = trimesh_render(completed_mesh, workspace + f"{filename}.png")
            

    def ply(self):
        with open(self.plypath, 'r') as f:
            lines = f.readlines()
        
        # Find where the header ends
        header_end = lines.index("end_header\n")
        
        # Read the vertex data
        vertex_data = []
        for line in lines[header_end + 1:]:
            vertex_data.append(list(map(float, line.strip().split())))
        
        return np.array(vertex_data)

    def pts(self):
        with open(self.ptspath, 'r') as file:
            lines = file.readlines()
            points = []
            for line in lines:
                values = line.strip().split()
                x, y, z = map(float, values[:3])
                r, g, b = map(float, values[3:])
                points.append([x, y, z, r, g, b])

        return np.array(points)


    def process_entry(self, entry):
        # 处理当前entry的objs并替换为点云
        if 'objs' in entry:
            processed_objs = []
            for obj_name in entry['objs']:
                mtl_file = os.path.join(self.meshpart_path, f"{obj_name}.mtl")
                obj_file = os.path.join(self.meshpart_path, f"{obj_name}.obj")

                # 检查mtl和obj文件是否同时存在
                if os.path.exists(mtl_file) and os.path.exists(obj_file):
                    point_cloud = self.load_mesh_as_pointcloud(obj_file)
                    processed_objs.append(point_cloud)  # 将点云转换为列表以存储在JSON中

            entry['objs'] = processed_objs
        
        # 递归处理children
        if 'children' in entry:
            for i, child in enumerate(entry['children']):
                entry['children'][i] = self.process_entry(child)

        return entry



    def ruletree(self):
        # 读取JSON文件
        with open(self.rulepath, 'r') as f:
            data = json.load(f)
        
        processed_data = []

        for entry in data:
            processed_entry = self.process_instree(entry)
            processed_data.append(processed_entry)

        return processed_data
    
    def process_instree(self, entry):
        # 递归处理children
        if 'children' in entry:
            for i, child in enumerate(entry['children']):
                entry['children'][i] = self.process_instree(child)
        return entry

    

if __name__ == "__main__":
    # <trimesh.Scene(len(geometry)=3, name=`new-5.obj`)>
    dataset = PartNetM(156, "/home/leech/code/partnet_m")
    # <trimesh.Trimesh(vertices.shape=(144, 3), faces.shape=(140, 3), name=`new-2.obj`)>
    # dataset = PartNetM(3593, "/home/leech/code/3DGT-LLM/partnet_m")
    pc = dataset.pc()
    print(f"PC shape:   " ,pc.shape)