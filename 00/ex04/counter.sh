#!/bin/sh

INPUT_CSV_FILE="../ex03/hh_positions.csv"
OUTPUT_CSV_FILE="hh_uniq_positions.csv"


{
    echo "\"name\",\"count\""
    
    tail -n +2 "$INPUT_CSV_FILE" |  
    awk -F, '{print $3}' |          
    sort |                           
    uniq -c |                        
    sort -nr |                       
    awk '{print " "$2 " , "$1}'
} > "$OUTPUT_CSV_FILE"