# Basemap

The general purpose basemap.

## OpenStreetMap base

The basemap tiles are generated by [planetiler](https://github.com/onthegomap/planetiler) from OSM data. Follow their instructions to set up the project. To generate the map for the western United States, use this command:

````
java -Xmx3g -jar planetiler.jar --download --area=us-west --output=us-west.pmtiles```
````

## Fonts

We use [Barlow](https://github.com/jpt/barlow) as the map's font.

Maplibre-gl requires a series of `.pbf` files to render text. Use [font maker](https://maplibre.org/font-maker/) to convert `Barlow Regular`, and download. Unzip and move the `Barlow Regular` directory of `.pbf` files to `/data`. You should have something like:

```
data/
    Barlow Regular/
        0-255.pbf
        256-511.pbf
        512-767.pbf
        ...
```