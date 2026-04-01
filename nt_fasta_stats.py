"""
This script takes a FASTA file as input,
calculates nucleotide statistics for each sequence,
and writes the results to an output file in tab-delimited format.

Usage:
  python script.py --infile input.fasta --outfile output.txt

Input:
  -i/--infile: Path to the input FASTA file.
  -o/--outfile: Path to the output file where statistics will be written.

The script calculates the number of A's, G's, C's, T's, N's, sequence length,
and GC% for each sequence in the input FASTA file.
The results are written to the output file in a tab-delimited format

Example:
  python script.py --infile input.fasta --outfile output.txt
"""
import argparse
import sys


def get_filehandle(file_name, mode):
    """
    Get a file handle for the given file name and mode.
    file_name: The name of the file.
    mode: The file access mode (e.g., 'r' or 'w').
    return: A file handle.
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
    Extract headers and sequences from a FASTA file.

    fasta_file: The file handle of the FASTA file.
    return: Lists of headers and sequences.
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
    Checks if Header and Sequence list have same size
    """
    if len(header_list) != len(sequence_list):
        print("Header and Sequence lists size are different in size")
        print("Did you provide a FASTA formatted file?")
        sys.exit(1)


def _get_num_nucleotides(nucleotide, sequence):
    """
    Count the occurrences of a specific nucleotide in a DNA sequence.
    """
    if nucleotide not in "AGCTN":
        sys.exit("Did not code this condition")

    return sequence.count(nucleotide)


def _get_gc_content(seq):
    """
    Calculate the GC content percentage of a DNA sequence.
    """
    gc_count = _get_num_nucleotides('G', seq) + _get_num_nucleotides('C', seq)
    return (gc_count / len(seq)) * 100 if len(seq) > 0 else 0


def _get_ncbi_accession(header_string):
    """
    Extract the NCBI accession number from FASTA header.
    """
    return header_string.split()[0].lstrip(">").strip()


def output_results_to_files(header_list, sequence_list, fh_out):
    """
    Generate nucleotide statistics for a list of sequences
    and write the results to an output file.

    Args:
    header_list (list): List of header lines from the FASTA file.
    sequence_list (list): List of sequences from the FASTA file.
    fh_out (file handle): The file handle for writing the statistics.

    The function determines A, G, C, T, N counts, sequence lengths, and GC%.
    It writes the results to the output file in a tab-delimited format.

    """
    fh_out.write("Number\t  Accession\t  "
                 "A's\t G's\t C's\t T's\t N's\tLength\t GC%\n")

    for i, seq in enumerate(sequence_list, start=1):
        accession = _get_ncbi_accession(header_list[i-1])
        a_count = _get_num_nucleotides('A', seq)
        g_count = _get_num_nucleotides('G', seq)
        c_count = _get_num_nucleotides('C', seq)
        t_count = _get_num_nucleotides('T', seq)
        n_count = _get_num_nucleotides('N', seq)
        seq_length = len(seq)
        gc_percent = _get_gc_content(seq)

        fh_out.write(f"{i}\t{accession}\t{a_count}\t{g_count}"
                     f"\t{c_count}\t{t_count}\t{n_count}"
                     f"\t{seq_length}\t{gc_percent:.1f}\n")


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(
        description='Provide a FASTA file to generate nucleotide statistics')
    PARSER.add_argument('-i', '--infile', dest='infile',
                        help='Path to file to open', required=True)
    PARSER.add_argument('-o', '--outfile', dest='outfile',
                        help='Path to file to write',
                        required=True)
    ARGS = PARSER.parse_args()

    FH_IN = get_filehandle(ARGS.infile, "r")
    FH_OUT = get_filehandle(ARGS.outfile, "w")

    LIST_HEADERS, LIST_SEQS = get_fasta_lists(FH_IN)

    output_results_to_files(LIST_HEADERS, LIST_SEQS, FH_OUT)

    FH_IN.close()
    FH_OUT.close()
