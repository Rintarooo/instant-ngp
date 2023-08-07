from PIL import Image
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Convert image into a different format. By default, converts to our binary fp16 '.bin' format, which helps quickly load large images.")
    parser.add_argument("--input", default="", help="Path to the image to convert.")
    parser.add_argument("--output", default="", help="Path to the output. Defaults to <input>.bin")
    parser.add_argument("--resize_h", default=6000, type=int, help="resize image uniformaly. Defaults: --resize_h 6000")
    parser.add_argument("--resize_w", default=4000, type=int, help="resize image uniformaly. Defaults: --resize_w 4000")
    parser.add_argument("--bits", default=8, type=int, help="bits: 8 or 16bit for png file. Defaults: --bits 8")
    parser.add_argument("--ext", default="JPG", type=str, help="PNG or JPG or JPEG. Defaults: --bits JPG")
    args = parser.parse_args()
    return args

def convert_tif_to_png(tif_path, png_path, bits, ext):
    with Image.open(tif_path) as img:
        print(f"tif_path: {tif_path}")
        print(f"width: {img.size[0]}, height: {img.size[1]} pixels")
        # if img.size[0]==4000 and img.size[1]==6000:
        if img.size[0]==5304 and img.size[1]==7952:
            print(f"png_path: {png_path}")
            img.save(png_path, "PNG", bits=bits)

        # # リサイズするサイズを指定 (幅, 高さ)
        # new_size = (args.resize_w, args.resize_h)
        # # 画像をリサイズ
        # img = img.resize(new_size, Image.LANCZOS)
        # print(f"resize to width: {img.size[0]}, height: {img.size[1]} pixels")
        # print(f"save bits: {bits}")
        # img.save(png_path, "PNG", bits=bits)
        

if __name__ == "__main__":
    args = parse_args()
    Image.MAX_IMAGE_PIXELS = 10000000000
    # tif_file_path = "/volume/data/nerf/multiview_img/ta/neutral/tif/00_A_3282930003040541_.tif"
    # png_file_path = "/volume/data/nerf/multiview_img/ta/neutral/png/00_A_3282930003040541_.png"
    # bits = 16
    convert_tif_to_png(args.input, args.output, args.bits, args.ext)