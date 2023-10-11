import pandas as pd


def search_dataframe(df, column, value):
    return df.loc[df[column] == value]


def search_course_grade(df, subject, subjectTitle, genEdRequirement):
    filtered_df = df[(df["Course Title"].isin([subjectTitle]))]
    result = 0
    total = 0
    grades = {
        "A+": 4.0,
        "A": 4.0,
        "A-": 3.67,
        "B+": 3.33,
        "B": 3.00,
        "B-": 2.67,
        "C+": 2.33,
        "C": 2.00,
        "C-": 1.67,
        "D+": 1.33,
        "D": 1.00,
        "D-": 0.67,
        "F": 0.0,
    }

    for index, row in filtered_df.iterrows():
        for grade, score in grades.items():
            count = row[grade]
            total += count
            result += count * score

    if total == 0:
        return 0

    result = result / total
    print(subjectTitle)
    print(round(result, 3))
    return round(result, 3)
