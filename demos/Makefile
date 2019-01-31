

ILE=$(shell which integrate_likelihood_extrinsic)
POST_GENERIC=$(shell which util_ConstructIntrinsicPosterior_GenericCoordinates.py)
PWD=$(shell pwd)

NPTS_START=100
NPTS_IT=20
DMAX=1000

ILE_MEM=2048
CIP_MEM=2048


EVENT_TIME=1000000014.236547946
APPROX=SEOBNRv4
APPROX_BNS=TaylorT4


###
### BBH 
###

mdc.xml.gz:
	util_WriteInjectionFile.py  --parameter m1 --parameter-value 35 --parameter m2 --parameter-value 30 --fname mdc --approx ${APPROX} --parameter tref --parameter-value ${EVENT_TIME} --parameter dist --parameter-value 200 --parameter fmin --parameter-value 20

zero_noise.cache: mdc.xml.gz
	util_WriteFrameAndCacheFromXML.sh mdc.xml.gz 0 zero_noise ${APPROX}

snr_table.dat: zero_noise.cache
	util_FrameZeroNoiseSNR.py --cache zero_noise.cache --psd-file H1=HLV-ILIGO_PSD.xml.gz  --psd-file L1=HLV-ILIGO_PSD.xml.gz  > snr_table.dat


HLV-ILIGO_PSD.xml.gz:
	./generate_iligo_psd

HLV-aLIGO_PSD.xml.gz:
	./generate_iligo_psd


STANDARD_ILE_OPTS=--n-chunk 10000 --time-marginalization --sim-xml overlap-grid.xml.gz --reference-freq 100.0 --adapt-weight-exponent 0.1  --event-time ${EVENT_TIME} --save-P 0.1 --cache-file ${PWD}/zero_noise.cache --fmin-template 10.0 --n-max 2000000 --fmax 1700.0 --save-deltalnL inf --l-max 2  --n-eff 50  --approximant ${APPROX} --adapt-floor-level 0.1 --maximize-only  --d-max ${DMAX}  --psd-file H1=${PWD}/HLV-ILIGO_PSD.xml.gz --psd-file L1=${PWD}/HLV-ILIGO_PSD.xml.gz --channel-name H1=FAKE-STRAIN --channel-name L1=FAKE-STRAIN --inclination-cosine-sampler --declination-cosine-sampler

test_workflow_nobatch: Makefile HLV-ILIGO_PSD.xml.gz zero_noise.cache
	(mkdir $@; exit 0)
#	(cd $@; echo X  --parameter mc --parameter-range '[30,60]' --parameter eta --parameter-range '[0.2,0.24999]' --grid-cartesian-npts ${NPTS_IT} --skip-overlap --fname overlap-grid-0 > args_grid.txt )
	util_ManualOverlapGrid.py --parameter mc --parameter-range '[25,35]' --parameter eta --parameter-range '[0.2,0.24999]' --grid-cartesian-npts ${NPTS_START} --skip-overlap
	(cd $@; echo X --mc-range '[25,35]'     --eta-range '[0.20,0.24999]' --parameter mc --parameter-implied eta --parameter-nofit delta_mc  --fit-method gp --verbose  --chi-max 0.05 --cap-points 12000  --no-plots  > args_cip.txt)
	(cd $@; echo X  ${STANDARD_ILE_OPTS}  --data-start-time 1000000008 --data-end-time 1000000016 --inv-spec-trunc-time 0 > args_ile.txt)
	(cd $@; echo X  --always-succeed --method lame  --parameter m1 > args_test.txt)
	(cd $@; echo X  --parameter m1 --parameter m2  > args_plot.txt)
#	(cd $@; ls ${PWD}/*psd.xml.gz  ${PWD}/*.cache  > file_names_transfer.txt)
	(cd $@;  create_event_parameter_pipeline_BasicIteration  --input-grid overlap-grid-0.xml.gz --ile-exe `which integrate_likelihood_extrinsic`   --ile-args args_ile.txt --cip-args args_cip.txt  --test-args args_test.txt --plot-args args_plot.txt --request-memory-CIP ${CIP_MEM} --request-memory-ILE ${ILE_MEM}  --input-grid ${PWD}/overlap-grid.xml.gz --n-samples-per-job ${NPTS_IT} --working-directory ${PWD}/$@ )
# --transfer-file-list file_names_transfer.txt


test_workflow_batch_gpu: Makefile HLV-ILIGO_PSD.xml.gz zero_noise.cache
	(mkdir $@; exit 0)
#	(cd $@; echo X  --parameter mc --parameter-range '[30,60]' --parameter eta --parameter-range '[0.2,0.24999]' --grid-cartesian-npts ${NPTS_IT} --skip-overlap --fname overlap-grid-0 > args_grid.txt )
	util_ManualOverlapGrid.py --parameter mc --parameter-range '[25,35]' --parameter eta --parameter-range '[0.2,0.24999]' --grid-cartesian-npts ${NPTS_START} --skip-overlap
	(cd $@; echo X --mc-range '[25,35]'     --eta-range '[0.20,0.24999]' --parameter mc --parameter-implied eta --parameter-nofit delta_mc  --fit-method gp --verbose  --chi-max 0.05 --cap-points 12000  --no-plots  > args_cip.txt)
	(cd $@; echo X   ${STANDARD_ILE_OPTS}  --data-start-time 1000000008 --data-end-time 1000000016 --inv-spec-trunc-time 0 > args_ile.txt)
	(cd $@; echo X  --always-succeed --method lame  --parameter m1 > args_test.txt)
	(cd $@; echo X  --parameter m1 --parameter m2  > args_plot.txt)
#	(cd $@; ls ${PWD}/*psd.xml.gz  ${PWD}/*.cache  > file_names_transfer.txt)
	(cd $@;  create_event_parameter_pipeline_BasicIteration --request-gpu-ILE --ile-n-events-to-analyze ${NPTS_IT} --input-grid overlap-grid-0.xml.gz --ile-exe `which integrate_likelihood_extrinsic_batchmode`   --ile-args args_ile.txt --cip-args args_cip.txt  --test-args args_test.txt --plot-args args_plot.txt --request-memory-CIP ${CIP_MEM} --request-memory-ILE ${ILE_MEM}  --input-grid ${PWD}/overlap-grid.xml.gz --n-samples-per-job ${NPTS_IT} --working-directory ${PWD}/$@ )
# --transfer-file-list file_names_transfer.txt



## Low latency configuration
##   - do not adapt in distance 
##   - disable sky localization adaptation after iteration 1
##
test_workflow_batch_gpu_lowlatency: Makefile HLV-ILIGO_PSD.xml.gz zero_noise.cache
	(mkdir $@; exit 0)
#	(cd $@; echo X  --parameter mc --parameter-range '[30,60]' --parameter eta --parameter-range '[0.2,0.24999]' --grid-cartesian-npts ${NPTS_IT} --skip-overlap --fname overlap-grid-0 > args_grid.txt )
	util_ManualOverlapGrid.py --parameter mc --parameter-range '[25,35]' --parameter eta --parameter-range '[0.2,0.24999]' --grid-cartesian-npts ${NPTS_START} --skip-overlap
	(cd $@; echo X --mc-range '[25,35]'     --eta-range '[0.20,0.24999]' --parameter mc --parameter-implied eta --parameter-nofit delta_mc  --fit-method gp --verbose  --chi-max 0.05 --cap-points 12000  --no-plots  > args_cip.txt)
	(cd $@; echo X   ${STANDARD_ILE_OPTS}  --data-start-time 1000000008 --data-end-time 1000000016 --inv-spec-trunc-time 0  --no-adapt-after-first --no-adapt-distance --srate 4096 > args_ile.txt)
	(cd $@; echo X  --always-succeed --method lame  --parameter m1 > args_test.txt)
	(cd $@; echo X  --parameter m1 --parameter m2  > args_plot.txt)
#	(cd $@; ls ${PWD}/*psd.xml.gz  ${PWD}/*.cache  > file_names_transfer.txt)
	(cd $@;  create_event_parameter_pipeline_BasicIteration --request-gpu-ILE --ile-n-events-to-analyze ${NPTS_IT} --input-grid overlap-grid-0.xml.gz  --ile-exe `which integrate_likelihood_extrinsic_batchmode`  --ile-args args_ile.txt --cip-args args_cip.txt  --test-args args_test.txt --plot-args args_plot.txt --request-memory-CIP ${CIP_MEM} --request-memory-ILE ${ILE_MEM}  --input-grid ${PWD}/overlap-grid.xml.gz --n-samples-per-job ${NPTS_IT} --working-directory ${PWD}/$@ )
# --transfer-file-list file_names_transfer.txt




###
### BNS
###

# 256 sec, starting at event time minus about 256, plus 10
START_BNS=999999768
STOP_BNS=1000000024
MC_RANGE_BNS='[1.1963,1.1972]' 

mdc_bns.xml.gz:
	util_WriteInjectionFile.py  --fname mdc_bns --parameter m1 --parameter-value 1.4 --parameter m2 --parameter-value 1.35 --fname mdc --approx ${APPROX} --parameter tref --parameter-value ${EVENT_TIME} --parameter dist --parameter-value 100 --parameter fmin --parameter-value 18 # make it slightly lower frequency to insure length adequate

bns.cache: mdc_bns.xml.gz
	util_WriteFrameAndCacheFromXML.sh mdc_bns.xml.gz 0 bns ${APPROX}

snr_bns_table.dat: bns.cache HLV-aLIGO_PSD.xml.gz
	util_FrameZeroNoiseSNR.py --cache bns.cache --psd-file H1=HLV-aLIGO_PSD.xml.gz  --psd-file L1=HLV-aLIGO_PSD.xml.gz  > $@


DMAX_BNS=500
STANDARD_ILE_OPTS_BNS=--n-chunk 10000 --time-marginalization --sim-xml overlap-grid-bns.xml.gz --reference-freq 100.0 --adapt-weight-exponent 0.1  --event-time ${EVENT_TIME} --save-P 0.1 --cache-file ${PWD}/bns.cache --fmin-template 23.0 --n-max 2000000 --fmax 1700.0 --save-deltalnL inf --l-max 2  --n-eff 50  --approximant ${APPROX_BNS} --adapt-floor-level 0.1 --maximize-only  --d-max ${DMAX_BNS}  --psd-file H1=${PWD}/HLV-aLIGO_PSD.xml.gz --psd-file L1=${PWD}/HLV-aLIGO_PSD.xml.gz --channel-name H1=FAKE-STRAIN --channel-name L1=FAKE-STRAIN --inclination-cosine-sampler --declination-cosine-sampler

test_workflow_nobatch_bns: Makefile HLV-aLIGO_PSD.xml.gz bns.cache
	(mkdir $@; exit 0)
	util_ManualOverlapGrid.py --parameter mc --parameter-range ${MC_RANGE_BNS} --parameter eta --parameter-range '[0.2,0.24999]' --grid-cartesian-npts ${NPTS_START} --skip-overlap --downselect-parameter m2 --downselect-parameter-range [1,2]
	(cd $@; echo X --mc-range   ${MC_RANGE_BNS}  --eta-range '[0.20,0.24999]' --parameter mc --parameter-implied eta --parameter-nofit delta_mc  --fit-method gp --verbose  --chi-max 0.05 --cap-points 12000  --no-plots  > args_cip.txt)
	(cd $@; echo X  ${STANDARD_ILE_OPTS_BNS}  --data-start-time ${START_BNS} --data-end-time ${STOP_BNS} --inv-spec-trunc-time 0 > args_ile.txt)
	(cd $@; echo X  --always-succeed --method lame  --parameter m1 > args_test.txt)
	(cd $@; echo X  --parameter m1 --parameter m2  > args_plot.txt)
#	(cd $@; ls ${PWD}/*psd.xml.gz  ${PWD}/*.cache  > file_names_transfer.txt)
	(cd $@;  create_event_parameter_pipeline_BasicIteration  --input-grid overlap-grid-0.xml.gz --ile-exe `which integrate_likelihood_extrinsic`   --ile-args args_ile.txt --cip-args args_cip.txt  --test-args args_test.txt --plot-args args_plot.txt --request-memory-CIP ${CIP_MEM} --request-memory-ILE ${ILE_MEM}  --input-grid ${PWD}/overlap-grid.xml.gz --n-samples-per-job ${NPTS_IT} --working-directory ${PWD}/$@ )
# --transfer-file-list file_names_transfer.txt


test_workflow_batch_bns_gpu_lowlatency: Makefile HLV-aLIGO_PSD.xml.gz bns.cache
	(mkdir $@; exit 0)
	util_ManualOverlapGrid.py --parameter mc --parameter-range ${MC_RANGE_BNS} --parameter eta --parameter-range '[0.2,0.24999]' --grid-cartesian-npts ${NPTS_START} --skip-overlap  --downselect-parameter m2 --downselect-parameter-range [1,2]
	(cd $@; echo X --mc-range ${MC_RANGE_BNS}    --eta-range '[0.20,0.24999]' --parameter mc --parameter-implied eta --parameter-nofit delta_mc  --fit-method gp --verbose  --chi-max 0.05 --cap-points 12000  --no-plots  > args_cip.txt)
	(cd $@; echo X  ${STANDARD_ILE_OPTS_BNS}  --data-start-time ${START_BNS} --data-end-time ${STOP_BNS} --inv-spec-trunc-time 0 --no-adapt-after-first --no-adapt-distance --srate 4096 > args_ile.txt)
	(cd $@; echo X  --always-succeed --method lame  --parameter m1 > args_test.txt)
	(cd $@; echo X  --parameter m1 --parameter m2  > args_plot.txt)
#	(cd $@; ls ${PWD}/*psd.xml.gz  ${PWD}/*.cache  > file_names_transfer.txt)
	(cd $@;  create_event_parameter_pipeline_BasicIteration --request-gpu-ILE  --ile-n-events-to-analyze ${NPTS_IT} --input-grid overlap-grid-0.xml.gz --ile-exe `which integrate_likelihood_extrinsic_batchmode`   --ile-args args_ile.txt --cip-args args_cip.txt  --test-args args_test.txt --plot-args args_plot.txt --request-memory-CIP ${CIP_MEM} --request-memory-ILE ${ILE_MEM}  --input-grid ${PWD}/overlap-grid.xml.gz --n-samples-per-job ${NPTS_IT} --working-directory ${PWD}/$@ )
# --transfer-file-list file_names_transfer.txt

