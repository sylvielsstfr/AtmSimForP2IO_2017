import os
import math
import numpy as np
import UVspec

home = os.environ['HOME']+'/'
        
############################################################################
def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(f):
        os.makedirs(f)
#########################################################################
        


#####################################################################
# The program simulation start here
#   Variation of precipitable water
####################################################################

if __name__ == "__main__":

    
    ensure_dir('input')
    ensure_dir('output')
    ensure_dir('output/afglus')
    

    # Set up type of run
    runtype= 'aerosol_special' #aerosol_default# #'clearsky'#     
    #runtype='clearsky' #'clearsky'#     
    if runtype=='clearsky':
        outtext='clearsky'
    elif runtype=='aerosol_default':
        outtext='aerosol_default'
    else:
        outtext='aerosol_special'
        


    molmodel='reptran'


    # atmospheric models
    # afglus.dat
    # afglms.dat
    # afglmw.dat
    # afglt.dat
    # afglss.dat				
    # afglsw.dat		  

    #theatmospheres = np.array(['afglus','afglms','afglmw','afglt','afglss','afglsw'])
    theatmospheres = np.array(['afglus'])
    for atmosphere in theatmospheres:
        #if atmosphere != 'afglus':  # just take us standard sky
        #    break
        # loop on molecular model resolution
        #molecularresolution = np.array(['COARSE','MEDIUM','FINE'])    
        molecularresolution = np.array(['COARSE'])    
        for molres in molecularresolution:
            if molres=='COARSE':
                molresol ='coarse'
            elif molres=='MEDIUM':
                molresol ='medium'
            else:
                molresol ='fine'
           
            #libradtranpath = home+'develop/libRadtran/'
            #libradtranpath = home+'MacOsX/LSST/softs/radtran-2.0/libRadtran-2.0/'
            #libradtranpath = home+'MacOSX/External/libRadtran//libRadtran-2.0.1/'
            libradtranpath = os.environ['LIBRADTRANDIR']+'/' 
    
            # Rough estimate of center wavlengths of LSST filters. Should use filter functions
            # instead.

            # loop on air-masses
            airmassesval = np.array([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])
            
            O3_values=np.linspace(240.,320.,5)
     
            for airmass in airmassesval:
                
                
                AOD_quantiles_names = ['qaod5','qaod10','qaod50','qaod90','qaod95']   # percentages of the quantiles
                AOD_quantiles_values= [0.030,0.0328,0.0576,0.103,0.123]  # quantiles values for AOD @ LSST
                #AOD_quantiles_values= [0.010,0.0328,0.0576,0.103,0.523]  # quantiles values for AOD @ LSST

                PWV_quantiles_names = ['qpwv5','qpwv10','qpwv50','qpwv90','qpwv95']   # percentages of the quantiles
                PWV_quantiles_values= [1.184,1.1472,2.699,4.676,5.216]  # quantiles values for PWV @ LSST

                lambda0=532.   # CALIPSO Lidar wavelength
 
                # loop on PWV
                for index, pwv in enumerate(PWV_quantiles_values):
                   #aerosolstring=str(lambda0)+' '+str(AOD_quantiles_values[2])  # take the 50% quantile
                   aerosolstring=str(lambda0)+' '+str(AOD_quantiles_values[index])  # take the equavalent quantile
                   
                   precipitablewatervaporstring='H2O '+str(pwv) + ' MM'
                   print '----------------------------------------------------'
                   print index
                   
                   
                   ozonestring='O3 ' + str(O3_values[index])+ ' DU'
                   
                   
                   verbose=True
                   uvspec = UVspec.UVspec()
                   uvspec.inp["data_files_path"]  =  libradtranpath+'data'
                   #uvspec.inp["atmosphere_file"] = libradtranpath+'data/atmmod/afglt.dat'
                   uvspec.inp["atmosphere_file"] = libradtranpath+'data/atmmod/'+atmosphere+'.dat'
                   uvspec.inp["albedo"]           = '0.2'
                   uvspec.inp["rte_solver"] = 'disort'
                   uvspec.inp["mol_abs_param"] = molmodel + ' ' + molresol 

                   am=airmass/10.
                   sza=math.acos(1./am)*180./math.pi
        

                   if runtype=='aerosol_default':
                       uvspec.inp["aerosol_default"] = ''
                   elif runtype=='aerosol_special':
                       uvspec.inp["aerosol_default"] = ''
                       uvspec.inp["aerosol_set_tau_at_wvl"] = aerosolstring
                    
                   uvspec.inp["mol_modify"] = precipitablewatervaporstring
                   uvspec.inp["mol_modify2"] = ozonestring
                
                   uvspec.inp["output_user"] = 'lambda edir'
                   uvspec.inp["altitude"] = '2.663'
#                uvspec.inp["source"] = 'solar '+libradtranpath+'data/solar_flux/kurudz_1.0nm.dat'
                   uvspec.inp["source"] = 'solar '+libradtranpath+'data/solar_flux/kurudz_0.1nm.dat'
                   uvspec.inp["sza"]        = str(sza)
                   uvspec.inp["phi0"]       = '0'
#                    uvspec.inp["wavelength"]       = '250.0 5000.0'
                   uvspec.inp["wavelength"]       = '250.0 1200.0'
                   uvspec.inp["output_quantity"] = 'reflectivity' #'transmittance' #
                   uvspec.inp["quiet"] = ''

                   if "output_quantity" in uvspec.inp.keys():
                       outtextfinal=outtext+'_'+uvspec.inp["output_quantity"]

                   inp = 'input/UVSPEC_REPTRAN_SOLAR_ALT26_REFL_{}_{:2.0f}'.format(PWV_quantiles_names[index],airmass)+'.inp'
                   out = 'output/{}/UVSPEC_REPTRAN_SOLAR_ALT26_{}_{}_{:2.0f}'.format(atmosphere,molres,PWV_quantiles_names[index],airmass)+'.out'
                   uvspec.write_input(inp)
                   uvspec.run(inp,out,verbose,path=libradtranpath)

                # Read output
                #uu0 = read_uu_map(out,nphi,numu)
                #
                #out0uu = out+'_uu'
                #write_uu_map(out0uu,uu0,nphi,numu)
