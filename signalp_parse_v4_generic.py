import csv

#################################################################
#################################################################
# Name - signalp_parse_v4_generic.py
# Creation Date - 8th September 2014
# Author: Soumya Banerjee
# Website: https://sites.google.com/site/neelsoumya/
#
# Description:
#   Parse output from SignalP
#   Complications: SignalP does not produce tab delimited or comma separated output
#   Example output format:
#
#   name                     Cmax  pos  Ymax  pos  Smax  pos  Smean   D     ?  Dmaxcut    Networks-used
#   PROKKA_00001               0.104  26  0.123  11  0.186   3  0.159   0.136 N  0.510      SignalP-TM
#   PROKKA_00002               0.111  28  0.197  12  0.459   9  0.391   0.288 N  0.570      SignalP-noTM
#
#   We are interested in the columns D and ?
#   However the number of fields and spaces is not fixed.
#   So the parser looks for the first occurrence of Y/N and then extracts that and the field before it
#
#
# Input - 003_signalp_neg.txt
#       SignalP-4.1 gram- predictions
#       name                     Cmax  pos  Ymax  pos  Smax  pos  Smean   D     ?  Dmaxcut    Networks-used
#       PROKKA_00001               0.104  26  0.123  11  0.186   3  0.159   0.136 N  0.510      SignalP-TM
#       PROKKA_00002               0.111  28  0.197  12  0.459   9  0.391   0.288 N  0.570      SignalP-noTM
#       PROKKA_00003               0.103  34  0.136  14  0.216   6  0.185   0.159 N  0.570      SignalP-noTM
#       PROKKA_00004               0.121  47  0.106  47  0.118   4  0.085   0.096 N  0.570      SignalP-noTM
#
# Output - 003_signalp_output_parsed.txt
#       PROKKA_00001	N	0.136
#       PROKKA_00002	N	0.288
#       PROKKA_00003	N	0.159
#       PROKKA_00004	N	0.096
#       PROKKA_00005	N	0.299
#
# Example - python signalp_parse_v4_generic.py '1003_signalp_neg' '1003_signalp_output_parsed.txt'
#
# License - GNU GPL
#
# Change History - 
#                   8th September 2014  - Creation by Soumya Banerjee
#
#################################################################
#################################################################

def func_column_parser(input_file_prism,output_file):


    ##########################
    # open output file
    ##########################

    output_file_ptr  = open(output_file, 'w')

    ###################################################################################
    # read input file
    ###################################################################################

    iLine_number = 1
    with open(input_file_prism, 'r') as input_file_ptr_prism:
        
        for line in input_file_ptr_prism:
            str_temp = str(line)
            str_split_line = str_temp.split(' ')
            # format is 
            #'PROKKA_00001', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '0.104', '', '26', '', '0.123', '', '11', '', '0.186', '', '', '3', '', '0.159', '', '', '0.136', 'N', '', '0.510', '', '', '', '', '', 'SignalP-TM\n']
            iColCount = 1
            if iLine_number >= 3: # disregard first two header lines

                ###################################################################################
                # start counting columns
                # if there is a column with Y/N, then extract that column and the column before it
                ###################################################################################
                
                for sub_string in str_split_line:
                    if sub_string == 'N' or sub_string == 'Y':
                        #print(iColCount - 1)
                        #print(str_split_line[iColCount - 1]) # Signal peptide or not (Y/N) 
                        #print(str_split_line[iColCount - 2]) # D threshold (number)
                        output_file_ptr.write('\t'.join([ str_split_line[0], str_split_line[iColCount - 1], str_split_line[iColCount - 2] ]) + '\n')
                    
                    iColCount = iColCount + 1
                
            iLine_number = iLine_number + 1



    print('done')
    output_file_ptr.close()


if __name__ == "__main__":
    import sys
    func_column_parser(str(sys.argv[1]),str(sys.argv[2]))
