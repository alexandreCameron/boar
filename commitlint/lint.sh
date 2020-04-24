#!/bin/bash

# $1 : BRANCH_NAME : str of git branch
# $2 : ENV_EXECUTION : str local or cloud

#Parse the branche name from /refs/heads/<BN> to <BN>
branch_name=$(echo $1 | sed 's/refs\/heads\///g')

#Check branching convention
if [ $branch_name = "master" ]
then
    echo "Master branch detected"
    exit 0
elif $(echo $branch_name | grep -Evq "^(feature-|bugfix-|hotfix-|release-|renovate-|renovate/)")
then
    echo "Wrong branch name, please use feature-, bugfix-, hotfix- or release- as prefix $branch_name"
    exit 1
fi

#Check messages convention
if [ $2 = "local" ]; then
    commitlint --config commitlint/commitlint.config.js --to $(git rev-parse $branch_name) --from $(git rev-parse origin/master)
elif [ $2 = "cloud" ]; then
    commitlint --config commitlint/commitlint.config.js --to $(git rev-parse origin/$branch_name) --from $(git rev-parse origin/master)
else
    echo $2 condition not defined
    exit 1
fi