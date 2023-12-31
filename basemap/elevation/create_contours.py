import glob
import multiprocessing
import os
import click
import shutil

from tqdm import tqdm
from osgeo import gdal, ogr, osr

# supress gdal exceptions
gdal.UseExceptions()


@click.command()
@click.option(
    "--input-files", default="data/sources/*.tif", help="Input files to process"
)
@click.option(
    "--workers", default=multiprocessing.cpu_count(), help="Number of workers to use"
)
def cli(workers, input_files):
    files = glob.glob(input_files)

    # create a data/temp/ directory if it doesn't exist
    try:
        if os.path.exists("data/temp"):
            shutil.rmtree("data/temp")
        os.mkdir("data/temp")
    except:
        pass

    # create a vrt file from the source files
    gdal.BuildVRT("data/temp/elevation.vrt", files)

    # scale the elevation values from meters to feet
    translate_options = gdal.TranslateOptions(
        format="VRT",
        outputSRS="EPSG:4326",
        outputType=gdal.GDT_Float32,
        scaleParams=[[0.0, 0.3048, 0.0, 1.0]],
    )

    ds = gdal.Open("data/temp/elevation.vrt")
    gdal.Translate("data/temp/elevation-feet.vrt", ds, options=translate_options)

    intervals = [40, 200, 1000]

    with multiprocessing.Pool(processes=workers) as pool:
        for _ in tqdm(
            pool.imap_unordered(create_contours, intervals), total=len(intervals)
        ):
            pass


def create_contours(interval):
    vds = gdal.Open("data/temp/elevation-feet.vrt")
    sr = osr.SpatialReference()
    sr.ImportFromEPSG(4326)

    # save output as GPKG
    out_dataset = ogr.GetDriverByName("GPKG").CreateDataSource(
        f"data/temp/contour_{interval}.gpkg",
    )

    contour_layer = out_dataset.CreateLayer("elevation", sr)
    contour_layer.CreateField(ogr.FieldDefn("ID", ogr.OFTInteger))
    contour_layer.CreateField(ogr.FieldDefn("elevation", ogr.OFTReal))

    # create the contours
    try:
        gdal.ContourGenerate(
            vds.GetRasterBand(1), interval, 0, [], 0, 0, contour_layer, 0, 1
        )
    except:
        print(f"error generating contours for {interval}")
        pass


if __name__ == "__main__":
    cli()
