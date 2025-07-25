import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.cm as cm
from scipy.ndimage import gaussian_filter
import os

file1 = "cont_0_1.dat"
file2 = "XXXX.dat"

pd = pd.read_csv(file1, sep='\s+')
cont_1 = pd_cycle.iloc[:,1]
list_1 = cont_1.tolist()

pd = pd.read_csv(file2, sep='\s+')
cont_1 = pd_cycle.iloc[:,1]
list_2 = cont_1.tolist()


X = list_1 #list_one require: python list or numpy array, you can load as: X=value
Y = list_2 #list_two require: python list or numpy array
# Please make sure X = Y, you can use print(len(X)) to comform

z,x,y = np.histogram2d(X,Y, bins=30) # bin mean space splite between one axis

# calculate the Z(energy) by paper
F = -np.log(z)
F[F == np.inf] = 0

extent = [x[0], x[-1], y[0], y[-1]]

# Using gaussian filter to make graph to be smooth
hist_smooth = gaussian_filter(F, sigma=0)
plt.figure(figsize=(12,10), dpi=300)

# Using this to plot outline, modify linewidths to change the line width.
#plt.contour(hist_smooth.T, 10, colors='black',linewidths=0.3, linestyles='solid', extent=extent)

# Plot contour graph, modify vmax and vmin to fit your value
#plt.contourf(hist_smooth.T, 10, cmap="gnuplot2", extent=extent, vmax=0, vmin=-4)
plt.contourf(hist_smooth.T, 10, cmap=cm.jet_r, extent=extent)

# add limitation to x and y axis
#plt.xlim(40,130)
#plt.ylim(0,100)

# plot colorbar or not
plt.colorbar()
plt.savefig(f"tot0_hb_2DFEL.eps", dpi=300)
plt.savefig(f"tot0_hb_2DFEL.png", dpi=300)
