#!/bin/bash

# ディレクトリと拡張子を指定
DIR_IN="/volume/data/nerf/multiview_img/ta/neutral/tif/"
EXT=".tif"
DIR_OUT="/volume/data/nerf/multiview_img/ta/neutral/bin/"
AABB_SCALE=4
DIR_OUT_COL=/volume/data/nerf/multiview_img/ta/colmap_pose/


# 指定したディレクトリ内の特定の拡張子を持つファイルを配列に格納
files=( "${DIR_IN}"*"${EXT}" )

# 配列内のファイル名を変数に代入して表示
for file in "${files[@]}"; do
  # ファイル名（拡張子なし）を取得
  file_name=$(basename "${file}" ${EXT})
  output=${DIR_OUT}${file_name}".bin"
  echo "input: ${file}"
  echo "output: ${output}"

  # Check if the file exists
  if [ -f ${file} ]; then
    python3 scripts/convert_image.py \
      --input ${file} \
      --output ${output} \
      --resize_h 6000 --resize_w 4000
      
  else
    echo "not found: ${file}"
  fi
done



python3 scripts/colmap2nerf.py --colmap_matcher exhaustive --run_colmap --aabb_scale $AABB_SCALE \
  --images ${DIR_OUT} \
  --out ${DIR_OUT_COL}
#   --images /volume/data/nerf/multiview_img/ta/neutral/tif/ \
#   --out /volume/data/nerf/multiview_img/ta/registration/