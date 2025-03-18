import cv2 as cv
import numpy as np

def zmanjsaj_sliko(slika, sirina, visina):
    '''Zmanjšaj sliko na velikost sirina x visina.'''
    pass

def obdelaj_sliko_s_skatlami(slika, sirina_skatle, visina_skatle, barva_koze) -> list:
    '''Sprehodi se skozi sliko v velikosti škatle (sirina_skatle x visina_skatle) in izračunaj število pikslov kože v vsaki škatli.
    Škatle se ne smejo prekrivati!
    Vrne seznam škatel, s številom pikslov kože.
    Primer: Če je v sliki 25 škatel, kjer je v vsaki vrstici 5 škatel, naj bo seznam oblike
      [[1,0,0,1,1],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[1,0,0,0,1]]. 
      V tem primeru je v prvi škatli 1 piksel kože, v drugi 0, v tretji 0, v četrti 1 in v peti 1.'''
    pass

def prestej_piklse_z_barvo_koze(slika, barva_koze) -> int:
    '''Prestej število pikslov z barvo kože v škatli.'''
    pass

def doloci_barvo_koze(slika,levo_zgoraj,desno_spodaj) -> tuple:
    roi = slika[levo_zgoraj[1]:desno_spodaj[1], levo_zgoraj[1]:desno_spodaj[0]]

    #Preverimo ce je izrezano obmocje
    if roi.size == 0:
        print("Napaka: Izrezana regija je prazna.")
        return None
    
    #izracun povprecne barve
    povprecna_barva = np.mean(roi, axis=(0,1))
    return povprecna_barva

if __name__ == '__main__':
    #Pripravi kamero
    kamera = cv.VideoCapture(0)
    #Zajami prvo sliko iz kamere
    if not kamera.isOpened():
        print('Kamera ni bila odprta.')
    else:
        while True:
            # Preberemo sliko iz kamere
            ret, slika = kamera.read()
            cv.imshow('Kamera', slika)

            # Če pritisnemo tipko 'q', shranimo prvo sliko in zapremo okno
            if cv.waitKey(1) & 0xFF == ord('q'):
                cv.imwrite(".utils/prva_slika.jpg", slika)
                break
        # Zapremo okno
        kamera.release()
        cv.destroyAllWindows()

    #Izračunamo barvo kože na prvi sliki
    slika = cv.imread('.utils/prva_slika.jpg')
    if slika is None:
        print('Slika ni bila naložena.')
    else:
        print('Slika je bila naložena.')

        #Pridobimo dimenzije slike
        height, width, _  = slika.shape
        #Velikost kvadrata (1/8 velikost slike)
        square_size = min(height, width) // 8

        #Izracun koordinat sredinskega kvadrata
        x1 = (width // 2) - (square_size // 2)
        y1 = (height // 2) - (square_size // 2)
        x2 = x1 + square_size
        y2 = y1 + square_size

        #Klic funkcije za izracun barve koze
        povprecna_barva = doloci_barvo_koze(slika, (x1, y1), (x2, y2))

        if povprecna_barva is not None:
            print(f"povprecna barva: {povprecna_barva}")
            

    #Zajemaj slike iz kamere in jih obdeluj     
    
    #Označi območja (škatle), kjer se nahaja obraz (kako je prepuščeno vaši domišljiji)
        #Vprašanje 1: Kako iz števila pikslov iz vsake škatle določiti celotno območje obraza (Floodfill)?
        #Vprašanje 2: Kako prešteti število ljudi?

        #Kako velikost prebirne škatle vpliva na hitrost algoritma in točnost detekcije? Poigrajte se s parametroma velikost_skatle
        #in ne pozabite, da ni nujno da je škatla kvadratna.
    pass