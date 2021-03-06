import argparse
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt

from rtapipe.analysis.models.anomaly_detector import AnomalyDetector
from rtapipe.analysis.dataset.dataset import APDataset

"""
Training with NOT-NORMALIZED samples (T integration)
python train.py \
    --bkg /data01/homes/baroncelli/phd/rtapipe/analysis/dataset/ap_data_for_training_and_testing_2021-07-21.10:22:32_NOT_NORMALIZED/simtype_bkg_os_0_tobs_1800_irf_South_z40_average_LST_30m_emin_0.03_emax_0.15_roi_2.5/integration_t_type_bkg_window_size_10_region_radius_0.2 \
    --grb /data01/homes/baroncelli/phd/rtapipe/analysis/dataset/ap_data_for_training_and_testing_2021-07-21.10:22:32_NOT_NORMALIZED/simtype_grb_os_900_tobs_1800_irf_South_z40_average_LST_30m_emin_0.03_emax_0.15_roi_2.5/integration_t_type_grb_window_size_10_region_radius_0.2

Training with NORMALIZED samples (T integration)
python train.py \
    --bkg /data01/homes/baroncelli/phd/rtapipe/analysis/dataset/ap_data_for_training_and_testing_2021-07-20.21:47:42_NORMALIZED/simtype_bkg_os_0_tobs_1800_irf_South_z40_average_LST_30m_emin_0.03_emax_0.15_roi_2.5/integration_t_type_bkg_window_size_10_region_radius_0.2 \
    --grb /data01/homes/baroncelli/phd/rtapipe/analysis/dataset/ap_data_for_training_and_testing_2021-07-20.21:47:42_NORMALIZED/simtype_grb_os_900_tobs_1800_irf_South_z40_average_LST_30m_emin_0.03_emax_0.15_roi_2.5/integration_t_type_grb_window_size_10_region_radius_0.2



Training with NOT-NORMALIZED samples (TE integration)
python train.py \
    --bkg /data01/homes/baroncelli/phd/rtapipe/analysis/dataset/ap_data_for_training_and_testing_2021-07-21.10:22:32_NOT_NORMALIZED/simtype_bkg_os_0_tobs_1800_irf_South_z40_average_LST_30m_emin_0.03_emax_0.15_roi_2.5/integration_te_type_bkg_window_size_10_region_radius_0.2 \
    --grb /data01/homes/baroncelli/phd/rtapipe/analysis/dataset/ap_data_for_training_and_testing_2021-07-21.10:22:32_NOT_NORMALIZED/simtype_grb_os_900_tobs_1800_irf_South_z40_average_LST_30m_emin_0.03_emax_0.15_roi_2.5/integration_te_type_grb_window_size_10_region_radius_0.2

Training with NORMALIZED samples (TE integration)
python train.py \
    --bkg /data01/homes/baroncelli/phd/rtapipe/analysis/dataset/ap_data_for_training_and_testing_2021-07-20.21:47:42_NORMALIZED/simtype_bkg_os_0_tobs_1800_irf_South_z40_average_LST_30m_emin_0.03_emax_0.15_roi_2.5/integration_te_type_bkg_window_size_10_region_radius_0.2  \
    --grb /data01/homes/baroncelli/phd/rtapipe/analysis/dataset/ap_data_for_training_and_testing_2021-07-20.21:47:42_NORMALIZED/simtype_grb_os_900_tobs_1800_irf_South_z40_average_LST_30m_emin_0.03_emax_0.15_roi_2.5/integration_te_type_grb_window_size_10_region_radius_0.2

"""


if __name__=='__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--bkg", type=str, required=True, help="The folder containing AP data (background only)")
    parser.add_argument("--grb", type=str, required=True, help="The folder containing AP data (grb)")
    args = parser.parse_args()

    ds = APDataset()
    ds.loadData(bkg=args.bkg, grb=args.grb)
    train, trainLabels, test, testLabels, val, valLabels = ds.getData()
    print(train.shape)
    print(trainLabels.shape)
    print(test.shape)
    print(testLabels.shape)

    # Params
    units = 32
    dropoutrate = 0.3
    epochs = 20
    batchSize = 30

    # Building the model
    # loadModelFrom="./single_feature_model"
    loadModelFrom = None
    lstm = AnomalyDetector(train[0].shape, units=units, dropoutRate=dropoutrate, loadModelFrom=loadModelFrom)

    # Compiling the model
    lstm.compile()

    lstm.summary()

    if lstm.isFresh():

        # Fitting the model
        lstm.fit(train, train, epochs=epochs, batchSize=batchSize, verbose=1, validation_data=(val, val),
                     plotLosses=True)    

        # Saving the model
        lstm.save("single_feature_model")


    lstm.computeThreshold(train, plotError=True)

    recostructions, _, mask = lstm.classify(test, plotError=True)

    lstm.plotPredictions2(test, testLabels, recostructions, mask, howMany=40)

  