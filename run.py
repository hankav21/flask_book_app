from app import app
   
if __name__ == '__main__':
    # with app.app_context():
    #    db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)
    '''Blok if __name__ == '__main__': zapewnia, że kod w nim zawarty zostanie wykonany tylko wtedy, gdy skrypt app.py jest uruchamiany bezpośrednio.
with app.app_context(): tworzy kontekst aplikacji, co pozwala na dostęp do konfiguracji i zasobów aplikacji.
db.create_all() tworzy wszystkie tabele zdefiniowane w modelach, jeśli jeszcze nie istnieją.
app.run(debug=True) uruchamia serwer Flask w trybie debugowania.'''
