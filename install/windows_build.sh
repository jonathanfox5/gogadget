#!/bin/bash

# Clear out any wheels and existing installers that we have
rm -f dist/* && rm -f install/bin/*.whl

# uv lock to check dependencies can be resolved
uv lock

# Build new wheel and copy to bin folder
uv build
cp dist/*.whl install/bin/

# Build windows installer and move to dist folder
iscc install/gogadget_windows.iss
