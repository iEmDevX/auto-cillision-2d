#!/usr/bin/env python3
"""
Simple demo: Load the example sprite and visualize its collision polygons
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

print("=" * 60)
print("🎮 Collision Polygon Demo")
print("=" * 60)
print()

# Load the example sprite
print("📁 Loading example/base.png...")
img = Image.open("example/base.png")
print(f"   Size: {img.size}")
print(f"   Mode: {img.mode}")
print()

# Load the collision data
print("📁 Loading example/base.json...")
with open("example/base.json", "r") as f:
    polygons = json.load(f)
print(f"   Total polygons: {len(polygons)}")
print(f"   Total vertices: {sum(len(p) for p in polygons)}")
print()

# Analyze polygons
print("📊 Polygon statistics:")
vertex_counts = {}
for poly in polygons:
    count = len(poly)
    vertex_counts[count] = vertex_counts.get(count, 0) + 1

for vertices, count in sorted(vertex_counts.items()):
    print(f"   {vertices} vertices: {count} polygon(s)")
print()

# Sample polygons
print("🔍 Sample polygons:")
for i in range(min(3, len(polygons))):
    print(f"   Polygon {i+1}: {polygons[i]}")
print()

# Visualize
print("🎨 Creating visualization...")
fig, axes = plt.subplots(1, 2, figsize=(15, 10))

# Left: Original sprite
axes[0].imshow(img)
axes[0].set_title("Original Sprite", fontsize=16, fontweight='bold')
axes[0].axis('off')

# Right: Sprite with collision overlay
axes[1].imshow(img, alpha=0.5)

# Draw all collision polygons
colors = plt.cm.rainbow(np.linspace(0, 1, len(polygons)))
for i, (poly, color) in enumerate(zip(polygons, colors)):
    poly_array = np.array(poly)
    # Close the polygon by adding the first point at the end
    poly_closed = np.vstack([poly_array, poly_array[0]])
    axes[1].plot(poly_closed[:, 0], poly_closed[:, 1], 
                color=color, linewidth=1.5, alpha=0.7)
    
    # Draw vertices
    axes[1].scatter(poly_array[:, 0], poly_array[:, 1], 
                   color=color, s=10, alpha=0.8, zorder=5)

axes[1].set_title(f"Collision Polygons ({len(polygons)} shapes)", 
                 fontsize=16, fontweight='bold')
axes[1].axis('off')

# Add info text
info_text = f"""
Sprite: base.png
Size: {img.size[0]}x{img.size[1]} pixels
Polygons: {len(polygons)}
Total vertices: {sum(len(p) for p in polygons)}
Avg vertices/polygon: {sum(len(p) for p in polygons) / len(polygons):.1f}
"""
fig.text(0.5, 0.02, info_text, ha='center', fontsize=10, 
         family='monospace', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.subplots_adjust(bottom=0.1)

# Save the visualization
output_path = "output/preview/demo_visualization.png"
plt.savefig(output_path, dpi=150, bbox_inches='tight')
print(f"   ✅ Saved to: {output_path}")
print()

print("=" * 60)
print("✨ Demo complete!")
print("=" * 60)
print()
print("The visualization shows:")
print("  - Left: Original sprite with alpha transparency")
print("  - Right: Collision polygons overlaid on sprite")
print()
print("Each colored line represents a collision polygon.")
print("Points show the vertices (max 8 per polygon).")
print()
