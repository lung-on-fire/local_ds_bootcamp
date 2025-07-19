#!/bin/sh

INPUT_CSV_FILE="../ex02/hh_sorted.csv"
OUTPUT_CSV_FILE="hh_positions.csv"

head -n 1 "$INPUT_CSV_FILE" > "$OUTPUT_CSV_FILE"
    
tail -n +2 "$INPUT_CSV_FILE" | 
while IFS=, read -r id created_at name has_test alternate_url; do

name=$(echo "$name" | tr -d '"')

if echo "$name" | grep -q "Junior"; then 
    cleaned_name="Junior"
elif echo "$name" | grep -q "Middle"; then 
    cleaned_name="Middle"
elif echo "$name" | grep -q "Senior"; then 
    cleaned_name="Senior"
else
    cleaned_name="-"
fi

echo "\"$id\",\"$created_at\",\"$cleaned_name\",\"$has_test\",\"$alternate_url\"" >> "$OUTPUT_CSV_FILE"
done