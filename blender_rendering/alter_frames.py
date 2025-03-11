import json
import bpy

def alter_not_still_frames(not_still_frames_path: str):
    """
    Reads a JSON file that has the following fields:
        {
          "not_still_frames": [3, 4, 5, 12, 123],
          "frame_num": <integer>,
          "time_effort": <float from 0 to 2.0>
        }

    For each frame f in not_still_frames, scale the time gap between f-1 and f 
    by 'time_effort'. This example code shifts all subsequent keyframes 
    cumulatively in the scene so that the motion curves are stretched/compressed.
    """

    # 1) Read the JSON file
    with open(not_still_frames_path, 'r') as f:
        data = json.load(f)

    frames_to_alter = data["not_still_frames"]
    time_effort = data["time_effort"]

    # If needed, ensure the frames are in ascending order
    frames_to_alter = sorted(frames_to_alter)

    # We'll track how much we've cumulatively shifted things in the timeline
    shift_cumulative = 0.0

    # 2) Go through each frame in ascending order
    for f_index in frames_to_alter:
        # The "old" frame location in the timeline is f_index + shift_cumulative
        old_frame = f_index + shift_cumulative

        # We want the new frame to be (f_index - 1) + shift_cumulative + time_effort
        new_frame = (f_index - 1) + shift_cumulative + time_effort

        # The difference
        shift_amount = new_frame - old_frame
        if abs(shift_amount) < 1e-8:
            continue

        # 3) Shift all keyframes >= old_frame by shift_amount
        for obj in bpy.data.objects:
            anim_data = obj.animation_data
            if not anim_data:
                continue

            action = anim_data.action
            if not action:
                continue

            for fcurve in action.fcurves:
                for kp in fcurve.keyframe_points:
                    # kp.co[0] is the frame/time of the keyframe
                    frame_time = kp.co[0]

                    # If this key is on or after old_frame, shift it
                    if frame_time >= old_frame - 0.0001:  # small epsilon
                        kp.co[0] += shift_amount
                        kp.handle_left[0] += shift_amount
                        kp.handle_right[0] += shift_amount

        # 4) Accumulate the shift so that subsequent frames are shifted further
        shift_cumulative += shift_amount

    # 5) Adjust scene end frame if needed (optional)
    bpy.context.scene.frame_end = int(bpy.context.scene.frame_end + shift_cumulative)

    # Optionally re-set the current frame to 0 so we can see the initial pose
    bpy.context.scene.frame_set(0)
