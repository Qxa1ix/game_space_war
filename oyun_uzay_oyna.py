
import pygame,random
pygame.init()

w=pygame.display.set_mode((1250,750))
d=True
fps=60
saat=pygame.time.Clock()

class Oyun():
    def __init__(self,oyuncu,uzayli_grup,oyuncu_mermi,uzayli_mermi):
        self.oyuncu=oyuncu
        self.uzayli_grup=uzayli_grup
        self.oyuncu_mermi=oyuncu_mermi
        self.uzayli_mermi=uzayli_mermi

        self.bolum_no=3
        self.puan=0

        self.arkaplan1=pygame.image.load('arka_plan1.jpg')
        self.arkaplan2=pygame.image.load('arka_plan2.jpg')
        self.arkaplan3=pygame.image.load('arka_plan3.jpg')
        self.tebrikler=pygame.image.load('tebrikler.png')

        self.oyuncu_vurus=pygame.mixer.Sound('oyuncu_vurus.wav')
        self.uzayli_vurus=pygame.mixer.Sound('uzayli_vurus.wav')
        pygame.mixer.music.load('arka_plan_sarki.wav')
        pygame.mixer.music.play(-1)

        self.oyun_font=pygame.font.Font('oyun_font.ttf',64)
    def update(self):
        oyun.uzayli_konum_degistirme()
        self.temas()
        self.tamamlandı()
    def cizdir(self):
        self.bolum_no_yazi=self.oyun_font.render('bölüm:'+str(self.bolum_no),True,(200,100,200))
        self.bolum_no_yazi_konum=self.bolum_no_yazi.get_rect()
        self.bolum_no_yazi_konum.topleft=(10,10)


        self.puan_yazi=self.oyun_font.render('puan:'+str(self.puan),True,(200,100,200))
        self.puan_yazi_konum=self.puan_yazi.get_rect()
        self.puan_yazi_konum.topleft=(1000,20)


        if self.bolum_no==1:
            w.blit(self.arkaplan1,(0,0))
        elif self.bolum_no==2:
            w.blit(self.arkaplan2,(0,0))
        elif self.bolum_no==3:
            w.blit(self.arkaplan3,(0,0))
        elif self.bolum_no==4:
            self.bitir()

        w.blit(self.bolum_no_yazi, self.bolum_no_yazi_konum)
        w.blit(self.puan_yazi, self.puan_yazi_konum)
    def uzayli_konum_degistirme(self):
        carpisma,haraket=False,False
        for uzayli in uzayli_grup.sprites():
            if uzayli.rect.right>=1250 or uzayli.rect.left<=0:
                haraket=True
        if haraket ==True:
            for uzayli in uzayli_grup.sprites():
                uzayli.rect.centery+=10*self.bolum_no
                uzayli.yon*=-1
                if uzayli.rect.bottom>680:
                    carpisma=True
        if carpisma==True:
            self.oyuncu.can-=1
            self.oyun_durumu()



    def temas(self):
        if pygame.sprite.groupcollide(self.oyuncu_mermi,self.uzayli_grup,True,True):
            self.oyuncu_vurus.set_volume(0.1)
            self.oyuncu_vurus.play()
            self.puan+=100
        if pygame.sprite.spritecollide(self.oyuncu,self.uzayli_mermi,True):
            self.uzayli_vurus.set_volume(0.2)
            self.uzayli_vurus.play()
            self.oyuncu.can-=1
            self.oyun_durumu()
    def bitir(self):
        b=True
        w.blit(self.tebrikler,(0,0))
        pygame.display.update()
        while b:
            for i in pygame.event.get():
                if i.type==pygame.KEYDOWN:
                    if i.key==pygame.K_RETURN:
                        self.oyun_reset()
                        b=False

    def bolum(self):
        for i in range(5):
            for j in range(10):
                uzayli=Uzayli(64+j*64,100+i*64,self.bolum_no,uzaylimermi)
                self.uzayli_grup.add(uzayli)
    def oyun_durumu(self):
        self.uzayli_mermi.empty()
        self.oyuncu_mermi.empty()
        self.oyuncu.reset()
        for uzayli in self.uzayli_grup.sprites():
            uzayli.reset()
        if self.oyuncu.can==0:
            self.oyun_reset()
        else:
            self.durdur()
    def tamamlandı(self):
        if not self.uzayli_grup:
            self.bolum_no+=1
            self.bolum()
    def durdur(self):
        dur=True
        global d


        yazi1=self.oyun_font.render('can:'+str(self.oyuncu.can),True,(0,100,150))
        yazi1_konum=yazi1.get_rect()
        yazi1_konum.topleft=(100,150)

        yazi2=self.oyun_font.render('devam etmek için "ENTER" bas', True, (0, 100, 150))
        yazi2_konum = yazi2.get_rect()
        yazi2_konum.topleft = (100, 250)

        w.blit(yazi1,yazi1_konum)
        w.blit(yazi2,yazi2_konum)

        pygame.display.update()

        while dur:
            for j in pygame.event.get():
                if j.type==pygame.KEYDOWN:
                    if j.key==pygame.K_RETURN:
                        dur=False
                if j.type==pygame.QUIT:
                    dur=False
                    d=False



    def oyun_reset(self):
        self.bolum_no=1
        self.puan=0
        self.oyuncu.can=5

        self.uzayli_grup.empty()
        self.oyuncu_mermi.empty()
        self.uzayli_mermi.empty()

        self.bolum()


class Oyuncu(pygame.sprite.Sprite):
    def __init__(self,oyuncu_mermi_grup):
        super().__init__()
        self.image = pygame.image.load('uzay_gemi.png')
        self.oyuncu_mermi_grup=oyuncu_mermi_grup
        self.rect=self.image.get_rect()
        self.rect.centerx=1250//2
        self.rect.top=680

        self.hiz=15
        self.can=5
    def update(self):
        tus=pygame.key.get_pressed()
        if tus[pygame.K_a] and self.rect.left>0:
            self.rect.centerx-=self.hiz
        if tus[pygame.K_d] and self.rect.left<1180:
            self.rect.centerx+=self.hiz
    def ates(self):
        if len(self.oyuncu_mermi_grup)<2:
            OyuncuMermi(self.rect.centerx,self.rect.top,self.oyuncu_mermi_grup)
    def reset(self):
        pass

class Uzayli(pygame.sprite.Sprite):
    def __init__(self,x,y,hiz,uzaylimermi):
        super().__init__()
        self.image=pygame.image.load('uzayli.png')
        self.rect=self.image.get_rect()
        self.rect.topleft=(x,y)
        self.uzaylimermi=uzaylimermi
        self.hiz=hiz

        self.basx=x
        self.basy=y
        self.yon=1

        self.uzayliates=pygame.mixer.Sound('uzayli_mermi.wav')
    def update(self):

        self.rect.centerx+=self.hiz*self.yon
        if random.randint(1, 100) > 99 and len(uzaylimermi) < 3:
            self.uzayliates.play()
            self.uzayliates.set_volume(0.1)
            self.ates()
    def ates(self):
        uzayliMermi(self.rect.centerx,self.rect.bottom,uzaylimermi)
    def reset(self):
        self.rect.centerx=self.basx
        self.rect.centery=self.basy
        self.yon=1
class OyuncuMermi(pygame.sprite.Sprite):
    def __init__(self,x,y,oyuncu_mermi_grup):
        super().__init__()
        self.image=pygame.image.load('oyuncu_mermi.png')
        self.rect=self.image.get_rect()
        self.rect.centerx=x
        self.rect.centery=y
        self.oyuncu_mermi_grup=oyuncu_mermi_grup
        self.hiz=10
        oyuncu_mermi_grup.add(self)
    def update(self):
        self.rect.y-=self.hiz
        if self.rect.bottom<0:
            self.kill()



class uzayliMermi(pygame.sprite.Sprite):
    def __init__(self,x,y,uzaylimermi):
        super().__init__()
        self.uzaylimermi=uzaylimermi
        self.image=pygame.image.load('uzayli_mermi.png')
        self.rect=self.image.get_rect()
        self.rect.centerx=x
        self.rect.centery=y
        self.hiz=10
        uzaylimermi.add(self)
    def update(self):
        self.rect.y+=self.hiz
        if self.rect.top>=750:
            self.kill()

oyuncumermi=pygame.sprite.Group()
uzaylimermi=pygame.sprite.Group()

oyuncu_grup=pygame.sprite.Group()
uzayli_grup=pygame.sprite.Group()

oyuncu=Oyuncu(oyuncumermi)
oyuncu_grup.add(oyuncu)



#oyun
oyun=Oyun(oyuncu,uzayli_grup,oyuncumermi,uzaylimermi)
oyun.bolum()



while d:
    for i in pygame.event.get():
        if i.type==pygame.QUIT:
            d=False
        if i.type==pygame.KEYDOWN:
            if i.key==pygame.K_SPACE:
                oyuncu.ates()

    oyun.update()
    oyun.cizdir()

    oyuncu_grup.update()
    oyuncu_grup.draw(w)

    oyuncumermi.update()
    oyuncumermi.draw(w)

    uzayli_grup.update()
    uzayli_grup.draw(w)


    uzaylimermi.update()
    uzaylimermi.draw(w)



    pygame.display.update()
    saat.tick(fps)


pygame.quit()
