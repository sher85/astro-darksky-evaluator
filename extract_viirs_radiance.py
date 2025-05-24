import argparse
import pandas as pd
import rasterio
from shapely.geometry import Point
import geopandas as gpd

def classify_bortle(radiance):
    """
    Classify Bortle scale based on radiance values.
    These thresholds are approximate and can be adjusted.
    """
    if radiance is None:
        return None
    if radiance < 0.1:
        return 1  # Excellent dark sky
    elif radiance < 0.5:
        return 2
    elif radiance < 1.0:
        return 3
    elif radiance < 2.5:
        return 4
    elif radiance < 5.0:
        return 5
    elif radiance < 10.0:
        return 6
    elif radiance < 20.0:
        return 7
    elif radiance < 40.0:
        return 8
    else:
        return 9  # Bright inner-city sky

def extract_radiance(input_csv, output_csv, viirs_path):
    # Load coordinates
    df = pd.read_csv(input_csv)
    geometry = [Point(xy) for xy in zip(df['Longitude'], df['Latitude'])]
    gdf = gpd.GeoDataFrame(df, geometry=geometry)

    # Open VIIRS GeoTIFF and extract radiance
    with rasterio.open(viirs_path) as src:
        gdf['Radiance'] = [
            val[0] if val[0] != src.nodata else None
            for val in src.sample([(pt.x, pt.y) for pt in gdf.geometry])
        ]

    # Classify Bortle scale based on radiance
    gdf['Bortle'] = gdf['Radiance'].apply(classify_bortle)

    # Save results
    gdf.drop(columns='geometry').to_csv(output_csv, index=False)
    print(f"✅ Done! File saved as: {output_csv}")

def main():
    parser = argparse.ArgumentParser(description="Extract VIIRS radiance at given coordinates and classify Bortle scale.")
    parser.add_argument('--input', '-i', required=True, help="Input CSV file with 'Latitude' and 'Longitude' columns.")
    parser.add_argument('--out', '-o', required=True, help="Output CSV file to save results.")
    parser.add_argument('--viirs', '-v', default="VNL_npp_2024_global_vcmslcfg_v2_c202502261200.average.dat.tif",
                        help="Path to VIIRS GeoTIFF file (default: VNL_npp_2024_global_vcmslcfg_v2_c202502261200.average.dat.tif).")

    args = parser.parse_args()
    extract_radiance(args.input, args.out, args.viirs)

if __name__ == "__main__":
    main()