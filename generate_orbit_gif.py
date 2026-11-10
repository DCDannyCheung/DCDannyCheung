"""
Kepler Elliptical Orbit Animation Generator (v2 — manual frame rendering)
Renders each frame as an independent PNG, then assembles them into a GIF
with PIL. This avoids the matplotlib/Pillow writer's frame-palette issues.

Orbit equation chain:
  1) M = E - e*sin(E)           (Kepler's equation, solved via Newton-Raphson)
  2) tan(ν/2) = √((1+e)/(1-e)) * tan(E/2)   (eccentric → true anomaly)
  3) r = a(1-e²) / (1 + e*cos ν)            (orbit equation)
  4) x = r*cos ν,  y = r*sin ν              (Cartesian coordinates)
  5) v = √(μ(2/r - 1/a))                    (vis-viva equation)
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import io
import os

# ─── Orbit Parameters ───────────────────────────────────────────────
a = 1.0          # semi-major axis
e = 0.5          # eccentricity
mu = 1.0         # gravitational parameter (normalized)
period = 2 * np.pi * np.sqrt(a**3 / mu)

# ─── Solve Kepler's Equation ────────────────────────────────────────
def solve_kepler(M, e, tol=1e-10, max_iter=100):
    E = M.copy()
    for _ in range(max_iter):
        dE = (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
        E -= dE
        if np.all(np.abs(dE) < tol):
            break
    return E

def true_anomaly(E, e):
    return 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2),
                           np.sqrt(1 - e) * np.cos(E / 2))

def orbit_radius(nu, a, e):
    return a * (1 - e**2) / (1 + e * np.cos(nu))

# ─── Compute Orbit ──────────────────────────────────────────────────
N_frames = 80
M_vals = np.linspace(0, 2 * np.pi, N_frames, endpoint=False)
E_vals = solve_kepler(M_vals, e)
nu_vals = true_anomaly(E_vals, e)
r_vals = orbit_radius(nu_vals, a, e)
sat_x = r_vals * np.cos(nu_vals)
sat_y = r_vals * np.sin(nu_vals)

# Full orbit for background
theta_full = np.linspace(0, 2 * np.pi, 500)
r_full = orbit_radius(theta_full, a, e)
orbit_x = r_full * np.cos(theta_full)
orbit_y = r_full * np.sin(theta_full)

# ─── Render Each Frame ──────────────────────────────────────────────
plt.rcParams['font.family'] = ['DejaVu Sans']

# Use a fixed DPI and figure size so every frame is identical
FIG_SIZE = 6       # inches
DPI = 100          # → 600×600 pixels
FPS = 15
trail_max = 35
sweep_window = 12

# Colors (GitHub dark theme)
BG       = '#0d1117'
ORBIT_C  = '#58a6ff'
BODY_C   = '#f0c674'
SAT_C    = '#58a6ff'
RADIUS_C = '#79c0ff'
AREA_C   = '#1f6feb'
TEXT_C   = '#8b949e'
TITLE_C  = '#58a6ff'
PERI_C   = '#3fb950'
APO_C    = '#f85149'
AXIS_C   = '#30363d'

output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'orbit-animation.gif')

frames_pil = []
trail_x = []
trail_y = []

for i in range(N_frames):
    fig, ax = plt.subplots(figsize=(FIG_SIZE, FIG_SIZE), facecolor=BG)
    ax.set_facecolor(BG)
    ax.set_aspect('equal')

    margin = 0.25
    ax.set_xlim(-a - margin, a + margin)
    ax.set_ylim(-a - margin, a + margin)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Orbit ellipse
    ax.plot(orbit_x, orbit_y, color=ORBIT_C, linewidth=1.5, alpha=0.4, linestyle='--')

    # Reference axes
    ax.axhline(y=0, color=AXIS_C, linewidth=0.5, alpha=0.3)
    ax.axvline(x=0, color=AXIS_C, linewidth=0.5, alpha=0.3)

    # Central body + glow
    ax.add_patch(plt.Circle((0, 0), 0.12, color=BODY_C, alpha=0.08, zorder=3))
    ax.add_patch(plt.Circle((0, 0), 0.09, color=BODY_C, alpha=0.2, zorder=4))
    ax.add_patch(plt.Circle((0, 0), 0.06, color=BODY_C, zorder=5))

    # Perigee / Apogee markers
    perigee_x = a * (1 - e)
    apogee_x  = -a * (1 + e)
    ax.plot(perigee_x, 0, 'o', color=PERI_C, markersize=5, zorder=6)
    ax.plot(apogee_x, 0, 'o', color=APO_C, markersize=5, zorder=6)
    ax.annotate('Perigee', xy=(perigee_x, 0), xytext=(perigee_x + 0.08, -0.13),
                color=PERI_C, fontsize=9, alpha=0.8)
    ax.annotate('Apogee', xy=(apogee_x, 0), xytext=(apogee_x - 0.38, -0.13),
                color=APO_C, fontsize=9, alpha=0.8)

    # Trail
    trail_x.append(sat_x[i])
    trail_y.append(sat_y[i])
    if len(trail_x) > trail_max:
        trail_x.pop(0)
        trail_y.pop(0)
    if len(trail_x) > 1:
        ax.plot(trail_x, trail_y, '-', color=SAT_C, linewidth=1.5, alpha=0.5, zorder=7)

    # Area sweep
    start_idx = max(0, i - sweep_window)
    sweep_x = [0] + sat_x[start_idx:i+1].tolist() + [0]
    sweep_y = [0] + sat_y[start_idx:i+1].tolist() + [0]
    ax.add_patch(patches.Polygon(list(zip(sweep_x, sweep_y)), closed=True,
                                 alpha=0.15, color=AREA_C, zorder=2))

    # Radius vector
    ax.plot([0, sat_x[i]], [0, sat_y[i]], '-', color=RADIUS_C, linewidth=1, alpha=0.5, zorder=6)

    # Satellite + glow
    ax.plot(sat_x[i], sat_y[i], 'o', color=SAT_C, markersize=30, alpha=0.08, zorder=8)
    ax.plot(sat_x[i], sat_y[i], 'o', color=SAT_C, markersize=20, alpha=0.2, zorder=9)
    ax.plot(sat_x[i], sat_y[i], 'o', color=SAT_C, markersize=10, zorder=10)

    # Title
    ax.text(0.5, 1.02, 'Kepler Elliptical Orbit',
            transform=ax.transAxes, ha='center', va='bottom',
            color=TITLE_C, fontsize=15, fontweight='bold')

    # Info readouts
    r = r_vals[i]
    nu_deg = np.degrees(nu_vals[i] % (2 * np.pi))
    v = np.sqrt(mu * (2 / r - 1 / a))
    M_deg = np.degrees(M_vals[i] % (2 * np.pi))
    E_deg = np.degrees(E_vals[i] % (2 * np.pi))

    ax.text(0.02, 0.98,
            f'r = {r:.4f}\n'
            f'v = {nu_deg:6.1f} deg\n'
            f'v = {v:.4f}',
            transform=ax.transAxes, va='top', color=TEXT_C, fontsize=9,
            fontfamily='monospace')

    ax.text(0.98, 0.98,
            f'M = {M_deg:6.1f} deg\n'
            f'E = {E_deg:6.1f} deg\n'
            f'e = {e}',
            transform=ax.transAxes, va='top', ha='right', color=TEXT_C, fontsize=9,
            fontfamily='monospace')

    # Render to PNG in memory — fixed size, no tight bbox (would crop inconsistently)
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=DPI, facecolor=BG,
                bbox_inches=None, pad_inches=0)
    plt.close(fig)
    buf.seek(0)
    img = Image.open(buf).convert('P', palette=Image.ADAPTIVE, colors=256)
    frames_pil.append(img)

# ─── Assemble GIF ───────────────────────────────────────────────────
frame_dur = int(1000 / FPS)  # ms per frame

frames_pil[0].save(
    output_path,
    save_all=True,
    append_images=frames_pil[1:],
    duration=frame_dur,
    loop=0,           # 0 = infinite loop
    optimize=True,
    disposal=2        # clear frame before drawing next (no ghosting)
)

size_kb = os.path.getsize(output_path) / 1024
print(f"GIF saved: {output_path}")
print(f"Size: {size_kb:.0f} KB")
print(f"Frames: {N_frames}, FPS: {FPS}, Duration: {N_frames/FPS:.1f}s")
print(f"Dimensions: {frames_pil[0].size}")
print(f"Orbit: a={a}, e={e}, period={period:.4f}")
