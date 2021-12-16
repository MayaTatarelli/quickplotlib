#-----------------------------------------------------
# Python code for easy post-processing
# - Written by Julien Brillon
# - Email: julien.brillon@mail.mcgill.ca
# - McGill University
#-----------------------------------------------------
# Import libraries
import numpy as np # NumPy: contains basic numerical routines
import scipy # SciPy: contains additional numerical routines to numpy
import matplotlib.pyplot as plt # Matlab-like plotting
#-----------------------------------------------------
# plotting essentials
#-----------------------------------------------------
from matplotlib.lines import Line2D
from matplotlib import rc as matplotlibrc
matplotlibrc('text.latex', preamble='\usepackage{color}')
matplotlibrc('text', usetex=True)
matplotlibrc('font', family='serif')
clr = ['tab:blue','tab:red','tab:green','tab:orange','tab:purple','tab:brown']
mrkr = ['o','s','^','d','v','>','<']
lnstl = ['solid','dashed','dashdot','dotted']
# Font sizes
axisTitle_FontSize = 16
axisTickLabel_FontSize = 14
legend_fontSize = 16
fig_directory = "figures"
#-----------------------------------------------------
# define functions
#-----------------------------------------------------
def plotfxn(xdata=[],ydata=[],ylabel="ydata",xlabel="xdata",
			figure_filename="myfig",
			figure_filetype="pdf",
			title_label=" ",
			markers=False,
			ndata=1,
			legend_labels_tex=[],
			black_lines=False,
			xlimits=[],ylimits=[],
			log_axes=None,
			error_bars_on_curve_number=[],
			yerr_above=[],yerr_below=[],
			which_lines_dashed=[],
			nlegendcols=1,legend_on=True,legend_inside=True,
			remove_vertical_asymptotes_on_curve_number=[]):
	print("---------------------------------------------")
	#-----------------------------------------------------
	# pre-plotting data manipulation:
	#-----------------------------------------------------
	if(remove_vertical_asymptotes_on_curve_number!=[]):
		tolerance_for_vertical_asymptote_value_difference = 1.0
		for i in remove_vertical_asymptotes_on_curve_number:
			N = int(len(ydata[i]))
			for j in range(0,N-1):
				condition1 = ydata[i][j+1]*ydata[i][j]<0
				condition2 = np.abs(ydata[i][j+1]-ydata[i][j]) > tolerance_for_vertical_asymptote_value_difference
				if(condition1 and condition2):
					ydata[i][j+1]=np.nan; ydata[i][j]=np.nan;
	#-----------------------------------------------------
	# plotting:
	#-----------------------------------------------------
	print('Plotting: ' + figure_filename)
	if(legend_inside):
		fig, ax = plt.subplots(figsize=(6,6))
	else:
		fig, ax = plt.subplots(figsize=(9,6))
	plt.grid()
	ax.set_xlabel(xlabel,fontsize=axisTitle_FontSize)
	ax.set_ylabel(ylabel,rotation=90,fontsize=axisTitle_FontSize)
	if(title_label!=" "):
		plt.title(title_label,fontsize=axisTitle_FontSize)
	plt.setp(ax.get_xticklabels(),fontsize=axisTickLabel_FontSize); plt.setp(ax.get_yticklabels(),fontsize=axisTickLabel_FontSize);
	if(xlimits!=[]):
		ax.set_xlim(xlimits)
	if(ylimits!=[]):
		ax.set_ylim(ylimits)
	ls = lnstl[0]  # default line style (ls)
	lc = clr[0] # default line color (lc)
	if(black_lines):
		lc = 'k' # set color to black
		
	if(ndata>1):
		leg_elements = []
		for i in range(0,ndata):
			if(black_lines):
				ls = lnstl[i]
			else:
				lc = clr[i]
				if(i in which_lines_dashed):
					ls = "dashed"
				else:
					ls = lnstl[0]
			x = xdata[i]; y = ydata[i];
			if(markers):
				if(log_axes==None):
					if(error_bars_on_curve_number!=[] and i==error_bars_on_curve_number):
						yerr = np.array([yerr_below,yerr_above])
						fmt_string = lc+mrkr[i]
						plt.errorbar(x, y, yerr, fmt=fmt_string, mfc='None')
						# plt.errorbar(x, y, yerr, color=lc, marker=mrkr[i], markersize=6, mfc='None', linestyle='None')
					else:
						plt.plot(x, y, color=lc, marker=mrkr[i], markersize=6, mfc='None', linestyle=ls)
				elif(log_axes=="both"):
					plt.loglog(x, y, color=lc, marker=mrkr[i], markersize=6, mfc='None', linestyle=ls)
				elif(log_axes=="x"):
					plt.semilogx(x, y, color=lc, marker=mrkr[i], markersize=6, mfc='None', linestyle=ls)
				elif(log_axes=="y"):
					plt.semilogy(x, y, color=lc, marker=mrkr[i], markersize=6, mfc='None', linestyle=ls)
				leg_elements.append(Line2D([0],[0], label=legend_labels_tex[i], color=lc, marker=mrkr[i], markersize=6, mfc='None',linestyle=ls))
			else:
				leg_elements.append(Line2D([0],[0], label=legend_labels_tex[i], color=lc, linestyle=ls))
			if(log_axes==None):
				plt.plot(x, y, color=lc, linestyle=ls)
			elif(log_axes=="both"):
				plt.loglog(x, y, color=lc, linestyle=ls)
			elif(log_axes=="x"):
				plt.semilogx(x, y, color=lc, linestyle=ls)
			elif(log_axes=="y"):
				plt.semilogy(x, y, color=lc, linestyle=ls)
		if(legend_on):
			if(legend_inside):
				leg = plt.legend(handles=leg_elements, loc="best", ncol=nlegendcols, shadow=False, fancybox=True, fontsize=legend_fontSize, framealpha=1.0,edgecolor='inherit')
			else:
				leg = plt.legend(handles=leg_elements, loc="upper center", bbox_to_anchor=(1.2, 1.0), ncol=nlegendcols, shadow=False, fancybox=True, fontsize=legend_fontSize, framealpha=1.0,edgecolor='inherit')
	else:
		if(markers):
			if(log_axes==None):
				plt.plot(xdata, ydata, color=lc, marker=mrkr[0], markersize=6, mfc='None', linestyle='None')
			elif(log_axes=="both"):
				plt.loglog(xdata, ydata, color=lc, marker=mrkr[0], markersize=6, mfc='None', linestyle='None')
			elif(log_axes=="x"):
				plt.semilogx(xdata, ydata, color=lc, marker=mrkr[0], markersize=6, mfc='None', linestyle='None')
			elif(log_axes=="y"):
				plt.semilogy(xdata, ydata, color=lc, marker=mrkr[0], markersize=6, mfc='None', linestyle='None')
		if(log_axes==None):
			plt.plot(xdata, ydata, color=lc, linestyle=ls)
		elif(log_axes=="both"):
			plt.loglog(xdata, ydata, color=lc, linestyle=ls)
		elif(log_axes=="x"):
			plt.semilogx(xdata, ydata, color=lc, linestyle=ls)
		elif(log_axes=="y"):
			plt.semilogy(xdata, ydata, color=lc, linestyle=ls)
	plt.tight_layout()
	print('\t ... Saving figure ...')
	plt.savefig(fig_directory+"/"+figure_filename+'.'+figure_filetype,format=figure_filetype,dpi=500)
	plt.close()
	print('\t     Saved.')
	print("---------------------------------------------")