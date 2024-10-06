import sys
sys.path.append('./')
import bpy

from options import Options
from load_bvh import load_bvh
from scene import make_scene, add_material_for_character, add_rendering_parameters

from load_sites import load_and_animate_sites

if __name__ == '__main__':
    args = Options(sys.argv).parse()

    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    character, normalization_factor = load_bvh(args.bvh_path)

    print(normalization_factor)
    scene = make_scene()
    add_material_for_character(character)
    bpy.ops.object.select_all(action='DESELECT')

    load_and_animate_sites(args.site_locations_path, normalization_factor)

    add_rendering_parameters(bpy.context.scene, args, scene[1])

    if args.render:
        bpy.ops.render.render(animation=True, use_viewport=True)
