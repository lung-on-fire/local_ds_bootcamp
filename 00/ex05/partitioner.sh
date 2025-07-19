#!/bin/sh

rm *.csv

INPUT_CSV_FILE="../ex03/hh_positions.csv"

tail -n +2 "$INPUT_CSV_FILE" | while IFS=, read -r id created_at name has_test alternate_url; do
    date=$(echo "$created_at" | cut -d'T' -f1)

    if [ ! -f "$date.csv" ]; then
        head -n 1 "../ex03/hh_positions.csv" > "$date.csv"
    fi

    echo  ""$id","$created_at","$name","$has_test","$alternate_url"" >> "$date.csv"
done