

ILE=$(shell which integrate_likelihood_extrinsic)
POST_GENERIC=$(shell which util_ConstructIntrinsicPosterior_GenericCoordinates.py)
PWD=$(shell pwd)

NPTS_START=100
NPTS_IT=20
DMAX=1000
N_IT=5

ILE_MEM=2048
CIP_MEM=2048


EVENT_TIME=1000000014.236547946
APPROX=SEOBNRv4
APPROX_BNS=TaylorT4


###
### BBH 
###

FMIN_INJ_BH=8
FMIN_TEMPLATE_BH=10

mdc.xml.gz:
	util_WriteInjectionFile.py  --parameter m1 --parameter-value 35 --parameter m2 --parameter-value 30 --fname mdc --approx ${APPROX} --parameter tref --parameter-value ${EVENT_TIME} --parameter dist --parameter-value 200 --parameter fmin --parameter-value ${FMIN_INJ_BH}

zero_noise.cache: mdc.xml.gz
	util_WriteFrameAndCacheFromXML.sh mdc.xml.gz 0 zero_noise ${APPROX}

snr_table.dat: zero_noise.cache
	util_FrameZeroNoiseSNR.py --cache zero_noise.cache --psd-file H1=HLV-ILIGO_PSD.xml.gz  --psd-file L1=HLV-ILIGO_PSD.xml.gz  > snr_table.dat


HLV-ILIGO_PSD.xml.gz:
	./generate_iligo_psd

HLV-aLIGO_PSD.xml.gz:
	./generate_iligo_psd


STANDARD_ILE_OPTS=--n-chunk 10000 --time-marginalization --sim-xml overlap-grid.xml.gz --reference-freq 100.0 --adapt-weight-exponent 0.1  --event-time ${EVENT_TIME} --save-P 0.1 --cache-file ${PWD}/zero_noise.cache --fmin-template ${FMIN_TEMPLATE_BH} --n-max 2000000 --fmax 1700.0 --save-deltalnL inf --l-max 2  --n-eff 50  --approximant ${APPROX} --adapt-floor-level 0.1 --maximize-only  --d-max ${DMAX}  --psd-file H1=${PWD}/HLV-ILIGO_PSD.xml.gz --psd-file L1=${PWD}/HLV-ILIGO_PSD.xml.gz --channel-name H1=FAKE-STRAIN --channel-name L1=FAKE-STRAIN --inclination-cosine-sampler --declination-cosine-sampler


MC_RANGE_BH=[23,35]
test_workflow_nobatch: Makefile HLV-ILIGO_PSD.xml.gz zero_noise.cache
	(mkdir $@; exit 0)
#	(cd $@; echo X  --parameter mc --parameter-range '[30,60]' --parameter eta --parameter-range '[0.2,0.24999]' --grid-cartesian-npts ${NPTS_IT} --skip-overlap --fname overlap-grid-0 > args_grid.txt )
	util_ManualOverlapGrid.py --parameter mc --parameter-range ${MC_RANGE_BH} --parameter delta_mc --parameter-range '[0.0,0.5]' --grid-cartesian-npts ${NPTS_START} --skip-overlap
	(cd $@; echo X --mc-range ${MC_RANGE_BH}     --eta-range '[0.20,0.24999]' --parameter mc --parameter-implied eta --parameter-nofit delta_mc  --fit-method gp --verbose  --lnL-offset ${LNL_OFFSET} --cap-points 12000  --n-output-samples 10000 --no-plots --n-eff 10000  > args_cip.txt)
	(cd $@; echo X  ${STANDARD_ILE_OPTS}  --data-start-time 1000000008 --data-end-time 1000000016 --inv-spec-trunc-time 0 > args_ile.txt)
	(cd $@; echo X  --always-succeed --method lame  --parameter m1 > args_test.txt)
	(cd $@; echo X  --parameter m1 --parameter m2  > args_plot.txt)
#	(cd $@; ls ${PWD}/*psd.xml.gz  ${PWD}/*.cache  > file_names_transfer.txt)
	(cd $@;  create_event_parameter_pipeline_BasicIteration  --input-grid overlap-grid-0.xml.gz --ile-exe `which integrate_likelihood_extrinsic`   --ile-args args_ile.txt --cip-args args_cip.txt  --test-args args_test.txt --plot-args args_plot.txt --request-memory-CIP ${CIP_MEM} --request-memory-ILE ${ILE_MEM}  --input-grid ${PWD}/overlap-grid.xml.gz --n-samples-per-job ${NPTS_IT} --working-directory ${PWD}/$@  --n-iterations ${N_IT} )
# --transfer-file-list file_names_transfer.txt


test_workflow_batch_gpu: Makefile HLV-ILIGO_PSD.xml.gz zero_noise.cache
	(mkdir $@; exit 0)
	util_ManualOverlapGrid.py --parameter mc --parameter-range ${MC_RANGE_BH} --parameter delta_mc --parameter-range '[0.0,0.5]' --grid-cartesian-npts ${NPTS_START} --skip-overlap
	(cd $@; echo X --mc-range ${MC_RANGE_BH}     --eta-range '[0.20,0.24999]' --parameter mc --parameter-implied eta --parameter-nofit delta_mc  --fit-method gp --verbose  --lnL-offset ${LNL_OFFSET} --cap-points 12000  --n-output-samples 10000 --no-plots --n-eff 10000  > args_cip.txt)
	(cd $@; echo X   ${STANDARD_ILE_OPTS}  --data-start-time 1000000008 --data-end-time 1000000016 --inv-spec-trunc-time 0 > args_ile.txt)
	(cd $@; echo X  --always-succeed --method lame  --parameter m1 > args_test.txt)
	(cd $@; echo X  --parameter m1 --parameter m2 --composite-file all.net --plot-1d-extra --ci-list [0.9] --truth-file ${PWD}/mdc.xml.gz  > args_plot.txt)
#	(cd $@; ls ${PWD}/*psd.xml.gz  ${PWD}/*.cache  > file_names_transfer.txt)
	(cd $@;  create_event_parameter_pipeline_BasicIteration --request-gpu-ILE --ile-n-events-to-analyze ${NPTS_IT} --input-grid overlap-grid-0.xml.gz --ile-exe `which integrate_likelihood_extrinsic_batchmode`   --ile-args args_ile.txt --cip-args args_cip.txt  --test-args args_test.txt --plot-args args_plot.txt --request-memory-CIP ${CIP_MEM} --request-memory-ILE ${ILE_MEM}  --input-grid ${PWD}/overlap-grid.xml.gz --n-samples-per-job ${NPTS_IT} --working-directory ${PWD}/$@ --n-iterations ${N_IT})
# --transfer-file-list file_names_transfer.txt



## Low latency configuration
##   - do not adapt in distance 
##   - disable sky localization adaptation after iteration 1
##
test_workflow_batch_gpu_lowlatency: Makefile HLV-ILIGO_PSD.xml.gz zero_noise.cache
	(mkdir $@; exit 0)
	util_ManualOverlapGrid.py --parameter mc --parameter-range ${MC_RANGE_BH} --parameter delta_mc --parameter-range '[0.0,0.5]' --grid-cartesian-npts ${NPTS_START} --skip-overlap
	(cd $@; echo X --mc-range ${MC_RANGE_BH}     --eta-range '[0.20,0.24999]' --parameter mc --parameter-implied eta --parameter-nofit delta_mc  --fit-method gp --verbose  --lnL-offset ${LNL_OFFSET} --cap-points 12000  --n-output-samples 10000 --no-plots --n-eff 10000  > args_cip.txt)
	(cd $@; echo X   ${STANDARD_ILE_OPTS}  --data-start-time 1000000008 --data-end-time 1000000016 --inv-spec-trunc-time 0  --no-adapt-after-first --no-adapt-distance --srate 4096 > args_ile.txt)
	(cd $@; echo X  --always-succeed --method lame  --parameter m1 > args_test.txt)
	(cd $@; echo X  --parameter m1 --parameter m2  > args_plot.txt)
#	(cd $@; ls ${PWD}/*psd.xml.gz  ${PWD}/*.cache  > file_names_transfer.txt)
	(cd $@;  create_event_parameter_pipeline_BasicIteration --request-gpu-ILE --ile-n-events-to-analyze ${NPTS_IT} --input-grid overlap-grid-0.xml.gz  --ile-exe `which integrate_likelihood_extrinsic_batchmode`  --ile-args args_ile.txt --cip-args args_cip.txt  --test-args args_test.txt --plot-args args_plot.txt --request-memory-CIP ${CIP_MEM} --request-memory-ILE ${ILE_MEM}  --input-grid ${PWD}/overlap-grid.xml.gz --n-samples-per-job ${NPTS_IT} --working-directory ${PWD}/$@ --n-iterations ${N_IT} )
# --transfer-file-list file_names_transfer.txt

test_workflow_batch_gpu_lowlatency_OSG: Makefile HLV-ILIGO_PSD.xml.gz zero_noise.cache
	(mkdir $@; exit 0)
	util_ManualOverlapGrid.py --parameter mc --parameter-range ${MC_RANGE_BH} --parameter delta_mc --parameter-range '[0.0,0.5]' --grid-cartesian-npts ${NPTS_START} --skip-overlap
	(cd $@; echo X --mc-range ${MC_RANGE_BH}     --eta-range '[0.20,0.24999]' --parameter mc --parameter-implied eta --parameter-nofit delta_mc  --fit-method gp --verbose  --lnL-offset ${LNL_OFFSET} --cap-points 12000  --n-output-samples 10000 --no-plots --n-eff 10000  > args_cip.txt)
	(cd $@; echo X   ${STANDARD_ILE_OPTS}  --data-start-time 1000000008 --data-end-time 1000000016 --inv-spec-trunc-time 0  --no-adapt-after-first --no-adapt-distance --srate 4096 > args_ile.txt)
	(cd $@; echo X  --always-succeed --method lame  --parameter m1 > args_test.txt)
	(cd $@; echo X  --parameter m1 --parameter m2  > args_plot.txt)
	(cd $@; ls ${PWD}/HLV-ILIGO_PSD.xml.gz  >  file_names_transfer.txt)
	(cd $@;  create_event_parameter_pipeline_BasicIteration --request-gpu-ILE --ile-n-events-to-analyze ${NPTS_IT} --input-grid overlap-grid-0.xml.gz  --ile-exe `which integrate_likelihood_extrinsic_batchmode`  --ile-args args_ile.txt --cip-args args_cip.txt  --test-args args_test.txt --plot-args args_plot.txt --request-memory-CIP ${CIP_MEM} --request-memory-ILE ${ILE_MEM}  --input-grid ${PWD}/overlap-grid.xml.gz --n-samples-per-job ${NPTS_IT} --working-directory ${PWD}/$@ --n-iterations ${N_IT}  --use-singularity --use-osg --frames-dir ../zero_noise  --transfer-file-list file_names_transfer.txt)



###
### Precessing BBH (v3)
###
MC_RANGE_BH_SPIN=[15,35]
PRECESSING_ILE_OPTS=--n-chunk 10000 --time-marginalization --sim-xml overlap-grid.xml.gz --reference-freq 100.0 --adapt-weight-exponent 0.1  --event-time ${EVENT_TIME} --save-P 0.1 --cache-file ${PWD}/zero_noise.cache --fmin-template ${FMIN_TEMPLATE_BH} --n-max 2000000 --fmax 1700.0 --save-deltalnL inf --l-max 2  --n-eff 50  --approximant SEOBNRv3 --adapt-floor-level 0.1 --maximize-only  --d-max ${DMAX}  --psd-file H1=${PWD}/HLV-ILIGO_PSD.xml.gz --psd-file L1=${PWD}/HLV-ILIGO_PSD.xml.gz --channel-name H1=FAKE-STRAIN --channel-name L1=FAKE-STRAIN --inclination-cosine-sampler --declination-cosine-sampler
PRECESSING_CIP_OPTS_BASE=--mc-range ${MC_RANGE_BH_SPIN}     --eta-range '[0.20,0.24999]' --cap-points 12000  --n-output-samples 10000 --no-plots --n-eff 10000 --approx-output SEOBNRv3 --use-precessing --fit-method gp --verbose --n-max 1e7



## SEOBNRv3 analysis
## Use multiple CIP
##    - first few iterations: just mc,eta chi_eff, with wide lnL cutoff
##    - subsequent iterations use all 8 dimensions, with tight lnL cutoff appropriate to production
## Low latency settings
##   - do not adapt in distance 
##   - disable sky localization adaptation after iteration 1
##
test_workflow_batch_gpu_SEOBNRv3: Makefile HLV-ILIGO_PSD.xml.gz zero_noise.cache
	(mkdir $@; exit 0)
	util_ManualOverlapGrid.py --parameter mc --parameter-range ${MC_RANGE_BH_SPIN} --parameter delta_mc  --parameter-range '[0.0,0.7]' --parameter chieff_aligned --parameter-range [-0.8,0.8] --grid-cartesian-npts 2000 --skip-overlap --approx SEOBNRv3
	(cd $@; echo 5  ${PRECESSING_CIP_OPTS_BASE}  --parameter mc --parameter-implied eta --parameter-nofit delta_mc   --parameter-implied xi --parameter-nofit s1z --parameter-nofit s2z  --parameter-nofit s1x --parameter-nofit s1y --parameter-nofit s2x --parameter-nofit s2y   --lnL-offset 50  > args_cip_list.txt)
	(cd $@; echo 5 ${PRECESSING_CIP_OPTS_BASE} --mc-range ${MC_RANGE_BH_SPIN}   --parameter mc --parameter-implied eta --parameter-nofit delta_mc   --parameter-implied xi --parameter-implied chiMinus --parameter-nofit s1z --parameter-nofit s2z  --parameter s1x --parameter s1y --parameter s2x --parameter s2y   --lnL-offset 25   >> args_cip_list.txt)
	(cd $@; echo X   ${PRECESSING_ILE_OPTS}  --data-start-time 1000000008 --data-end-time 1000000016 --inv-spec-trunc-time 0  --no-adapt-after-first --no-adapt-distance --srate 4096 > args_ile.txt)
	(cd $@; echo X  --always-succeed --method lame  --parameter m1 > args_test.txt)
	(cd $@; echo X  --parameter m1 --parameter m2  > args_plot.txt)
#	(cd $@; ls ${PWD}/*psd.xml.gz  ${PWD}/*.cache  > file_names_transfer.txt)
	(cd $@;  create_event_parameter_pipeline_BasicIteration --request-gpu-ILE --ile-n-events-to-analyze ${NPTS_IT} --input-grid ${PWD}/overlap-grid.xml.gz  --ile-exe `which integrate_likelihood_extrinsic_batchmode`  --ile-args args_ile.txt --cip-args-list args_cip_list.txt  --test-args args_test.txt --plot-args args_plot.txt --request-memory-CIP 30000 --request-memory-ILE 4096  --input-grid ${PWD}/overlap-grid.xml.gz --n-samples-per-job 500 --working-directory ${PWD}/$@ --n-iterations 10 --ile-retries 3)
# --transfer-file-list file_names_transfer.txt

# Just to see how painful this would be ... no throttling of GPUs
# Use batchmode so I am modestly more efficient for the first iteration
test_workflow_batch_nogpu_SEOBNRv3: Makefile HLV-ILIGO_PSD.xml.gz zero_noise.cache
	(mkdir $@; exit 0)
	util_ManualOverlapGrid.py --parameter mc --parameter-range ${MC_RANGE_BH_SPIN} --parameter delta_mc  --parameter-range '[0.0,0.7]' --parameter chieff_aligned --parameter-range [-0.8,0.8] --grid-cartesian-npts 2000 --skip-overlap --approx SEOBNRv3
	(cd $@; echo 5  ${PRECESSING_CIP_OPTS_BASE}  --parameter mc --parameter-implied eta --parameter-nofit delta_mc   --parameter-implied xi --parameter-nofit s1z --parameter-nofit s2z  --parameter-nofit s1x --parameter-nofit s1y --parameter-nofit s2x --parameter-nofit s2y   --lnL-offset 50  > args_cip_list.txt)
	(cd $@; echo 5 ${PRECESSING_CIP_OPTS_BASE} --mc-range ${MC_RANGE_BH_SPIN}   --parameter mc --parameter-implied eta --parameter-nofit delta_mc   --parameter-implied xi --parameter-implied chiMinus --parameter-nofit s1z --parameter-nofit s2z  --parameter s1x --parameter s1y --parameter s2x --parameter s2y   --lnL-offset 25   >> args_cip_list.txt)
	(cd $@; echo X   ${PRECESSING_ILE_OPTS}  --data-start-time 1000000008 --data-end-time 1000000016 --inv-spec-trunc-time 0  --no-adapt-after-first --no-adapt-distance --srate 4096 > args_ile.txt)
	(cd $@; echo X  --always-succeed --method lame  --parameter m1 > args_test.txt)
	(cd $@; echo X  --parameter m1 --parameter m2  > args_plot.txt)
#	(cd $@; ls ${PWD}/*psd.xml.gz  ${PWD}/*.cache  > file_names_transfer.txt)
	(cd $@;  create_event_parameter_pipeline_BasicIteration  --ile-n-events-to-analyze 5  --input-grid ${PWD}/overlap-grid.xml.gz  --ile-exe `which integrate_likelihood_extrinsic_batchmode`  --ile-args args_ile.txt --cip-args-list args_cip_list.txt  --test-args args_test.txt --plot-args args_plot.txt --request-memory-CIP 30000 --request-memory-ILE 4096  --input-grid ${PWD}/overlap-grid.xml.gz --n-samples-per-job 500 --working-directory ${PWD}/$@ --n-iterations 10 --ile-retries 3 )
# --transfer-file-list file_names_transfer.txt


test_workflow_batch_nogpu_SEOBNRv3_OSG: Makefile HLV-ILIGO_PSD.xml.gz zero_noise.cache
	(mkdir $@; exit 0)
	util_ManualOverlapGrid.py --parameter mc --parameter-range ${MC_RANGE_BH_SPIN} --parameter delta_mc  --parameter-range '[0.0,0.5]' --parameter chieff_aligned --parameter-range [-0.5,0.5] --grid-cartesian-npts 2000 --skip-overlap --approx SEOBNRv3
	(cd $@; echo 5  ${PRECESSING_CIP_OPTS_BASE}  --parameter mc --parameter-implied eta --parameter-nofit delta_mc   --parameter-implied xi --parameter-nofit s1z --parameter-nofit s2z  --parameter-nofit s1x --parameter-nofit s1y --parameter-nofit s2x --parameter-nofit s2y   --lnL-offset 50  > args_cip_list.txt)
	(cd $@; echo 5 ${PRECESSING_CIP_OPTS_BASE} --mc-range ${MC_RANGE_BH_SPIN}   --parameter mc --parameter-implied eta --parameter-nofit delta_mc   --parameter-implied xi --parameter-implied chiMinus --parameter-nofit s1z --parameter-nofit s2z  --parameter s1x --parameter s1y --parameter s2x --parameter s2y   --lnL-offset 25   >> args_cip_list.txt)
	(cd $@; echo X   ${PRECESSING_ILE_OPTS}  --data-start-time 1000000008 --data-end-time 1000000016 --inv-spec-trunc-time 0  --no-adapt-after-first --no-adapt-distance --srate 4096 > args_ile.txt)
	(cd $@; echo X  --always-succeed --method lame  --parameter m1 > args_test.txt)
	(cd $@; echo X  --parameter m1 --parameter m2  > args_plot.txt)
	(cd $@; ls ${PWD}/*PSD.xml.gz    > file_names_transfer.txt)
	(cd $@;  create_event_parameter_pipeline_BasicIteration  --ile-n-events-to-analyze 5  --input-grid ${PWD}/overlap-grid.xml.gz  --ile-exe `which integrate_likelihood_extrinsic_batchmode`  --ile-args args_ile.txt --cip-args-list args_cip_list.txt  --test-args args_test.txt --plot-args args_plot.txt --request-memory-CIP 30000 --request-memory-ILE 4096  --input-grid ${PWD}/overlap-grid.xml.gz --n-samples-per-job 500 --working-directory ${PWD}/$@ --n-iterations 10 --ile-retries 3 --transfer-file-list file_names_transfer.txt --frames-dir ${PWD}/zero_noise --use-singularity --use-osg )


###
### BNS
###

# 256 sec, starting at event time minus about 256, plus 10
START_BNS=999999768
STOP_BNS=1000000024
MC_RANGE_BNS='[1.1962,1.1970]' 
LNL_CUT=120  # based on peak lnL of 400, this is useful
LNL_OFFSET=120 # because we are fitting in low dimensions, we should keep more.

N_IT_BNS=5

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
	util_ManualOverlapGrid.py --parameter mc --parameter-range ${MC_RANGE_BNS} --parameter delta_mc --parameter-range '[0.,0.25]' --grid-cartesian-npts ${NPTS_START} --skip-overlap --downselect-parameter m2 --downselect-parameter-range [1,2]
	(cd $@; echo X --mc-range   ${MC_RANGE_BNS}  --eta-range '[0.20,0.24999]' --parameter mc --parameter-implied eta --parameter-nofit delta_mc  --fit-method gp --verbose  --lnL-offset ${LNL_OFFSET} --cap-points 12000  --n-output-samples 10000 --no-plots --n-eff 10000  > args_cip.txt)
	(cd $@; echo X  ${STANDARD_ILE_OPTS_BNS}  --data-start-time ${START_BNS} --data-end-time ${STOP_BNS} --inv-spec-trunc-time 0 > args_ile.txt)
	(cd $@; echo X  --always-succeed --method lame  --parameter m1 > args_test.txt)
	(cd $@; echo X  --parameter mc --parameter delta_mc  --mc-range ${MC_RANGE_BNS} --plot-1d-extra --ci-list [0.9] --truth-file ${PWD}/mdc_bns.xml.gz  > args_plot.txt)
#	(cd $@; ls ${PWD}/*psd.xml.gz  ${PWD}/*.cache  > file_names_transfer.txt)
	(cd $@;  create_event_parameter_pipeline_BasicIteration  --input-grid overlap-grid-0.xml.gz --ile-exe `which integrate_likelihood_extrinsic`   --ile-args args_ile.txt --cip-args args_cip.txt  --test-args args_test.txt --plot-args args_plot.txt --request-memory-CIP ${CIP_MEM} --request-memory-ILE ${ILE_MEM}  --input-grid ${PWD}/overlap-grid.xml.gz --n-samples-per-job ${NPTS_IT} --working-directory ${PWD}/$@ --n-iterations ${N_IT_BNS} )
# --transfer-file-list file_names_transfer.txt


test_workflow_batch_bns_gpu_lowlatency: Makefile HLV-aLIGO_PSD.xml.gz bns.cache
	(mkdir $@; exit 0)
	util_ManualOverlapGrid.py --parameter mc --parameter-range ${MC_RANGE_BNS} --parameter delta_mc --parameter-range '[0., 0.25]' --grid-cartesian-npts ${NPTS_START} --skip-overlap  --downselect-parameter m2 --downselect-parameter-range [1,2]
	(cd $@; echo X --mc-range ${MC_RANGE_BNS}    --eta-range '[0.20,0.24999]' --parameter mc --parameter-implied eta --parameter-nofit delta_mc  --fit-method gp --verbose  --lnL-offset ${LNL_OFFSET} --cap-points 12000  --n-output-samples 10000 --no-plots --n-eff 10000  > args_cip.txt)
	(cd $@; echo X  ${STANDARD_ILE_OPTS_BNS}  --data-start-time ${START_BNS} --data-end-time ${STOP_BNS} --inv-spec-trunc-time 0 --no-adapt-after-first --no-adapt-distance --srate 4096 > args_ile.txt)
	(cd $@; echo X  --always-succeed --method lame  --parameter m1 > args_test.txt)
	(cd $@; echo X  --parameter mc --parameter delta_mc  --mc-range ${MC_RANGE_BNS}  --composite-file all.net   --plot-1d-extra --ci-list [0.9] --truth-file ${PWD}/mdc_bns.xml.gz --lnL-cut ${LNL_CUT} > args_plot.txt)
#	(cd $@; ls ${PWD}/*psd.xml.gz  ${PWD}/*.cache  > file_names_transfer.txt)
	(cd $@;  create_event_parameter_pipeline_BasicIteration --request-gpu-ILE  --ile-n-events-to-analyze ${NPTS_IT} --input-grid overlap-grid-0.xml.gz --ile-exe `which integrate_likelihood_extrinsic_batchmode`   --ile-args args_ile.txt --cip-args args_cip.txt  --test-args args_test.txt --plot-args args_plot.txt --request-memory-CIP ${CIP_MEM} --request-memory-ILE ${ILE_MEM}  --input-grid ${PWD}/overlap-grid.xml.gz --n-samples-per-job ${NPTS_IT} --working-directory ${PWD}/$@  --n-iterations ${N_IT_BNS})
# --transfer-file-list file_names_transfer.txt



# Key difference: ampO=0
test_workflow_batch_bns_gpu_lowlatency_noHM: Makefile HLV-aLIGO_PSD.xml.gz bns.cache
	(mkdir $@; exit 0)
	util_ManualOverlapGrid.py --parameter mc --parameter-range ${MC_RANGE_BNS} --parameter delta_mc --parameter-range '[0., 0.25]' --grid-cartesian-npts ${NPTS_START} --skip-overlap  --downselect-parameter m2 --downselect-parameter-range [1,2]  --amplitude-order 0
	(cd $@; echo X --mc-range ${MC_RANGE_BNS}    --eta-range '[0.20,0.24999]' --parameter mc --parameter-implied eta --parameter-nofit delta_mc  --fit-method gp --verbose  --lnL-offset ${LNL_OFFSET}  --cap-points 12000  --n-output-samples 10000 --no-plots --n-eff 10000  > args_cip.txt)
	(cd $@; echo X  ${STANDARD_ILE_OPTS_BNS}  --data-start-time ${START_BNS} --data-end-time ${STOP_BNS} --inv-spec-trunc-time 0 --no-adapt-after-first --no-adapt-distance --srate 4096 > args_ile.txt)
	(cd $@; echo X  --always-succeed --method lame  --parameter m1 > args_test.txt)
	(cd $@; echo X  --parameter mc --parameter delta_mc  --mc-range ${MC_RANGE_BNS}  --composite-file all.net --plot-1d-extra --ci-list [0.9] --truth-file ${PWD}/mdc_bns.xml.gz  > args_plot.txt)
#	(cd $@; ls ${PWD}/*psd.xml.gz  ${PWD}/*.cache  > file_names_transfer.txt)
	(cd $@;  create_event_parameter_pipeline_BasicIteration --request-gpu-ILE  --ile-n-events-to-analyze ${NPTS_IT} --input-grid overlap-grid-0.xml.gz --ile-exe `which integrate_likelihood_extrinsic_batchmode`   --ile-args args_ile.txt --cip-args args_cip.txt  --test-args args_test.txt --plot-args args_plot.txt --request-memory-CIP ${CIP_MEM} --request-memory-ILE ${ILE_MEM}  --input-grid ${PWD}/overlap-grid.xml.gz --n-samples-per-job ${NPTS_IT} --working-directory ${PWD}/$@ --n-iterations ${N_IT_BNS} )
# --transfer-file-list file_names_transfer.txt




# Key difference: ampO=0, + approx -> TaylorF2 + more parameters
# ... problem, TaylorF2 or ANY FD hitting random technical problems?
#       --> DOES NOT WORK ON CIT, WORKS ELSEWHERE
#  ... problem: SEOBNRv4 time domain requires high sampling rate !
APPROX_BNS_SPIN=SEOBNRv4_ROM
SRATE_BNS=4096
ILE_MEM_SPIN=2048
CIP_MEM_SPIN=10000
CIP_N_MAX_SPIN=30000000

SPIN_ILE_OPTS_BNS=--n-chunk 10000 --time-marginalization --sim-xml overlap-grid-bns.xml.gz --reference-freq 100.0 --adapt-weight-exponent 0.1  --event-time ${EVENT_TIME} --save-P 0.1 --cache-file ${PWD}/bns.cache --fmin-template 23.0 --n-max 2000000 --fmax 1700.0 --save-deltalnL inf --l-max 2  --n-eff 50  --approximant ${APPROX_BNS_SPIN} --adapt-floor-level 0.1 --maximize-only  --d-max ${DMAX_BNS}  --psd-file H1=${PWD}/HLV-aLIGO_PSD.xml.gz --psd-file L1=${PWD}/HLV-aLIGO_PSD.xml.gz --channel-name H1=FAKE-STRAIN --channel-name L1=FAKE-STRAIN --inclination-cosine-sampler --declination-cosine-sampler

test_workflow_nobatch_bns_noHM_withspin: Makefile HLV-aLIGO_PSD.xml.gz bns.cache
	(mkdir $@; exit 0)
	util_ManualOverlapGrid.py --parameter mc --parameter-range ${MC_RANGE_BNS} --parameter delta_mc --parameter-range '[0., 0.25]' --parameter s1z --parameter-range [-0.05,0.05] --parameter s2z --parameter-range [-0.05,0.05] --grid-cartesian-npts 5000 --skip-overlap  --downselect-parameter m2 --downselect-parameter-range [1,2]  --amplitude-order 0  --approx TaylorT4  # approximant does not matter, and this causes problems
	(cd $@; echo X --mc-range ${MC_RANGE_BNS}    --eta-range '[0.20,0.24999]' --parameter mc --parameter-implied eta --parameter-nofit delta_mc  --parameter-implied xi --parameter-nofit s1z --parameter-nofit s2z  --chi-max 0.05 --fit-method gp --verbose  --lnL-offset ${LNL_OFFSET}  --cap-points 12000  --n-output-samples 10000 --no-plots --n-eff 10000 --n-max ${CIP_N_MAX_SPIN} > args_cip.txt)
	(cd $@; echo X  ${SPIN_ILE_OPTS_BNS}  --data-start-time ${START_BNS} --data-end-time ${STOP_BNS} --inv-spec-trunc-time 0 --no-adapt-after-first --no-adapt-distance --srate ${SRATE_BNS} > args_ile.txt)
	(cd $@; echo X  --always-succeed --method lame  --parameter m1 > args_test.txt)
	(cd $@; echo X  --parameter mc --parameter delta_mc  --parameter xi --mc-range ${MC_RANGE_BNS}  --composite-file all.net --plot-1d-extra --ci-list [0.9] --truth-file ${PWD}/mdc_bns.xml.gz  > args_plot.txt)
#	(cd $@; ls ${PWD}/*psd.xml.gz  ${PWD}/*.cache  > file_names_transfer.txt)
	(cd $@;  create_event_parameter_pipeline_BasicIteration  --input-grid overlap-grid-0.xml.gz --ile-exe `which integrate_likelihood_extrinsic`   --ile-args args_ile.txt --cip-args args_cip.txt  --test-args args_test.txt --plot-args args_plot.txt --request-memory-CIP ${CIP_MEM} --request-memory-ILE ${ILE_MEM}  --input-grid ${PWD}/overlap-grid.xml.gz --n-samples-per-job 500 --working-directory ${PWD}/$@ --n-iterations ${N_IT_BNS} )
# --transfer-file-list file_names_transfer.txt

test_workflow_batch_bns_gpu_lowlatency_noHM_withspin: Makefile HLV-aLIGO_PSD.xml.gz bns.cache
	(mkdir $@; exit 0)
	util_ManualOverlapGrid.py --parameter mc --parameter-range ${MC_RANGE_BNS} --parameter delta_mc --parameter-range '[0., 0.25]' --parameter s1z --parameter-range [-0.05,0.05] --parameter s2z --parameter-range [-0.05,0.05] --grid-cartesian-npts 5000 --skip-overlap  --downselect-parameter m2 --downselect-parameter-range [1,2]  --amplitude-order 0  --approx ${APPROX_BNS_SPIN}
	(cd $@; echo X --mc-range ${MC_RANGE_BNS}    --eta-range '[0.20,0.24999]' --parameter mc --parameter-implied eta --parameter-nofit delta_mc  --parameter-implied xi --parameter-nofit s1z --parameter-nofit s2z  --chi-max 0.05 --fit-method gp --verbose  --lnL-offset ${LNL_OFFSET}  --cap-points 12000  --n-output-samples 10000 --no-plots --n-eff 10000 --n-max ${CIP_N_MAX_SPIN}  > args_cip.txt)
	(cd $@; echo X  ${SPIN_ILE_OPTS_BNS}  --data-start-time ${START_BNS} --data-end-time ${STOP_BNS} --inv-spec-trunc-time 0 --no-adapt-after-first --no-adapt-distance --srate ${SRATE_BNS} > args_ile.txt)
	(cd $@; echo X  --always-succeed --method lame  --parameter m1 > args_test.txt)
	(cd $@; echo X  --parameter mc --parameter delta_mc  --parameter xi --mc-range ${MC_RANGE_BNS}  --composite-file all.net --plot-1d-extra --ci-list [0.9] --truth-file ${PWD}/mdc_bns.xml.gz  > args_plot.txt)
#	(cd $@; ls ${PWD}/*psd.xml.gz  ${PWD}/*.cache  > file_names_transfer.txt)
	(cd $@;  create_event_parameter_pipeline_BasicIteration --request-gpu-ILE  --ile-n-events-to-analyze ${NPTS_IT} --input-grid overlap-grid-0.xml.gz --ile-exe `which integrate_likelihood_extrinsic_batchmode`   --ile-args args_ile.txt --cip-args args_cip.txt  --test-args args_test.txt --plot-args args_plot.txt --request-memory-CIP ${CIP_MEM_SPIN} --request-memory-ILE ${ILE_MEM_SPIN}  --input-grid ${PWD}/overlap-grid.xml.gz --n-samples-per-job 500 --working-directory ${PWD}/$@ --n-iterations ${N_IT_BNS} )
# --transfer-file-list file_names_transfer.txt

