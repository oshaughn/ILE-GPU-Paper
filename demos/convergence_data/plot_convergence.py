#! /usr/bin/env python

# plot_posterior_corner.py
#
#  --posterior-file f1 --posterior-label n1 --posterior-file f2 --posterior-label n2 ...
#  --parameter p1 --parameter p2 ...
#
# EXAMPLE
#    python plot_posterior_corner.py --posterior-file downloads/TidalP4.dat --parameter lambda1 --parameter lambda2 --parameter mc
#   python plot_posterior_corner.py --parameter mc --parameter eta --posterior-file G298048/production_C00_cleaned_TaylorT4/posterior-samples.dat  --parameter lambdat
#
# USAGE
#    - hardcoded list of colors, used in order, for multiple plots
#

import lalsimutils
import lal
import numpy as np
import argparse

try:
    import matplotlib
    print " Matplotlib backend ", matplotlib.get_backend()
    if matplotlib.get_backend() is 'agg':
        fig_extension = '.png'
        bNoInteractivePlots=True
    else:
	matplotlib.use('agg')
        fig_extension = '.png'
        bNoInteractivePlots =True
    from matplotlib import pyplot as plt
    bNoPlots=False
except:
    print " Error setting backend"

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.lines as mlines
import corner

import our_corner
try:
    import bounded_kde
except:
    print " -No 1d kdes- "

dpi_base=200
legend_font_base=30
rc_params = {'backend': 'ps',
             'axes.labelsize': 16,
             'axes.titlesize': 16,
             'font.size': 30,
             'legend.fontsize': legend_font_base,
             'xtick.labelsize': 16,
             'ytick.labelsize': 16,
             #'text.usetex': True,
             'font.family': 'Times New Roman'}#,
             #'font.sans-serif': ['Bitstream Vera Sans']}#,
plt.rcParams.update(rc_params)


# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("--convergence-file",action='append',help="filename of *.dat file [standard LI output]")
parser.add_argument("--output",default='convergence',help="filename for plot")
parser.add_argument("--pdf",action='store_true',help="filename for plot")
parser.add_argument("--color",action='append')
parser.add_argument("--linestyle",action='append')
parser.add_argument("--label",action='append')
parser.add_argument("--use-legend",action='store_true')
opts=  parser.parse_args()
if opts.pdf:
    fig_extension='.pdf'


# Legend
color_list=['black', 'red', 'green', 'blue','yellow']
if opts.color:
    color_list  =opts.color + color_list
linestyle_list = ['-' for k in color_list]
if opts.linestyle:
    linestyle_list = opts.linestyle + linestyle_list
#linestyle_remap_contour  = {":", 'dotted', '-'
    
line_handles = []
corner_legend_location=None; corner_legend_prop=None
if opts.use_legend and opts.label:
    n_elem = len(opts.file)
    for indx in np.arange(n_elem):
        my_line = mlines.Line2D([],[],color=color_list[indx],linestyle=linestyle_list[indx],label=opts.label[indx])
        line_handles.append(my_line)

    corner_legend_location=(0.7, 1.0)
    corner_legend_prop = {'size':8}
# https://stackoverflow.com/questions/7125009/how-to-change-legend-size-with-matplotlib-pyplot
#params = {'legend.fontsize': 20, 'legend.linewidth': 2}
#plt.rcParams.update(params)


# Import
convergence_list = []
label_list = []
# Load posterior files
if opts.convergence_file:
 for fname in opts.convergence_file:
    samples = np.loadtxt(fname)
    # Save samples
    convergence_list.append(samples)



# Import
# Generate labels
#labels_tex = render_coordinates(opts.parameter)#map(lambda x: tex_dictionary[x], coord_names)
my_cmap_values=None
for pIndex in np.arange(len(convergence_list)):
    samples = convergence_list[pIndex]
    # Create data for corner plot
    dat = np.zeros( (len(samples),3) )
    dat[:,0] = samples[:,0]
    dat[:,1] = samples[:,1]
    dat[:,2] = 1/np.sqrt(samples[:,2])
    my_cmap_values = color_list[pIndex]
    plt.plot(dat[:,0], dat[:,1],c=my_cmap_values,ls=linestyle_list[pIndex])

plt.xlabel("iteration")
plt.xticks( dat[:,0])
plt.ylabel(r'$\ln Z$')
plt.savefig(opts.output+fig_extension)        # use more resolution, to make sure each image remains of consistent quality
