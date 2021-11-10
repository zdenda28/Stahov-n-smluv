# Diplomová práce - Implementace nástroje pro analýzu dat z Registru smluv

Autor: Zdeněk Tomka

Popis: Repozitář obsahuje potřebné zdrojové soubory k nastartování systému navrženého v diplomové práci včetně scriptu, který stahuje ICT smlouvy z Registru smluv.

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


