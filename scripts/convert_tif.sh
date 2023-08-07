#!/bin/bash

# ディレクトリと拡張子を指定
DIR_IN="/volume/data/nerf/multiview_img/ta/5_91/tif/"
# "/volume/data/nerf/multiview_img/ta/5_91/tif/"
EXT_IN=".tif"
DIR_OUT="/volume/data/nerf/multiview_img/ta/5_91/jpg_w5h8/"
# "/volume/data/nerf/multiview_img/ta/5_91/jpg/"
# "/volume/data/nerf/multiview_img/ta/neutral/jpg/"
# "/volume/data/nerf/multiview_img/ta/neutral/png/"
# "/volume/data/nerf/multiview_img/ta/neutral/bin/"
EXT_OUT=".jpg"
# ".png"
EXT="JPG"
# "PNG"
BITS=8
# ".bin"
RESIZE_H="6000"
RESIZE_W="4000"


# ディレクトリが存在しない場合に作成
if [ ! -d "$DIR_OUT" ]; then
  mkdir -p "$DIR_OUT"
  echo "made dir: $DIR_OUT"
else
  echo "this dir already exists: $DIR_OUT"
fi

# 指定したディレクトリ内の特定の拡張子を持つファイルを配列に格納
files=( "${DIR_IN}"*"${EXT_IN}" )
# files=( "${DIR_IN}"00_A_3282930003040541_"${EXT_IN}" )

# 配列内のファイル名を変数に代入して表示
for file in "${files[@]}"; do
  # ディレクトリ名を除いたファイル名（拡張子なし）を取得
  file_name=$(basename "${file}" ${EXT_IN})
  output=${DIR_OUT}${file_name}${EXT_OUT}
  echo "input: ${file}"
  echo "output: ${output}"

  # Check if the file exists
  if [ -f ${file} ]; then
    python3 convert_tif.py \
      --input ${file} \
      --output ${output} \
      --resize_h ${RESIZE_H} --resize_w ${RESIZE_W} \
      --bits ${BITS} --ext ${EXT}
    # python3 ./convert_image.py \
    #   --input ${file} \
    #   --output ${output} \
    #   --resize_h ${RESIZE_H} --resize_w ${RESIZE_W}
  else
    echo "not found: ${file}"
  fi
done