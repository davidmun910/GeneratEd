import pandas as pd
from data_loader import load_data
from gpa_calculator import calculate_average_gpa

GENED_BRANCHES = {
    "ACP": ["ACP"],
    "HUM": ["HP", "LA"],
    "SBS": ["BSC", "SS"],
    "NAT": ["LS", "PS"],
    "CS": ["NW", "US", "WCC"],
    "QR": ["QR1", "QR2"],
}


def select_courses_based_on_requirements():
    gened_df, gpa_df, catalog_df = load_data()
    average_gpa_df = calculate_average_gpa(gpa_df)

    catalog_df["Course"] = (
        catalog_df["Subject"] + " " + catalog_df["Number"].astype(str)
    )

    # User input for GenEd requirement
    gen_ed_requirement = input(
        "Enter the GenEd requirement (e.g., US, HP, LA, BSC, SS, LS, PS, NW, WCC): "
    ).strip()

    # Determine the branch for the provided GenEd requirement
    branch_columns = []
    for branch, requirements in GENED_BRANCHES.items():
        if gen_ed_requirement in requirements:
            branch_columns.append(branch)
            break

    gened_courses = gened_df[
        gened_df.apply(
            lambda row: any(row[col] for col in branch_columns)
            and gen_ed_requirement in row.values,
            axis=1,
        )
    ]

    # Extract the 'Course' column to a list
    gened_courses_list = gened_courses["Course"].tolist()

    # Filter GPA data to only courses that are in the gened_courses_list
    relevant_gpa_data = average_gpa_df[
        average_gpa_df["CourseKey"].isin(gened_courses_list)
    ]
    relevant_gpa_data = relevant_gpa_data.rename(columns={"CourseKey": "Course"})

    # Merge the GPA data with the catalog data
    merged_data = catalog_df.merge(relevant_gpa_data, on="Course", how="inner")

    # Filter for lecture or lecture-discussion at a specific time
    desired_time = input(
        "Enter the desired time for the course (e.g., 09:00 AM): "
    ).strip()
    lecture_at_desired_time = merged_data[
        (merged_data["Type"].isin(["Lecture", "Lecture-Discussion"]))
        & (merged_data["Start Time"] == desired_time)
    ]

    # Sorting by Average GPA (highest first)
    lecture_at_desired_time = lecture_at_desired_time.sort_values(
        by="Average_GPA", ascending=False
    )

    for _, lecture_row in lecture_at_desired_time.iterrows():
        # Store lecture information
        res = {
            "Course": f"{lecture_row['Subject']} {lecture_row['Number']}",
            "Name": lecture_row["Name"],
            "LectureTime": lecture_row["Start Time"],
            "AverageGPA": round(lecture_row["Average_GPA"], 2),
        }

        # Print course info
        print(res["Course"], "-", res["Name"])
        print(
            f"Lecture at: {lecture_row['Start Time']} - {lecture_row['End Time']} on {lecture_row['Days of Week']}"
        )
        print("Average GPA:", res["AverageGPA"])

        # Find the associated discussion sections
        relevant_discussions = merged_data[
            (merged_data["Subject"] == lecture_row["Subject"])
            & (merged_data["Number"] == lecture_row["Number"])
            & (merged_data["Name"] == lecture_row["Name"])
            & (merged_data["Type"] == "Discussion/Recitation")
        ]

        if not relevant_discussions.empty:
            print("Discussion options:")
            for _, dis_row in relevant_discussions.iterrows():
                print(
                    f"{dis_row['Start Time']} - {dis_row['End Time']} on {dis_row['Days of Week']}"
                )
        print("========================================")


if __name__ == "__main__":
    select_courses_based_on_requirements()
