#!/bin/bash

scp ./*.py pi@r-1:~/python/
scp manifest pi@r-1:~/python/manifest

ssh pi@r-1 'cd python && ./build.sh'