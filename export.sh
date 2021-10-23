#!/usr/bin/env bash
###################
# INCOMPLETE
###################

# check version
version=$(cat ./itn_export/version.txt)
echo "Exporting version $version"
# export
python pynini_export_beta.py --output_dir far_beta --grammars itn_grammars --force
zip ./itn_export/itn_far-latest.zip far_beta
zip ./itn_export/itn_far-"${version}".zip far_beta
cp -R ./far_beta ./release_history/far_v"${version}"

# push
git add ./itn_export ./release_history
git commit -m "release $version"
git checkout -b "${version}"
git push origin "${version}"

