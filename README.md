# Diplomka-ETL-script

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


