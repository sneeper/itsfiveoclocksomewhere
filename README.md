# It's 5 o'clock Somewhere!


This is a silly test project written in python using Flask.

The list of cities mapping to timezones was downloaded from [geonames](http://download.geonames.org/export/dump/).

 
 

### Testing

```
git clone git@github.com:sneeper/itsfiveoclocksomewhere.git

docker build itsfiveoclocksomewhere -t fiveoclocksomewhere

docker run -p 5001:5001 --env PORT=5001 -it fiveoclocksomewhere

open http://localhost:5001
```

