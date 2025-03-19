import cv2 as cv
import numpy as np

def zmanjsaj_sliko(slika, sirina, visina):
    '''Zmanjšaj sliko na velikost sirina x visina.'''
    pass

def obdelaj_sliko_s_skatlami(slika, sirina_skatle, visina_skatle, barva_koze) -> list:
    height, width, _ = slika.shape
    
    spodnja_meja = np.array(barva_koze) - 35
    zgornja_meja = np.array(barva_koze) + 35
    
    #Preverimo, da so vrednosti znotraj mej (omejimo jih na 0-255)
    spodnja_meja = np.clip(spodnja_meja, 0, 255)
    zgornja_meja = np.clip(zgornja_meja, 0, 255)

    maska = np.all(np.logical_and(spodnja_meja <= slika, slika <= zgornja_meja), axis=-1)

    rezultat = []

    for y in range(0, height, visina_skatle):
        vrsta = []
        for x in range(0, width, sirina_skatle):
            kvadrat = maska[y:y+visina_skatle, x:x+sirina_skatle]

            if np.any(kvadrat):
                vrsta.append(1)
                cv.rectangle(slika, (x, y), (x + sirina_skatle, y + sirina_skatle), (0, 0, 0), -1) #Oznaci kvadrat
            else:
                vrsta.append(0)
        rezultat.append(vrsta)

    return rezultat

def prestej_piklse_z_barvo_koze(slika, barva_koze) -> int:
    '''Prestej število pikslov z barvo kože v škatli.'''
    pass

def doloci_barvo_koze(slika,levo_zgoraj,desno_spodaj) -> tuple:
    x1, y1 = levo_zgoraj
    x2, y2 = desno_spodaj
    roi = slika[y1:y2, x1:x2]

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
                break
        # Zapremo okno
        kamera.release()
        cv.destroyAllWindows()

    #Izračunamo barvo kože na prvi sliki
    if slika is None:
        print('Slika ni bila naložena.')
    else:
        print('Slika je bila naložena.')

        #Pridobimo dimenzije slike
        height, width, _  = slika.shape
        #Velikost kvadrata (1/8 velikost slike)
        square_size = min(height, width) // 14

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
        kamera = cv.VideoCapture(0)
        if not kamera.isOpened():
            print('Kamera ni bila odprta.')
        else:
            while True:
                # Preberemo sliko iz kamere
                ret1, slika1 = kamera.read()
                cv.imshow('Kamera', slika1)

                # Če pritisnemo tipko 'q', shranimo prvo sliko in zapremo okno
                if cv.waitKey(1) & 0xFF == ord('q'):
                    neobdelana_slika = slika1
                    break
        kamera.release()
        cv.destroyAllWindows()

        sirina_skatle, visina_skatle = 40, 40
        rezultat = obdelaj_sliko_s_skatlami(neobdelana_slika, sirina_skatle, visina_skatle, povprecna_barva)

        print(rezultat)
        cv.imshow("Slika s skatlami", neobdelana_slika)
        cv.waitKey(0)
        cv.destroyAllWindows()

    #Označi območja (škatle), kjer se nahaja obraz (kako je prepuščeno vaši domišljiji)
        #Vprašanje 1: Kako iz števila pikslov iz vsake škatle določiti celotno območje obraza (Floodfill)?
        #Vprašanje 2: Kako prešteti število ljudi?

        #Kako velikost prebirne škatle vpliva na hitrost algoritma in točnost detekcije? Poigrajte se s parametroma velikost_skatle
        #in ne pozabite, da ni nujno da je škatla kvadratna.
    pass