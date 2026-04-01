# DNA-sequence-analyzer

Python tools for parsing FASTA files, splitting protein secondary structure sequences, and computing nucleotide statistics including GC content.

## Scripts

1. **secondary_structure_splitter.py** — Extracts protein sequences and secondary structure data from a combined FASTA file into two separate output files: `pdb_protein.fasta` and `pdb_ss.fasta`.

   ```bash
   python secondary_structure_splitter.py -i input_file.fasta
   ```

2. **nt_fasta_stats.py** — Calculates per-sequence nucleotide statistics (A, G, C, T, N counts, GC%, and length) from a FASTA file and writes results in tab-delimited format.

   ```bash
   python nt_fasta_stats.py --infile input.fasta --outfile output.txt
   ```

## Dependencies

Python 3
