#!/bin/sh

INPUT_JSON_FILE="$1"
OUTPUT_CSV_FILE="hh.csv"

cp ../ex00/hh.json ./
jq -r -f filter.jq "$INPUT_JSON_FILE"  > "$OUTPUT_CSV_FILE"