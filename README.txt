
- Backend starten (auf api-terminal tab):
    uvicorn app.main:app --reload
        --> falls nicht klappt (Fehler unbekannt)
            dann das versuchen:
             uvicorn app.main:app --reload

- Frontend starten (auf web-terminal tab):
        (nicht immer) rm -rf .next
    npm run dev
    NEXT_DISABLE_TURBOPACK=1 npm run dev
    --> falls es zu lange dauert beim compilen

WICHTIG: neue eigene .env machen mit Template aus .env.example und API Key setzen

- In Bildbeschreibung_txt sind alle generierten captions und die Ground Truth
- In rosbag_sampling ist der Bilddatensatz einzusehen
