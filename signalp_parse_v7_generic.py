import csv

#################################################################
#################################################################
# Name - signalp_parse_v6_generic.py
# Creation Date - 12th September 2014
# Author: Soumya Banerjee
# Website: https://sites.google.com/site/neelsoumya/
#
# Description:
#   Parse output from SignalP, but "pasted" for both Gram -ve and +ve
#   Complications: SignalP does not produce tab delimited or comma separated output
#   Called from main_signalp_shellparse.sh
#
#   Example output format:
#
#   name                     Cmax  pos  Ymax  pos  Smax  pos  Smean   D     ?  Dmaxcut    Networks-used      name   Cmax  pos  Ymax  pos  Smax  pos  Smean   D     ?  Dmaxcut    Networks-used
#   PROKKA_00001               0.104  26  0.123  11  0.186   3  0.159   0.136 N  0.510      SignalP-TM       PROKKA_00001               0.104  26  0.123  11  0.186   3  0.159   0.136 N  0.510      SignalP-TM
#   PROKKA_00002               0.111  28  0.197  12  0.459   9  0.391   0.288 N  0.570      SignalP-noTM     PROKKA_00002               0.111  28  0.197  12  0.459   9  0.391   0.288 N  0.570      SignalP-noTM
#
#   We are interested in the columns D and ?
#   However the number of fields and spaces is not fixed.
#   So the parser looks for the first occurrence of Y/N and then extracts that and the field before it
#
#
# Input - 1003_pasted_negposfile.txt
# SignalP-4.1 gram- predictions # SignalP-4.1 gram+ predictions
# name                     Cmax  pos  Ymax  pos  Smax  pos  Smean   D     ?  Dmaxcut    Networks-used # name                     Cmax  pos  Ymax  pos  Smax  pos  Smean   D     ?  Dmaxcut    Networks-used
# PROKKA_00001               0.104  26  0.123  11  0.186   3  0.159   0.136 N  0.510      SignalP-TM PROKKA_00001               0.110  31  0.114  12  0.171   6  0.133   0.122 N  0.450      SignalP-TM
# PROKKA_00002               0.111  28  0.197  12  0.459   9  0.391   0.288 N  0.570      SignalP-noTM PROKKA_00002               0.115  49  0.198  19  0.469   7  0.381   0.270 N  0.450      SignalP-TM
#
# Output - 1003_signalp_output_parsed.txt
#       1003	PROKKA_00001	N	0.136     0.122 N 
#       1003	PROKKA_00002	N	0.288     0.270 N
#
#
# Example - python signalp_parse_v6_generic.py 1003 '1003_pasted_negposfile.txt' '1003_signalp_output_parsed.txt'
#
# License - GNU GPL
#
# Change History - 
#                   12th September 2014  - Creation by Soumya Banerjee
#
#################################################################
#################################################################

def func_column_parser(iPartition_number,input_file_prism,output_file):


    ##########################
    # read input file
    ##########################

    #input_file_prism = '1003_signalp_neg.txt'
    #output_file = '1003_signalp_output_parsed.txt'

    output_file_ptr  = open(output_file, 'w')

    ###################################################################################
    # read input file
    ###################################################################################

    iLine_number = 1
    with open(input_file_prism, 'r') as input_file_ptr_prism:
        
        #reader = csv.reader(input_file_ptr_prism)#, delimiter = '\t')
        for line in input_file_ptr_prism:
 
            str_temp = str(line)
            str_split_line = str_temp.split(' ')
 
            # format is 
            #'PROKKA_00001', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '0.104', '', '26', '', '0.123', '', '11', '', '0.186', '', '', '3', '', '0.159', '', '', '0.136', 'N', '', '0.510', '', '', '', '', '', 'SignalP-TM\n']
            iColCount = 1
            if iLine_number >= 3: # disregard first two header lines
                #    print(str_split_line[32])
                #    print(str_split_line[31])

                ###################################################################################
                # start counting columns
                # if there is a column with Y/N, then extract that column and the column before it
                ###################################################################################

                iSecondYFound = 0
                
                for sub_string in str_split_line:
                    if sub_string == 'N' or sub_string == 'Y':
                        if iSecondYFound == 0:
                            #print(iColCount - 1)
                            #print(str_split_line[iColCount - 1]) # Signal peptide or not (Y/N) 
                            #print(str_split_line[iColCount - 2]) # D threshold (number)

                            # store values
                            temp_str_name       = str_split_line[0]
                            temp_str_Dthreshold = str_split_line[iColCount - 2]
                            temp_str_signalp    = str_split_line[iColCount - 1]
                            #print(temp_str_signalp)

                            # toggle switch
                            iSecondYFound = 1
                            
                        elif iSecondYFound == 1: # now you have found your second foundation (ahem, Y)

                            # logic: OR logic
                            # Please note that SignalP returns two files per partition for
                            # gram positive and gram negative databases (you can read more on the
                            # SignalP website). While parsing, you can either keep results from both positive
                            # and negative for each PROKKAid for each partition or you can keep only the
                            # positive result (i.e, if it is yes in one and no in another, keep yes.
                            # if yes in both, keep yes. if no in both, keep no. this is the Y/N status for signaling).

                            #print(str_split_line[iColCount - 1])

                            if temp_str_signalp == 'Y' and str_split_line[iColCount - 1] == 'N':
                                temp_str_signalp_output_FINAL = 'Y'
                            elif temp_str_signalp == 'N' and str_split_line[iColCount - 1] == 'Y':
                                temp_str_signalp_output_FINAL = 'Y'
                            elif temp_str_signalp == 'Y' and str_split_line[iColCount - 1] == 'Y':
                                temp_str_signalp_output_FINAL = 'Y'
                            elif temp_str_signalp == 'N' and str_split_line[iColCount - 1] == 'N':
                                temp_str_signalp_output_FINAL = 'N'
                            
                            
                            output_file_ptr.write('\t'.join([ str(iPartition_number), temp_str_name, temp_str_Dthreshold, temp_str_signalp, str_split_line[iColCount - 2], str_split_line[iColCount - 1], temp_str_signalp_output_FINAL ]) + '\n')

                            # toggle switch (REDUNDANT) but still left in there
                            iSecondYFound = 0
                    
                    iColCount = iColCount + 1
                
            iLine_number = iLine_number + 1



    print('Successfully completed')
    output_file_ptr.close()


if __name__ == "__main__":
    import sys

    func_column_parser(int(sys.argv[1]),str(sys.argv[2]),str(sys.argv[3]))

