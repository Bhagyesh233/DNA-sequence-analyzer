"""
secondary_structure_splitter.py

This script extracts protein sequences
and secondary structure data from a combined input file
and creates two separate output files: 'pdb_protein.fasta' and 'pdb_ss.fasta'.

Usage:
  python secondary_structure_splitter.py -i input_file.fasta

Example:
  python secondary_structure_splitter.py -i input_file.fasta
"""


import argparse
import sys


def get_file_handle(file_name, mode):
    """
    Get a file handle for the given file and mode.
    """
    try:
        f_h = open(file_name, mode)
        return f_h
    except OSError as os_er:
        raise os_er
    except ValueError:
        raise ValueError("Invalid file open mode")


def get_fasta_lists(fasta_file):
    """
    Parse the given FASTA file and return header and sequence lists.
    """
    header_list = []
    sequence_list = []

    current_sequence = ""
    for line in fasta_file:
        line = line.strip()
        if line.startswith(">"):
            if current_sequence:
                sequence_list.append(current_sequence)
            header_list.append(line)
            current_sequence = ""
        else:
            current_sequence += line

    if current_sequence:
        sequence_list.append(current_sequence)

    _verify_lists(header_list, sequence_list)

    return header_list, sequence_list


def _verify_lists(header_list, sequence_list):
    """
    Verify that header and sequence lists have the same size.
    """
    if len(header_list) != len(sequence_list):
        print("Header and Sequence lists size are different in size")
        print("Did you provide a FASTA formatted file?")
        sys.exit(1)


def split_sequences(infile):
    """
    Split sequences into protein and secondary structure files.
    """
    fh_in = get_file_handle(infile, "r")
    protein_file = get_file_handle("pdb_protein.fasta", "w")
    ss_file = get_file_handle("pdb_ss.fasta", "w")

    header_list, sequence_list = get_fasta_lists(fh_in)

    protein_count = 0
    ss_count = 0

    for i in range(len(header_list)):
        if header_list[i].endswith(":sequence"):
            protein_file.write(header_list[i] + "\n")
            protein_file.write(sequence_list[i] + "\n")
            protein_count += 1
        elif header_list[i].endswith(":secstr"):
            ss_file.write(header_list[i] + "\n")
            ss_file.write(sequence_list[i] + "\n")
            ss_count += 1

    fh_in.close()
    protein_file.close()
    ss_file.close()

    # Print the counts to stderr
    sys.stderr.write(f"Found {protein_count} protein sequences\n")
    sys.stderr.write(f"Found {ss_count} ss sequences\n")


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(
        description='Provide a FASTA file '
                    'to perform splitting on sequence and secondary structure')
    PARSER.add_argument('-i', '--infile', dest='infile',
                        help='Path to file to open', required=True)
    ARGS = PARSER.parse_args()

    split_sequences(ARGS.infile)
