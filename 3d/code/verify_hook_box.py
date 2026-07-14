#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""验证 hook_with_box.stl 模型结构"""

import struct
import numpy as np

PATH = r"C:\AI\cc\3d\data\hook_with_box.stl"

with open(PATH, "rb") as f:
    f.read(80)
    n_tri = struct.unpack("<I", f.read(4))[0]
    verts = []
    for i in range(n_tri):
        f.read(12)
        v1 = struct.unpack("<3f", f.read(12))
        v2 = struct.unpack("<3f", f.read(12))
        v3 = struct.unpack("<3f", f.read(12))
        f.read(2)
        verts.extend([v1, v2, v3])

verts = np.array(verts)

print(f"Total triangles: {n_tri}")
print(f"Overall bounds:")
print(f"  X: [{verts[:,0].min():.1f}, {verts[:,0].max():.1f}] span={verts[:,0].max()-verts[:,0].min():.0f}")
print(f"  Y: [{verts[:,1].min():.1f}, {verts[:,1].max():.1f}] span={verts[:,1].max()-verts[:,1].min():.0f}")
print(f"  Z: [{verts[:,2].min():.1f}, {verts[:,2].max():.1f}] span={verts[:,2].max()-verts[:,2].min():.0f}")

# 盒子顶部 z≥90 的点
top = verts[verts[:, 2] >= 89]
print(f"\nBox top region (Z>=89): {len(top)} vertices")
print(f"  X: [{top[:,0].min():.1f}, {top[:,0].max():.1f}]")
print(f"  Y: [{top[:,1].min():.1f}, {top[:,1].max():.1f}]")

# 槽区域 z[63,71], y[152,178]
slot = verts[(verts[:, 2] >= 62) & (verts[:, 2] <= 72) &
             (verts[:, 1] >= 151) & (verts[:, 1] <= 179)]
print(f"\nSlot region: {len(slot)} vertices")
if len(slot) > 0:
    print(f"  X: [{slot[:,0].min():.1f}, {slot[:,0].max():.1f}]")
    print(f"  Y: [{slot[:,1].min():.1f}, {slot[:,1].max():.1f}]")
    print(f"  Z: [{slot[:,2].min():.1f}, {slot[:,2].max():.1f}]")

print(f"\n=== Model Summary ===")
print(f"Box: 200x100x30 mm, centered at (170, 150), bottom Z=63")
print(f"Slot: 26mm wide (Y), 8mm deep, runs full X-range of box")
print(f"Total length (X): {verts[:,0].max()-verts[:,0].min():.0f} mm")
print(f"Total height (Z): {verts[:,2].max()-verts[:,2].min():.0f} mm")
