# Astro Dark Sky Evaluator

This tool helps astrophotographers evaluate sky darkness for a list of locations using NASA's VIIRS Nighttime Lights data. It maps real radiance values to an estimated Bortle Class and friendly darkness ratings.

## Features

- Extracts radiance from high-res VIIRS GeoTIFF files
- Estimates Bortle Class from real satellite data
- Appends darkness ratings to your location CSV
- Reusable for any region or trip planning

## Quickstart

### 1. Install dependencies

Make sure you're in a Python environment (e.g. Anaconda), then run:

```bash
pip install -r requirements.txt
```

### 2. Prepare your files

- Add your `.csv` of locations with `Latitude` and `Longitude` columns into `sample_data/`
- Download the VIIRS VNL V2 `.tif` file from [EOG](https://eogdata.mines.edu/products/vnl/)
- Place the `.tif` file in your project folder

### 3. Run the extractor

```bash
python extract_viirs_radiance.py
```

It will output a new `.csv` file in `output/` with `Radiance`, `Bortle Class`, and `Dark Sky Rating`.

## Bortle Class Mapping

Radiance values (nW/cm²/sr) are approximated to Bortle classes:

| Radiance Range | Bortle | Rating     |
|----------------|--------|------------|
| < 0.25         | 1–2    | 🌑 Pristine |
| 0.25–1.0       | 3–4    | 🌘 Great    |
| 1.0–3.0        | 5–6    | 🌗 Decent   |
| 3.0–10.0       | 7–8    | 🌒 Poor     |
| > 10.0         | 9      | 🌓 Awful    |

## Notes

- This repo does not include the VIIRS GeoTIFF file due to its size (~9GB).
- You must download it separately from the [EOG VIIRS portal](https://eogdata.mines.edu/products/vnl/).
