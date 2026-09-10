#!/usr/bin/env python3
"""Compile a static glTF 2.0 GLB into a rigid-pivot Character Studio descriptor.

The compiler intentionally runs at build time so the browser does not need GLTFLoader.
It preserves PBR material/texture references and partitions complete triangles into
rigid body regions that can be attached to the existing THREE.Group animation rig.
"""
from __future__ import annotations

import argparse
import base64
import json
import math
import mimetypes
import struct
from pathlib import Path
from typing import Any

TARGET_HEIGHT = 3.35
GLB_JSON = 0x4E4F534A
GLB_BIN = 0x004E4942
COMPONENT = {
    5120: ("b", 1),
    5121: ("B", 1),
    5122: ("h", 2),
    5123: ("H", 2),
    5125: ("I", 4),
    5126: ("f", 4),
}
TYPE_SIZE = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4, "MAT2": 4, "MAT3": 9, "MAT4": 16}


def _identity() -> list[list[float]]:
    return [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]


def _mul(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
    return [[sum(a[r][k] * b[k][c] for k in range(4)) for c in range(4)] for r in range(4)]


def _trs(node: dict[str, Any]) -> list[list[float]]:
    if "matrix" in node:
        src = node["matrix"]
        if len(src) != 16:
            raise ValueError("node.matrix must contain 16 values")
        return [[float(src[c * 4 + r]) for c in range(4)] for r in range(4)]
    tx, ty, tz = (node.get("translation") or [0, 0, 0])[:3]
    sx, sy, sz = (node.get("scale") or [1, 1, 1])[:3]
    x, y, z, w = (node.get("rotation") or [0, 0, 0, 1])[:4]
    xx, yy, zz = x * x, y * y, z * z
    xy, xz, yz = x * y, x * z, y * z
    wx, wy, wz = w * x, w * y, w * z
    r = [
        [1 - 2 * (yy + zz), 2 * (xy - wz), 2 * (xz + wy), 0],
        [2 * (xy + wz), 1 - 2 * (xx + zz), 2 * (yz - wx), 0],
        [2 * (xz - wy), 2 * (yz + wx), 1 - 2 * (xx + yy), 0],
        [0, 0, 0, 1],
    ]
    s = [[sx, 0, 0, 0], [0, sy, 0, 0], [0, 0, sz, 0], [0, 0, 0, 1]]
    t = _identity(); t[0][3], t[1][3], t[2][3] = tx, ty, tz
    return _mul(t, _mul(r, s))


def _point(m: list[list[float]], v: list[float] | tuple[float, ...]) -> list[float]:
    x, y, z = map(float, v[:3])
    return [
        m[0][0] * x + m[0][1] * y + m[0][2] * z + m[0][3],
        m[1][0] * x + m[1][1] * y + m[1][2] * z + m[1][3],
        m[2][0] * x + m[2][1] * y + m[2][2] * z + m[2][3],
    ]


def _direction(m: list[list[float]], v: list[float] | tuple[float, ...]) -> list[float]:
    x, y, z = map(float, v[:3])
    out = [
        m[0][0] * x + m[0][1] * y + m[0][2] * z,
        m[1][0] * x + m[1][1] * y + m[1][2] * z,
        m[2][0] * x + m[2][1] * y + m[2][2] * z,
    ]
    length = math.sqrt(sum(n * n for n in out)) or 1.0
    return [n / length for n in out]


def _q(values: list[float], q: int = 6) -> list[float]:
    return [round(float(v), q) for v in values]


def _quantile(values: list[float], p: float, fallback: float) -> float:
    if not values:
        return fallback
    seq = sorted(values)
    pos = max(0.0, min(1.0, p)) * (len(seq) - 1)
    lo, hi = int(math.floor(pos)), int(math.ceil(pos))
    if lo == hi:
        return seq[lo]
    a = pos - lo
    return seq[lo] * (1 - a) + seq[hi] * a


class GLB:
    def __init__(self, path: Path):
        self.path = path
        data = path.read_bytes()
        if len(data) < 20 or data[:4] != b"glTF":
            raise ValueError("not a glTF binary")
        version, declared = struct.unpack_from("<II", data, 4)
        if version != 2:
            raise ValueError(f"unsupported glTF version {version}")
        if declared > len(data):
            raise ValueError("truncated GLB")
        self.json: dict[str, Any] | None = None
        self.bin_chunk = b""
        offset = 12
        while offset + 8 <= declared:
            length, kind = struct.unpack_from("<II", data, offset)
            offset += 8
            chunk = data[offset: offset + length]
            offset += length
            if kind == GLB_JSON:
                self.json = json.loads(chunk.rstrip(b"\x00 \t\r\n").decode("utf-8"))
            elif kind == GLB_BIN:
                self.bin_chunk = chunk
        if self.json is None:
            raise ValueError("GLB JSON chunk missing")
        self.buffers = self._load_buffers()

    def _load_buffers(self) -> list[bytes]:
        out = []
        for index, item in enumerate(self.json.get("buffers", [])):
            uri = item.get("uri")
            if not uri and index == 0:
                out.append(self.bin_chunk)
            elif isinstance(uri, str) and uri.startswith("data:"):
                out.append(base64.b64decode(uri.split(",", 1)[1]))
            elif isinstance(uri, str):
                out.append((self.path.parent / uri).read_bytes())
            else:
                raise ValueError(f"buffer {index} has no data")
        return out

    def _raw_accessor(self, index: int) -> list[list[float] | float | int]:
        accessor = self.json["accessors"][index]
        size = TYPE_SIZE[accessor["type"]]
        component_type = int(accessor["componentType"])
        fmt, component_bytes = COMPONENT[component_type]
        count = int(accessor["count"])
        view = self.json.get("bufferViews", [])[accessor["bufferView"]]
        buf = self.buffers[int(view.get("buffer", 0))]
        base = int(view.get("byteOffset", 0)) + int(accessor.get("byteOffset", 0))
        stride = int(view.get("byteStride", component_bytes * size))
        unpack = struct.Struct("<" + fmt * size)
        values = []
        for i in range(count):
            row = list(unpack.unpack_from(buf, base + i * stride))
            if accessor.get("normalized") and component_type != 5126:
                row = [self._normalize_component(v, component_type) for v in row]
            values.append(row[0] if size == 1 else row)
        sparse = accessor.get("sparse")
        if sparse:
            self._apply_sparse(values, sparse, size, component_type)
        return values

    @staticmethod
    def _normalize_component(value: int, component_type: int) -> float:
        if component_type == 5120:
            return max(float(value) / 127.0, -1.0)
        if component_type == 5121:
            return float(value) / 255.0
        if component_type == 5122:
            return max(float(value) / 32767.0, -1.0)
        if component_type == 5123:
            return float(value) / 65535.0
        if component_type == 5125:
            return float(value) / 4294967295.0
        return float(value)

    def _apply_sparse(self, values: list, sparse: dict[str, Any], size: int, component_type: int) -> None:
        count = int(sparse["count"])
        idx_info = sparse["indices"]
        idx_view = self.json["bufferViews"][idx_info["bufferView"]]
        idx_fmt, idx_bytes = COMPONENT[int(idx_info["componentType"])]
        idx_buf = self.buffers[int(idx_view.get("buffer", 0))]
        idx_base = int(idx_view.get("byteOffset", 0)) + int(idx_info.get("byteOffset", 0))
        val_info = sparse["values"]
        val_view = self.json["bufferViews"][val_info["bufferView"]]
        val_buf = self.buffers[int(val_view.get("buffer", 0))]
        val_base = int(val_view.get("byteOffset", 0)) + int(val_info.get("byteOffset", 0))
        fmt, component_bytes = COMPONENT[component_type]
        value_unpack = struct.Struct("<" + fmt * size)
        for i in range(count):
            target = struct.unpack_from("<" + idx_fmt, idx_buf, idx_base + i * idx_bytes)[0]
            row = list(value_unpack.unpack_from(val_buf, val_base + i * component_bytes * size))
            values[target] = row[0] if size == 1 else row

    def accessor(self, index: int) -> list:
        return self._raw_accessor(index)

    def buffer_view_bytes(self, index: int) -> bytes:
        view = self.json["bufferViews"][index]
        buf = self.buffers[int(view.get("buffer", 0))]
        start = int(view.get("byteOffset", 0))
        return buf[start: start + int(view["byteLength"])]


def _scene_primitives(glb: GLB) -> list[dict[str, Any]]:
    doc = glb.json
    nodes = doc.get("nodes", [])
    meshes = doc.get("meshes", [])
    scenes = doc.get("scenes", [])
    if scenes:
        roots = scenes[int(doc.get("scene", 0))].get("nodes", [])
    else:
        children = {c for n in nodes for c in n.get("children", [])}
        roots = [i for i in range(len(nodes)) if i not in children]
    result = []

    def visit(index: int, parent: list[list[float]], lineage: list[str]) -> None:
        node = nodes[index]
        world = _mul(parent, _trs(node))
        name = str(node.get("name") or f"node_{index}")
        lineage2 = lineage + [name]
        if "mesh" in node:
            mesh_index = int(node["mesh"])
            mesh = meshes[mesh_index]
            mesh_name = str(mesh.get("name") or f"mesh_{mesh_index}")
            for pindex, primitive in enumerate(mesh.get("primitives", [])):
                if int(primitive.get("mode", 4)) != 4:
                    continue
                attrs = primitive.get("attributes", {})
                if "POSITION" not in attrs:
                    continue
                positions = [_point(world, p) for p in glb.accessor(int(attrs["POSITION"]))]
                normals = None
                if "NORMAL" in attrs:
                    normals = [_direction(world, n) for n in glb.accessor(int(attrs["NORMAL"]))]
                uvs = glb.accessor(int(attrs["TEXCOORD_0"])) if "TEXCOORD_0" in attrs else None
                indices = glb.accessor(int(primitive["indices"])) if "indices" in primitive else list(range(len(positions)))
                indices = [int(v) for v in indices]
                result.append({
                    "id": len(result), "node": name, "mesh": mesh_name, "lineage": lineage2,
                    "positions": positions, "normals": normals, "uvs": uvs,
                    "indices": indices, "material": int(primitive.get("material", -1)),
                })
        for child in node.get("children", []):
            visit(int(child), world, lineage2)

    for root in roots:
        visit(int(root), _identity(), [])
    if not result:
        raise ValueError("GLB contains no TRIANGLES primitive with POSITION")
    return result


def _normalize_primitives(primitives: list[dict[str, Any]]) -> dict[str, Any]:
    points = [p for primitive in primitives for p in primitive["positions"]]
    mins = [min(p[a] for p in points) for a in range(3)]
    maxs = [max(p[a] for p in points) for a in range(3)]
    height = maxs[1] - mins[1]
    if height <= 1e-8:
        raise ValueError("GLB has zero height")
    scale = TARGET_HEIGHT / height
    cx = (mins[0] + maxs[0]) * .5
    cz = (mins[2] + maxs[2]) * .5
    for primitive in primitives:
        primitive["positions"] = [[(p[0] - cx) * scale, (p[1] - mins[1]) * scale, (p[2] - cz) * scale] for p in primitive["positions"]]
    return {
        "sourceBounds": {"min": _q(mins), "max": _q(maxs)},
        "sourceHeight": height,
        "scale": scale,
        "targetHeight": TARGET_HEIGHT,
    }


def _infer_rig(primitives: list[dict[str, Any]]) -> dict[str, Any]:
    points = [p for primitive in primitives for p in primitive["positions"]]
    h = TARGET_HEIGHT
    torso_band = [abs(p[0]) for p in points if .52 * h <= p[1] <= .79 * h]
    torso_half = _quantile(torso_band, .58, .13 * h)
    torso_half = max(.085 * h, min(torso_half, .18 * h))
    upper = [abs(p[0]) for p in points if .54 * h <= p[1] <= .82 * h]
    arm_reach = max(upper or [torso_half])
    spread = arm_reach > .30 * h
    shoulder_x = max(.105 * h, min(torso_half * 1.08, .17 * h))
    hip_x = max(.045 * h, min(torso_half * .48, .09 * h))
    if spread:
        wrist_x = max(shoulder_x + .16 * h, arm_reach * .94)
        elbow_x = (shoulder_x + wrist_x) * .52
        shoulder_y, elbow_y, wrist_y = .705 * h, .695 * h, .685 * h
    else:
        arm_side = _quantile(upper, .88, shoulder_x * 1.18)
        elbow_x = max(shoulder_x, min(arm_side, .20 * h))
        wrist_x = elbow_x
        shoulder_y, elbow_y, wrist_y = .705 * h, .565 * h, .405 * h

    # glTF characters commonly face +Z; anatomical right is then -X.
    right_sign = -1
    name_right_x, name_left_x = [], []
    for primitive in primitives:
        label = " ".join(primitive["lineage"] + [primitive["mesh"]]).lower()
        avg_x = sum(p[0] for p in primitive["positions"]) / max(1, len(primitive["positions"]))
        if any(t in label for t in ("right", "_r", ".r")):
            name_right_x.append(avg_x)
        if any(t in label for t in ("left", "_l", ".l")):
            name_left_x.append(avg_x)
    if name_right_x and name_left_x:
        rx = sum(name_right_x) / len(name_right_x)
        lx = sum(name_left_x) / len(name_left_x)
        if rx * lx < 0:
            right_sign = 1 if rx > 0 else -1
    left_sign = -right_sign

    def side(sign: int, x: float) -> float:
        return float(sign) * x

    joints = {
        "pelvis": [0, .50 * h, 0],
        "chest": [0, .665 * h, 0],
        "neck": [0, .805 * h, 0],
        "head": [0, .865 * h, 0],
        "shoulderL": [side(left_sign, shoulder_x), shoulder_y, 0],
        "elbowL": [side(left_sign, elbow_x), elbow_y, 0],
        "wristL": [side(left_sign, wrist_x), wrist_y, 0],
        "shoulderR": [side(right_sign, shoulder_x), shoulder_y, 0],
        "elbowR": [side(right_sign, elbow_x), elbow_y, 0],
        "wristR": [side(right_sign, wrist_x), wrist_y, 0],
        "hipL": [side(left_sign, hip_x), .485 * h, 0],
        "kneeL": [side(left_sign, hip_x), .265 * h, 0],
        "ankleL": [side(left_sign, hip_x), .065 * h, 0],
        "hipR": [side(right_sign, hip_x), .485 * h, 0],
        "kneeR": [side(right_sign, hip_x), .265 * h, 0],
        "ankleR": [side(right_sign, hip_x), .065 * h, 0],
    }
    return {
        "pose": "spread" if spread else "arms-down",
        "rightSign": right_sign,
        "torsoHalfWidth": torso_half,
        "armReach": arm_reach,
        "joints": {k: _q(v) for k, v in joints.items()},
    }


def _name_hint(label: str, side_name: str | None = None) -> str | None:
    n = label.lower()
    side = None
    if any(x in n for x in ("left", "_l", ".l")):
        side = "L"
    elif any(x in n for x in ("right", "_r", ".r")):
        side = "R"
    if side_name:
        side = side_name
    if any(x in n for x in ("head", "face", "hair", "eye", "mouth", "brow")):
        return "head"
    if "neck" in n:
        return "neck"
    if any(x in n for x in ("hand", "palm", "finger")) and side:
        return "hand" + side
    if any(x in n for x in ("forearm", "lowerarm", "lower_arm")) and side:
        return "lowerArm" + side
    if any(x in n for x in ("upperarm", "upper_arm", "shoulder", "arm")) and side:
        return "upperArm" + side
    if any(x in n for x in ("foot", "shoe", "boot", "toe")) and side:
        return "foot" + side
    if any(x in n for x in ("shin", "calf", "lowerleg", "lower_leg")) and side:
        return "shin" + side
    if any(x in n for x in ("thigh", "upperleg", "upper_leg", "leg")) and side:
        return "thigh" + side
    if any(x in n for x in ("hip", "pelvis", "waist")):
        return "pelvis"
    if any(x in n for x in ("torso", "chest", "body", "shirt", "jacket")):
        return "chest"
    return None


def _classify(centroid: list[float], primitive: dict[str, Any], rig: dict[str, Any]) -> str:
    x, y, _ = centroid
    h = TARGET_HEIGHT
    right_sign = int(rig["rightSign"])
    side = "R" if (x > 0) == (right_sign > 0) else "L"
    label = " ".join(primitive["lineage"] + [primitive["mesh"]])
    hinted = _name_hint(label)
    if hinted:
        return hinted
    ax = abs(x)
    shoulder_x = abs(rig["joints"]["shoulderR"][0])
    elbow_x = abs(rig["joints"]["elbowR"][0])
    wrist_x = abs(rig["joints"]["wristR"][0])
    spread = rig["pose"] == "spread"
    if y >= .835 * h:
        return "head"
    if y >= .795 * h and ax < shoulder_x * .75:
        return "neck"
    if spread and y >= .50 * h and ax > shoulder_x * .88:
        if ax >= (elbow_x + wrist_x) * .5:
            return "hand" + side
        if ax >= (shoulder_x + elbow_x) * .5:
            return "lowerArm" + side
        return "upperArm" + side
    if not spread and y >= .30 * h and ax > shoulder_x * .90:
        if y >= .61 * h:
            return "upperArm" + side
        if y >= .44 * h:
            return "lowerArm" + side
        return "hand" + side
    if y >= .555 * h:
        return "chest"
    if y >= .47 * h:
        return "pelvis"
    if y >= .265 * h:
        return "thigh" + side
    if y >= .075 * h:
        return "shin" + side
    return "foot" + side


def _materials_and_textures(glb: GLB, output_dir: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    doc = glb.json
    texture_dir = output_dir / "textures"
    texture_dir.mkdir(parents=True, exist_ok=True)
    images_out = []
    for index, image in enumerate(doc.get("images", [])):
        mime = image.get("mimeType")
        data = None
        uri = image.get("uri")
        if "bufferView" in image:
            data = glb.buffer_view_bytes(int(image["bufferView"]))
        elif isinstance(uri, str) and uri.startswith("data:"):
            header, encoded = uri.split(",", 1)
            if not mime and ";" in header:
                mime = header[5:].split(";", 1)[0]
            data = base64.b64decode(encoded)
        elif isinstance(uri, str):
            src = glb.path.parent / uri
            if src.is_file():
                data = src.read_bytes()
                if not mime:
                    mime = mimetypes.guess_type(src.name)[0]
        if data is None:
            images_out.append({"path": None, "mimeType": mime})
            continue
        ext = {"image/png": ".png", "image/jpeg": ".jpg", "image/webp": ".webp"}.get(mime)
        if not ext:
            ext = Path(uri or "").suffix or ".bin"
        name = f"image-{index}{ext}"
        (texture_dir / name).write_bytes(data)
        images_out.append({"path": f"./assets/runtime/tripo_5889e73e/textures/{name}", "mimeType": mime})

    textures_out = []
    for texture in doc.get("textures", []):
        source = texture.get("source")
        image = images_out[int(source)] if source is not None and int(source) < len(images_out) else {"path": None, "mimeType": None}
        textures_out.append({"path": image.get("path"), "mimeType": image.get("mimeType"), "sampler": texture.get("sampler")})

    def tex(slot: Any) -> int | None:
        return int(slot["index"]) if isinstance(slot, dict) and "index" in slot else None

    materials = []
    for index, material in enumerate(doc.get("materials", [])):
        pbr = material.get("pbrMetallicRoughness", {})
        materials.append({
            "name": str(material.get("name") or f"material_{index}"),
            "baseColorFactor": _q((pbr.get("baseColorFactor") or [1, 1, 1, 1])[:4]),
            "metallicFactor": round(float(pbr.get("metallicFactor", 1)), 6),
            "roughnessFactor": round(float(pbr.get("roughnessFactor", 1)), 6),
            "emissiveFactor": _q((material.get("emissiveFactor") or [0, 0, 0])[:3]),
            "baseColorTexture": tex(pbr.get("baseColorTexture")),
            "metallicRoughnessTexture": tex(pbr.get("metallicRoughnessTexture")),
            "normalTexture": tex(material.get("normalTexture")),
            "emissiveTexture": tex(material.get("emissiveTexture")),
            "occlusionTexture": tex(material.get("occlusionTexture")),
            "doubleSided": bool(material.get("doubleSided", False)),
            "alphaMode": str(material.get("alphaMode", "OPAQUE")),
            "alphaCutoff": round(float(material.get("alphaCutoff", .5)), 6),
        })
    if not materials:
        materials.append({
            "name": "Tripo Default", "baseColorFactor": [1, 1, 1, 1], "metallicFactor": 0,
            "roughnessFactor": .72, "emissiveFactor": [0, 0, 0], "baseColorTexture": None,
            "metallicRoughnessTexture": None, "normalTexture": None, "emissiveTexture": None,
            "occlusionTexture": None, "doubleSided": False, "alphaMode": "OPAQUE", "alphaCutoff": .5,
        })
    return materials, textures_out


def _partition(primitives: list[dict[str, Any]], rig: dict[str, Any]) -> tuple[dict[str, Any], dict[str, int]]:
    segment_joint = {
        "pelvis": "pelvis", "chest": "chest", "neck": "neck", "head": "head",
        "upperArmL": "shoulderL", "lowerArmL": "elbowL", "handL": "wristL",
        "upperArmR": "shoulderR", "lowerArmR": "elbowR", "handR": "wristR",
        "thighL": "hipL", "shinL": "kneeL", "footL": "ankleL",
        "thighR": "hipR", "shinR": "kneeR", "footR": "ankleR",
    }
    groups: dict[tuple[str, int], dict[str, Any]] = {}
    region_triangles: dict[str, int] = {name: 0 for name in segment_joint}
    for primitive in primitives:
        positions, normals, uvs, indices = primitive["positions"], primitive["normals"], primitive["uvs"], primitive["indices"]
        if len(indices) % 3:
            indices = indices[:len(indices) - len(indices) % 3]
        for t in range(0, len(indices), 3):
            tri = indices[t:t + 3]
            centroid = [sum(positions[i][a] for i in tri) / 3.0 for a in range(3)]
            region = _classify(centroid, primitive, rig)
            material = primitive["material"] if primitive["material"] >= 0 else 0
            key = (region, material)
            bucket = groups.setdefault(key, {"positions": [], "normals": [], "uvs": [], "indices": [], "map": {}})
            for source_index in tri:
                source_key = (primitive["id"], source_index)
                mapped = bucket["map"].get(source_key)
                if mapped is None:
                    mapped = len(bucket["positions"]) // 3
                    bucket["map"][source_key] = mapped
                    bucket["positions"].extend(_q(positions[source_index]))
                    normal = normals[source_index] if normals and source_index < len(normals) else [0, 1, 0]
                    bucket["normals"].extend(_q(normal))
                    uv = uvs[source_index] if uvs and source_index < len(uvs) else [0, 0]
                    bucket["uvs"].extend(_q(list(uv)[:2]))
                bucket["indices"].append(mapped)
            region_triangles[region] += 1
    parts = {name: {"joint": joint, "primitives": []} for name, joint in segment_joint.items()}
    for (region, material), bucket in groups.items():
        bucket.pop("map", None)
        bucket["material"] = material
        bucket["vertexCount"] = len(bucket["positions"]) // 3
        bucket["triangleCount"] = len(bucket["indices"]) // 3
        parts[region]["primitives"].append(bucket)
    return parts, region_triangles


def compile_glb(input_path: Path, output_dir: Path) -> dict[str, Any]:
    glb = GLB(input_path)
    primitives = _scene_primitives(glb)
    normalization = _normalize_primitives(primitives)
    rig = _infer_rig(primitives)
    materials, textures = _materials_and_textures(glb, output_dir)
    parts, region_triangles = _partition(primitives, rig)
    total_vertices = sum(len(p["positions"]) for p in primitives)
    total_triangles = sum(len(p["indices"]) // 3 for p in primitives)
    descriptor = {
        "schema": "studio-rigid-glb-v1",
        "version": "1.0.0",
        "id": "tripo-5889e73e-rigid-v1",
        "source": "assets/imports/tripo_5889e73e/tripo_5889e73e.glb",
        "sourceFormat": "glTF 2.0 binary",
        "primary": True,
        "architecture": "THREE.Group",
        "normalization": normalization,
        "rig": rig,
        "materials": materials,
        "textures": textures,
        "parts": parts,
        "stats": {
            "sourcePrimitives": len(primitives),
            "sourceVertices": total_vertices,
            "sourceTriangles": total_triangles,
            "rigidTriangles": sum(region_triangles.values()),
            "regions": region_triangles,
        },
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "rigid-model.json").write_text(json.dumps(descriptor, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    return descriptor


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    descriptor = compile_glb(args.input, args.output)
    print(json.dumps({"id": descriptor["id"], "stats": descriptor["stats"], "rig": {"pose": descriptor["rig"]["pose"], "rightSign": descriptor["rig"]["rightSign"]}}, indent=2))


if __name__ == "__main__":
    main()
