#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成半圆管 STL 3D 文件
外径 40mm, 内径 35mm, 长度 50mm
"""

import numpy as np
import os

# 参数
OUTER_RADIUS = 20.0      # mm (外径 40mm / 2)
INNER_RADIUS = 17.5      # mm (内径 35mm / 2)
LENGTH = 50.0            # mm (管长)
N_THETA = 80             # 半圆角度分段数
N_Z = 20                 # 长度方向分段数
N_R = 6                  # 端面径向分段数

OUTPUT_PATH = r"C:\AI\cc\3d\data\half_pipe.stl"


def generate_half_pipe_stl():
    triangles = []

    def add_tri(v1, v2, v3):
        triangles.append((v1.copy(), v2.copy(), v3.copy()))

    def compute_normal(v1, v2, v3):
        u = v2 - v1
        v = v3 - v1
        n = np.cross(u, v)
        norm = np.linalg.norm(n)
        return n / norm if norm > 1e-12 else np.array([0.0, 0.0, 1.0])

    thetas = np.linspace(0, np.pi, N_THETA + 1)
    zs = np.linspace(0, LENGTH, N_Z + 1)
    rs = np.linspace(INNER_RADIUS, OUTER_RADIUS, N_R + 1)

    # ── 1. 外曲面 (r=20), 法线向外 (径向向外) ──
    for i in range(N_THETA):
        for j in range(N_Z):
            t1, t2 = thetas[i], thetas[i + 1]
            z1, z2 = zs[j], zs[j + 1]

            v1 = np.array([OUTER_RADIUS * np.cos(t1), OUTER_RADIUS * np.sin(t1), z1])
            v2 = np.array([OUTER_RADIUS * np.cos(t2), OUTER_RADIUS * np.sin(t2), z1])
            v3 = np.array([OUTER_RADIUS * np.cos(t1), OUTER_RADIUS * np.sin(t1), z2])
            v4 = np.array([OUTER_RADIUS * np.cos(t2), OUTER_RADIUS * np.sin(t2), z2])

            add_tri(v1, v2, v3)
            add_tri(v2, v4, v3)

    # ── 2. 内曲面 (r=17.5), 法线指向圆心 (固体外侧 = 空心方向) ──
    for i in range(N_THETA):
        for j in range(N_Z):
            t1, t2 = thetas[i], thetas[i + 1]
            z1, z2 = zs[j], zs[j + 1]

            v1 = np.array([INNER_RADIUS * np.cos(t1), INNER_RADIUS * np.sin(t1), z1])
            v2 = np.array([INNER_RADIUS * np.cos(t2), INNER_RADIUS * np.sin(t2), z1])
            v3 = np.array([INNER_RADIUS * np.cos(t1), INNER_RADIUS * np.sin(t1), z2])
            v4 = np.array([INNER_RADIUS * np.cos(t2), INNER_RADIUS * np.sin(t2), z2])

            # 反转绕序使法线指向圆心
            add_tri(v1, v3, v2)
            add_tri(v2, v3, v4)

    # ── 3. 平面切口 θ=0 (法线 -y) ──
    for j in range(N_Z):
        z1, z2 = zs[j], zs[j + 1]
        v1 = np.array([INNER_RADIUS, 0.0, z1])
        v2 = np.array([OUTER_RADIUS, 0.0, z1])
        v3 = np.array([INNER_RADIUS, 0.0, z2])
        v4 = np.array([OUTER_RADIUS, 0.0, z2])

        add_tri(v1, v2, v3)
        add_tri(v2, v4, v3)

    # ── 4. 平面切口 θ=π (法线 -y, 需反转绕序) ──
    for j in range(N_Z):
        z1, z2 = zs[j], zs[j + 1]
        v1 = np.array([-INNER_RADIUS, 0.0, z1])
        v2 = np.array([-OUTER_RADIUS, 0.0, z1])
        v3 = np.array([-INNER_RADIUS, 0.0, z2])
        v4 = np.array([-OUTER_RADIUS, 0.0, z2])

        add_tri(v1, v3, v2)
        add_tri(v2, v3, v4)

    # ── 5. 底部端面 z=0 (法线 -z, 需反转绕序) ──
    for i in range(N_THETA):
        for k in range(N_R):
            t1, t2 = thetas[i], thetas[i + 1]
            r1, r2 = rs[k], rs[k + 1]

            v1 = np.array([r1 * np.cos(t1), r1 * np.sin(t1), 0.0])
            v2 = np.array([r1 * np.cos(t2), r1 * np.sin(t2), 0.0])
            v3 = np.array([r2 * np.cos(t1), r2 * np.sin(t1), 0.0])
            v4 = np.array([r2 * np.cos(t2), r2 * np.sin(t2), 0.0])

            add_tri(v1, v3, v2)
            add_tri(v2, v3, v4)

    # ── 6. 顶部端面 z=L (法线 +z) ──
    for i in range(N_THETA):
        for k in range(N_R):
            t1, t2 = thetas[i], thetas[i + 1]
            r1, r2 = rs[k], rs[k + 1]

            v1 = np.array([r1 * np.cos(t1), r1 * np.sin(t1), LENGTH])
            v2 = np.array([r1 * np.cos(t2), r1 * np.sin(t2), LENGTH])
            v3 = np.array([r2 * np.cos(t1), r2 * np.sin(t1), LENGTH])
            v4 = np.array([r2 * np.cos(t2), r2 * np.sin(t2), LENGTH])

            add_tri(v1, v2, v3)
            add_tri(v2, v4, v3)

    # ── 写入 ASCII STL ──
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="ascii") as f:
        f.write("solid half_pipe\n")
        for v1, v2, v3 in triangles:
            n = compute_normal(v1, v2, v3)
            f.write(f"  facet normal {n[0]:.6e} {n[1]:.6e} {n[2]:.6e}\n")
            f.write("    outer loop\n")
            f.write(f"      vertex {v1[0]:.6e} {v1[1]:.6e} {v1[2]:.6e}\n")
            f.write(f"      vertex {v2[0]:.6e} {v2[1]:.6e} {v2[2]:.6e}\n")
            f.write(f"      vertex {v3[0]:.6e} {v3[1]:.6e} {v3[2]:.6e}\n")
            f.write("    endloop\n")
            f.write("  endfacet\n")
        f.write("endsolid half_pipe\n")

    file_size_mb = os.path.getsize(OUTPUT_PATH) / (1024 * 1024)
    print(f"STL file generated: {OUTPUT_PATH}")
    print(f"  Triangles: {len(triangles)}")
    print(f"  File size:  {file_size_mb:.2f} MB")
    print(f"  Params: OD={OUTER_RADIUS*2}mm, ID={INNER_RADIUS*2}mm, wall={OUTER_RADIUS-INNER_RADIUS:.1f}mm, length={LENGTH}mm")


if __name__ == "__main__":
    generate_half_pipe_stl()
