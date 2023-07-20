import numpy as np
import math
import json
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="read eular export to nerf format transforms.json")
    parser.add_argument("--csv", default="/volume/data/nerf/multiview_img/ta/registration/20210514-AITOMINAGA-FACE-MLT-003-RC.csv", help="csv path.")
    parser.add_argument("--out", default="transforms.json", help="Output path.")
    args = parser.parse_args()
    return args

def rotation_matrix(roll, pitch, yaw, tx, ty, tz):
    # オイラー角をラジアンに変換
    roll_rad = math.radians(roll)
    pitch_rad = math.radians(pitch)
    yaw_rad = math.radians(yaw)

    # 回転行列の計算
    R_x = np.array([[1, 0, 0, 0],
                    [0, math.cos(roll_rad), -math.sin(roll_rad), 0],
                    [0, math.sin(roll_rad), math.cos(roll_rad), 0],
                    [0, 0, 0, 1]])

    R_y = np.array([[math.cos(pitch_rad), 0, math.sin(pitch_rad), 0],
                    [0, 1, 0, 0],
                    [-math.sin(pitch_rad), 0, math.cos(pitch_rad), 0],
                    [0, 0, 0, 1]])

    R_z = np.array([[math.cos(yaw_rad), -math.sin(yaw_rad), 0, 0],
                    [math.sin(yaw_rad), math.cos(yaw_rad), 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]])

    # 並進移動量の行列
    T = np.array([[1, 0, 0, tx],
                  [0, 1, 0, ty],
                  [0, 0, 1, tz],
                  [0, 0, 0, 1]])

    # 回転行列と並進移動量の行列を掛け合わせる
    R = np.dot(np.dot(R_z, R_y), R_x)
    result = np.dot(R, T)

    return result




def get_transform_json(OUT_PATH, csv, camera)
    print(f"outputting to {OUT_PATH}...")
    cameras = {}
    i = 0
    bottom = np.array([0.0, 0.0, 0.0, 1.0]).reshape([1, 4])
    out = {
        "camera_angle_x": camera["camera_angle_x"],
        "camera_angle_y": camera["camera_angle_y"],
        "fl_x": camera["fl_x"],
        "fl_y": camera["fl_y"],
        "k1": camera["k1"],
        "k2": camera["k2"],
        "k3": camera["k3"],
        "k4": camera["k4"],
        "p1": camera["p1"],
        "p2": camera["p2"],
        "is_fisheye": camera["is_fisheye"],
        "cx": camera["cx"],
        "cy": camera["cy"],
        "w": camera["w"],
        "h": camera["h"],
        "aabb_scale": AABB_SCALE,
        "frames": [],
    }

    up = np.zeros(3)
    with open(csv), "r") as f:
        for line in f:
            line = line.strip()
            if line[0] == "#":
                continue
            i = i + 1
            if  i % 2 == 1:
                elems=line.split(" ") # 1-4 is quat, 5-7 is trans, 9ff is filename (9, if filename contains no spaces)
                #name = str(PurePosixPath(Path(IMAGE_FOLDER, elems[9])))
                # why is this requireing a relitive path while using ^
                image_rel = os.path.relpath(IMAGE_FOLDER)
                name = str(f"./{image_rel}/{'_'.join(elems[9:])}")
                b = sharpness(name)
                print(name, "sharpness=",b)
                image_id = int(elems[0])
                qvec = np.array(tuple(map(float, elems[1:5])))
                tvec = np.array(tuple(map(float, elems[5:8])))
                R = qvec2rotmat(-qvec)
                t = tvec.reshape([3,1])
                m = np.concatenate([np.concatenate([R, t], 1), bottom], 0)
                c2w = np.linalg.inv(m)
                if not args.keep_colmap_coords:
                    c2w[0:3,2] *= -1 # flip the y and z axis
                    c2w[0:3,1] *= -1
                    c2w = c2w[[1,0,2,3],:]
                    c2w[2,:] *= -1 # flip whole world upside down

                    up += c2w[0:3,1]

                frame = {"file_path":name,"sharpness":b,"transform_matrix": c2w}
                if len(cameras) != 1:
                    frame.update(cameras[int(elems[8])])
                out["frames"].append(frame)
            nframes = len(out["frames"])

            if args.keep_colmap_coords:
                flip_mat = np.array([
                    [1, 0, 0, 0],
                    [0, -1, 0, 0],
                    [0, 0, -1, 0],
                    [0, 0, 0, 1]
                ])

                for f in out["frames"]:
                    f["transform_matrix"] = np.matmul(f["transform_matrix"], flip_mat) # flip cameras (it just works)
            else:
                # don't keep colmap coords - reorient the scene to be easier to work with

                up = up / np.linalg.norm(up)
                print("up vector was", up)
                R = rotmat(up,[0,0,1]) # rotate up vector to [0,0,1]
                R = np.pad(R,[0,1])
                R[-1, -1] = 1

                for f in out["frames"]:
                    f["transform_matrix"] = np.matmul(R, f["transform_matrix"]) # rotate up to be the z axis

                # find a central point they are all looking at
                print("computing center of attention...")
                totw = 0.0
                totp = np.array([0.0, 0.0, 0.0])
                for f in out["frames"]:
                    mf = f["transform_matrix"][0:3,:]
                    for g in out["frames"]:
                        mg = g["transform_matrix"][0:3,:]
                        p, w = closest_point_2_lines(mf[:,3], mf[:,2], mg[:,3], mg[:,2])
                        if w > 0.00001:
                            totp += p*w
                            totw += w
                if totw > 0.0:
                    totp /= totw
                print(totp) # the cameras are looking at totp
                for f in out["frames"]:
                    f["transform_matrix"][0:3,3] -= totp

                avglen = 0.
                for f in out["frames"]:
                    avglen += np.linalg.norm(f["transform_matrix"][0:3,3])
                avglen /= nframes
                print("avg camera distance from origin", avglen)
                for f in out["frames"]:
                    f["transform_matrix"][0:3,3] *= 4.0 / avglen # scale to "nerf sized"

            for f in out["frames"]:
                f["transform_matrix"] = f["transform_matrix"].tolist()
            print(nframes,"frames")
            print(f"writing {OUT_PATH}")
            with open(OUT_PATH, "w") as outfile:
                json.dump(out, outfile, indent=2)
        
if __name__ == "__main__":
    args = parse_args()
    camera={
        "camera_angle_x": 0.7481849417937728,
        "camera_angle_y": 1.2193576119562444,
        "fl_x": 2164.43,
        "fl_y": 2164.43,
        "k1": 0.0578421,
        "k2": -0.0805099,
        "p1": -0.000980296,
        "p2": 0.00015575,
        "cx": 2000.0#2652.0,
        "cy": 3000.0#3976.0,
        "w": 4000.0#5304.0,
        "h": 6000.0#7952.0,
        "aabb_scale": 4}

    # 例: オイラー角 (30, 45, 60) と並進移動量 (1, 2, 3) を4x4の回転行列に変換
    roll, pitch, yaw = 30, 45, 60
    tx, ty, tz = 1, 2, 3
    result_matrix = rotation_matrix(roll, pitch, yaw, tx, ty, tz)
    print(result_matrix)