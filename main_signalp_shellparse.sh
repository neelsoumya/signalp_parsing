#!/bin/sh

#################################################################
# Name - main_signalp_shellparse.sh
# Creation Date - 12th September 2014
# Author: Soumya Banerjee
# Website: https://sites.google.com/site/neelsoumya/
#
# Description:
#   Shell script to repeatedly call SignalP parser
#   Parse output from SignalP, but "pasted" for both Gram -ve and +ve
#   Complications: SignalP does not produce tab delimited or comma separated output
#   Repeatedly calls from signalp_parse_v7_generic.py
#
#   Assumes that SignalP produces a bunch of files of the form 997_signalp_neg, 997_signalp_pos
#   where neg is for Gram negative bacteria and pos is for Gram positive bacteria.
#   This program combines data from both files to produce a single output variable that is the logical OR
#   i.e. if a peptide is secreted in either the neg or pos files, it will output Yes.
#   This shell script repeatedly iterates over many files of the type
#   997_signalp_neg, 997_signalp_pos and repeatedly call the program signalp_parse_v7_generic.py
#   Finally it cleans up temporary files and produces a consolidated output file
#
#   Example input format: 997_signalp_neg
#
#   name                     Cmax  pos  Ymax  pos  Smax  pos  Smean   D     ?  Dmaxcut    Networks-used     
#   PROKKA_00001               0.104  26  0.123  11  0.186   3  0.159   0.136 N  0.510      SignalP-TM       
#   PROKKA_00002               0.111  28  0.197  12  0.459   9  0.391   0.288 N  0.570      SignalP-noTM     
#
#
# Output - FINAL_SignalP_parsed_file_secreted
#	Partition_number        Protein_id      Dthreshold_neg  Signalp_neg     Dthreshold_pos  Signalp_pos     Signalp_output_FINAL
#	1003    PROKKA_00001    0.136   N       N       0.122   N
#	1003    PROKKA_00002    0.288   N       N       0.270   N
#	1003    PROKKA_00003    0.159   N       N       0.141   N
#	1003    PROKKA_00004    0.096   N       N       0.108   N
#
#
# Example - nohup ./main_signalp_shellparse.sh
#
# License - GNU GPL
#
# Change History - 
#                   12th September 2014  - Creation by Soumya Banerjee
#
#################################################################
#################################################################



iCount=1
for file_name in `ls *_signalp_neg *_signalp_pos | sort`
do
        if [ $iCount = 1 ]
        then
                prev_filename=$file_name
                #echo $prev_filename

                # toggle switch
                iCount=2
        else
                paste -d' ' $prev_filename $file_name > temp_file

                # split name on _ (underscore) to get partition number
                str_partition_array=(${prev_filename//_/ })
                echo ${str_partition_array[0]}

                # call python parser to parse pasted file and infer whether secreted peptide or not
                # no header line use signalp_parse_v7_generic.py
                # if you want header line use signalp_parse_v6_generic.py
                # Syntax is     
                # syntax is python signalp_parse_v6_generic.py 1003 '1003_pasted_negposfile.txt' '1003_signalp_output_parsed.txt'
                python signalp_parse_v7_generic.py ${str_partition_array[0]} temp_file ${str_partition_array[0]}_signalp_parsed_output

                #cat temp_file

                # remove temp_file so that it is not read by for loop as list of files
                rm temp_file

                #echo $prev_filename 
                #echo $file_name
                #sleep 10
                #rm temp_file

                # toggle switch
                iCount=1
        fi

done


# concatenate all parsed output files of 1003_signalp_output_parsed
# output header line
echo -e 'Partition_number\tProtein_id\tDthreshold_neg\tSignalp_neg\tDthreshold_pos\tSignalp_pos\tSignalp_output_FINAL' > FINAL_SignalP_parsed_file_secreted
cat *_signalp_parsed_output >> FINAL_SignalP_parsed_file_secreted


# remove temporary parsed files
rm *_signalp_parsed_output

