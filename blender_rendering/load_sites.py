import json
import bpy
import mathutils
import numpy as np

# Load the sphere positions from a JSON file
def load_sites(json_file_path):
    with open(json_file_path, 'r') as f:
        data = json.load(f)

    raw_positions = np.asarray(data['positions'])

    positions = np.zeros_like(raw_positions)

    positions[:,:,0] = raw_positions[:,:,2]
    positions[:,:,1] = raw_positions[:,:,0]
    positions[:,:,2] = raw_positions[:,:,1]
    
    return positions, data['frame_num']

# Create 4 spheres in Blender and return them as objects
def create_spheres():
    spheres = []
    for i in range(4):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.1, enter_editmode=False, location=(0, 0, 0))
        sphere = bpy.context.object
        sphere.name = f'Sphere_{i+1}'
        spheres.append(sphere)
    return spheres

# Animate the spheres' locations based on the JSON file data
def animate_spheres(spheres, positions, frame_num):
    bpy.context.scene.frame_start = 0
    bpy.context.scene.frame_end = frame_num - 1
    
    for frame in range(frame_num):
        for i, sphere in enumerate(spheres):
            loc = positions[frame][i]
            sphere.location = mathutils.Vector((loc[0], loc[1], loc[2]))
            sphere.keyframe_insert(data_path='location', frame=frame)

    bpy.context.scene.frame_current = 0

def load_and_animate_sites(json_file_path, normalization_factor):
    positions, frame_num = load_sites(json_file_path)
    positions /= normalization_factor
    positions[:,:,2] += 6.5
    spheres = create_spheres()
    animate_spheres(spheres, positions, frame_num)