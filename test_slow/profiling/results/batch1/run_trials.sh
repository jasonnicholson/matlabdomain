#!/bin/bash
# usage: run_trials.sh <label> <python> <n>
cd /home/jason/Desktop/sphinx_workspace
label=$1; py=$2; n=$3
for t in $(seq 1 $n); do
  out=/tmp/p1trials/$label-$t
  start=$(date +%s.%N)
  PYTHONPATH="$PWD/matlabdomain" "$py" -X faulthandler -c "
import pathlib, runpy, sphinxcontrib
sphinxcontrib.__path__=[str(pathlib.Path('matlabdomain/sphinxcontrib').resolve())]+[p for p in sphinxcontrib.__path__ if 'matlabdomain/sphinxcontrib' not in p]
ns=runpy.run_path('matlabdomain/test_slow/profiling/profile_build.py')
import sphinxcontrib.mat_types as mt; print('mat_types:', mt.__file__)
ns['main'].__globals__['PROFILE_OUT']=pathlib.Path('$out.prof')
ns['main']()
" > $out.log 2>&1
  rc=$?
  end=$(date +%s.%N)
  echo "$label trial $t rc=$rc wall=$(echo "$end - $start" | bc)" | tee -a /tmp/p1trials/summary.txt
done
