#!/bin/bash

DIR_IMG="/volume/data/nerf/multiview_img/ta/5_91/jpg_w5h8/imgs/"
# "/volume/data/nerf/multiview_img/ta/neutral/jpg/"
AABB_SCALE=8
# 4
OUT_JSON="/volume/data/nerf/multiview_img/ta/5_91/jpg_w5h8/json/transforms.json"
# /volume/data/nerf/multiview_img/ta/colmap_pose/transforms.json
MASK_CATEGORY="person"
COLMAP_DB="/volume/data/nerf/multiview_img/ta/5_91/jpg_w5h8/colmap/colmap.db"
OUT_TEXT="/volume/data/nerf/multiview_img/ta/5_91/jpg_w5h8/colmap/colmap_text"

python3 ./colmap2nerf.py --colmap_matcher exhaustive --run_colmap --aabb_scale $AABB_SCALE \
  --images ${DIR_IMG} \
  --text ${OUT_TEXT} \
  --out ${OUT_JSON} \
  --mask_categories ${MASK_CATEGORY} \
  --colmap_db ${COLMAP_DB}

#   --images /volume/data/nerf/multiview_img/ta/neutral/tif/ \
#   --out /volume/data/nerf/multiview_img/ta/registration/