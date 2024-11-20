#!/bin/bash

# Clear out any wheels and existing installers that we have
rm dist/*
rm install/bin/*.whl

# Build new wheel and copy to bin folder
poetry build
cp dist/*.whl install/bin/

# Build windows installer and move to dist folder
iscc install/gogadget_windows.iss
mv install/output/*.exe dist/
