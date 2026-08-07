
Backend starten (auf api Terminal tab):
uvicorn app.main:app --reload
--> falls nicht klappt (lol)
    dann hier einfahch den versuchen:
     uvicorn app.main:app --reload

Frontend starten (auf web terminal tab):
        (nicht immer)rm -rf .next
    npm run dev
    NEXT_DISABLE_TURBOPACK=1 npm run dev
    --> falls es zu lange dauert beim compilen

neue eigene .env machen mit Template aus .env.example und API Key setzen