#!/bin/env python
# -*- coding: utf-8 -*-

import os, sys
# Add path to PYTHONPATH
sys.path.append("/home/ysilvy/Density_bining/Yona_analysis/programs")
from netCDF4 import Dataset as open_ncfile
import matplotlib.pyplot as plt
from maps_matplot_lib import defVarmme, defVarDurack, remapToZ, zon_2Dz, custom_div_cmap, modelagree
import numpy as np
import datetime


# -------------------------------------------------------------------------------
#                                Define work
# -------------------------------------------------------------------------------

# -- Choose what to compute
# name = 'mme_hist_histNat'
name = 'mme_hist'
# name = 'mme_1pctCO2vsPiC'
#name = 'mme_rcp85_histNat'

# -- Choose where to stop for 1%CO2 simulations : 2*CO2 (70 years) or 4*CO2 (140 years) or 1.4*CO2 (34 years)
focus_1pctCO2 = '2*CO2'  # 1.4 or 2*CO2 or 4*CO2

# output format
# outfmt = 'view'
outfmt = 'save'

# Model agreement level
agreelev = 0.6
modelAgree = True

valmask = 1.e20
basinN = 4


# -- Choose work files

indir_density = '/home/ysilvy/Density_bining/Yona_analysis/data/remaptoz/density/'

if name == 'mme_hist_histNat':
    indirh = '/data/ericglod/Density_binning/Prod_density_april15/mme_hist/'
    fileh_2d = 'cmip5.multimodel_Nat.historical.ensm.an.ocn.Omon.density_zon2D.nc'
    # fileh_2d = 'cmip5.CCSM4.historical.ensm.an.ocn.Omon.density.ver-v20121128_zon2D.nc'
    fileh_1d = 'cmip5.multimodel_Nat.historical.ensm.an.ocn.Omon.density_zon1D.nc'
    # fileh_1d = 'cmip5.CCSM4.historical.ensm.an.ocn.Omon.density.ver-v20121128_zon1D.nc'
    datah_2d = indirh + fileh_2d; datah_1d = indirh + fileh_1d
    indirhn = '/data/ericglod/Density_binning/Prod_density_april15/mme_histNat/'
    filehn_2d = 'cmip5.multimodel_Nat.historicalNat.ensm.an.ocn.Omon.density_zon2D.nc'
    # filehn_2d = 'cmip5.CCSM4.historicalNat.ensm.an.ocn.Omon.density.ver-v20121128_zon2D.nc'
    filehn_1d = 'cmip5.multimodel_Nat.historicalNat.ensm.an.ocn.Omon.density_zon1D.nc'
    # filehn_1d = 'cmip5.CCSM4.historicalNat.ensm.an.ocn.Omon.density.ver-v20121128_zon1D.nc'
    datahn_2d = indirhn + filehn_2d; datahn_1d = indirhn + filehn_1d
    fh2d = open_ncfile(datah_2d,'r')
    fh1d = open_ncfile(datah_1d,'r')
    fhn2d = open_ncfile(datahn_2d,'r')
    fhn1d = open_ncfile(datahn_1d,'r')

    # File for remapped density
    file = 'cmip5.multimodel_Nat.historical.remaptoz_density.zon2D.nc'
    fsigma = open_ncfile(indir_density+file,'r')

if name == 'mme_hist':
    indir = '/data/ericglod/Density_binning/Prod_density_april15/mme_hist/'
    file_2d = 'cmip5.multimodel_Nat.historical.ensm.an.ocn.Omon.density_zon2D.nc'
    file_1d = 'cmip5.multimodel_Nat.historical.ensm.an.ocn.Omon.density_zon1D.nc'
    data_2d = indir + file_2d
    data_1d = indir + file_1d
    fh2d = open_ncfile(data_2d, 'r')
    fh1d = open_ncfile(data_1d, 'r')

    # File for remapped density
    file = 'cmip5.multimodel_Nat.historical.remaptoz_density.zon2D.nc'
    fsigma = open_ncfile(indir_density+file,'r')


if name == 'mme_1pctCO2vsPiC':
    indir_1pctCO2 = '/data/ericglod/Density_binning/Prod_density_april15/mme_1pctCO2/'
    file_2d = 'cmip5.multimodel_piCtl.1pctCO2.ensm.an.ocn.Omon.density_zon2D.nc'
    # file_2d = 'cmip5.CCSM4.1pctCO2.ensm.an.ocn.Omon.density.ver-v20121128_zon2D.nc'
    file_1d = 'cmip5.multimodel_piCtl.1pctCO2.ensm.an.ocn.Omon.density_zon1D.nc'
    # file_1d = 'cmip5.CCSM4.1pctCO2.ensm.an.ocn.Omon.density.ver-v20121128_zon1D.nc'
    data_2d = indir_1pctCO2 + file_2d
    data_1d = indir_1pctCO2 + file_1d
    fh2d = open_ncfile(data_2d,'r')
    fh1d = open_ncfile(data_1d,'r')

    indir_piC = '/data/ericglod/Density_binning/Prod_density_april15/mme_piControl/'
    file_2d = 'cmip5.multimodel_1pct.piControl.ensm.an.ocn.Omon.density_zon2D.nc'
    # file_2d = 'cmip5.CCSM4.piControl.ensm.an.ocn.Omon.density.ver-v20130513_zon2D.nc'
    file_1d = 'cmip5.multimodel_1pct.piControl.ensm.an.ocn.Omon.density_zon1D.nc'
    # file_1d = 'cmip5.CCSM4.piControl.ensm.an.ocn.Omon.density.ver-v20130513_zon1D.nc'
    data_2d = indir_piC + file_2d
    data_1d = indir_piC + file_1d
    fhn2d = open_ncfile(data_2d,'r')
    fhn1d = open_ncfile(data_1d,'r')

    # File for remapped density
    file = 'cmip5.multimodel_piCtl.1pctCO2.'+focus_1pctCO2+'remaptoz_density.zon2D.nc'
    fsigma = open_ncfile(indir_density+file,'r')


if name == 'mme_rcp85_histNat':
    indir_rcp85 = '/data/ericglod/Density_binning/Prod_density_april15/mme_rcp85/'
    filercp85_2d = 'cmip5.multimodel_Nat.rcp85.ensm.an.ocn.Omon.density_zon2D.nc'
    filercp85_1d = 'cmip5.multimodel_Nat.rcp85.ensm.an.ocn.Omon.density_zon1D.nc'
    indirhn = '/data/ericglod/Density_binning/Prod_density_april15/mme_histNat/'
    filehn_2d = 'cmip5.multimodel_Nat.historicalNat.ensm.an.ocn.Omon.density_zon2D.nc'
    filehn_1d = 'cmip5.multimodel_Nat.historicalNat.ensm.an.ocn.Omon.density_zon1D.nc'
    fh2d = open_ncfile(indir_rcp85 + filercp85_2d, 'r')
    fh1d = open_ncfile(indir_rcp85 + filercp85_1d, 'r')
    fhn2d = open_ncfile(indirhn + filehn_2d, 'r')
    fhn1d = open_ncfile(indirhn + filehn_1d, 'r')

    file = 'cmip5.multimodel_Nat.rcp85.remaptoz_density.zon2D.nc'
    fsigma = open_ncfile(indir_density+file,'r')


# -------------------------------------------------------------------------------
#                                Build variables
# -------------------------------------------------------------------------------

# == Define variables ==

# -- Salinity or temperature
varname = defVarmme('salinity'); v = 'S'
# varname = defVarmme('temp'); v = 'T'

var = varname['var_zonal_w/bowl']

if name == 'mme_rcp85_histNat':
    minmax = varname['minmax_zonal_rcp85']
else:
    minmax = varname['minmax_zonal']
clevsm = varname['clevsm_zonal']
legVar = varname['legVar']
unit = varname['unit']


# == Read variables ==
lat = fh2d.variables['latitude'][:]
density = fh2d.variables['lev'][:]
basin = fh2d.variables['basin'][:]
# # Repeat density into (basin,density,latitude)
# lat2d,density2d = np.meshgrid(lat,density)
# density3d = np.repeat(density2d[np.newaxis,:,:],4,axis=0)
# Read remapped density
density_z = fsigma.variables['density'][:]

if name == 'mme_hist_histNat' or name == 'mme_rcp85_histNat':
    field2r = fh2d.variables[var][-5:,:,:,:] # historical or RCP8.5
    depthr = fh2d.variables['isondepth'][-5:,:,:,:]
    volumr = fh2d.variables['isonvol'][-5:,:,:,:]
    bowl2z = fh1d.variables['ptopdepth'][-5:,:,:]
    if name == 'mme_hist_histNat':
        field1r = fhn2d.variables[var][-5:,:,:] # historicalNat (last five years to average)
        bowl1z = fhn1d.variables['ptopdepth'][-5:,:,:]
    else :
        field1r = fhn2d.variables[var][:,:,:] # historicalNat (entire time series to average)
        bowl1z = fhn1d.variables['ptopdepth'][:,:,:]
    if name == 'mme_rcp85_histNat':
        labBowl = ['histNat', 'RCP8.5']
    else:
        labBowl = ['histNat', 'hist']

if name == 'mme_hist':
    field2r = fh2d.variables[var][-5:,:,:,:]
    field1r = fh2d.variables[var][88:93,:,:,:] # 1950
    depthr = fh2d.variables['isondepth'][-5:,:,:,:]
    volumr = fh2d.variables['isonvol'][-5:,:,:,:]
    bowl2z = fh1d.variables['ptopdepth'][-5:,:,:]
    bowl1z = fh1d.variables['ptopdepth'][88:93,:,:]
    bowlr = fh1d.variables['ptopsigma'][88:93,:,:]
    labBowl = ['1950','2000']
    if modelAgree:
        var_agreer = fh2d.variables['isonso' + 'Agree'][-5:,:,:,:]

if name == 'mme_1pctCO2vsPiC':
    if focus_1pctCO2 == '4*CO2':
        y1 = 134
        y2 = 140
    if focus_1pctCO2 == '2*CO2':
        y1 = 69
        y2 = 74
    if focus_1pctCO2 == '1.4*CO2':
        y1 = 33
        y2 = 38
    field2r = fh2d.variables[var][y1:y2,:,:,:] # 1pctCO2
    field1r = fhn2d.variables[var][-20:,:,:,:] # PiControl
    depthr = fh2d.variables['isondepth'][y1:y2,:,:,:]
    volumr = fh2d.variables['isonvol'][y1:y2,:,:,:]
    bowl2z = fh1d.variables['ptopdepth'][y1:y2,:,:]
    bowl1z = fhn1d.variables['ptopdepth'][-10:,:,:]
    labBowl = ['PiControl', focus_1pctCO2]

if v != 'V': # If not volume (but not tried on volume yet)
#     field2r[np.ma.nonzero(field2r>40)] = np.ma.masked
#     field1r[np.ma.nonzero(field1r>40)] = np.ma.masked

    # == Compute signal hist - histNat or 1pctCO2 - PiControl or rcp8.5 - histNat ==
    vardiffr = np.ma.average(field2r, axis=0) - np.ma.average(field1r, axis=0)

# == Average other variables ==
depthr = np.ma.average(depthr, axis=0)
volumr = np.ma.average(volumr, axis=0)
bowl2z = np.ma.average(bowl2z, axis=0)
bowl1z = np.ma.average(bowl1z, axis=0)
if name=='mme_hist' and modelAgree :
    var_agreer = np.ma.average(var_agreer, axis=0)
    bowlr = np.ma.average(bowlr,axis=0)
#     for ilat in range(len(lat)):
#         if np.ma.is_masked(bowlr[1,ilat]) == False:
#             inda = np.ma.nonzero(bowlr[1,ilat]>=density)
#             var_agreer[1,inda,ilat] = np.ma.masked
#         if np.ma.is_masked(bowlr[2,ilat]) == False:
#             indp = np.ma.nonzero(bowlr[2,ilat]>=density)
#             var_agreer[2,indp,ilat] = np.ma.masked
#         if np.ma.is_masked(bowlr[3,ilat]) == False:
#             indi = np.ma.nonzero(bowlr[3,ilat]>=density)
#             var_agreer[3,inda,ilat] = np.ma.masked



# == Bathymetry ==
# Read masks
fmask = open_ncfile('/home/ysilvy/Density_bining/Yona_analysis/data/170224_WOD13_masks.nc','r')
basinmask = fmask.variables['basinmask3'][:] # (latitude, longitude)
depthmask = fmask.variables['depthmask'][:] # (latitude, longitude)
# Create basin masks
mask_a = basinmask != 1
mask_p = basinmask != 2
mask_i = basinmask != 3
# Take max value along lon for each latitude of each basin --> gives us the bathymetry
depthmask_a = np.ma.array(depthmask, mask=mask_a)
bathy_a = np.ma.max(depthmask_a, axis=1)
depthmask_p = np.ma.array(depthmask, mask=mask_p)
bathy_p = np.ma.max(depthmask_p, axis=1)
depthmask_i = np.ma.array(depthmask, mask=mask_i)
bathy_i = np.ma.max(depthmask_i, axis=1)

bathy = np.ma.masked_all((basinN,len(lat)))
bathy[1,:] = bathy_a
bathy[2,:] = bathy_p
bathy[3,:] = bathy_i


# == Target grid for remapping ==

# targetz = [0.,5.,15.,25.,35.,45.,55.,65.,75.,85.,95.,105.,116.,128.,142.,158.,181.,216.,272.,364.,511.,732.,
# 1033.,1405.,1830.,2289.,2768.,3257.,3752.,4350.,4749.,5250.]

# WOA09 grid
# targetz = [0, 10, 20, 30, 50, 75, 100, 125, 150, 200, 250, 300, 400, 500, 600,
# 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1750, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500]

# WOA13 grid
targetz = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80,
   85, 90, 95, 100, 125, 150, 175, 200, 225, 250, 275, 300, 325, 350, 375,
   400, 425, 450, 475, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950,
   1000, 1050, 1100, 1150, 1200, 1250, 1300, 1350, 1400, 1450, 1500, 1550,
   1600, 1650, 1700, 1750, 1800, 1850, 1900, 1950, 2000, 2100, 2200, 2300,
   2400, 2500, 2600, 2700, 2800, 2900, 3000, 3100, 3200, 3300, 3400, 3500,
   3600, 3700, 3800, 3900, 4000, 4100, 4200, 4300, 4400, 4500, 4600, 4700,
   4800, 4900, 5000, 5100, 5200, 5300, 5400, 5500]


# == Remap ==
fieldz = remapToZ(vardiffr.data, depthr, volumr, targetz, bowl2z, bathy)
print('field remapped')
# density_z = remapToZ(density3d, depthr, volumr, targetz, bowl2z, bathy)
# print('density remapped')
if name=='mme_hist' and modelAgree:
    var_agreez = remapToZ(var_agreer.data, depthr, volumr, targetz, bowl2z, bathy)

# Mask bad values
if v=='S':
    fieldz[np.ma.nonzero(np.ma.abs(fieldz)>1.2)] = np.ma.masked
# if v=='T':
#     fieldz[np.ma.nonzero(np.ma.abs(fieldz)>2)] = np.ma.masked

# # Mask above bowl2z
# for ilat in range(len(lat)):
#     if np.ma.is_masked(bowl2z[1,ilat]) == False :
#         inda = np.ma.nonzero(bowl2z[1,ilat]>=targetz)
#         var_agreez[1,inda,ilat] = np.ma.masked
#     if np.ma.is_masked(bowl2z[2,ilat]) == False :
#         indp = np.ma.nonzero(bowl2z[2,ilat]>=targetz)
#         var_agreez[2,indp,ilat] = np.ma.masked
#     if np.ma.is_masked(bowl2z[3,ilat]) == False :
#         indi = np.ma.nonzero(bowl2z[3,ilat]>=targetz)
#         var_agreez[3,indi,ilat] = np.ma.masked

# -- Make variable bundles for each basin
varAtl = {'name': 'Atlantic', 'var_change': fieldz[1,:,:], 'bowl1': bowl1z[1,:], 'bowl2': bowl2z[1,:],
          'labBowl': labBowl, 'density':density_z[1,:,:]}
varPac = {'name': 'Pacific', 'var_change': fieldz[2,:,:], 'bowl1': bowl1z[2,:], 'bowl2': bowl2z[2,:],
          'labBowl': labBowl, 'density':density_z[2,:,:]}
varInd = {'name': 'Indian', 'var_change': fieldz[3,:,:], 'bowl1': bowl1z[3,:], 'bowl2': bowl2z[3,:],
          'labBowl': labBowl, 'density':density_z[3,:,:]}


# -------------------------------------------------------------------------------
#                                Plot
# -------------------------------------------------------------------------------

domzed = [0,500,2000]

# -- Create figure and axes instances
fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(17, 5))

# -- color map
cmap = custom_div_cmap()

# -- levels
levels = np.linspace(minmax[0],minmax[1],minmax[2]) # Change
#levels = np.arange(33.5,35.5,0.2) # Mean salinity
#levels = np.arange(-2,30,2) # Mean temperature
#levels = np.arange(0,701,50) # Mean volume

ext_cmap = 'both'
contourDict = {'cmap':cmap, 'levels':levels, 'ext_cmap':ext_cmap,'isopyc':False}

# -- Contourf of signal
cnplot = zon_2Dz(plt, axes[0,0], axes[1,0], 'left', lat, targetz, varAtl,
                 contourDict, domzed)
cnplot = zon_2Dz(plt, axes[0,1], axes[1,1], 'mid', lat, targetz, varPac,
                 contourDict, domzed)
cnplot = zon_2Dz(plt, axes[0,2], axes[1,2], 'right', lat, targetz, varInd,
                 contourDict, domzed)

if name=='mme_hist' and modelAgree:
    modelagree(axes[0,0],axes[1,0],agreelev,lat,targetz,var_agreez[1,:,:])
    modelagree(axes[0,1],axes[1,1],agreelev,lat,targetz,var_agreez[2,:,:])
    modelagree(axes[0,2],axes[1,2],agreelev,lat,targetz,var_agreez[3,:,:])

# Bathymetry
# for i in range(3):
#     axes[0,i].fill_between(lat,[targetz[-1]]*len(lat),bathy[i+1,:],facecolor='0.7')
#     axes[1,i].fill_between(lat,[targetz[-1]]*len(lat),bathy[i+1,:],facecolor='0.7')

plt.subplots_adjust(hspace=.0001, wspace=0.05, left=0.04, right=0.86)

# -- Add colorbar
cb = plt.colorbar(cnplot[0], ax=axes.ravel().tolist(), ticks=levels[::3], fraction=0.015, shrink=2.0, pad=0.05)
cb.set_label('%s (%s)' % (legVar, unit), fontweight='bold')

# -- Add Title text
if name == 'mme_hist_histNat':
    plotTitle = '%s changes %s' %(legVar,name)
    plotName = 'remapping_' + name + '_' + legVar
    figureDir = 'models/zonal_remaptoz/'
if name == 'mme_hist':
    plotTitle = '%s changes (2000-1950), %s' %(legVar, name)
    plotName = 'remapping_' + name + '_' + legVar
    if modelAgree:
        plotName = 'remapping_' + name + '_' + legVar + '_modelAgree'
    figureDir = 'models/zonal_remaptoz/'
if name == 'mme_1pctCO2vsPiC':
    plotTitle  = '%s changes %s, %s' %(legVar,name,focus_1pctCO2)
    plotName = 'remapping_' + name + '_' + focus_1pctCO2 + '_' + legVar
    figureDir = 'models/zonal_remaptoz/'
if name == 'mme_rcp85_histNat':
    plotTitle = '%s changes %s' %(legVar,name)
    plotName = 'remapping_' + name + '_' + legVar + '_meanhistNat'
    figureDir = 'models/zonal_remaptoz/'

fig.suptitle(plotTitle, fontsize=14, fontweight='bold')
plt.figtext(.004,.65,'Pseudo-depth (m)',rotation='vertical',fontweight='bold')

# Date
now = datetime.datetime.now()
date = now.strftime("%Y-%m-%d")

plt.figtext(.5,.01,'Computed by : remap_to_z_changes.py,  '+date,fontsize=9,ha='center')
if name == 'mme_hist' and modelAgree:
    plt.figtext(.2,.01,'Model agreement level : ' + str(agreelev),fontsize=9,ha='center')

if outfmt == 'view':
    plt.show()
else:
    plt.savefig('/home/ysilvy/figures/'+figureDir+plotName+'.pdf', bbox_inches='tight')
