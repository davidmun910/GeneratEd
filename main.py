import pandas as pd
import numpy as np
from search import search_dataframe, search_course_grade

# Initializing the CSVs
grade = pd.read_csv(
    "https://raw.githubusercontent.com/wadefagen/datasets/master/gpa/uiuc-gpa-dataset.csv"
)
classes = pd.read_csv("https://waf.cs.illinois.edu/discovery/course-catalog.csv")

geneds = pd.read_csv(
    "https://raw.githubusercontent.com/wadefagen/datasets/master/geneds/gened-courses.csv"
)

# Setting result to the time and degree attribute
# result = search_dataframe(classes, "Start Time", "09:00 AM")
subject = search_dataframe(
    classes,
    "Degree Attributes",
    "Social & Beh Sci - Soc Sci, and Cultural Studies - US Minority course.",
)

requiredClass = "CS"

# Get just the course and number -> remove the duplicates
selected_df = geneds[["Course", "Course Title", requiredClass]]
bool_series = pd.notnull(selected_df["CS"])
# selected_df.drop_duplicates(inplace=True)

# Checking the easiest classes given a Degree Attribute
highest = 0
highest_course = {"Subject": "", "Number": ""}

for index, row in selected_df[bool_series].iterrows():
    course = row["Course"]
    courseTitle = row["Course Title"]
    genEdRequirement = row[requiredClass]

    gpa = search_course_grade(grade, course, courseTitle, genEdRequirement)
    max_gpa = np.max(gpa)  # Calculate the maximum GPA

    if max_gpa > highest:
        highest = max_gpa
        highest_course["Subject"] = courseTitle  # Update Subject

print(
    f"Highest GPA is {highest} for Course: {highest_course['Subject']} {highest_course['Number']}"
)
