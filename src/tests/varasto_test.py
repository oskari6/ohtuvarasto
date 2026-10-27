import unittest
from varasto import Varasto


class TestVarasto(unittest.TestCase):
    def setUp(self):
        self.varasto = Varasto(10)

    def test_konstruktori_luo_tyhjan_varaston(self):
        # https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertAlmostEqual
        self.assertAlmostEqual(self.varasto.saldo, 0)

    def test_uudella_varastolla_oikea_tilavuus(self):
        self.assertAlmostEqual(self.varasto.tilavuus, 10)

    def test_lisays_lisaa_saldoa(self):
        self.varasto.lisaa_varastoon(8)

        self.assertAlmostEqual(self.varasto.saldo, 8)

    def test_lisays_lisaa_pienentaa_vapaata_tilaa(self):
        self.varasto.lisaa_varastoon(8)

        # vapaata tilaa pitäisi vielä olla tilavuus-lisättävä määrä eli 2
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 2)

    def test_ottaminen_palauttaa_oikean_maaran(self):
        self.varasto.lisaa_varastoon(8)

        saatu_maara = self.varasto.ota_varastosta(2)

        self.assertAlmostEqual(saatu_maara, 2)

    def test_ottaminen_lisaa_tilaa(self):
        self.varasto.lisaa_varastoon(8)

        self.varasto.ota_varastosta(2)

        # varastossa pitäisi olla tilaa 10 - 8 + 2 eli 4
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 4)

    def test_negatiivinen_tilavuus_nollataan():
        varasto = Varasto(-10)

        assert varasto.tilavuus == 0


    def test_negatiivinen_alkusaldo_nollataan():
        varasto = Varasto(10, -5)

        assert varasto.saldo == 0


    def test_liian_suuri_alkusaldo_tayttaa_varaston():
        varasto = Varasto(10, 15)

        assert varasto.saldo == 10


    def test_negatiivinen_lisays_ei_muuta_saldoa():
        varasto = Varasto(10, 5)

        varasto.lisaa_varastoon(-2)

        assert varasto.saldo == 5


    def test_liian_suuri_lisays_tayttaa_varaston():
        varasto = Varasto(10, 5)

        varasto.lisaa_varastoon(8)

        assert varasto.saldo == 10


    def test_negatiivinen_ottaminen_ei_muuta_saldoa():
        varasto = Varasto(10, 5)

        assert varasto.ota_varastosta(-2) == 0
        assert varasto.saldo == 5


    def test_liian_suuri_ottaminen_tyhjentaa_varaston():
        varasto = Varasto(10, 5)

        assert varasto.ota_varastosta(8) == 5
        assert varasto.saldo == 0


    def test_varaston_merkkijono():
        varasto = Varasto(10, 5)

        assert str(varasto) == "saldo = 5, vielä tilaa 5"
