#!/bin/sh
# Container entrypoint
set -euo pipefail

## functions ####################################

function teardown {
  local status=${1}

  debug "Teardown" "trace=$0#teardown" \
    "status=$status"
  kill -TERM -1 2>/dev/null ||:
}

function logs {
  # uses built-in logger to perform "internal" logging, or logging
  # within lib code
  local level=${1}
  local message=${2}

  shift 2
  logger \
    -p $level \
    -t "`date -u --rfc-2822` ${0}[$$]" \
    -s "$message" -- \
      "--" \
      "$@"
}
function debug { logs DEBUG "$@" ; }
function info  { logs INFO  "$@" ; }
function warning  { logs WARNING  "$@" ; }
function error {
  status=${?}
  logs ERROR "$@"
  return $status
}

## arguments ####################################

export JOBID=${JOBID:?required}

## properties ###################################

ctx="trace=$0#main JOBID=$JOBID"

## main #########################################

trap 'teardown $?' \
  HUP \
  INT \
  EXIT

# reap everything on exit
debug "Enter" $ctx \
  "arguments=`echo $@ | base64 | tr -d '\n'`"

# ensure requirements are satisfied
pip install -r requirements.txt
debug "PIP dependencies resolved" $ctx

if
  info "Launch job" $ctx
  eval "$@" & wait

then
  debug "Job finished" $ctx

else
  error "Job failed" $ctx
fi
