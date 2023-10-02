import pandas as pd
import numpy as np
from search import search_dataframe, search_course_grade

# Initializing the CSVs
grade = pd.read_csv(
    "https://raw.githubusercontent.com/wadefagen/datasets/master/gpa/uiuc-gpa-dataset.csv"
)
classes = pd.read_csv("https://waf.cs.illinois.edu/discovery/course-catalog.csv")

# Setting result to the time and degree attribute
# result = search_dataframe(classes, "Start Time", "09:00 AM")
subject = search_dataframe(
    classes,
    "Degree Attributes",
    "Social & Beh Sci - Soc Sci, and Cultural Studies - US Minority course.",
)

# Get just the course and number -> remove the duplicates
selected_df = subject[["Subject", "Number", "Section Info"]]
selected_df.drop_duplicates(inplace=True)

# Checking the easiest classes given a Degree Attribute
highest = 0
highest_course = {"Subject": "", "Number": ""}

for index, row in selected_df.iterrows():
    subject = row["Subject"]
    number = row["Number"]
    sectionInfo = row["Section Info"]

    gpa = search_course_grade(grade, subject, number, str(sectionInfo))
    max_gpa = np.max(gpa)  # Calculate the maximum GPA

    # print(subject + ", " + str(number) + ": " + str(max_gpa))
    # if max_gpa > highest:
    #     highest = round(gpa.item(), 3)
    #     highest_course["Subject"] = subject  # Update Subject
    #     highest_course["Number"] = number  # Update Number

print(
    f"Highest GPA is {highest} for Course: {highest_course['Subject']} {highest_course['Number']}"
)
