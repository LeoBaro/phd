#!/bin/bash

dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"


today=`date +%Y-%m-%d.%H:%M:%S`

echo "Output dir: $dir/ap_data_for_training_and_testing_$today" 

#echo "Generating AP data for bkg"
#python generate_ap_data.py \
#        -dd $DATA/obs/simtype_bkg_os_0_tobs_1800_irf_South_z40_average_LST_30m_emin_0.03_emax_0.15_roi_2.5 \
#        -t bkg \
#        -mp no \
#        -lim 100 \
#        -ws 10 \
#        -rr 0.2 \
#        -norm no \
#        -out $dir/ap_data_for_training_and_testing_$today

      
echo "Generating AP data for grb_os_900"
python generate_ap_data.py \
        -dd $DATA/obs/simtype_grb_os_900_tobs_1800_irf_South_z40_average_LST_30m_emin_0.03_emax_0.15_roi_2.5 \
        -t grb \
        -mp no \
        -lim 100 \
        -ws 10 \
        -rr 0.2 \
        -norm yes \
        -out $dir/ap_data_for_training_and_testing_$today