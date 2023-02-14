#1672978481
ls
#1672978488
cat .envrc 
#1672978497
poetry install
#1672978515
lca
#1672978540
poetry install
#1672978729
. .venv/bin/pytes
#1672978731
. .venv/bin/activate
#1672978743
pytest --log-cli-level=DEBUG integration_tests/test_datasets.py 
#1672978815
pytest --log-cli-level=DEBUG -n auto integration_tests/test_datasets.py 
#1672978932
pytest --log-cli-level=DEBUG -n auto integration_tests/test_datasets.py::test_validate_tags
#1673015422
echo "foo fum" | tr ' ' '\n' | grep -E 'fumx$' || echo "OK"
#1673015428
echo "foo fum" | tr ' ' '\n' | grep -E 'fum$' || echo "OK"
#1673015438
FOO=$(echo "foo fum" | tr ' ' '\n' | grep -E 'fum$' || true) ; echo $FOO
#1673015441
FOO=$(echo "foo fum" | tr ' ' '\n' | grep -E 'fuxm$' || true) ; echo $FOO
#1673016595
cd ../../../
#1673027584
vi chariot/models/_upload.py 
#1673027622
vi ~/mup/sklearn_upload.py 
#1673027741
vi chariot/models/_upload.py 
#1673027833
ls ~/.cache/
#1673028778
vi chariot/storage/chariot_storage.py 
#1673028808
vi chariot/models/_upload.py 
#1673028819
vi tests/test_models.py 
#1673028828
vi integration_tests/test_models.py 
#1673028884
vi chariot/models/_upload.py 
#1673028952
ls ~/mup/
#1673029007
ksecret minio
#1673029015
cd ../../../
#1673029355
. .venv/bin/activate
#1673029363
python ~/mup/resnet_upload.py 
#1673029458
python ~/mup/sklearn_predict.py 
#1673029531
ls ~/tmp/*jpg
#1673029539
python ~/mup/sklearn_predict.py 
#1673029601
python ~/mup/chariot_upload.py 
#1673029632
python ~/mup/sklearn_predict.py 
#1673029959
k get isvc
#1673029969
k describe isvc m-2jxpsrheybgjpkutm590xyewfry
#1673039009
cd
#1673041130
ls
#1673041132
gss
#1673041133
make
#1673041138
make codegen-datasets
#1673041143
gs
#1673041152
gs py/libs/sdk
#1673041160
git add py
#1673041162
git add .
#1673041164
gs
#1673041165
gss
#1673041172
git commit -m 'update SDK swagger for datasets'
#1673041174
gsend
#1673041528
cd ../../../
#1673401043
poetry run python -c "import PIL"
#1673542244
gsync
#1673542246
poetry install
#1673542328
k get pods | grep project
#1673542335
k logs chariot-projects-5fb5f76cdd-8qdvs --tail 100 -f
#1673542372
k logs chariot-projects-5fb5f76cdd-8qdvs --tail 100 -f | grep -v healthz
#1673542924
cd ../../../
#1673561288
cd integration_tests/
#1673562589
.venv/bin/pytest integration_tests/test_models.py::test_custom_inference_server
#1673562871
gsync
#1673562910
gc
#1673562915
gc spollack-gha-image-gate-fix
#1673562917
gsync
#1673562921
cd
#1673564595
chariot show
#1673564599
make codegen
#1673564601
make
#1673564604
make codegen-all
#1673564637
gs
#1673564647
gs | grep py$
#1673564651
gd
#1673565132
gss
#1673565145
git commit -m 'sdk codegen' .
#1673565145
gss
#1673565146
gs
#1673565147
git add .
#1673565148
gcan .
#1673565149
gss
#1673565151
gsend
#1673565153
gmr
#1673565299
chariot use-context staging
#1673565309
chariot set base_url https://staging-platform.chariot.striveworks.us
#1673565317
grep BASE_URL *
#1673565328
DEV_BASE_URL=https://staging-platform.chariot.striveworks.us make codegen-all 
#1673565639
settoken
#1673565644
gss
#1673565645
gs
#1673565648
greset .
#1673565648
gs
#1673565652
settoken
#1673565659
DEV_BASE_URL=https://staging-platform.chariot.striveworks.us make codegen-models
#1673565671
DEV_BASE_URL=https://staging-platform.chariot.striveworks.us make codegen-all
#1673565705
vi Makefile 
#1673565718
grep '-all' Makefile 
#1673565723
grep all Makefile 
#1673565728
DEV_BASE_URL=https://staging-platform.chariot.striveworks.us make codegen-resources
#1673565732
grep all Makefile 
#1673565754
~DEV_BASE_URL=https://staging-platform.chariot.striveworks.us make codegen-models codegen-projects codegen-training codegen-validation codegen-resources  codegen-identity codegen-modelexport
#1673565758
DEV_BASE_URL=https://staging-platform.chariot.striveworks.us make codegen-models codegen-projects codegen-training codegen-validation codegen-resources  codegen-identity codegen-modelexport
#1673565999
chariot use-context dev
#1673566007
make codegen-all 
#1673566032
greset .
#1673566034
make codegen-all 
#1673566355
gss
#1673566358
gll
#1673566529
helm get values -n chariot chariot | less
#1673566607
k get configmap
#1673566617
k get configmap flyte-admin-base-config
#1673566620
k get configmap flyte-admin-base-config -o json
#1673566672
helm get values -n chariot chariot > /tmp/a
#1673566677
kc dev02
#1673566679
helm get values -n chariot chariot > /tmp/b
#1673566687
diff /tmp/a /tmp/b
#1673566689
diff /tmp/a /tmp/b | less
#1673566729
diff /tmp/a <(sed 's/dev02/staging-platform/' /tmp/b) | less
#1673566735
diff /tmp/a <(sed 's/dev02/staging-platform/' /tmp/b) | sort | less
#1673566845
kc staging-devops
#1673566849
k get pods | grep flyte
#1673566871
k get -n flyte pods
#1673566877
kc staging-platform
#1673566880
k get -n flyte pods
#1673566887
k get namepsace
#1673566890
k get namespace
#1673566899
k -n flyte get pods
#1673566923
k get namespaces
#1673566930
k -n flyte get all
#1673567048
gsync
#1673567056
gs
#1673567057
gss
#1673567058
gdd
#1673567079
vi generate_enums.py 
#1673567127
DEV_BASE_URL=https://staging-platform.chariot.striveworks.us make codegen-models
#1673567135
Dmake codegen-models
#1673567137
make codegen-models
#1673567147
gss
#1673567149
gdd
#1673567161
vi generate_enums.py 
#1673567192
make -n codegen-models
#1673567196
poetry run python generate_enums.py
#1673567202
fg
#1673567221
poetry run python generate_enums.py
#1673567225
gdd
#1673567231
fg
#1673567235
vi generate_enums.py 
#1673567288
gss
#1673567289
greset generate_enums.py 
#1673567292
poetry run python generate_enums.py
#1673567301
gss
#1673567303
gd chariot/models/_enum.py 
#1673567315
fg
#1673567325
vi chariot/models/_enum.py 
#1673567335
vi generate_enums.py 
#1673567370
fg
#1673567449
poetry run python generate_enums.py
#1673567454
gdd .
#1673567462
fg
#1673567464
vi generate_enums.py 
#1673567482
poetry run python generate_enums.py
#1673567492
fg
#1673567495
poetry run python generate_enums.py
#1673567555
jobs
#1673567556
fg
#1673567642
poetry run python generate_enums.py
#1673567664
fg
#1673567668
jobs
#1673567669
vi generate_enums.py 
#1673567681
poetry run python generate_enums.py
#1673567708
gdd
#1673567718
gss
#1673567725
git commit -m 'sort enum values' generate_enums.py chariot/models/_enum.py 
#1673567727
gsend
#1673568051
gc
#1673568053
gc main
#1673568056
gsync
#1673568061
git checkout origin/resolve-flyte-admin -b resolve-flyte-admin
#1673568197
kc staging-platform
#1673568200
k get pods | grep flyte
#1673568267
cd ../../../
#1673991655
. .venv/bin/activate
#1673991684
pytest -n auto --durations=0 ./integration_tests/test_training.py 
#1673992551
pytest -n auto --durations=0 ./integration_tests/test_training.py::test_errored_after_steps
#1674065385
clear
#1674065386
cd
#1674749408
.venv/bin/pytest --log-cli-level=DEBUG integration_tests/test_checkpoint_to_model_nlp.py 
#1674749440
vi integration_tests/test_checkpoint_to_model_nlp.py 
#1674749456
.venv/bin/pytest --log-cli-level=DEBUG integration_tests/test_checkpoint_to_model_nlp.py 
#1674749482
settoken
#1674749502
.venv/bin/pytest --log-cli-level=DEBUG integration_tests/test_checkpoint_to_model_nlp.py 
#1674749583
fg
#1674749591
.venv/bin/pytest --log-cli-level=DEBUG integration_tests/test_checkpoint_to_model_nlp.py 
#1674749930
cd ../teddy
#1674750915
.venv/bin/pytest --log-cli-level=DEBUG integration_tests/test_checkpoint_to_model_nlp.py 
#1674751060
podman run --rm -it 724664234782.dkr.ecr.us-east-1.amazonaws.com/library/teddy-consumer:main_d7e9e84b43c4cb14b088509c64f98f33aa6b1b12
#1674751083
cd ../teddy
#1674784504
gss
#1674784515
vi integration_tests/test_checkpoint_to_model_nlp.py 
#1674784944
.venv/bin/pytest --log-cli-level=DEBUG integration_tests/test_checkpoint_to_model_nlp.py 
#1674830050
gs
#1674830051
jobs
#1674830054
gs
#1674830059
vi integration_tests/test_checkpoint_to_model_nlp.py 
#1674830070
.venv/bin/pytest --log-cli-level=DEBUG integration_tests/test_checkpoint_to_model_nlp.py 
#1674830185
fg
#1674830192
.venv/bin/pytest --log-cli-level=DEBUG integration_tests/test_checkpoint_to_model_nlp.py 
#1674830685
gd
#1674830687
gd 
#1674830689
gd  .
#1674834362
gh workflow run py-project.yml -f project-path=py/libs/tinnie
#1674834395
cd
#1674868808
.venv/bin/python
#1674868850
cd
#1674953036
ls
#1674953036
gs
#1674953079
vi tools/nx/py/affected.py
#1674953084
vi ~/src/chariot/tools/nx/py/affected.py
#1674953894
vi chariot/config.py 
#1674954043
fg
#1674954728
ack issub chariot/
#1674954732
ack issubclss chariot/
#1674954738
ack issubclass chariot/ | grep -v swagger
#1674954767
fg
#1674954770
jobs
#1674954777
vi ../../../tools/nx/py/affected.py 
#1674954820
vi /home/s.pollack/src/chariot/py/libs/sdk/chariot/config.py
#1674954855
fg
#1674954868
jobs
#1674954874
vi ../../../tools/nx/py/affected.py 
#1674955109
ack subprocess
#1674955110
ack subprocess chariot/
#1674955118
ack subprocess ../teddy
#1674955131
fg
#1674962908
grep model integration_tests/test_training
#1674962909
grep model integration_tests/test_training.py 
#1674962925
ack model chariot/training/
#1674962927
ack model chariot/training/ | grep import
#1674962970
vi chariot/training/_config_types.py
#1674963020
gss
#1674963025
gdd chariot/
#1674963031
greset chariot/
#1674963032
gss
#1674963034
gd integration_tests/
#1674963104
jobs
#1674963105
fg
#1674964200
vi ../../apps/model-recommender/Makefile 
#1674964519
jobs
#1674964520
fg
#1674964699
vi Makefile 
#1674964700
jobs
#1674964703
vi Makefile 
#1674964705
fg
#1674964826
ls
#1674964827
ls -a
#1674964828
ls .nx
#1674964830
du -sh .nx
#1674964833
find .nx
#1674964836
wc -l .nx
#1674964839
ffind .nx | xargs ls
#1674964841
ffind .nx | xargs wc -l
#1674964850
less .nx/integration_tests/test_training_wizard_segmentation.dep
#1674964903
ffind .nx | xargs wc -l
#1674964911
du -sh .nx
#1674964921
jobs
#1674964926
vi ../../../tools/nx/py/f
#1674964930
vi ../../../tools/nx/py/a
#1674964934
vi ../../../tools/nx/py/affected.py 
#1674965800
vi ../../../tools/nx/py/get_deps.py 
#1675126439
jobs
#1675126441
fg
#1675126446
jobs
#1675134335
cd 
#1675302308
vi pyproject.toml 
#1675302396
gnew spollack-sdk-authors
#1675302439
poetry build
#1675302446
twine check
#1675302448
twice
#1675302467
grep author ../*/pyproject.toml
#1675302550
which python
#1675302553
vi .envrc
#1675302579
which python
#1675302584
pytest Striveworks <developers@striveworks.us>"]
#1675302591
pytest integration_tests/test_models.py::test_chariot_classification_model
#1675302637
pytest integration_tests/test_models.py::test_chariot_detection_model
#1675302843
vi integration_tests/test_models.py 
#1675303506
pytest integration_tests/test_models.py::test_chariot_detection_model
#1675303514
fg
#1675303521
pytest integration_tests/test_models.py::test_chariot_detection_model
#1675303551
vi integration_tests/test_models.py 
#1675303560
vi chariot/models/_model.py 
#1675303563
fg
#1675303672
vi pytest integration_tests/test_training.py::test_errored_after_steps
#1675303676
pytest integration_tests/test_training.py::test_errored_after_steps
#1675303689
chariot show
#1675303693
chariot reset
#1675303694
chariot show
#1675303695
pytest integration_tests/test_training.py::test_errored_after_steps
#1675303912
vi ~/src/chariot/.github/workflows/integration-sdk.yml 
#1675303928
vi integration_tests/test_training_wizard_
#1675303932
vi integration_tests/test_training_wizard_detection.py 
#1675304022
vi integration_tests/test_training_advanced_nlp.py 
#1675304060
vi integration_tests/test_checkpoint_to_model_nlp.py 
#1675304086
vi integration_tests/test_training_advanced_nlp.py 
#1675304094
vi integration_tests/test_training_wizard_detection.py 
#1675304111
vi integration_tests/test_training
#1675304114
vi integration_tests/test_training.py 
#1675304130
gdd
#1675304135
gs
#1675304209
ack skip tests/
#1675304211
ack skip integration_tests/
#1675304217
vi integration_tests/test_models.py
#1675304570
gs
#1675304574
vi py/libs/sdk/chariot/models/_model.py
#1675304579
vi chariot/models/_model.py 
#1675304850
pytest integration_tests/test_training_wizard_token_classification.py::test_wizard_token_classification_cpu
#1675305083
echo $RNADOM
#1675305086
echo $RANDOM
#1675305093
echo $(($RANDOM/60))
#1675305095
echo $(($RANDOM/360))
#1675305097
echo $(($RANDOM/60))
#1675305106
man RANDOM
#1675305115
echo $(($RANDOM(1)/60))
#1675305118
echo $(($RANDOM/60))
#1675305122
echo $(($RANDOM/100))
#1675305129
echo $(($RANDOM/300))
#1675305134
echo $(($RANDOM/200))
#1675305143
echo $(($RANDOM/200 + 30))
#1675305176
echo $(($RANDOM/300 + 30))
#1675305468
gc main
#1675305477
ack TODO .github
#1675305482
cd ../../../
#1675359665
python
#1675359730
pytest integration_tests/test_projects.py::test_version
#1675359745
pytest -n auto integration_tests/
#1675362977
pytest -n auto integration_tests/test_projects.py 4
#1675362982
pytest -n auto integration_tests/test_projects.py
#1675362990
pytest -n auto integration_tests/test_datasets.py 
#1675363794
vi integration_tests/test_datasets.py 
#1675363837
pytest --log-cli-level=DEBUG integration_tests/test_datasets.py::test_create_empty_dataset
#1675363841
fg
#1675363860
pytest --log-cli-level=DEBUG integration_tests/test_datasets.py::test_create_empty_dataset
#1675363888
fg
#1675363899
pytest --log-cli-level=DEBUG integration_tests/test_datasets.py::test_create_empty_dataset
#1675363902
fg
#1675363911
ack PROJECT_ID integration_tests/
#1675363914
fg
#1675363992
ack PROJECT_ID integration_tests/
#1675363993
fg
#1675363995
pytest --log-cli-level=DEBUG integration_tests/test_datasets.py::test_create_empty_dataset
#1675363999
fg
#1675364020
pytest --log-cli-level=DEBUG integration_tests/test_datasets.py::test_create_empty_dataset
#1675364026
fg
#1675364813
ack PROJECT_ID integration_tests/
#1675364830
sed -i 's/PROJECT_ID/get_project_id()/g' integration_tests/*
#1675364843
grep 'from.*get_project_id' integration_tests/
#1675364846
ack 'from.*get_project_id' integration_tests/
#1675364882
gs
#1675364886
gd
#1675364907
gss
#1675364911
greset integration_tests/test_*
#1675364918
sed -i 's/PROJECT_ID/get_test_project_id()/g' integration_tests/*
#1675364920
gd
#1675364992
sed 's/\(from integration.*get_test_project_id\)()/\1/' integration_tests/*py
#1675364994
sed -i 's/\(from integration.*get_test_project_id\)()/\1/' integration_tests/*py
#1675364995
gd
#1675365004
gss
#1675365005
jobs
#1675365009
pytest --log-cli-level=DEBUG integration_tests/test_datasets.py::test_create_empty_dataset
#1675365020
jobs
#1675365021
vi integration_tests/conftest.py 
#1675365051
pytest --log-cli-level=DEBUG integration_tests/test_datasets.py::test_create_empty_dataset
#1675365058
vi integration_tests/conftest.py 
#1675365066
pytest --log-cli-level=DEBUG integration_tests/test_datasets.py::test_create_empty_dataset
#1675365068
vi integration_tests/conftest.py 
#1675365071
pytest --log-cli-level=DEBUG integration_tests/test_datasets.py::test_create_empty_dataset
#1675365287
cd ../../../go/apps/api-gateway/
#1675367618
cd src/chariot
#1675392729
cd src/chariot2
#1675398191
cd src/chariot
#1675444925
cd src
#1675449443
cd src/chariot
#1675459826
ls
#1675966339
cd
#1675966340
cd src/api-
#1675966344
cd src/api-comittee/
#1675966514
ls
#1675966516
cd src
#1675969017
cd sr/cchairot2
#1675969020
cd src/chariot2
