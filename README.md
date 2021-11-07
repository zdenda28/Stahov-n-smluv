# Diplomová práce - Analýza dat z registru smluv v kontextu způsobu řízení projektů ve veřejné správě v ČR

Autor: Zdeněk Tomka

Popis: Repozitář obsahuje potřebné zdrojové soubory k nastartování systému navrženého v diplomové práci včetně scriptu, který stahuje stahuje ICT smlouvy z Registru smluv.

## Spuštění

Nastartování systému:

1) Vytvoření a spuštění prostředí
```
docker-compose up
```

2) Vytvoření a spuštění kontejneru s ETL scriptem
```
docker-compose run --name python python
```

3) Opakované nastartování kontejneru s ETL scriptem
```
docker start -a -i python
```


