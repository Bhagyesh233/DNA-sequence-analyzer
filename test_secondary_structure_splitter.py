import pytest
from secondary_structure_splitter import get_file_handle, get_fasta_lists, _verify_lists


def test_get_fasta_lists():
    fasta_content = ">Header 1\nACGT\n>Header 2\nTGCA\n>Header 3\nGATA\n"
    fasta_file = [line + "\n" for line in fasta_content.split("\n") if line.strip()]
    header_list, sequence_list = get_fasta_lists(fasta_file)
    assert header_list == [">Header 1", ">Header 2", ">Header 3"]
    assert sequence_list == ["ACGT", "TGCA", "GATA"]

def test_verify_lists():
    header_list = [">Header 1", ">Header 2"]
    sequence_list = ["ACGT", "TGCA", "GATA"]
    with pytest.raises(SystemExit) as excinfo:
        _verify_lists(header_list, sequence_list)
    assert excinfo.value.code == 1


