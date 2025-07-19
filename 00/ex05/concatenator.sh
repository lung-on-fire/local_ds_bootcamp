#!/bin/sh

OUTPUT_CSV_FILE="hh_combined.csv"

head -n 1 "../ex03/hh_positions.csv" > "$OUTPUT_CSV_FILE"

for file in *.csv; do
    if [ "$file" != "$OUTPUT_CSV_FILE" ]; then

        tail -n +2 "$file" >> "$OUTPUT_CSV_FILE"
    fi
done