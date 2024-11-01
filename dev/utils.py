import os
import sys
sys.path.append('/home/leech/3d/code/PartRules')

import trimesh
import numpy as np
import matplotlib.pyplot as plt

from PIL import Image
from io import BytesIO



def load_trimesh_mesh(mesh_file):
    mesh = trimesh.load(mesh_file, process=False)
    return trimesh.util.concatenate(mesh)



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
    bbox_min, bbox_max = mesh.bounds
    scale = bbox_max - bbox_min
    max_scale = max(scale)
    mesh.vertices -= bbox_min 
    mesh.vertices /= max_scale  
    return mesh

