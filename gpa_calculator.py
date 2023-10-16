import pandas as pd


def calculate_average_gpa(gpa_df):
    # Create a unique course key in the GPA dataframe for merging
    gpa_df["CourseKey"] = gpa_df["Subject"] + " " + gpa_df["Number"].astype(str)

    # Calculate the average GPA for each course
    gpa_df["Total_students"] = (
        gpa_df["A+"]
        + gpa_df["A"]
        + gpa_df["A-"]
        + gpa_df["B+"]
        + gpa_df["B"]
        + gpa_df["B-"]
        + gpa_df["C+"]
        + gpa_df["C"]
        + gpa_df["C-"]
        + gpa_df["D+"]
        + gpa_df["D"]
        + gpa_df["D-"]
        + gpa_df["F"]
    )
    gpa_df["Total_points"] = (
        gpa_df["A+"] * 4.0
        + gpa_df["A"] * 4.0
        + gpa_df["A-"] * 3.7
        + gpa_df["B+"] * 3.3
        + gpa_df["B"] * 3.0
        + gpa_df["B-"] * 2.7
        + gpa_df["C+"] * 2.3
        + gpa_df["C"] * 2.0
        + gpa_df["C-"] * 1.7
        + gpa_df["D+"] * 1.3
        + gpa_df["D"] * 1.0
        + gpa_df["D-"] * 0.7
    )
    gpa_df["Average_GPA"] = gpa_df["Total_points"] / gpa_df["Total_students"]
    average_gpa = gpa_df.groupby(["CourseKey"])["Average_GPA"].mean().reset_index()

    return average_gpa
