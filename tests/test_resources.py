"""
Copyright (C) 2017 Andrew Riha

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

import gzip
import os
import shutil
import warnings

from atomicwrites import atomic_write
import numpy as np

from lineage.resources import Resources, ReferenceSequence
from tests import BaseLineageTestCase


class TestResources(BaseLineageTestCase):
    def setUp(self):
        self.resource = Resources(resources_dir="resources")
        self.del_output_dir_helper()

    def test_get_genetic_map_HapMapII_GRCh37(self):
        genetic_map_HapMapII_GRCh37 = self.resource.get_genetic_map_HapMapII_GRCh37()
        assert len(genetic_map_HapMapII_GRCh37) == 23

    def test_get_cytoBand_hg19(self):
        cytoBand_hg19 = self.resource.get_cytoBand_hg19()
        assert len(cytoBand_hg19) == 862

    def test_get_knownGene_hg19(self):
        knownGene_hg19 = self.resource.get_knownGene_hg19()
        assert len(knownGene_hg19) == 82960

    def test_get_kgXref_hg19(self):
        kgXref_hg19 = self.resource.get_kgXref_hg19()
        assert len(kgXref_hg19) == 82960

    def test_get_assembly_mapping_data_bad_tar(self):
        if os.getenv("DOWNLOADS_ENABLED"):
            with atomic_write(
                "resources/NCBI36_GRCh37.tar.gz", mode="w", overwrite=True
            ):
                pass
            assembly_mapping_data = self.resource.get_assembly_mapping_data(
                "NCBI36", "GRCh37"
            )
            assert len(assembly_mapping_data) == 25

    def test_get_assembly_mapping_data(self):
        assembly_mapping_data = self.resource.get_assembly_mapping_data(
            "NCBI36", "GRCh37"
        )
        assert len(assembly_mapping_data) == 25

    def test_get_all_resources(self):
        resources = self.resource.get_all_resources()
        for k, v in resources.items():
            if v is None:
                assert False
        assert True

    def test__all_chroms_in_tar(self):
        assert not self.resource._all_chroms_in_tar(
            ["PAR"], "resources/NCBI36_GRCh37.tar.gz"
        )

    def test_download_example_datasets(self):
        paths = self.resource.download_example_datasets()

        for path in paths:
            if path is None or not os.path.exists(path):
                warnings.warn("Example dataset(s) not currently available")
                return

        assert True

    def test__load_genetic_map_None(self):
        result = self.resource._load_genetic_map(None)
        assert not result

    def test__load_cytoBand_None(self):
        result = self.resource._load_cytoBand(None)
        assert result.empty

    def test__load_knownGene_None(self):
        result = self.resource._load_knownGene(None)
        assert result.empty

    def test__load_kgXref_None(self):
        result = self.resource._load_kgXref(None)
        assert result.empty

    def test__load_assembly_mapping_data_None(self):
        result = self.resource._load_assembly_mapping_data(None)
        assert not result

    def test__download_file_compress(self):
        result = self.resource._download_file("", "", compress=True)
        assert not result

    def test_get_paths_reference_sequences_invalid_assembly(self):
        assembly, chroms, urls, paths = self.resource._get_paths_reference_sequences(
            assembly="36"
        )
        assert not assembly
        assert not chroms
        assert not urls
        assert not paths

    def test_create_reference_sequences_NCBI36(self):
        assembly, chroms, urls, paths = self.resource._get_paths_reference_sequences(
            assembly="NCBI36", chroms=["MT"]
        )
        seqs = self.resource._create_reference_sequences(assembly, chroms, urls, paths)
        assert len(seqs) == 1
        assert seqs["MT"].__repr__() == "ReferenceSequence(assembly='NCBI36', ID='MT')"
        assert seqs["MT"].ID == "MT"
        assert seqs["MT"].chrom == "MT"
        assert (
            seqs["MT"].url
            == "ftp://ftp.ensembl.org/pub/release-54/fasta/homo_sapiens/dna/Homo_sapiens.NCBI36.54.dna.chromosome.MT.fa.gz"
        )
        assert (
            seqs["MT"].path
            == "resources/reference_sequences/NCBI36/Homo_sapiens.NCBI36.54.dna.chromosome.MT.fa.gz"
        )
        assert os.path.exists(seqs["MT"].path)
        assert seqs["MT"].assembly == "NCBI36"
        assert seqs["MT"].build == "B36"
        assert seqs["MT"].species == "Homo sapiens"
        assert seqs["MT"].taxonomy == "x"

    def test_create_reference_sequences_GRCh37(self):
        assembly, chroms, urls, paths = self.resource._get_paths_reference_sequences(
            assembly="GRCh37", chroms=["MT"]
        )
        seqs = self.resource._create_reference_sequences(assembly, chroms, urls, paths)
        assert len(seqs) == 1
        assert seqs["MT"].__repr__() == "ReferenceSequence(assembly='GRCh37', ID='MT')"
        assert seqs["MT"].ID == "MT"
        assert seqs["MT"].chrom == "MT"
        assert (
            seqs["MT"].url
            == "ftp://ftp.ensembl.org/pub/grch37/current/fasta/homo_sapiens/dna/Homo_sapiens.GRCh37.dna.chromosome.MT.fa.gz"
        )
        assert (
            seqs["MT"].path
            == "resources/reference_sequences/GRCh37/Homo_sapiens.GRCh37.dna.chromosome.MT.fa.gz"
        )
        assert os.path.exists(seqs["MT"].path)
        assert seqs["MT"].assembly == "GRCh37"
        assert seqs["MT"].build == "B37"
        assert seqs["MT"].species == "Homo sapiens"
        assert seqs["MT"].taxonomy == "x"

    def test_create_reference_sequences_GRCh38(self):
        assembly, chroms, urls, paths = self.resource._get_paths_reference_sequences(
            assembly="GRCh38", chroms=["MT"]
        )
        seqs = self.resource._create_reference_sequences(assembly, chroms, urls, paths)
        assert len(seqs) == 1
        assert seqs["MT"].__repr__() == "ReferenceSequence(assembly='GRCh38', ID='MT')"
        assert seqs["MT"].ID == "MT"
        assert seqs["MT"].chrom == "MT"
        assert (
            seqs["MT"].url
            == "ftp://ftp.ensembl.org/pub/release-96/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.chromosome.MT.fa.gz"
        )
        assert (
            seqs["MT"].path
            == "resources/reference_sequences/GRCh38/Homo_sapiens.GRCh38.dna.chromosome.MT.fa.gz"
        )
        assert os.path.exists(seqs["MT"].path)
        assert seqs["MT"].assembly == "GRCh38"
        assert seqs["MT"].build == "B38"
        assert seqs["MT"].species == "Homo sapiens"
        assert seqs["MT"].taxonomy == "x"

    def test_create_reference_sequences_invalid_path(self):
        assembly, chroms, urls, paths = self.resource._get_paths_reference_sequences(
            assembly="GRCh38", chroms=["MT"]
        )
        paths[0] = ""
        seqs = self.resource._create_reference_sequences(assembly, chroms, urls, paths)
        assert len(seqs) == 0

    def test_get_reference_sequences(self):
        seqs = self.resource.get_reference_sequences(chroms=["MT"])
        assert len(seqs) == 1
        assert seqs["MT"].__repr__() == "ReferenceSequence(assembly='GRCh37', ID='MT')"
        assert seqs["MT"].ID == "MT"
        assert seqs["MT"].chrom == "MT"
        assert (
            seqs["MT"].url
            == "ftp://ftp.ensembl.org/pub/grch37/current/fasta/homo_sapiens/dna/Homo_sapiens.GRCh37.dna.chromosome.MT.fa.gz"
        )
        assert (
            seqs["MT"].path
            == "resources/reference_sequences/GRCh37/Homo_sapiens.GRCh37.dna.chromosome.MT.fa.gz"
        )
        assert os.path.exists(seqs["MT"].path)
        assert seqs["MT"].assembly == "GRCh37"
        assert seqs["MT"].build == "B37"
        assert seqs["MT"].species == "Homo sapiens"
        assert seqs["MT"].taxonomy == "x"

    def test_get_all_reference_sequences(self):
        seqs = self.resource.get_all_reference_sequences(chroms=["MT"])
        assert len(seqs) == 3
        assert len(seqs["NCBI36"]) == 1
        assert (
            seqs["NCBI36"]["MT"].path
            == "resources/reference_sequences/NCBI36/Homo_sapiens.NCBI36.54.dna.chromosome.MT.fa.gz"
        )
        assert len(seqs["GRCh37"]) == 1
        assert (
            seqs["GRCh37"]["MT"].path
            == "resources/reference_sequences/GRCh37/Homo_sapiens.GRCh37.dna.chromosome.MT.fa.gz"
        )
        assert len(seqs["GRCh38"]) == 1
        assert (
            seqs["GRCh38"]["MT"].path
            == "resources/reference_sequences/GRCh38/Homo_sapiens.GRCh38.dna.chromosome.MT.fa.gz"
        )

    def test_get_reference_sequences_invalid_assembly(self):
        seqs = self.resource.get_reference_sequences(assembly="36")
        assert len(seqs) == 0

    def test_get_reference_sequences_chrom_not_available(self):
        self.resource.get_reference_sequences(chroms=["MT"])
        del self.resource._reference_sequences["GRCh37"]["MT"]
        seqs = self.resource.get_reference_sequences(chroms=["MT"])
        assert len(seqs) == 1
        assert seqs["MT"].__repr__() == "ReferenceSequence(assembly='GRCh37', ID='MT')"
        assert seqs["MT"].ID == "MT"
        assert seqs["MT"].chrom == "MT"
        assert (
            seqs["MT"].url
            == "ftp://ftp.ensembl.org/pub/grch37/current/fasta/homo_sapiens/dna/Homo_sapiens.GRCh37.dna.chromosome.MT.fa.gz"
        )
        assert (
            seqs["MT"].path
            == "resources/reference_sequences/GRCh37/Homo_sapiens.GRCh37.dna.chromosome.MT.fa.gz"
        )
        assert os.path.exists(seqs["MT"].path)
        assert seqs["MT"].assembly == "GRCh37"
        assert seqs["MT"].build == "B37"
        assert seqs["MT"].species == "Homo sapiens"
        assert seqs["MT"].taxonomy == "x"

    def test_reference_sequence_load_sequence(self):
        seqs = self.resource.get_reference_sequences(chroms=["MT"])
        assert len(seqs["MT"].sequence) == 16569
        assert seqs["MT"].md5 == "c68f52674c9fb33aef52dcf399755519"
        assert seqs["MT"].start == 1
        assert seqs["MT"].end == 16569
        assert seqs["MT"].length == 16569

        seqs["MT"].clear()
        assert seqs["MT"]._sequence.size == 0
        assert seqs["MT"]._md5 == ""
        assert seqs["MT"]._start == 0
        assert seqs["MT"]._end == 0
        assert seqs["MT"]._length == 0

        assert len(seqs["MT"].sequence) == 16569
        assert seqs["MT"].md5 == "c68f52674c9fb33aef52dcf399755519"
        assert seqs["MT"].start == 1
        assert seqs["MT"].end == 16569
        assert seqs["MT"].length == 16569

    def test_reference_sequence_generic_load_sequence(self):
        with open("tests/input/generic.fa", "rb") as f_in:
            with atomic_write(
                "tests/input/generic.fa.gz", mode="wb", overwrite=True
            ) as f_out:
                with gzip.open(f_out, "wb") as f_gzip:
                    shutil.copyfileobj(f_in, f_gzip)

        seq = ReferenceSequence(ID="1", path="tests/input/generic.fa.gz")
        assert seq.ID == "1"
        assert seq.chrom == "1"
        assert seq.path == "tests/input/generic.fa.gz"
        np.testing.assert_array_equal(
            seq.sequence,
            np.array(
                bytearray(
                    "NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNAGGCCGGACN",
                    encoding="utf-8",
                    errors="strict",
                ),
                dtype=np.uint8,
            ),
        )
        assert list("AGGCCGGAC") == list(map(chr, seq.sequence[100:109]))
        assert seq.md5 == "dc86fbda2f6febd77622407beae66b9a"
        assert seq.start == 1
        assert seq.end == 110
        assert seq.length == 110
