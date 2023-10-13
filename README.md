# Online evalueringer worker

## Beskrivelse

Dette Python script er designet til at automatisere processen med at sende fagevalueringer via Lectio's og en anden evalueringsplatform. Scriptet har flere funktioner, herunder at tjekke tidsfrister og planlægge evalueringer baseret på databasen.

## Forudsætninger

- Python
- PostgreSQL database
- FastAPI eller anden API for Lectio
- Eval API (bruges til at lukke evalueringer)
- `decouple` Python pakken for at læse konfigurationsfiler

## Opsætning

1. Installer nødvendige Python pakke som er i requirements.txt filen:

    ```
    pip install -r requirements.txt
    ```



2. Opret en `.env` fil med følgende indhold:

    ```
    LECTIO_RPA_USER= 
    LECTIO_RPA_PASSWORD= 
    LECTIO_RPA_TEST_CLASS= 
    LECTIO_SEND_MSG_URL= 
    LECTIO_LOGIN_URL= 
    PSQL_DATABASENAME=
    PSQL_USER=ivvbbxpfxninvn
    PSQL_PASSWORD=
    PSQL_HOST=
    PSQL_PORT=
    SMS_API_KEY=
    ```

## Brug af scriptet lokalt

For at køre scriptet:

```
python dit_script_navn.py
```

## Drift

Skriptet kører i vores Docker Swarm miljø. For at deploy scriptet, skal du push'e en ny version til GitHubs `main` branch. Derefter vil GitHub Actions automatisk bygge og deploy'e en ny version af scriptet i vores Docker Swarm miljø.


## Funktioner

### `if_final_datetime_passed()`

Tjekker om den endelige frist er overskredet. Hvis ja, vil den sende alle tilbageværende opgaver.

### `final_datetime_passed_sending_the_rest()`

Sender alle evalueringer, der ikke har en registreringsdato, når den endelige registreringsdato er overskredet.

### `sending_scheduled_evals()`

Sender planlagte evalueringer baseret på deres tidsstempel i databasen.

### `close_evals_scheduled()`

Lukker alle evalueringer, der har overskredet deres lukkedato i databasen.

### `final_reg_date_complete_state()`

Returnerer en boolsk værdi baseret på, om den nuværende tid er større end den endelige registreringstid.

## Databasestruktur

Dette script antager en PostgreSQL databasestruktur med en tabel ved navn `eval_app_classschool`. Hvert felt i denne tabel bruges i scriptet for at afgøre, hvilke evalueringer der skal sendes.

## Logs

Scriptet bruger et log-modul til at registrere aktiviteter og eventuelle fejl.

## Fejlfinding

Scriptet indeholder en række loginstruktioner, der hjælper med fejlfinding. Hvis der opstår fejl, kan du tjekke logfilen for mere information.