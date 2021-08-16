#!/bin/bash
for f in *.dat; do rdsamp -r "$(basename "$f" | sed 's/\(.*\)\..*/\1/')"  >"$(basename "$f" | sed 's/\(.*\)\..*/\1/')".txt; done;
