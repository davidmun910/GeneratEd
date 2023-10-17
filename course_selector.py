import pandas as pd
from datetime import datetime
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

    # User input for desired time range
    time_format = "%I:%M %p"  # Time format, e.g., "09:00 AM"
    start_time_str = input(
        "Enter the start time for the desired time range (e.g., 09:00 AM): "
    ).strip()
    end_time_str = input(
        "Enter the end time for the desired time range (e.g., 01:00 PM): "
    ).strip()

    start_time = datetime.strptime(start_time_str, time_format)
    end_time = datetime.strptime(end_time_str, time_format)

    # New input for the day of the week
    day_input = (
        input("Enter the day of the week (e.g., Monday, Tuesday, etc.): ")
        .strip()
        .capitalize()
    )
    day_map = {
        "Monday": "M",
        "Tuesday": "T",
        "Wednesday": "W",
        "Thursday": "R",
        "Friday": "F",
    }
    day_of_week = day_map.get(day_input)

    if not day_of_week:
        print("Invalid day entered!")
        return

    # Adjusting the lecture filtering criteria
    lecture_within_time_range = merged_data[
        (merged_data["Type"].isin(["Lecture", "Lecture-Discussion"]))
        & (
            merged_data["Days of Week"].str.contains(day_of_week)
        )  # Check if the lecture is on the desired day
        & (
            merged_data["Start Time"].apply(
                lambda x: start_time <= datetime.strptime(x, time_format) <= end_time
                if x != "ARRANGED"
                else False
            )
        )
    ]

    # Sorting by Average GPA (highest first)
    lecture_within_time_range = lecture_within_time_range.sort_values(
        by="Average_GPA", ascending=True
    )

    for _, lecture_row in lecture_within_time_range.iterrows():
        # Store lecture information
        res = {
            "Course": f"{lecture_row['Subject']} {lecture_row['Number']}",
            "Name": lecture_row["Name"],
            "LectureTimeStart": lecture_row["Start Time"],
            "LectureTimeEnd": lecture_row["End Time"],
            "AverageGPA": round(lecture_row["Average_GPA"], 2),
        }

        # Print course info
        print(res["Course"], "-", res["Name"])
        print("Lecture at:", res["LectureTimeStart"], "-", res["LectureTimeEnd"])
        print("Average GPA:", res["AverageGPA"])

        # Print Days of the Week for the lecture
        print("Days of the Week:")
        for i, c in enumerate(lecture_row["Days of Week"]):
            if i == len(lecture_row["Days of Week"]) - 1:
                print(f"{list(day_map.keys())[list(day_map.values()).index(c)]}")
            else:
                print(
                    f"{list(day_map.keys())[list(day_map.values()).index(c)]}, ",
                    end="",
                )

        # Adjusting the discussion filtering criteria without day filter
        relevant_discussions = merged_data[
            (merged_data["Subject"] == lecture_row["Subject"])
            & (merged_data["Number"] == lecture_row["Number"])
            & (merged_data["Name"] == lecture_row["Name"])
            & (merged_data["Type"] == "Discussion/Recitation")
        ]

        if not relevant_discussions.empty:
            print("Discussion options:")
            for _, dis_row in relevant_discussions.iterrows():
                day_strs = [
                    list(day_map.keys())[list(day_map.values()).index(day_char)]
                    for day_char in dis_row["Days of Week"]
                ]
                day_representation = ", ".join(day_strs)
                print(
                    f"{dis_row['Start Time']} - {dis_row['End Time']} on {day_representation}"
                )
        print("========================================")


if __name__ == "__main__":
    select_courses_based_on_requirements()
