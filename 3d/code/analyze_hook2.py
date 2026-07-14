#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""详细分析 hook.stl 几何结构"""

import struct
import numpy as np

HOOK_PATH = r"C:\AI\cc\3d\input\hook.stl"

with open(HOOK_PATH, "rb") as f:
    f.read(80)  # header
    n_tri = struct.unpack("<I", f.read(4))[0]
    vertices = []
    for i in range(n_tri):
        f.read(12)  # normal
        v1 = struct.unpack("<3f", f.read(12))
        v2 = struct.unpack("<3f", f.read(12))
        v3 = struct.unpack("<3f", f.read(12))
        f.read(2)   # attr
        vertices.extend([v1, v2, v3])

verts = np.array(vertices)

# YZ 截面分析 (固定 X 中间值附近)
mid_x = 170.0
mask_near_mid = np.abs(verts[:, 0] - mid_x) < 2.0
near_mid = verts[mask_near_mid]
if len(near_mid) > 0:
    print(f"--- YZ截面 near X={mid_x} ---")
    print(f"  Y: min={near_mid[:,1].min():.2f}, max={near_mid[:,1].max():.2f}")
    print(f"  Z: min={near_mid[:,2].min():.2f}, max={near_mid[:,2].max():.2f}")

# XY 截面分析 (固定 Z 中间值附近)
mid_z = 31.5
mask_near_z = np.abs(verts[:, 2] - mid_z) < 2.0
near_z = verts[mask_near_z]
if len(near_z) > 0:
    print(f"--- XY截面 near Z={mid_z} ---")
    print(f"  X: min={near_z[:,0].min():.2f}, max={near_z[:,0].max():.2f}")
    print(f"  Y: min={near_z[:,1].min():.2f}, max={near_z[:,1].max():.2f}")

# 找 X 最小值平面上的点
x_min = verts[:,0].min()
mask_xmin = np.abs(verts[:, 0] - x_min) < 0.2
xmin_pts = verts[mask_xmin]
if len(xmin_pts) > 0:
    print(f"\n--- X最小面 (X≈{x_min:.1f}) ---")
    print(f"  Y: min={xmin_pts[:,1].min():.2f}, max={xmin_pts[:,1].max():.2f}")
    print(f"  Z: min={xmin_pts[:,2].min():.2f}, max={xmin_pts[:,2].max():.2f}")
    print(f"  点数: {len(xmin_pts)}")

# 找 X 最大值平面上的点
x_max = verts[:,0].max()
mask_xmax = np.abs(verts[:, 0] - x_max) < 0.2
xmax_pts = verts[mask_xmax]
if len(xmax_pts) > 0:
    print(f"\n--- X最大面 (X≈{x_max:.1f}) ---")
    print(f"  Y: min={xmax_pts[:,1].min():.2f}, max={xmax_pts[:,1].max():.2f}")
    print(f"  Z: min={xmax_pts[:,2].min():.2f}, max={xmax_pts[:,2].max():.2f}")
    print(f"  点数: {len(xmax_pts)}")

# Y 最小/最大面上的点
y_min = verts[:,1].min()
y_max = verts[:,1].max()
mask_ymin = np.abs(verts[:, 1] - y_min) < 0.2
mask_ymax = np.abs(verts[:, 1] - y_max) < 0.2
ymin_pts = verts[mask_ymin]
ymax_pts = verts[mask_ymax]
if len(ymin_pts) > 0:
    print(f"\n--- Y最小面 (Y≈{y_min:.1f}) ---")
    print(f"  X: min={ymin_pts[:,0].min():.2f}, max={ymin_pts[:,0].max():.2f}")
    print(f"  Z: min={ymin_pts[:,2].min():.2f}, max={ymin_pts[:,2].max():.2f}")
    print(f"  点数: {len(ymin_pts)}")
if len(ymax_pts) > 0:
    print(f"\n--- Y最大面 (Y≈{y_max:.1f}) ---")
    print(f"  X: min={ymax_pts[:,0].min():.2f}, max={ymax_pts[:,0].max():.2f}")
    print(f"  Z: min={ymax_pts[:,2].min():.2f}, max={ymax_pts[:,2].max():.2f}")
    print(f"  点数: {len(ymax_pts)}")

# Z 最小/最大面上的点
z_min = verts[:,2].min()
z_max = verts[:,2].max()
mask_zmin = np.abs(verts[:, 2] - z_min) < 0.2
mask_zmax = np.abs(verts[:, 2] - z_max) < 0.2
zmin_pts = verts[mask_zmin]
zmax_pts = verts[mask_zmax]
if len(zmin_pts) > 0:
    print(f"\n--- Z最小面 (Z≈{z_min:.1f}) ---")
    print(f"  X: min={zmin_pts[:,0].min():.2f}, max={zmin_pts[:,0].max():.2f}")
    print(f"  Y: min={zmin_pts[:,1].min():.2f}, max={zmin_pts[:,1].max():.2f}")
    print(f"  点数: {len(zmin_pts)}")
if len(zmax_pts) > 0:
    print(f"\n--- Z最大面 (Z≈{z_max:.1f}) ---")
    print(f"  X: min={zmax_pts[:,0].min():.2f}, max={zmax_pts[:,0].max():.2f}")
    print(f"  Y: min={zmax_pts[:,1].min():.2f}, max={zmax_pts[:,1].max():.2f}")
    print(f"  点数: {len(zmax_pts)}")

# 分析 Y=150 截面 (中间Y) 看 XZ 轮廓
mask_y150 = np.abs(verts[:, 1] - 150.0) < 1.0
y150_pts = verts[mask_y150]
if len(y150_pts) > 0:
    print(f"\n--- Y=150截面 ---")
    print(f"  X: min={y150_pts[:,0].min():.2f}, max={y150_pts[:,0].max():.2f}")
    print(f"  Z: min={y150_pts[:,2].min():.2f}, max={y150_pts[:,2].max():.2f}")

# 整体结论
print(f"\n=== 总结 ===")
print(f"整体包围盒: X[{x_min:.0f}, {x_max:.0f}] Y[{y_min:.0f}, {y_max:.0f}] Z[{z_min:.0f}, {z_max:.0f}]")
print(f"尺寸: {x_max-x_min:.0f} x {y_max-y_min:.0f} x {z_max-z_min:.0f} mm")
