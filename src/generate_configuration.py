import json


pi = 3.14159
d2r = pi / 180
r2d = 180 / pi

shape_config = {

    'ENGINE': 'solid', # 'solid' = solid python / OpenSCAD, 'cadquery' = cadquery / OpenCascade
    # 'ENGINE':  'cadquery', # 'solid' = solid python / OpenSCAD, 'cadquery' = cadquery / OpenCascade


    ######################
    ## Shape parameters ##
    ######################

    'save_dir': '.',
    'config_name':  "DM",

    'show_caps':  False,

    'nrows':  5, #5,  # key rows
    'ncols':  6, #6,  # key columns

    'alpha':  pi / 12.0,  # curvature of the columns
    'beta':  pi / 36.0,  # curvature of the rows
    'centercol':  3,  # controls left_right tilt / tenting (higher number is more tenting)
    'centerrow_offset':  3,  # rows from max, controls front_back tilt
    'tenting_angle':  pi / 12.0,  # or, change this for more precise tenting control

    # symmetry states if it is a symmetric or asymmetric build.  If asymmetric it doubles the generation time.
    'symmetry':  "symmetric",  # "asymmetric" or "symmetric"

    'column_style_gt5':  "orthographic",
    'column_style':  "standard",  # options include :standard, :orthographic, and :fixed

    'thumb_offsets':  [6, -3, 7],
    'keyboard_z_offset':  (
        13  # controls overall height# original=9 with centercol=3# use 16 for centercol=2
    ),

    'thumb_style': 'MINI',  # 'DEFAULT', 'MINI', 'CARBONFET'

    ##############################
    # EXPERIMENTAL PARAMETERS
    ##############################
    'pinky_1_5U': False,  # LEAVE AS FALSE, CURRENTLY BROKEN
    'first_1_5U_row': 0,
    'last_1_5U_row': 5,
    ##############################


    'extra_width':  2.5,  # extra space between the base of keys# original= 2
    'extra_height':  1.0,  # original= 0.5

    'wall_z_offset':  15,  # length of the first downward_sloping part of the wall
    'wall_x_offset':  5,  # offset in the x and/or y direction for the first downward_sloping part of the wall (negative)
    'wall_y_offset':  6,  # offset in the x and/or y direction for the first downward_sloping part of the wall (negative)
    'left_wall_x_offset':  12,  # specific values for the left side due to the minimal wall.
    'left_wall_z_offset':  3,  # specific values for the left side due to the minimal wall.
    'wall_thickness':  4.5,  # wall thickness parameter used on upper/mid stage of the wall
    'wall_base_y_thickness':  4.5,  # wall thickness at the lower stage
    'wall_base_x_thickness':  4.5,  # wall thickness at the lower stage

    'wall_base_back_thickness':  4.5,  # wall thickness at the lower stage in the specifically in back for interface.

    ## Settings for column_style == :fixed
    ## The defaults roughly match Maltron settings
    ##   http://patentimages.storage.googleapis.com/EP0219944A2/imgf0002.png
    ## fixed_z overrides the z portion of the column ofsets above.
    ## NOTE: THIS DOESN'T WORK QUITE LIKE I'D HOPED.
    'fixed_angles':  [d2r * 10, d2r * 10, 0, 0, 0, d2r * -15, d2r * -15],
    'fixed_x':  [-41.5, -22.5, 0, 20.3, 41.4, 65.5, 89.6],  # relative to the middle finger
    'fixed_z':  [12.1, 8.3, 0, 5, 10.7, 14.5, 17.5],
    'fixed_tenting':  d2r * 0,

    #################
    ## Switch Hole ##
    #################

    # plate options are
    # 'HOLE' = a square hole.  Also useful for applying custom plate files.
    # 'NUB' = original side nubs.
    # 'UNDERCUT' = snap fit undercut.  May require CLIP_THICKNESS and possibly CLIP_UNDERCUT tweaking
    #       and/or filing to get proper snap.
    # 'NOTCH' = snap fit undercut only near switch clip.  May require CLIP_THICKNESS and possibly CLIP_UNDERCUT
    #       tweaking and/or filing to get proper snap.
    # 'HS_NUB' = hot swap underside with nubs.
    # 'HS_UNDERCUT' = hot swap underside with undercut. Does not generate properly.  Hot swap step needs to be modified.
    # 'HS_NOTCH' = hot swap underside with notch.  Does not generate properly.  Hot swap step needs to be modified.
    'plate_style':  'NOTCH',

    'hole_keyswitch_height':  14.0,
    'hole_keyswitch_width':  14.0,

    'nub_keyswitch_height':  14.4,
    'nub_keyswitch_width':  14.4,

    'undercut_keyswitch_height':  14.0,
    'undercut_keyswitch_width':  14.0,
    'notch_width': 5.0, # If using notch, it is identical to undecut, but only locally by the switch clip

    'sa_profile_key_height':  12.7,
    'plate_thickness':  4+1.1,

    'plate_rim': 1.5 + 0.5,
    # Undercut style dimensions
    'clip_thickness':  1.4,
    'clip_undercut':  1.0,
    'undercut_transition':  .2,  # NOT FUNCTIONAL WITH OPENSCAD, ONLY WORKS WITH CADQUERY

    # Custom plate step file
    'plate_file':  None,
    'plate_offset':  0.0,

    ##########################
    ## OLED Mount Location
    ##########################
    # Initial pass will be manual placement.  Can be used to create other mounts as well.
    # Mount type options:
    # None or 'NONE' = No OLED mount
    # 'UNDERCUT' = Simple rectangle with undercut for clip in item
    # 'SLIDING' = Features to slide the OLED in place and use a pin or block to secure from underneath.
    # 'CLIP' = Features to set the OLED in a frame a snap a bezel down to hold it in place.

    'oled_mount_type':  None,
    'oled_center_row': 1.5, # if not None, this will override the oled_mount_location_xyz and oled_mount_rotation_xyz settings
    'oled_translation_offset': (0, 0, 4), # Z offset tweaks are expected depending on curvature and OLED mount choice.
    'oled_rotation_offset': (0, 0, 0),

    'oled_configurations': {
        'UNDERCUT':{
            # Common parameters
            'oled_mount_width': 15.0,
            'oled_mount_height': 35.0,
            'oled_mount_rim': 3.0,
            'oled_mount_depth': 6.0,
            'oled_mount_cut_depth': 20.0,
            'oled_mount_location_xyz': (-80.0, 20.0, 45.0), # will be overwritten if oled_center_row is not None
            'oled_mount_rotation_xyz': (13.0, 0.0, -6.0), # will be overwritten if oled_center_row is not None
            'oled_left_wall_x_offset_override': 28.0,
            'oled_left_wall_z_offset_override': 0.0,

            # 'UNDERCUT' Parameters
            'oled_mount_undercut': 1.0,
            'oled_mount_undercut_thickness': 2.0,
        },
        'SLIDING': {
            # Common parameters
            'oled_mount_width': 12.5,  # width of OLED, plus clearance
            'oled_mount_height': 25.0,  # length of screen
            'oled_mount_rim': 2.5,
            'oled_mount_depth': 8.0,
            'oled_mount_cut_depth': 20.0,
            'oled_mount_location_xyz': (-78.0, 10.0, 41.0), # will be overwritten if oled_center_row is not None
            'oled_mount_rotation_xyz': (6.0, 0.0, -3.0), # will be overwritten if oled_center_row is not None
            'oled_left_wall_x_offset_override': 24.0,
            'oled_left_wall_z_offset_override': 0.0,

            # 'SLIDING' Parameters
            'oled_thickness': 4.2,  # thickness of OLED, plus clearance.  Must include components
            'oled_edge_overlap_end': 6.5,  # length from end of viewable screen to end of PCB
            'oled_edge_overlap_connector': 5.5,  # length from end of viewable screen to end of PCB on connection side.
            'oled_edge_overlap_thickness': 2.5,  # thickness of material over edge of PCB
            'oled_edge_overlap_clearance': 2.5,  # Clearance to insert PCB before laying down and sliding.
            'oled_edge_chamfer': 2.0,
        },
        'CLIP': {
            # Common parameters
            'oled_mount_width': 12.5,  # whole OLED width
            'oled_mount_height': 39.0,  # whole OLED length
            'oled_mount_rim': 2.0,
            'oled_mount_depth': 7.0,
            'oled_mount_cut_depth': 20.0,
            'oled_mount_location_xyz': (-78.0, 20.0, 42.0), # will be overwritten if oled_center_row is not None
            'oled_mount_rotation_xyz': (12.0, 0.0, -6.0), # will be overwritten if oled_center_row is not None
            'oled_left_wall_x_offset_override': 24.0,
            'oled_left_wall_z_offset_override': 0.0,

            # 'CLIP' Parameters
            'oled_thickness': 4.2,  # thickness of OLED, plus clearance.  Must include components
            'oled_mount_bezel_thickness': 3.5,  # z thickness of clip bezel
            'oled_mount_bezel_chamfer': 2.0,  # depth of the 45 degree chamfer
            'oled_mount_connector_hole': 6.0,
            'oled_screen_start_from_conn_end': 6.5,
            'oled_screen_length': 24.5,
            'oled_screen_width': 10.5,
            'oled_clip_thickness': 1.5,
            'oled_clip_width': 6.0,
            'oled_clip_overhang': 1.0,
            'oled_clip_extension': 5.0,
            'oled_clip_width_clearance': 0.5,
            'oled_clip_undercut': 0.5,
            'oled_clip_undercut_thickness': 2.5,
            'oled_clip_y_gap': .2,
            'oled_clip_z_gap': .2,
        }
    },
    'web_thickness':  4.0,
    'post_size':  0.1,
    # post_adj':  post_size / 2
    'post_adj':  0,
    'screws_offset': 'INSIDE', #'OUTSIDE', 'INSIDE', 'ORIGINAL'

    ###################################
    ## Controller Mount / Connectors ##
    ###################################
    # connector options are
    # 'RJ9_USB_WALL' = Standard internal plate with RJ9 opening and square cutout for connection.
    # 'USB_WALL' = Standard internal plate with a square cutout for connection, no RJ9.
    # 'RJ9_USB_TEENSY' = Teensy holder
    # 'USB_TEENSY' = Teensy holder, no RJ9
    # 'EXTERNAL' = square cutout for a holder such as the one from lolligagger.
    # 'NONE' = No openings in the back.
    'controller_mount_type':  'PCB_MOUNT',

    'external_holder_height':  12.5,
    'external_holder_width':  28.75,
    'external_holder_xoffset': -5.0,

    ###################################
    ## PCB Screw Mount               ##
    ###################################
    "pcb_mount_ref_offset": [1, -5, 0],
    "pcb_holder_size": [34.6, 0, 3],
    "pcb_holder_offset": [9.9, 3, 0],

    "pcb_usb_hole_size": [9.3, 10.0, 4.5],
    "pcb_usb_hole_offset": [16, 0, 4.5],
    "pcb_usb_hole_z_offset": 2.5,

    "wall_thinner_size": [33, 5, 10],

    "trrs_hole_size": [3, 20],
    #right
    #"trrs_offset": [2, 0, 7],
    #left
    "trrs_offset": [0, 0, 7],

    "pcb_screw_hole_size": [.7, 10],
    "pcb_screw_x_offsets": [- 4.5, 8.75, 23], # for the screw positions off of reference
    "pcb_screw_y_offset": 1,

    # Offset is from the top inner corner of the top inner key.

    ###################################
    ## Bottom Plate Dimensions
    ###################################
    # COMMON DIMENSION
    'screw_hole_diameter': 2,
    # USED FOR CADQUERY ONLY
    'base_thickness': 3.0, # thickness in the middle of the plate
    'base_offset': 3.0, # Both start flat/flush on the bottom.  This offsets the base up (if positive)
    'base_rim_thickness': 5.0,  # thickness on the outer frame with screws
    'screw_cbore_diameter': 4.0,
    'screw_cbore_depth': 2.0,

    # Offset is from the top inner corner of the top inner key.

    ###################################
    ## EXPERIMENTAL
    ###################################
    'plate_holes':  True,
    'plate_holes_xy_offset': (0.0, 0.0),
    'plate_holes_width': 14.3,
    'plate_holes_height': 14.3,
    'plate_holes_diameter': 1.3,
    'plate_holes_depth': 20.0,

    ###################################
    ## COLUMN OFFSETS
    ####################################

    'column_offsets':  [
        [0, 0, 0],
        [0, 0, 0],
        [0, 2.82, -4.5],
        [0, 0, 0],
        [0, -6, 5],# REDUCED STAGGER
        [0, -6, 5],# REDUCED STAGGER
        [0, -6, 5],# NOT USED IN MOST FORMATS (7th column)
    ],

}

    ####################################
    ## END CONFIGURATION SECTION
    ####################################

def save_config():
    with open('run_config.json', mode='w') as fid:
        json.dump(shape_config, fid, indent=4)

def update_config(fname, fname_out=None):
    if fname_out is None:
        fname_out == "updated_config.json"
    # Open existing config, update with any new parameters, and save to updated_config.json
    with open(fname, mode='r') as fid:
        last_shape_config = json.load(fid)
    shape_config.update(last_shape_config)

    with open(fname_out, mode='w') as fid:
        json.dump(shape_config, fid, indent=4)


if __name__ == '__main__':
    save_config()
    from dactyl_manuform import *
    run()
