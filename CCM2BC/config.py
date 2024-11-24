wrf_dir="/home/u002/CCM/wrf"
#for main domain
domain=1
wrf_input_file=f"wrfinput_d0{domain}"
wrf_bdy_file="wrfbdy_d01"
wrf_met_dir="/home/u002/CCM/wrf"
wrf_met_files=f"met_em.d0{domain}.80*"
mera_dir="/home/u002/CCM/CCM2WPS"
mera_files="CCM_400.inst3_3d_aer_Np.1980.nc"
do_IC=True
do_BC=True if domain==1 else False # True only for first domain (domain=1); False For nested domain no need (domain > 1)
CHEMOPT='GOCART'  # 'MOSAIC'
spc_map = [ 'DUST_1 -> 1.0*[DU001];1.e9',
            'DUST_2 -> 1.0*[DU002];1.e9',
            'DUST_3 -> 1.0*[DU003];1.e9',
            'DUST_4 -> 1.0*[DU004];1.e9',
            'DUST_5 -> 1.0*[DU005];1.e9',
            'SEAS_1 -> 1.0*[SS002];1.e9',
            'SEAS_2 -> 1.0*[SS003];1.e9',
            'SEAS_3 -> 1.0*[SS004];1.e9',
            'SEAS_4 -> 1.0*[SS005];1.e9',
            'so2 -> 0.453*[SO2];1.e6',
            'sulf -> 0.302*[SO4];1.e6',
            'BC1 -> 1.0*[BCPHOBIC];1.e9',
            'BC2 -> 1.0*[BCPHILIC];1.e9',
            'OC1 -> 1.0*[OCPHOBIC];1.e9', 
            'OC2 -> 1.0*[OCPHILIC];1.e9',
            'dms -> 0.467*[DMS];1.e6']

