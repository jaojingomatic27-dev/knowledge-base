#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成带扎带槽的半圆管 STL 3D 文件
内径 15mm, 壁厚 6mm (外径 27mm), 长度 60mm
两个扎带槽: 宽 3mm, 深 1mm
"""

import numpy as np
import os

# ── 尺寸参数 ──
INNER_RADIUS = 7.5       # mm (内径 15mm / 2)
WALL = 6.0               # mm 壁厚
OUTER_RADIUS = INNER_RADIUS + WALL  # 13.5mm
LENGTH = 60.0            # mm 总长

# ── 槽参数 ──
GROOVE_WIDTH = 3.0       # mm
GROOVE_DEPTH = 1.0       # mm
GROOVE_RADIUS = OUTER_RADIUS - GROOVE_DEPTH  # 12.5mm
GROOVE_OFFSET = 10.0     # mm 从端面到槽的距离

# ── 网格精度 ──
N_THETA = 80             # 半圆角度分段
N_R = 6                  # 端面径向分段

OUTPUT_PATH = r"C:\AI\cc\3d\data\half_pipe_slotted.stl"


def make_outer_z_segments():
    """将 Z 轴按槽分段，每段有不同的外半径"""
    segments = []
    groove_starts = [GROOVE_OFFSET, LENGTH - GROOVE_OFFSET - GROOVE_WIDTH]
    last_z = 0.0
    for gs in groove_starts:
        ge = gs + GROOVE_WIDTH
        if gs > last_z:
            segments.append((last_z, gs, OUTER_RADIUS))
        segments.append((gs, ge, GROOVE_RADIUS))
        last_z = ge
    if last_z < LENGTH:
        segments.append((last_z, LENGTH, OUTER_RADIUS))
    return segments


def generate_slotted_half_pipe():
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
    rs = np.linspace(INNER_RADIUS, OUTER_RADIUS, N_R + 1)

    z_segs = make_outer_z_segments()
    # 为每段计算 Z 方向分段数（与段长成比例）
    z_counts = []
    total_len = sum(se[1] - se[0] for se in z_segs)
    for z1, z2, _ in z_segs:
        nz = max(2, int((z2 - z1) / total_len * 200))
        z_counts.append(nz)

    # ── 1. 外曲面 (分段不同半径) ──
    for seg_idx, ((z1, z2, r), nz) in enumerate(zip(z_segs, z_counts)):
        zs_seg = np.linspace(z1, z2, nz + 1)
        for i in range(N_THETA):
            for j in range(nz):
                t1, t2 = thetas[i], thetas[i + 1]
                z_a, z_b = zs_seg[j], zs_seg[j + 1]

                v1 = np.array([r * np.cos(t1), r * np.sin(t1), z_a])
                v2 = np.array([r * np.cos(t2), r * np.sin(t2), z_a])
                v3 = np.array([r * np.cos(t1), r * np.sin(t1), z_b])
                v4 = np.array([r * np.cos(t2), r * np.sin(t2), z_b])

                add_tri(v1, v2, v3)
                add_tri(v2, v4, v3)

    # ── 2. 槽壁 — 半径变化处的竖直环面 ──
    #    每个台阶: z 不变, r 从 GROOVE_RADIUS 到 OUTER_RADIUS
    for seg_idx in range(len(z_segs) - 1):
        z_curr = z_segs[seg_idx][1]      # 当前段结束 Z = 下一段开始 Z
        r_small = z_segs[seg_idx][2]     # 当前段半径
        r_big   = z_segs[seg_idx + 1][2] # 下一段半径

        if abs(r_small - r_big) < 1e-9:
            continue  # 半径相同, 无台阶

        # r_small → r_big, 各占一半 N_R
        n_sub = max(3, N_R // 2)
        dr = (r_big - r_small) / n_sub
        rr = np.linspace(r_small, r_big, n_sub + 1)

        for i in range(N_THETA):
            t1, t2 = thetas[i], thetas[i + 1]
            for k in range(n_sub):
                r_a, r_b = rr[k], rr[k + 1]

                v1 = np.array([r_a * np.cos(t1), r_a * np.sin(t1), z_curr])
                v2 = np.array([r_a * np.cos(t2), r_a * np.sin(t2), z_curr])
                v3 = np.array([r_b * np.cos(t1), r_b * np.sin(t1), z_curr])
                v4 = np.array([r_b * np.cos(t2), r_b * np.sin(t2), z_curr])

                if r_b > r_small:
                    # 外径增大 (槽结束，向外扩) — 法线 +z
                    add_tri(v1, v2, v3)
                    add_tri(v2, v4, v3)
                else:
                    # 外径减小 (进入槽) — 法线 -z
                    add_tri(v1, v3, v2)
                    add_tri(v2, v3, v4)

    # ── 3. 内曲面 (r=INNER_RADIUS, 法线指向圆心) ──
    zs = np.linspace(0, LENGTH, 100)
    for i in range(N_THETA):
        for j in range(len(zs) - 1):
            t1, t2 = thetas[i], thetas[i + 1]
            z1, z2 = zs[j], zs[j + 1]

            v1 = np.array([INNER_RADIUS * np.cos(t1), INNER_RADIUS * np.sin(t1), z1])
            v2 = np.array([INNER_RADIUS * np.cos(t2), INNER_RADIUS * np.sin(t2), z1])
            v3 = np.array([INNER_RADIUS * np.cos(t1), INNER_RADIUS * np.sin(t1), z2])
            v4 = np.array([INNER_RADIUS * np.cos(t2), INNER_RADIUS * np.sin(t2), z2])

            add_tri(v1, v3, v2)
            add_tri(v2, v3, v4)

    # ── 4. 平面切口 θ=0 ──
    for z1, z2, r in z_segs:
        zs_seg = np.linspace(z1, z2, max(2, int((z2 - z1) / LENGTH * 100)) + 1)
        for j in range(len(zs_seg) - 1):
            za, zb = zs_seg[j], zs_seg[j + 1]
            v1 = np.array([INNER_RADIUS, 0.0, za])
            v2 = np.array([r, 0.0, za])
            v3 = np.array([INNER_RADIUS, 0.0, zb])
            v4 = np.array([r, 0.0, zb])

            add_tri(v1, v2, v3)
            add_tri(v2, v4, v3)

    # ── 5. 平面切口 θ=π ──
    for z1, z2, r in z_segs:
        zs_seg = np.linspace(z1, z2, max(2, int((z2 - z1) / LENGTH * 100)) + 1)
        for j in range(len(zs_seg) - 1):
            za, zb = zs_seg[j], zs_seg[j + 1]
            v1 = np.array([-INNER_RADIUS, 0.0, za])
            v2 = np.array([-r, 0.0, za])
            v3 = np.array([-INNER_RADIUS, 0.0, zb])
            v4 = np.array([-r, 0.0, zb])

            add_tri(v1, v3, v2)
            add_tri(v2, v3, v4)

    # ── 6. 底部端面 z=0 ──
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

    # ── 7. 顶部端面 z=L ──
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
        f.write("solid half_pipe_slotted\n")
        for v1, v2, v3 in triangles:
            n = compute_normal(v1, v2, v3)
            f.write(f"  facet normal {n[0]:.6e} {n[1]:.6e} {n[2]:.6e}\n")
            f.write("    outer loop\n")
            for v in [v1, v2, v3]:
                f.write(f"      vertex {v[0]:.6e} {v[1]:.6e} {v[2]:.6e}\n")
            f.write("    endloop\n")
            f.write("  endfacet\n")
        f.write("endsolid half_pipe_slotted\n")

    file_size_mb = os.path.getsize(OUTPUT_PATH) / (1024 * 1024)
    print(f"STL file generated: {OUTPUT_PATH}")
    print(f"  Triangles: {len(triangles)}")
    print(f"  File size:  {file_size_mb:.2f} MB")
    print(f"  Params: ID={INNER_RADIUS*2}mm, wall={WALL}mm, OD={OUTER_RADIUS*2}mm, L={LENGTH}mm")
    print(f"  Grooves: {GROOVE_WIDTH}mm wide x {GROOVE_DEPTH}mm deep")
    print(f"    at z={GROOVE_OFFSET}-{GROOVE_OFFSET+GROOVE_WIDTH} mm")
    print(f"    and z={LENGTH-GROOVE_OFFSET-GROOVE_WIDTH}-{LENGTH-GROOVE_OFFSET} mm")


if __name__ == "__main__":
    generate_slotted_half_pipe()
