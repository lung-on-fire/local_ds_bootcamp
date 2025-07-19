#!/bin/sh

VACANCY_NAME="$1"
OUTPUT_FILE="hh.json"

if [ $# -eq 1 ]; then
	curl -k "https://api.hh.ru/vacancies?text=${VACANCY_NAME}&per_page=20" | jq '.' > hh.json
else
	echo "Usage: ./hh.sh 'vacancy name'"
fi

#Dlinnaya suboptimalnaya versiya
#curl -H 'User-Agent: shylaisa (shylaisa@student.21-school.ru)' "https://api.hh.ru/vacancies?text=${VACANCY_NAME}&per_page=20" | 
#jq -r '"page: \\(.page)\\nfound: \\(.found)\\nclusters: \\(.clusters)\\narguments: \\(.arguments)\\nper_page: \\(.per_page)\\npages: \\(.pages)\\nitems: \[\\n" + (.items\[\] | (tojson | 
#gsub("\\\\,"; ",\\n") | 
#gsub("\\\\\["; "\[\\n" ) | 
#gsub("\\\\{"; "{\\n") |
#gsub("\\\\\]"; "\\n\]") | 
#gsub("\\\\}"; "\\n}") ))
#\+ "\\n\]"' > "$OUTPUT_FILE"

