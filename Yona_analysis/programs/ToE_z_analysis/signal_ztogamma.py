import sys
sys.path.append("/home/ysilvy/Density_bining/Yona_analysis/programs/")
sys.path.append("/home/ysilvy/Density_bining/")
import numpy as np
from netCDF4 import Dataset as open_ncfile
from maps_matplot_lib import defVarmme, zon_2Dz, custom_div_cmap, zonal_2D
#from modelsDef import defModels 
import glob
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import datetime
from binDensity import rhonGrid
from functions_z_analysis import maptogamma
from libToE import ToEdomainrcp85vshistNat

indirz = '/home/ysilvy/Density_bining/Yona_analysis/data/toe_zonal_z/toe_rcp85_histNat/'
indirr = '/home/ysilvy/Density_bining/Yona_analysis/data/toe_zonal/toe_rcp85_histNat/'

varname = defVarmme('salinity'); v = 'S'
#varname = defVarmme('temp'); v = 'T'
var = varname['var_zonal_w/bowl']
legVar = varname['legVar']
unit = varname['unit']

if v=='S':
    varName = 'salinity'
else:
    varName = 'temperature'

filez = 'cmip5.IPSL-CM5A-LR.r2i1p1.'+legVar+'_toe_zonal_rcp_histNat.nc'
fz = open_ncfile(indirz+filez,'r')
lat = fz.variables['latitude'][:]
lev = fz.variables['density'][:]

model = {'name':'IPSL-CM5A-LR'  ,'props':[6,3,11,156], 'picontrol':[1000],'correctFile':[0,0,0],
          'file_end_hist':'v20111119', 'file_end_histNat':'v20120430',
          'hist-rcp85':['r2i1p1','r3i1p1','r4i1p1']}
tstart = model['props'][2]
tend = model['props'][3]
model_name = filez.split('.')[1]
run = filez.split('.')[2]

# Read gamma(z) file
f = open_ncfile('/data/ysilvy/CMIP5_annual/so_thetao_gamma_Oan_IPSL-CM5A-LR_historical-rcp85_r2i1p1_185001-210012.nc')

# Density grid
targetrho, s_sax, del_s, N_s = rhonGrid(19, 26, 28.501, 0.2, 0.1)

# Define Gamma/depth relationship for mapping
gammaz = np.ma.average(f.variables['density'][tstart:tend+95,:,:,:],axis=0)

# Read signal
signal = fz.variables[varName+'_change'][:]

# Map to gamma
signal_gamma = maptogamma(signal,gammaz,targetrho)

# -- Make variable bundles for each basin
varAtl = {'name': 'Atlantic', 'var_change': signal_gamma[1,:,:], 'var_mean':None, 'bowl1': None, 'bowl2': None, 'labBowl': None}
varPac = {'name': 'Pacific', 'var_change': signal_gamma[2,:,:], 'var_mean':None, 'bowl1': None, 'bowl2': None, 'labBowl': None}
varInd = {'name': 'Indian', 'var_change': signal_gamma[3,:,:], 'var_mean':None, 'bowl1': None, 'bowl2': None, 'labBowl': None}

# density domain
rhomin = 21
rhomid = 26
rhomax = 28.5
domrho = [rhomin, rhomid, rhomax]

# -- Create figure and axes instances
fig12, axes12 = plt.subplots(nrows=2, ncols=3, figsize=(17, 5))

# -- Color map
cmap = custom_div_cmap()
# -- Unit
unit = varname['unit']
# -- Levels
minmax = varname['minmax_zonal_rcp85']
minmax = [-2,2,16]
levels = np.linspace(minmax[0], minmax[1], minmax[2])

# -- Contourf
# Atlantic
cnplot12 = zonal_2D(plt, 'total_mme', axes12[0,0], axes12[1,0], 'left', lat, lev, varAtl, domrho, cmap, levels)

# -- Add colorbar
cb12 = fig12.colorbar(cnplot12[1], ax=axes12.ravel().tolist(), ticks=levels[::3], fraction=0.015, shrink=2.0, pad=0.05)
cb12.set_label('%s' % (unit,), fontweight='bold')

# Pacific
cnplot12 = zonal_2D(plt, 'total_mme', axes12[0,1], axes12[1,1], 'mid', lat, lev, varPac, domrho, cmap, levels)

# Indian
cnplot12 = zonal_2D(plt, 'total_mme', axes12[0,2], axes12[1,2], 'right', lat, lev, varInd, domrho, cmap, levels)

# # == Plot ToE boxes on top ==
# # Read boses
# South_ST_a = ToEdomainrcp85vshistNat(model_name, 'Southern ST')[0]['Atlantic']
# South_ST_p = ToEdomainrcp85vshistNat(model_name, 'Southern ST')[0]['Pacific']
# South_ST_i = ToEdomainrcp85vshistNat(model_name, 'Southern ST')[0]['Indian']
# North_ST = ToEdomainrcp85vshistNat(model_name, 'Northern ST')[0]
# SO = ToEdomainrcp85vshistNat(model_name, 'SO')[0]
# NA = ToEdomainrcp85vshistNat(model_name, 'North Atlantic')[0]
# NP = ToEdomainrcp85vshistNat(model_name, 'North Pacific')[0]

# # Create a Rectangle patch
# rect_SouthST_a = patches.Rectangle((South_ST_a[0],South_ST_a[3]),South_ST_a[1]-South_ST_a[0],South_ST_a[3]-South_ST_a[2],linewidth=1,edgecolor='k',facecolor='none')

# # Add the patch to the Axes
# axes12[0,0].add_patch(rect_SouthST_a)
# axes12[1,0].add_patch(rect_SouthST_a)

plt.subplots_adjust(hspace=.01, wspace=0.05, left=0.04, right=0.86)

# -- Add title
plotTitle = legVar + ' signal, analyzed on pressure surfaces, mapped to gamma, RCP8.5 - histNat (last 5 years) \n' \
    '%s , %s '%(model_name,run)

plt.suptitle(plotTitle, fontweight='bold', fontsize=14, verticalalignment='top')

# Date
now = datetime.datetime.now()
date = now.strftime("%Y-%m-%d")

plt.figtext(.5,.02,'Computed by : signal_ztogamma.py  '+date,fontsize=9,ha='center')
plt.figtext(.004,.6,'Pseudo-density (kg.m-3)',rotation='vertical',fontweight='bold')


figureDir = 'models/ToE_z_analysis/'
plotName = 'signal'+v+'_zmappedtogamma_IPSL_r2i1p1_rcp85vshistNat'
#if fig == 'save':
#plt.savefig('/home/ysilvy/figures/'+figureDir+plotName+'.pdf', bbox_inches='tight')
