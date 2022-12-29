# TEE PELI TÄHÄN
import pygame
from random import sample, randint, choice

class Robo_hyppely:
    def __init__(self):
        pygame.init()
    
        pygame.display.set_caption('Robo hyppely') 
        self.leveys, self.korkeus = 660, 750
        self.naytto = pygame.display.set_mode((self.leveys, self.korkeus))
        self.kello = pygame.time.Clock() 

        self.lataa_kuvat()
        self.y = self.korkeus-self.robo.get_height()-50
        self.x = self.leveys//2-self.robo.get_width()//2

        self.kaynnissa = False
        self.ohje_paalla = True
        self.laskuri = 0

        self.vasemmalle = False
        self.oikealle = False
        self.hyppaa = False

        self.painovoima = 1
        self.hyppy =  17
        self.nopeus = self.hyppy

        self.kolikot()
        self.hirviot()
        self.silmukka()

    def lataa_kuvat(self):
        self.robo = pygame.image.load("robo.png")
        self.hirvio = pygame.image.load("hirvio.png")
        self.kolikko = pygame.image.load("kolikko.png")

    def kolikot(self):
        self.maara = 5
        self.kolikko_lista = []
        for i in range(self.maara):
            x = randint(0, self.leveys-self.kolikko.get_width())
            y = -randint(self.kolikko.get_height(), 1000)
            self.kolikko_lista.append([x, y])

    # Tässä funktiossa on tarkoitus lisätä hirviöt listaan niin, että niiden välimatka olisi satunnainen. 
    # Alla oleva koodi ajaa asian mutta nyt hirviöt loppuvat jossain vaiheessa kun ne ovat menneet ruudun ulkopuolle koska x koordinaattia ei aseteta uudelleen (katso rivistä 94 alken oleva koodi).
    # Jos x koordinaatti asetettaisiin loopissa niin se aiheuttaa sen, että hirviot voivat tulla päällekkäin vaikka käyetetään randint funktiota. Tästä syystä pitäisi löytää jokin muu ratkaisu.
    def hirviot(self):
        hirviot_otanta = sample(range(self.leveys, 500000, 260),1000)
        self.hirvio_lista = []
        for i in range(1000):
            x = hirviot_otanta[i]
            y = self.korkeus-self.hirvio.get_height()-50
            self.hirvio_lista.append([x, y])
            
    def silmukka(self):
        self.pelin_ohje()
        while self.kaynnissa:
            self.naytto.fill((0, 30, 60))
            self.piirra_naytto()
            self.piirra_otsikot()
            self.tutki_tapahtumat()
            self.liikuta_robottia()
            pygame.display.flip()
            self.kello.tick(60)
    
    def pelin_ohje(self):
        self.fontti = pygame.font.SysFont("Verdana", 50)
        self.fontti2 = pygame.font.SysFont("Verdana", 18)

        peli = self.fontti.render("*ROBO HYPPELY*", True, (0, 150, 0))
        nappaimet = self.fontti2.render("Liikuta robottia nuolinäppäimillä ja hyppää välilyönnillä", True, (0, 150, 0))
        nappaimet_ohje = self.fontti2.render("Aloita peli painamalla Enter tai lopeta painamalla escape", True, (0, 150, 0))

        peli_keskella = peli.get_rect(center=(self.leveys//2, 250))
        nappaimet_keskella = nappaimet.get_rect(center=(self.leveys//2, 400))
        nappaimet_ohje_keskella = nappaimet.get_rect(center=(self.leveys//2, 450))
        while self.ohje_paalla:
            self.naytto.fill((0, 0, 0))
            self.naytto.blit(peli, peli_keskella)
            self.naytto.blit(nappaimet, nappaimet_ohje_keskella)
            self.naytto.blit(nappaimet_ohje, nappaimet_keskella)
            self.tutki_tapahtumat()
            pygame.display.flip()
        
    def piirra_naytto(self):
        self.naytto.blit(self.robo, (self.x, self.y))
        for i in range(self.maara):
            self.kolikko_lista[i][1] += 4
            self.naytto.blit(self.kolikko, (self.kolikko_lista[i][0], self.kolikko_lista[i][1]))
            if self.y + self.robo.get_height() >= self.kolikko_lista[i][1]+self.kolikko.get_height() >= self.y and self.x-self.kolikko.get_width() <= self.kolikko_lista[i][0] <= self.x + self.kolikko.get_width():
                self.laskuri += 1  
                self.kolikko_lista[i][0] = randint(0, self.leveys-self.kolikko.get_width())
                self.kolikko_lista[i][1] = -randint(self.kolikko.get_height(), 1000)
            elif self.kolikko_lista[i][1] >= self.korkeus - 50:
                self.kolikko_lista[i][0] = randint(0, self.leveys-self.kolikko.get_width())
                self.kolikko_lista[i][1] = -randint(self.kolikko.get_height(), 1000)

        for hirvio in self.hirvio_lista:
            hirvio[0] -= 5
            self.naytto.blit(self.hirvio, (hirvio[0], hirvio[1]))
            if hirvio[1] <= self.y+self.robo.get_height() and self.x-self.hirvio.get_width() <= hirvio[0] <= self.x + self.hirvio.get_width():
                self.kaynnissa = False
                self.peli_loppu()
                    
    def piirra_otsikot(self):
        self.fontti = pygame.font.SysFont("Verdana", 14)
        laskuri = self.fontti.render(f"Pisteet: {self.laskuri}", True, (0, 150, 0))
        valikko = self.fontti.render(f"{'Escape = poistu pelistä'} {'F2 = uusi peli':>20}", True, (0, 0, 0))
        keskita_valikko_teksti = valikko.get_rect(center=(self.leveys//2, self.korkeus-50//2))

        pygame.draw.rect(self.naytto, (50, 50, 0), (0, self.korkeus-50, self.leveys, 50))
        pygame.draw.line(self.naytto, (200, 0, 0), (0, self.korkeus-50), (self.leveys, self.korkeus-50), 2)

        self.naytto.blit(laskuri, (10, 10))
        self.naytto.blit(valikko, keskita_valikko_teksti)

    def tutki_tapahtumat(self):
        for tapahtuma in pygame.event.get():
            if tapahtuma.type == pygame.KEYDOWN:
                if tapahtuma.key == pygame.K_SPACE:
                    self.hyppaa = True
                if tapahtuma.key == pygame.K_LEFT:
                    self.vasemmalle = True 
                if tapahtuma.key == pygame.K_RIGHT:
                    self.oikealle = True
                if tapahtuma.key == pygame.K_RETURN:
                    self.ohje_paalla = False
                    self.kaynnissa = True
                if tapahtuma.key == pygame.K_F2:
                    self.uusi_peli()
                if tapahtuma.key == pygame.K_ESCAPE:
                    exit()

            if tapahtuma.type == pygame.KEYUP:
                if tapahtuma.key == pygame.K_LEFT:
                    self.vasemmalle = False
                if tapahtuma.key == pygame.K_RIGHT:
                    self.oikealle = False
                    
            if tapahtuma.type == pygame.QUIT:
                exit()
    
    def liikuta_robottia(self):
        if self.vasemmalle and self.x >= 0:
            self.x -= 4
        if self.oikealle and self.x <= self.leveys - self.robo.get_width():
            self.x += 4
        if self.hyppaa:
            self.y -= self.nopeus
            self.nopeus -= self.painovoima
            if self.nopeus < -self.hyppy:
                self.hyppaa = False
                self.nopeus = self.hyppy
    
    def peli_loppu(self):
        fontti = pygame.font.SysFont("Verdana", 34)
        peli_ohi_ilmoitus = fontti.render(f"Peli päättyi!", True, (255, 0, 0))
        keskita_teksti = peli_ohi_ilmoitus.get_rect(center=(self.leveys//2, self.korkeus//2))
        while True:
            self.naytto.fill((0, 0, 0))
            self.naytto.blit(peli_ohi_ilmoitus, keskita_teksti)
            self.piirra_otsikot()
            self.tutki_tapahtumat()
            pygame.display.flip()
        
    def uusi_peli(self):
        Robo_hyppely()

if __name__ == "__main__":
    Robo_hyppely()
    
