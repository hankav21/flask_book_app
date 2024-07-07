# Bazowy obraz
FROM python:3.7.3-alpine

# Ustawienie katalogu roboczego w kontenerze
WORKDIR /app

# Kopiowanie plików do kontenera
COPY . .

# Aktualizacja pip i instalacja zależności z pliku requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Definiowanie domyślnego polecenia uruchomienia
CMD ["python", "app.py"]
