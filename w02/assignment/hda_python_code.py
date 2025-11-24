import hou
import math
import sys
import random

sys.path.append(r"E:\repos\rebelway-applied-ml\w02\a_star\scripts")

from a_star import AStarPathFinding

def _get_maze_from_grid(node):
    grid = node.parm('grid_path').eval()
    geo = hou.node(grid).geometry()    
    prims = geo.prims()    
    num_rows = num_cols = int(math.sqrt(len(prims)))    
    grid_matrix = []
    
    for row in range(num_rows):
        new_row = []
        for col in range(num_cols):
            prim_index = (row * num_cols) + col
            prim = geo.prim(prim_index)
            color = prim.attribValue("Cd")
            new_row.append(1 if color == (1.0, 1.0, 1.0) else 0)
        grid_matrix.append(new_row)
    
    return grid_matrix
    
    
def _position_object(obj_path, row, col):
    main_char = hou.node(obj_path)
    main_char_geo = main_char.geometry()
    
    grid_case_length = main_char_geo.attribValue("grid_case_length")
    world_x = (col * grid_case_length) + (grid_case_length / 2)
    world_z = (row * grid_case_length) + (grid_case_length / 2)
    
    main_char.parmTuple("t").set((world_x, 0, world_z))
    pos = (row, col)
    return pos
    
def _get_path_cache(node, key="maze_path_cache"):
    cache = node.cachedUserData(key)
    if cache is None:
        cache = {}
    return cache
    
def _set_path_cache(node, cache, key="maze_path_cache"):
    node.setCachedUserData(key, cache)
    
def reset_maze(hda_node=None):
    if hda_node is None:
        hda_node = hou.pwd()
    node = hda_node
    node.setCachedUserData("maze_path_cache", None)
    hou.setFrame(1)
    solve_maze(node)
    
def solve_maze(hda_node=None):
    
    if hda_node is None:
        hda_node = hou.pwd()    
    node = hda_node

    main_char_path = node.parm("main_char").eval()
    maze = _get_maze_from_grid(node)
    
    # Collect all walkable maze cells for random NPC start
    walkable_positions = [
        (row_idx, col_idx)
        for row_idx, row in enumerate(maze)
        for col_idx, v in enumerate(row)
        if v == 1
    ]

    # Cache
    path_cache = _get_path_cache(node)

    # Current frame
    frame = int(hou.frame())
    if frame < 1:
        frame = 1

    # Target maze cell for the main character (always 6,1)
    target_row, target_col = 6, 1
    target_pos = (target_row, target_col)

    # Place main character at (6,1)
    _position_object(main_char_path, target_row, target_col)

    # Number of NPC instances in multiparm
    npc_count = node.evalParm("npcs")

    for i in range(1, npc_count + 1):
        npc_parm_name = f"npc_{i}"
        
        npc_parm = node.parm(npc_parm_name)
        if npc_parm is None:
            continue

        npc_obj_path = npc_parm.eval().strip()
        if not npc_obj_path:
            continue

        npc_cache = path_cache.get(npc_parm_name)

        if npc_cache is None:
            # without cache, or after reset at frame 1
            if walkable_positions:
                start_row, start_col = random.choice(walkable_positions)
            else:
                # if no walkable cells
                start_row, start_col = 0, 0

            start_pos = (start_row, start_col)

            # Compute path to the main character
            pf = AStarPathFinding(maze, start_pos, target_pos)
            path = pf.find_path()

            #if path:
            #    print(f"path found for {npc_parm_name} (start {start_pos} -> {target_pos}): {path}")
            #else:
            #    print(f"no path found for {npc_parm_name} from {start_pos} to {target_pos}")
            #    path = []

            # cache calculated path
            npc_cache = {
                "start": start_pos,
                "target": target_pos,
                "path": path,
            }
            path_cache[npc_parm_name] = npc_cache
        else:
            path = npc_cache.get("path", [])
            start_pos = npc_cache.get("start", (0, 0))

        # Calculate NPC position at frame N
        if path:
            idx = frame - 1
            if idx >= len(path):
                idx = len(path) - 1
            row, col = path[idx]
        else:
            row, col = start_pos

        # Place NPC object
        _position_object(npc_obj_path, row, col)

    # Save cache back on the node
    _set_path_cache(node, path_cache)