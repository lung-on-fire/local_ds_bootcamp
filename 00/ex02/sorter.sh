#!/bin/sh

INPUT_CSV_FILE="../ex01/hh.csv"
OUTPUT_CSV_FILE="hh_sorted.csv"

head -n 1 "$INPUT_CSV_FILE" > "$OUTPUT_CSV_FILE"
tail -n +2 "$INPUT_CSV_FILE" | sort -t "," -k 2 -k 1n >> "$OUTPUT_CSV_FILE"


#alternative
#head -n 1 "$INPUT_CSV_FILE" > "$OUTPUT_CSV_FILE"
#tail -n +2 "$INPUT_CSV_FILE" | sort -t, -k2,2 -k1,1n >> "$OUTPUT_CSV_FILE"
