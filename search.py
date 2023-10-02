import pandas as pd


def search_dataframe(df, column, value):
    return df.loc[df[column] == value]


def search_course_grade(df, subject, number, sectionInfo):
    filtered_df = df[(df["Subject"].isin([subject])) & (df["Number"].isin([number]))]
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
        # Extract the section and number from the "Section Info" string
        course_numbers = []
        section_titles = []

        # Split the "Section Info" string into words
        words = sectionInfo.split()
        removewords = ["Same", "as", "and"]

        # Iterate over words to extract course numbers and section titles
        if words[0] == "Same" and words[1] == "as":
            for word in list(words):
                if word == "Prerequisite:":
                    break

                word = "".join(letter for letter in word if letter.isalnum())
                if word in removewords:
                    words.remove(word)
                    continue

                if word.isnumeric():
                    course_numbers.append(word)
                else:
                    section_titles.append(word)
        else:
            words = []

        # Check if the extracted course number and section title match the desired values
        for grade, score in grades.items():
            count = row.get(grade, 0)
            total += count
            result += count * score

    if total == 0:
        return 0

    result = result / total
    return round(result, 3)
