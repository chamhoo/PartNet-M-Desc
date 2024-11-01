import os
import sys
sys.path.append('/home/leech/3d/code/PartRules')

import trimesh
import numpy as np
import matplotlib.pyplot as plt

from PIL import Image
from io import BytesIO






def load_trimesh_mesh(mesh_file):
    # 使用 trimesh 加载 mesh
    mesh = trimesh.load(mesh_file, process=False)
    return trimesh.util.concatenate(mesh)


def check_trimesh_info(mesh):
    # 检查顶点和面信息
    print(f"Vertices shape: {mesh.vertices.shape}")
    print(f"Faces shape: {mesh.faces.shape}")
    
    # 检查 UV 坐标
    if hasattr(mesh.visual, 'uv') and mesh.visual.uv is not None:
        print(f"UV coordinates shape: {mesh.visual.uv.shape}")
    else:
        print("No UV coordinates found.")
    
    # 检查是否存在纹理贴图
    if hasattr(mesh.visual, 'material') and mesh.visual.material.image is not None:
        print(f"Texture image size: {mesh.visual.material.image.size}")
        print(f"Texture image mode: {mesh.visual.material.image.mode}")
    else:
        print("No texture image found.")
    
    # 检查法线
    if hasattr(mesh, 'vertex_normals') and mesh.vertex_normals is not None:
        print(f"Vertex normals shape: {mesh.vertex_normals.shape}")
    else:
        print("No vertex normals found.")
    
    # 检查材质信息
    if hasattr(mesh.visual, 'material'):
        print(f"Material information: {mesh.visual.material}")
    else:
        print("No material information found.")


# 检查 PyTorch3D Meshes 对象
def check_pytorch3d_info(pt3d_mesh):
    # 检查是否有顶点信息
    if pt3d_mesh.isempty():
        print("Error: Mesh is empty!")
        return
    
    # 检查顶点
    verts = pt3d_mesh.verts_packed()
    print(f"Vertices shape: {verts.shape}")
    
    # 检查面的信息
    faces = pt3d_mesh.faces_packed()
    print(f"Faces shape: {faces.shape}")
    
    # 检查是否有纹理
    if pt3d_mesh.textures is not None:
        if hasattr(pt3d_mesh.textures, 'verts_rgb'):
            verts_rgb = pt3d_mesh.textures.verts_rgb_packed()
            print(f"Vertex RGB color shape: {verts_rgb.shape}")
        elif hasattr(pt3d_mesh.textures, 'maps'):
            texture_maps = pt3d_mesh.textures.maps_packed()
            print(f"Texture map shape: {texture_maps.shape}")
        else:
            print("Warning: Mesh has textures, but the texture format is not recognized.")
    else:
        print("Mesh does not have any textures.")
    
    # 获取批大小
    batch_size = len(pt3d_mesh.verts_list())
    print(f"Batch size: {batch_size}")
    
    # 检查每个网格的顶点数量和面数量
    for i in range(batch_size):
        print(f"Mesh {i}:")
        print(f"  Number of vertices: {len(pt3d_mesh.verts_list()[i])}")
        print(f"  Number of faces: {len(pt3d_mesh.faces_list()[i])}")


def trimesh_render(mesh, saved_path, title=""):

    scene = mesh.scene()
    rotate1 = trimesh.transformations.rotation_matrix(
        angle=np.radians(-30.0), direction=[1, 0, 0], point=scene.centroid
    )
    rotate2 = trimesh.transformations.rotation_matrix(
        angle=np.radians(30.0), direction=[0, 1, 0], point=scene.centroid
    )
    translate_back = trimesh.transformations.translation_matrix([0.3, 0.2, 0.4])
    # rotate the camera view transform
    camera_old, _geometry = scene.graph[scene.camera.name]
    camera_new = np.dot(rotate1, camera_old)
    camera_new = np.dot(rotate2, camera_new)
    camera_new = np.dot(translate_back, camera_new)
    # apply the new transform
    scene.graph[scene.camera.name] = camera_new

    # saving an image requires an opengl context, so if -nw
    # is passed don't save the image
    # increment the file name
    # save a render of the object as a png
    # png = scene.save_image(resolution=[1920, 1080], visible=False)  # [1920, 1080]
    png = scene.save_image(resolution=[500, 500], visible=False)  # [1920, 1080]
    # if title is None:
    #     with open(saved_path, "wb") as f:
    #         f.write(png)
    #         f.close()
    # title
    # if title is not None:
        # Convert the PNG image to a format matplotlib can use
    with Image.open(BytesIO(png)) as image:
        # Plot the image with matplotlib and add title
        plt.figure(figsize=(10, 10), dpi=50)
        plt.imshow(image)
        plt.axis('off')  # Hide the axes
        plt.title(title, fontsize=18)  # Add the title
        plt.savefig(saved_path, bbox_inches='tight')  # Save the image with title
        plt.close()
        # plt.show()  # Display the image with the title
    return camera_new


def normalize_trimesh(mesh):
    # 获取包围盒的最小值和最大值
    bbox_min, bbox_max = mesh.bounds
    
    # 计算包围盒每个轴的尺寸 (x, y, z)
    scale = bbox_max - bbox_min
    
    # 找到最大的轴大小
    max_scale = max(scale)
    
    # 将顶点按最大轴大小缩放，使得最大轴范围变为 [0, 1]
    mesh.vertices -= bbox_min  # 将模型的所有顶点移动到原点 (0,0,0)
    mesh.vertices /= max_scale  # 缩放所有顶点
    
    return mesh

