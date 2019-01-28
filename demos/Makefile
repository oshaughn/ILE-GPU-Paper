

ILE=$(shell which integrate_likelihood_extrinsic)
POST_GENERIC=$(shell which util_ConstructIntrinsicPosterior_GenericCoordinates.py)
PWD=$(shell pwd)

NPTS_START=100
NPTS_IT=5


EVENT_TIME=1000000014.236547946
APPROX=SEOBNRv4

mdc.xml.gz:
	util_WriteInjectionFile.py  --parameter m1 --parameter-value 35 --parameter m2 --parameter-value 30 --fname mdc --approx ${APPROX} --parameter tref --parameter-value ${EVENT_TIME} --parameter dist --parameter-value 1000 --parameter fmin --parameter-value 20

zero_noise.cache: mdc.xml.gz
	util_WriteFrameAndCacheFromXML.sh mdc.xml.gz 0 zero_noise ${APPROX}

HLV-ILIGO_PSD.xml.gz:
	./generate_iligo_psd


test_workflow_batch_gpu: Makefile HLV-ILIGO_PSD.xml.gz zero_noise.cache
	(mkdir $@; exit 0)
#	(cd $@; echo X  --parameter mc --parameter-range '[30,60]' --parameter eta --parameter-range '[0.2,0.24999]' --grid-cartesian-npts ${NPTS_IT} --skip-overlap --fname overlap-grid-0 > args_grid.txt )
	util_ManualOverlapGrid.py --parameter mc --parameter-range '[30,60]' --parameter eta --parameter-range '[0.2,0.24999]' --grid-cartesian-npts ${NPTS_IT} --skip-overlap
	(cd $@; echo X --mc-range '[30,60]'     --eta-range '[0.20,0.24999]' --parameter mc --parameter-implied eta --parameter-nofit delta_mc  --fit-method polynomial --fit-order 0 --verbose  --chi-max 0.05 --cap-points 12000  --no-plots  > args_cip.txt)
	(cd $@; echo X  --n-chunk 4000 --time-marginalization --sim-xml overlap-grid.xml.gz --reference-freq 100.0 --adapt-weight-exponent 0.1  --event-time ${EVENT_TIME} --save-P 0.1 --cache-file ${PWD}/zero_noise.cache --fmin-template 10.0 --n-max 2000000 --fmax 1700.0 --save-deltalnL inf --l-max 2  --n-eff 1000  --approximant SEOBNRv4 --adapt-floor-level 0.1 --maximize-only  --d-max 10000.0  --psd-file H1=${PWD}/HLV-ILIGO_PSD.xml.gz --psd-file L1=${PWD}/HLV-ILIGO_PSD.xml.gz --channel-name H1=FAKE-STRAIN --channel-name L1=FAKE-STRAIN  --data-start-time 1000000008 --data-end-time 1000000016 --inv-spec-trunc-time 0 > args_ile.txt)
	(cd $@; echo X  --always-succeed --method lame  --parameter m1 > args_test.txt)
	(cd $@; echo X  --parameter m1 --parameter m2  > args_plot.txt)
#	(cd $@; ls ${PWD}/*psd.xml.gz  ${PWD}/*.cache  > file_names_transfer.txt)
	(cd $@;  create_event_parameter_pipeline_BasicIteration --request-gpu-ILE --ile-n-events-to-analyze 5 --input-grid overlap-grid-0.xml.gz  --ile-args args_ile.txt --cip-args args_cip.txt  --test-args args_test.txt --plot-args args_plot.txt --request-memory-CIP 1024 --request-memory-ILE 1024  --input-grid ${PWD}/overlap-grid.xml.gz --n-samples-per-job ${NPTS_IT} --working-directory ${PWD}/$@ )
# --transfer-file-list file_names_transfer.txt
