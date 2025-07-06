# Tablica Ogłoszeń

Prosta aplikacja FastAPI z frontendem HTML, działająca lokalnie i w chmurze (Railway).

## Funkcje
- Przeglądanie ogłoszeń
- Dodawanie, edycja i usuwanie ogłoszeń
- Zapis do pliku `data.json` 

## Technologie
- Backend: FastAPI
- Frontend: HTML + CSS (inline)
- Hosting: Railway
- Konteneryzacja: Docker

## Uruchomienie lokalne

### 1. Klonuj repozytorium
bash
git clone https://github.com/annaguzowska/tablica_ogloszen.git
cd tablica_ogloszen

### 2. Zbuduj obraz Dockera
bash
docker build -t tablica_ogloszen

### 3. Uruchom kontener
bash
docker run -p 8000:8000 tablica_ogloszen

### 4. Otwórz aplikację w przeglądarce
http://localhost:8000/tablica

## Wersja chmurowa
Aplikacja jest dostępna pod adresem: tablicaogloszen-production-85ba.up.railway.app

## Screeny aplikacji

### Uruchomiony Docker
![Docker run](screenshots/docker_running.png)

### Widok strony głównej
![Strona główna](screenshots/homepage.png)

### Widok strony głównej railway
![Railway](screenshots/railway_live.png)

