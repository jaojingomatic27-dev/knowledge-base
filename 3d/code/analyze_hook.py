#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""分析 hook.stl 二进制 STL 文件的结构"""

import struct
import numpy as np

HOOK_PATH = r"C:\AI\cc\3d\input\hook.stl"

with open(HOOK_PATH, "rb") as f:
    # 跳过 80 字节 header
    header = f.read(80)
    print(f"Header (first 40 bytes): {header[:40]}")

    # 读取三角形数量 (4 bytes, uint32 little-endian)
    n_tri = struct.unpack("<I", f.read(4))[0]
    print(f"Triangle count: {n_tri}")

    # 读取所有三角形
    vertices = []
    for i in range(n_tri):
        normal = struct.unpack("<3f", f.read(12))
        v1 = struct.unpack("<3f", f.read(12))
        v2 = struct.unpack("<3f", f.read(12))
        v3 = struct.unpack("<3f", f.read(12))
        attr = f.read(2)  # attribute byte count
        vertices.extend([v1, v2, v3])

    verts = np.array(vertices)

    print(f"\n--- Bounding Box ---")
    print(f"X: min={verts[:,0].min():.4f}, max={verts[:,0].max():.4f}")
    print(f"Y: min={verts[:,1].min():.4f}, max={verts[:,1].max():.4f}")
    print(f"Z: min={verts[:,2].min():.4f}, max={verts[:,2].max():.4f}")

    print(f"\n--- Dimensions (range) ---")
    print(f"X span: {verts[:,0].max() - verts[:,0].min():.4f}")
    print(f"Y span: {verts[:,1].max() - verts[:,1].min():.4f}")
    print(f"Z span: {verts[:,2].max() - verts[:,2].min():.4f}")

    # 采样一些点看看
    print(f"\n--- Sample points (first 10 vertices) ---")
    for i, v in enumerate(verts[:10]):
        print(f"  v{i}: ({v[0]:.4f}, {v[1]:.4f}, {v[2]:.4f})")

    # 分析几何特征
    # 找出可能的圆柱体中心 (XZ 平面上的模式)
    mid_x = (verts[:,0].max() + verts[:,0].min()) / 2
    mid_y = (verts[:,1].max() + verts[:,1].min()) / 2
    mid_z = (verts[:,2].max() + verts[:,2].min()) / 2
    print(f"\nCenter: X={mid_x:.4f}, Y={mid_y:.4f}, Z={mid_z:.4f}")

    print(f"\n--- Ratio HINT ---")
    print("Model seems to be in meters or mm — check manual scaling")
    print(f"X range = {verts[:,0].max() - verts[:,0].min():.4f}")
