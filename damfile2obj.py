import numpy as np

import damfile_pb2 as damfile


def write_mtl_file(root, mtl_file):
    material_names = sorted(set(chunk.material_name for chunk in root.chunks))
    for material_name in material_names:
        mtl_file.write(f"newmtl {material_name}\n")
        mtl_file.write(f"map_Ka {material_name}\n")
        mtl_file.write(f"map_Kd {material_name}\n\n")


def write_obj_vertices(root, obj_file):
    chunk_vert_sizes = []
    for chunk_id, chunk in enumerate(root.chunks):
        xyz = np.array(chunk.vertices.xyz).reshape(-1, 3)
        for x, y, z in xyz:
            obj_file.write(f"v {x} {y} {z}\n")

        chunk_vert_sizes.append(len(xyz))

    obj_file.write("\n")

    return chunk_vert_sizes


def write_obj_uv(root, obj_file):
    for chunk in root.chunks:
        uv = np.array(chunk.vertices.uv).reshape(-1, 2)
        for u, v in uv:
            obj_file.write(f"vt {u} {v}\n")

    obj_file.write("\n")


def write_obj_faces(root, obj_file, chunk_vert_sizes):
    for chunk_id, chunk in enumerate(root.chunks):

        chunk_name = chunk.chunk_name
        material_name = chunk.material_name

        obj_file.write(f"usemtl {material_name}\n")
        obj_file.write(f"{chunk_name}\n")

        offset = sum(chunk_vert_sizes[:chunk_id])
        faces = np.array(chunk.faces.faces)
        for face_index in range(0, len(faces), 3):
            f1, f2, f3 = (
                faces[face_index] + 1 + offset,
                faces[face_index + 1] + 1 + offset,
                faces[face_index + 2] + 1 + offset,
            )
            t1, t2, t3 = f1, f2, f3
            # obj_file.write(f'f {f1} {f2} {f3}\n')
            obj_file.write(f"f {f1}/{t1} {f2}/{t2} {f3}/{t3}\n")
        obj_file.write("\n")


def write_obj_file(root, obj_file, mtl_filename):
    obj_file.write(f"mtllib {mtl_filename}\n\n")
    chunk_vert_sizes = write_obj_vertices(root, obj_file)
    write_obj_uv(root, obj_file)
    write_obj_faces(root, obj_file, chunk_vert_sizes)


if __name__ == "__main__":
    import argparse
    import shlex
    from pathlib import Path

    parser = argparse.ArgumentParser(
        description="Convert matterport .dam file to .obj",
        epilog="example: python damfile2obj.py --out-dir=8800BLR_dollhouse da1a5ccd99d044f586788232864f0004_50k.dam",
        # formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--out-dir", dest="out_dir", type=Path, default=None, help="output directory"
    )
    parser.add_argument("dam_pth", type=Path, help="Path of .dam file")

    args = parser.parse_args()

    dam_path = args.dam_pth
    out_dir = args.out_dir

    if out_dir is None:
        out_dir = Path(dam_path.stem)

    out_dir.mkdir(exist_ok=True)

    with open(dam_path, "rb") as f:
        raw = f.read()

    root = damfile.BinaryMesh()
    root.ParseFromString(raw)

    model_id = dam_path.stem

    mtl_filename = model_id + ".mtl"
    obj_filename = model_id + ".obj"

    mtl_path = out_dir / mtl_filename
    obj_path = out_dir / obj_filename

    # mtl file
    with open(mtl_path, "wt") as mtl_file:
        write_mtl_file(root, mtl_file)
    print(f"saved mtl:", shlex.quote(str(mtl_path)))

    # obj file
    with open(obj_path, "wt") as obj_file:
        write_obj_file(root, obj_file, mtl_filename)
    print(f"saved obj:", shlex.quote(str(obj_path)))
