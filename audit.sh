#!/bin/env bash

if [ -z "$1" ]; then
	echo "Please supply a threshold value for session to be considered complete"
	exit
fi
# Set threshold for number of lines required to be considered complete data 
thresh=$1
path=/home/jackgray/Downloads/aliens/aliens

pushd $path
rm *${thresh}.*sv 	# delete file if one for designated threshold exists so that new data isn't appended with old

ls $path
find . -maxdepth 1 -type f ! -name "sub-s9*" ! -name "sub-s8*" ! -name "sub-s6*"
for subj in $(find . -maxdepth 1 -type d ! -name "sub-s9*" ! -name "sub-s8*" ! -name "sub-s7*" ! -name "sub-s6*" -name "sub-*"); do
    
	((subj_count++))
	subj_sessions=$(ls $subj | wc -l)
    printf "\n${subj},${subj_sessions}" >> summary_${thresh}.csv
	
	for ses in $(ls $subj); do

		response_count=$(cat $subj/$ses/*raw* | wc -l)

		if [ "$response_count" -lt $thresh ]; then

			printf "\n\n!******Session possibly incomplete: *******"
			printf "\n${subj}	${ses}	${response_count}" #>> missing_data_${thresh}.tsv
			((incomplete_count++))
			else
				printf "\n${subj}	${ses}	${response_count}" >> complete_data_${thresh}.tsv
				((complete_count++))	
		fi
	done
	((total_sessions+=${subj_sessions}))
done

popd

printf "Moving log files to current directory..\n"

# Add header labels
printf "subject	session	responses \n$(cat ${path}/missing_data_${thresh}.tsv)" > missing_data_${thresh}.tsv
printf "subject,total_sessions\n$(cat ${path}/summary_${thresh}.csv)" > summary_${thresh}.csv
printf "subject	session	responses\n$(cat ${path}/complete_data_${thresh}.tsv)" > complete_data_${thresh}.tsv

# Print report
printf "\n\n\n\n\n\n\n\n\n**************************************************************" > report.txt
printf "\nNumber of sessions with fewer than ${thresh} responses: ${incomplete_count}" > report.txt

printf "\nTotal number of subjects scanned: ${subj_count}" >> report_${thresh}.txt
printf "\nTotal number of sessions: ${total_sessions}" >> report_${thresh}.txt

avg_compl=$((${total_sessions}/${subj_count}))

printf "\nAverage completion rate: ${avg_compl}" >> report_${thresh}.txt

exceed_count=$((${total_sessions}-${incomplete_count})) >> report_${thresh}.txt
printf "\nNumber of sessions with more than ${thresh} responses: ${exceed_count}\n\n\n"

cat complete_data_$thresh.tsv
cat report_${thresh}.txt

