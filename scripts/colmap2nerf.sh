#!/bin/bash

DIR_OUT="/volume/data/nerf/multiview_img/ta/neutral/jpg/"
AABB_SCALE=4
OUT_JSON=/volume/data/nerf/multiview_img/ta/colmap_pose/transforms.json

python3 ./colmap2nerf.py --colmap_matcher exhaustive --run_colmap --aabb_scale $AABB_SCALE \
  --images ${DIR_OUT} \
  --out ${OUT_JSON}
#   --images /volume/data/nerf/multiview_img/ta/neutral/tif/ \
#   --out /volume/data/nerf/multiview_img/ta/registration/