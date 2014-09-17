readme

A combination shell script and python program to parse SignalP output

   Shell script (main_signalp_shellparse.sh) to repeatedly call SignalP parser (signalp_parse_v7_generic.py)

   Assumes that SignalP produces a bunch of files of the form 997_signalp_neg, 997_signalp_pos
   where neg is for Gram negative bacteria and pos is for Gram positive bacteria.
   The python program combines data from both files to produce a single output variable that is the logical OR
   i.e. if a peptide is secreted in either the neg or pos files, it will output Yes.

   The shell script repeatedly iterates over many files of the type
   997_signalp_neg, 997_signalp_pos and repeatedly call the program signalp_parse_v7_generic.py
   Finally it cleans up temporary files and produces a consolidated output file

   Example input format: 997_signalp_neg

   name                     Cmax  pos  Ymax  pos  Smax  pos  Smean   D     ?  Dmaxcut    Networks-used     
   PROKKA_00001               0.104  26  0.123  11  0.186   3  0.159   0.136 N  0.510      SignalP-TM       
   PROKKA_00002               0.111  28  0.197  12  0.459   9  0.391   0.288 N  0.570      SignalP-noTM     


 Output - FINAL_SignalP_parsed_file_secreted
	Partition_number        Protein_id      Dthreshold_neg  Signalp_neg     Dthreshold_pos  Signalp_pos     Signalp_output_FINAL
	1003    PROKKA_00001    0.136   N       N       0.122   N
	1003    PROKKA_00002    0.288   N       N       0.270   N
	1003    PROKKA_00003    0.159   N       N       0.141   N
	1003    PROKKA_00004    0.096   N       N       0.108   N


 Example - nohup ./main_signalp_shellparse.sh

 License - GNU GPL

1) main_signalp_shellparse.sh
	Shell script to compute  FINAL_SignalP_parsed_file_secreted
	repeatedly calls signalp_parse_v7_generic.py to parse SignalP output

	
2) signalp_parse_v7_generic.py
	Python script to parse SignalP output
	Produces complete output with Dthreshold values for Gram -ve and +ve

3) signalp_parse_v4_generic.py
	Python script to parse a single file with SignalP output (either Gram -ve or Gram +ve)
	Extracts the Dthreshold and Signalling peptide secreted flag (Y/N)
	Example command - python signalp_parse_v4_generic.py '1003_signalp_neg.txt' '1003_signalp_output_parsed.txt'

4) Example data files
	1003_signalp_neg
	1003_signalp_pos