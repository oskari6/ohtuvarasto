class Varasto:
    def __init__(self, tilavuus, alku_saldo = 0):
        self.tilavuus = max(tilavuus, 0.0)
        self.saldo = min(max(alku_saldo, 0.0), self.tilavuus)

    # Ominaisuuden voi laskea, joten erillistä kenttää ei tarvita.
    def paljonko_mahtuu(self):
        return self.tilavuus - self.saldo

    def lisaa_varastoon(self, maara):
        if maara < 0:
            return
        if maara <= self.paljonko_mahtuu():
            self.saldo = self.saldo + maara
        else:
            self.saldo = self.tilavuus

    def ota_varastosta(self, maara):
        if maara < 0:
            maara = 0.0
        elif maara > self.saldo:
            maara = self.saldo
            self.saldo = 0.0
        else:
            self.saldo = self.saldo - maara
        return maara

    def __str__(self):
        return f"saldo = {self.saldo}, vielä tilaa {self.paljonko_mahtuu()}"

# test comment
