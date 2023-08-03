#!/usr/bin/env bash

function print_helper() {
  echo -e "Please use latest perception_training docker image, you can enter \n" \
    "  bash docker/scripts/autocar/perception_training_dev_start.sh &&" \
    "  bash docker/scripts/autocar/perception_training_dev_into.sh\n" \
    "Then use:\n" \
    "  bash pyformat.sh, format all different py files with origin/master\n" \
    "  bash pyformat.sh [FORMAT_PATH], format FORMAT_PATH's all py files"
}

if [ $HOSTNAME != "in-dev-autocar" ]; then
  print_helper
  exit
fi

if ! command -v yapf3 &> /dev/null; then
  print_helper
  exit
fi

if ! command -v pylint3 &> /dev/null; then
  print_helper
  exit
fi

FORMAT_PATH=$1
if [ -z "${FORMAT_PATH}" ]; then
  CURRENT_BRANCH_NAME=$(git rev-parse --abbrev-ref HEAD)
  DEVEL_COMMIT_ID=$(git rev-parse --verify origin/master)
  NCA_COMMIT_ID=$(git merge-base ${CURRENT_BRANCH_NAME} origin/master)
  if [ ${DEVEL_COMMIT_ID} != ${NCA_COMMIT_ID} ]; then
    echo "Please rebase origin/master first!"
    exit
  fi
  FORMAT_FILES=$(git diff origin/master --name-only | grep .py$)
else
  FORMAT_FILES=$(find $FORMAT_PATH -name "*.py")
fi
echo $FORMAT_FILES

if [ -n "${FORMAT_FILES}" ]; then
  yapf3 -i ${FORMAT_FILES}
  pylint3 ${FORMAT_FILES}
else
  echo "there is no python diff between current branch and origin/master"
fi
