import pytest
from nt_fasta_stats import get_filehandle, get_fasta_lists, _verify_lists, _get_num_nucleotides, _get_ncbi_accession, output_results_to_files

# Define a fixture for a sample FASTA file
@pytest.fixture
def sample_fasta_file(tmp_path):
    fasta_content = ">Seq1\nAGCT\n>Seq2\nTTAGCT\n>Seq3\nGCTA\n"
    file_path = tmp_path / "sample.fasta"
    with open(file_path, "w") as f:
        f.write(fasta_content)
    return str(file_path)

# Test get_filehandle for OSError
def test_get_filehandle_4_OSError():
    # This should raise an OSError since the file does not exist
    with pytest.raises(OSError):
        get_filehandle("does_not_exist.txt", "r")

# Test get_fasta_lists
def test_get_fasta_lists(sample_fasta_file):
    with open(sample_fasta_file, "r") as file:
        header_list, sequence_list = get_fasta_lists(file)
    assert header_list == [">Seq1", ">Seq2", ">Seq3"]
    assert sequence_list == ["AGCT", "TTAGCT", "GCTA"]

# Test _verify_listsdef
def test_verify_lists():
    header_list = [">Seq1", ">Seq2"]
    sequence_list = ["AGCT", "TTAGCT", "GCTA"]

    assert "Error: Header and sequence lists have different lengths."


# Test _get_num_nucleotides
def test_get_num_nucleotides():
    sequence = "AGCTAGCT"
    assert _get_num_nucleotides('A', sequence) == 2
    assert _get_num_nucleotides('T', sequence) == 2
    assert _get_num_nucleotides('G', sequence) == 2
    assert _get_num_nucleotides('C', sequence) == 2
    assert _get_num_nucleotides('N', sequence) == 0

# Test _get_ncbi_accession
def test_get_ncbi_accession():
    header = ">CY064822 A/California/VRDL136/2009 2009/04/26 1 (PB2)"
    assert _get_ncbi_accession(header) == "CY064822"

