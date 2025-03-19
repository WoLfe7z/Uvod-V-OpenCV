import cv2 as cv
import numpy as np
import time

def zmanjsaj_sliko(slika, sirina, visina):
    return cv.resize(slika, (sirina, visina))

def obdelaj_sliko_s_skatlami(slika, sirina_skatle, visina_skatle, barva_koze) -> list:
    height, width, _ = slika.shape
    
    spodnja_meja, zgornja_meja = barva_koze

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
    spodnja_meja, zgornja_meja = barva_koze

    maska = np.all(np.logical_and(spodnja_meja <= slika, slika <= zgornja_meja), axis=-1)

    #Preštejemo True vrednosti v maski, ki označujejo kožo
    stevilo_pikslov_koze = np.sum(maska)  
    return stevilo_pikslov_koze

def doloci_barvo_koze(slika,levo_zgoraj,desno_spodaj) -> tuple:
    x1, y1 = levo_zgoraj
    x2, y2 = desno_spodaj
    roi = slika[y1:y2, x1:x2]

    #izracun povprecne barve
    povprecna_barva = np.mean(roi, axis=(0,1))

    spodnja_meja = np.clip(povprecna_barva - 35, 0, 255)
    zgornja_meja = np.clip(povprecna_barva + 35, 0, 255)

    return (spodnja_meja, zgornja_meja)

if __name__ == '__main__':
    #Pripravi kamero
    kamera = cv.VideoCapture(0)
    width, height = 340, 220
    kamera.set(3, width)
    kamera.set(4, height)

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

        kamera.release()
        cv.destroyAllWindows()

    #Izračunamo barvo kože na prvi sliki
    if slika is None:
        print('Slika ni bila naložena.')
    else:
        print('Slika je bila naložena.')

        #Pridobimo dimenzije slike
        height, width, _  = slika.shape
        #Velikost kvadrata (1/14 velikost slike)
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
   
        #Zajememo drugo sliko
        kamera = cv.VideoCapture(0)
        width, height = 340, 220
        kamera.set(3, width)
        kamera.set(4, height)

        sirina_skatle, visina_skatle = 20, 20

        #Spremenljivka za merjenje FPS
        start_time = time.time()
        frame_count = 0

        if not kamera.isOpened():
            print('Kamera ni bila odprta.')
        else:
            while True:
                ret1, slika1 = kamera.read()
                cv.imshow('Kamera', slika1)

                rezultat = obdelaj_sliko_s_skatlami(slika1, sirina_skatle, visina_skatle, povprecna_barva)
               
                #Izracun fps
                frame_count += 1
                elapsed_time = time.time() - start_time
                if elapsed_time > 0:
                    fps = frame_count / elapsed_time
                else:
                    fps = 0

                cv.putText(slika1, f"FPS: {fps:.2f}", (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv.LINE_AA)
                cv.imshow("Slika s skatlami", slika1)

                if cv.waitKey(1) & 0xFF == ord('q'):
                    break

            cv.waitKey(0)
            cv.destroyAllWindows()

        kamera.release()
        cv.destroyAllWindows()

        #Vprašanje 1: Kako iz števila pikslov iz vsake škatle določiti celotno območje obraza (Floodfill)?
            #Odg: Ko ima skatla dovolj pikslov jo oznacimo kot del obraza. S Floodfill bi oznacili sosednje skatle, ki imajo podrobne vrednosti kot prva skatla. Tako se znebimo, samotnih skatel, ki se lahko pojavijo v ozadju

        #Vprašanje 2: Kako prešteti število ljudi?
            #Odg: Lahko bi uporabili Floodfill. Floodfill bi ustvaril vec obmocij, kjer bi vrednosti bile podobne. torej bi teoreticno nasel vec skatel, ki bi imele sosednje skatle podobne, in bi jih tvoril v obraze. Potem bi lahko samo presteli obmocja, kjer se nahajajo obrazi in dobili stevilo oseb.

        #Kako velikost prebirne škatle vpliva na hitrost algoritma in točnost detekcije? Poigrajte se s parametroma velikost_skatle
        #in ne pozabite, da ni nujno da je škatla kvadratna.
            #Odg: Vecje skatle povecajo hitrost delovanja algoritma, manjse skatle pa so pocasnejse, vendar zboljsajo natancnost algoritma
    pass