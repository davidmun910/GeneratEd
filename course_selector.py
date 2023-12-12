import pandas as pd
from datetime import datetime
from data_loader import load_data
from gpa_calculator import calculate_average_gpa


def to_datetime(time_str, time_format, default):
    if isinstance(time_str, str) and time_str != "ARRANGED":
        return datetime.strptime(time_str, time_format)
    else:
        return default


def select_courses_based_on_requirements(
    gen_ed_requirements, start_time_str, end_time_str, day_input
):
    gened_df, gpa_df, catalog_df = load_data()
    average_gpa_df = calculate_average_gpa(gpa_df)

    catalog_df["Course"] = (
        catalog_df["Subject"] + " " + catalog_df["Number"].astype(str)
    )

    # Split the gen_ed_requirements into a list
    gen_ed_list = gen_ed_requirements.split(",")

    # Reverse mapping: GenEd requirement to DataFrame column
    reversed_gened_branches = {
        "ACP": "ACP",
        "HP": "HUM",
        "LA": "HUM",
        "BSC": "SBS",
        "SS": "SBS",
        "LS": "NAT",
        "PS": "NAT",
        "NW": "CS",
        "US": "CS",
        "WCC": "CS",
        "QR1": "QR",
        "QR2": "QR",
    }

    gened_courses = gened_df[
        gened_df.apply(
            lambda row: all(
                row[reversed_gened_branches[gen_ed]] == gen_ed for gen_ed in gen_ed_list
            ),
            axis=1,
        )
    ]

    # Map each course to its GenEd requirements
    course_gened_mapping = {
        row["Course"]: [
            gen_ed
            for gen_ed in gen_ed_list
            if row[reversed_gened_branches[gen_ed]] == gen_ed
        ]
        for _, row in gened_courses.iterrows()
    }

    gened_courses_list = gened_courses["Course"].tolist()

    relevant_gpa_data = average_gpa_df[
        average_gpa_df["CourseKey"].isin(gened_courses_list)
    ]
    relevant_gpa_data = relevant_gpa_data.rename(columns={"CourseKey": "Course"})

    merged_data = catalog_df.merge(relevant_gpa_data, on="Course", how="inner")

    time_format = "%I:%M %p"
    start_time = datetime.strptime(start_time_str, time_format)
    end_time = datetime.strptime(end_time_str, time_format)

    day_map = {
        "Monday": "M",
        "Tuesday": "T",
        "Wednesday": "W",
        "Thursday": "R",
        "Friday": "F",
    }
    day_of_week = day_map.get(day_input.capitalize())

    if not day_of_week:
        print("Invalid day entered!")
        return []

    # Apply filters for time and day
    merged_data["Start Time Datetime"] = merged_data["Start Time"].apply(
        lambda x: to_datetime(x, time_format, None)
    )
    merged_data["End Time Datetime"] = merged_data["End Time"].apply(
        lambda x: to_datetime(x, time_format, end_time)
    )

    filtered_data = merged_data[
        (merged_data["Type"].isin(["Lecture", "Lecture-Discussion"]))
        & merged_data["Days of Week"].str.contains(day_of_week)
        & merged_data["Start Time Datetime"].apply(
            lambda x: x is not None and start_time <= x
        )
        & (merged_data["End Time Datetime"] <= end_time)
    ]

    filtered_data = filtered_data.sort_values(by="Average_GPA", ascending=False)

    results = []
    for _, lecture_row in filtered_data.iterrows():
        days_of_week = [
            day for day in day_map.keys() if day_map[day] in lecture_row["Days of Week"]
        ]
        discussions = []

        relevant_discussions = merged_data[
            (merged_data["Subject"] == lecture_row["Subject"])
            & (merged_data["Number"] == lecture_row["Number"])
            & (merged_data["Name"] == lecture_row["Name"])
            & (merged_data["Type"] == "Discussion/Recitation")
        ]

        if not relevant_discussions.empty:
            for _, dis_row in relevant_discussions.iterrows():
                discussion_time = f"{dis_row['Start Time']} - {dis_row['End Time']}"
                discussion_days = [
                    day
                    for day in day_map.keys()
                    if day_map[day] in dis_row["Days of Week"]
                ]
                discussions.append(
                    {
                        "DiscussionTime": discussion_time,
                        "DiscussionDays": ", ".join(discussion_days),
                    }
                )

        course_key = f"{lecture_row['Subject']} {lecture_row['Number']}"
        course_geneds = course_gened_mapping.get(course_key, [])

        course_info = {
            "Course": course_key,
            "Name": lecture_row["Name"],
            "LectureTime": f"{lecture_row['Start Time']} - {lecture_row['End Time']}",
            "LectureDays": ", ".join(days_of_week),
            "AverageGPA": round(lecture_row["Average_GPA"], 2),
            "Discussions": discussions,
            "GenEdRequirements": course_geneds,  # Add GenEd requirements here
        }
        results.append(course_info)

    return results
