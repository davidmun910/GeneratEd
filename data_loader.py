import pandas as pd


def load_data():
    # URLs for the datasets
    gened_url = "https://raw.githubusercontent.com/wadefagen/datasets/master/geneds/gened-courses.csv"
    gpa_url = "https://raw.githubusercontent.com/wadefagen/datasets/master/gpa/uiuc-gpa-dataset.csv"
    # catalog_url = "https://raw.githubusercontent.com/wadefagen/datasets/master/course-catalog/data/2023-sp.csv"

    # For the Spring 2024 Semester
    catalog_url = "2024-sp.csv"

    # Load the datasets
    gened_df = pd.read_csv(gened_url)
    gpa_df = pd.read_csv(gpa_url)
    catalog_df = pd.read_csv(catalog_url)

    return gened_df, gpa_df, catalog_df
