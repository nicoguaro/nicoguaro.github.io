# -*- coding: utf-8 -*-
"""
Duplicating Hankel plot from Abramowitz and Stegun.

This was inspired by John Cook's post:


  https://www.johndcook.com/blog/2025/01/22/duplicating-hankel-plot-from-as/

The original image is located at

  https://personal.math.ubc.ca/~cbm/aands/page_359.htm


@author: Nicolás Guarín-Zapata
@date: April 2025
"""

  
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import hankel1


#%% Data
y, x = np.mgrid[-1.5:1.5:2500j, -4:2:5000j]
z = x + 1j*y
H = hankel1(0, z)

abs_H = np.abs(H)
abs_H[(x < 0) *  (np.abs(y) < 0.01)] = np.nan
levels_abs = np.arange(0.2, 3.3, 0.2)


arg_H = np.rad2deg(np.angle(H))
arg_H[(x < 0) *  (np.abs(y) < 0.01)] = np.nan
arg_H[arg_H < -179] += 360
arg_H[arg_H < -178] = np.nan
levels_arg = np.arange(-165, 181, 15)


#%% Plots setup
labels = True
manual_labels = True


#%% Ploting
fig, ax = plt.subplots(figsize=(12, 6))

# Jump line
plt.plot([-4, 0], [0, 0], color="black", linewidth=3, zorder=3)

# Contours
abs_contours = plt.contour(x, y, abs_H, levels_abs, colors="black",
                            linestyles="solid", zorder=4)
arg_contours = plt.contour(x, y, arg_H, levels_arg, colors="#757575",
                            linestyles="solid", zorder=6)

# Figure details
plt.xticks(np.arange(-4, 2.5, 0.5))
plt.yticks(np.arange(-1.5, 2, 0.5))

plt.xlabel("Real axis")
plt.ylabel("Imaginary axis")

plt.grid("True", color="#BDBDBD", zorder=3)
plt.axis("image")

# Labels
if labels:
    ax.clabel(abs_contours, levels_abs, fontsize=8, fmt="%.1f",
              use_clabeltext=True, manual=manual_labels, zorder=5)
    ax.clabel(arg_contours, levels_arg, fontsize=8, fmt="%d°",
              colors="#757575",
              use_clabeltext=True, manual=manual_labels, zorder=6)

plt.savefig("abramowitz_stegun-hankel-manual.svg", bbox_inches="tight")
plt.show()