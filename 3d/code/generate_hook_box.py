#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""基于 hook.stl 添加挂载盒子 (200x100x30mm) + 底部卡槽
读取 binary STL 的 hook, 在其顶部加盒子, 输出合并的 STL
"""

import struct
import numpy as np
import os

HOOK_PATH = r"C:\AI\cc\3d\input\hook.stl"
OUTPUT_PATH = r"C:\AI\cc\3d\data\hook_with_box.stl"

# ── 盒子参数 (mm) ──
BOX_L = 200.0   # X 方向 (长)
BOX_W = 100.0   # Y 方向 (宽)
BOX_H = 30.0    # Z 方向 (厚)

# 盒子位置: 底部放在 hook 顶部 (Z=63), XY 居中于 hook 中心 (170, 150)
BOX_CX = 170.0
BOX_CY = 150.0
BOX_BZ = 63.0   # 盒子底面 Z

# 卡槽参数: 钩子顶部接触区域 Y≈[155, 175], 槽略大于接触区
SLOT_Y1 = 152.0  # 槽 Y 起点 (留余量)
SLOT_Y2 = 178.0  # 槽 Y 终点
SLOT_D = 8.0     # 槽深 (从盒子底面向上)

# 钩子 X 范围 [80, 260], 槽在 X 方向留壁
SLOT_X1 = 80.0   # 槽 X 起点
SLOT_X2 = 260.0  # 槽 X 终点


def generate_box_with_slot():
    """生成带底部卡槽的盒子三角面片"""
    tris = []

    def add_quad(v1, v2, v3, v4, flip=False):
        """添加两个三角面片组成四边形"""
        if flip:
            tris.append((v1.copy(), v3.copy(), v2.copy()))
            tris.append((v2.copy(), v3.copy(), v4.copy()))
        else:
            tris.append((v1.copy(), v2.copy(), v3.copy()))
            tris.append((v2.copy(), v4.copy(), v3.copy()))

    x1 = BOX_CX - BOX_L / 2  # 70
    x2 = BOX_CX + BOX_L / 2  # 270
    y1 = BOX_CY - BOX_W / 2  # 100
    y2 = BOX_CY + BOX_W / 2  # 200
    z1 = BOX_BZ               # 63 (底面)
    z2 = BOX_BZ + BOX_H       # 93 (顶面)
    zg = BOX_BZ + SLOT_D      # 71 (槽内顶面)

    sy1 = SLOT_Y1  # 152
    sy2 = SLOT_Y2  # 178
    sx1 = SLOT_X1  # 80
    sx2 = SLOT_X2  # 260

    # ── 1. 顶面 (z=z2, 完整矩形) ──
    v1 = np.array([x1, y1, z2])
    v2 = np.array([x2, y1, z2])
    v3 = np.array([x1, y2, z2])
    v4 = np.array([x2, y2, z2])
    add_quad(v1, v2, v3, v4)  # 法线 +z

    # ── 2. 底面 — 分三块 (左 + 槽底 + 右) ──
    # 左块: y1 → sy1
    v1 = np.array([x1, y1, z1])
    v2 = np.array([x2, y1, z1])
    v3 = np.array([x1, sy1, z1])
    v4 = np.array([x2, sy1, z1])
    add_quad(v1, v3, v2, v4)  # flip for -z normal

    # 右块: sy2 → y2
    v1 = np.array([x1, sy2, z1])
    v2 = np.array([x2, sy2, z1])
    v3 = np.array([x1, y2, z1])
    v4 = np.array([x2, y2, z1])
    add_quad(v1, v3, v2, v4)  # flip for -z normal

    # 槽底面: X 方向也分三段(左壁 + 槽 + 右壁)
    # 槽内顶面 (zg): sx1→sx2, sy1→sy2
    v1 = np.array([sx1, sy1, zg])
    v2 = np.array([sx2, sy1, zg])
    v3 = np.array([sx1, sy2, zg])
    v4 = np.array([sx2, sy2, zg])
    add_quad(v1, v2, v3, v4)  # 法线 -z (朝下)

    # 底面 X 左端 (x1→sx1): sy1→sy2, z=z1
    v1 = np.array([x1, sy1, z1])
    v2 = np.array([sx1, sy1, z1])
    v3 = np.array([x1, sy2, z1])
    v4 = np.array([sx1, sy2, z1])
    add_quad(v1, v3, v2, v4)

    # 底面 X 右端 (sx2→x2): sy1→sy2
    v1 = np.array([sx2, sy1, z1])
    v2 = np.array([x2, sy1, z1])
    v3 = np.array([sx2, sy2, z1])
    v4 = np.array([x2, sy2, z1])
    add_quad(v1, v3, v2, v4)

    # ── 3. 前面 (y=y1) ──
    v1 = np.array([x1, y1, z1])
    v2 = np.array([x2, y1, z1])
    v3 = np.array([x1, y1, z2])
    v4 = np.array([x2, y1, z2])
    add_quad(v1, v2, v3, v4)

    # ── 4. 后面 (y=y2) ──
    v1 = np.array([x1, y2, z1])
    v2 = np.array([x2, y2, z1])
    v3 = np.array([x1, y2, z2])
    v4 = np.array([x2, y2, z2])
    add_quad(v1, v3, v2, v4)

    # ── 5. 左面 (x=x1), 从上到下完整 ──
    v1 = np.array([x1, y1, z1])
    v2 = np.array([x1, y2, z1])
    v3 = np.array([x1, y1, z2])
    v4 = np.array([x1, y2, z2])
    add_quad(v1, v3, v2, v4)

    # ── 6. 右面 (x=x2) ──
    v1 = np.array([x2, y1, z1])
    v2 = np.array([x2, y2, z1])
    v3 = np.array([x2, y1, z2])
    v4 = np.array([x2, y2, z2])
    add_quad(v1, v2, v3, v4)

    # ── 7. 槽内壁 Y=sy1 (Z: z1→zg) ──
    v1 = np.array([sx1, sy1, z1])
    v2 = np.array([sx2, sy1, z1])
    v3 = np.array([sx1, sy1, zg])
    v4 = np.array([sx2, sy1, zg])
    add_quad(v1, v2, v3, v4)

    # ── 8. 槽内壁 Y=sy2 (Z: z1→zg) ──
    v1 = np.array([sx1, sy2, z1])
    v2 = np.array([sx2, sy2, z1])
    v3 = np.array([sx1, sy2, zg])
    v4 = np.array([sx2, sy2, zg])
    add_quad(v1, v3, v2, v4)

    # ── 9. 槽内壁 X=sx1 (Z: z1→zg, Y: sy1→sy2) ──
    v1 = np.array([sx1, sy1, z1])
    v2 = np.array([sx1, sy2, z1])
    v3 = np.array([sx1, sy1, zg])
    v4 = np.array([sx1, sy2, zg])
    add_quad(v1, v3, v2, v4)

    # ── 10. 槽内壁 X=sx2 ──
    v1 = np.array([sx2, sy1, z1])
    v2 = np.array([sx2, sy2, z1])
    v3 = np.array([sx2, sy1, zg])
    v4 = np.array([sx2, sy2, zg])
    add_quad(v1, v2, v3, v4)

    return tris


def compute_normal(v1, v2, v3):
    u = v2 - v1
    v = v3 - v1
    n = np.cross(u, v)
    norm = np.linalg.norm(n)
    return n / norm if norm > 1e-12 else np.array([0.0, 0.0, 1.0])


def read_binary_stl(path):
    """读取 binary STL, 返回三角面片列表 [(v1,v2,v3), ...]"""
    tris = []
    with open(path, "rb") as f:
        f.read(80)  # header
        n_tri = struct.unpack("<I", f.read(4))[0]
        for _ in range(n_tri):
            f.read(12)  # normal
            v1 = np.array(struct.unpack("<3f", f.read(12)))
            v2 = np.array(struct.unpack("<3f", f.read(12)))
            v3 = np.array(struct.unpack("<3f", f.read(12)))
            f.read(2)   # attr
            tris.append((v1, v2, v3))
    return tris


def write_binary_stl(path, triangles):
    """写入 binary STL 文件"""
    with open(path, "wb") as f:
        f.write(b"\x00" * 80)  # header
        f.write(struct.pack("<I", len(triangles)))
        for v1, v2, v3 in triangles:
            n = compute_normal(v1, v2, v3)
            f.write(struct.pack("<3f", n[0], n[1], n[2]))
            f.write(struct.pack("<3f", v1[0], v1[1], v1[2]))
            f.write(struct.pack("<3f", v2[0], v2[1], v2[2]))
            f.write(struct.pack("<3f", v3[0], v3[1], v3[2]))
            f.write(b"\x00\x00")


def main():
    print("Reading hook.stl...")
    hook_tris = read_binary_stl(HOOK_PATH)
    print(f"  Hook triangles: {len(hook_tris)}")

    print("Generating box with slot...")
    box_tris = generate_box_with_slot()
    print(f"  Box triangles: {len(box_tris)}")

    all_tris = hook_tris + box_tris
    print(f"  Total triangles: {len(all_tris)}")

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    write_binary_stl(OUTPUT_PATH, all_tris)
    file_size_mb = os.path.getsize(OUTPUT_PATH) / (1024 * 1024)
    print(f"\nSTL file: {OUTPUT_PATH}")
    print(f"  Triangles: {len(all_tris)}")
    print(f"  File size: {file_size_mb:.2f} MB")
    print(f"\nBox: {BOX_L}x{BOX_W}x{BOX_H} mm")
    print(f"  Position: bottom Z={BOX_BZ}, center XY=({BOX_CX}, {BOX_CY})")
    print(f"Slot: Y[{SLOT_Y1}, {SLOT_Y2}] x Z[{BOX_BZ}, {BOX_BZ+SLOT_D}]")
    print(f"      X[{SLOT_X1}, {SLOT_X2}] through box")


if __name__ == "__main__":
    main()
