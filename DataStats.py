# Christian Nelson
# 6/13/2020
# DATA-51100-002, SUMMER 2020
# PROGRAMMING ASSIGNMENT #5 DataStats

# Import pandas
import pandas as pd
from pandas import DataFrame
# Formats
fm1 = "College Enrollment Rate for High Schools = {j:.2f} (sd={i:.2f})"
fm2 = "Total Student Count for non-High Schools = {j:.2f} (sd={i:.2f})"

# load in 'cps.csv' into DataFrame
cps_dataframe = pd.read_csv('cps.csv',usecols=(0,3,6,18,30,69))
cps_dervive_dataframe = pd.read_csv('cps.csv',usecols=(28,49))

# Replace missing numeric values with the mean for the column
cps_dataframe.fillna(cps_dataframe.mean(), inplace=True)

# Derive lowest grade
# Get grades for every school
lowest_grades = cps_dervive_dataframe.Grades_Offered_All
highest_grades = lowest_grades.copy()
# Create loop variables
grade = 0
j = 0

# Find the lowest grades taught
for x in lowest_grades:
    for y in x:
        if y > grade:
            grade = y
    # Replace grade with min grade
    if grade == 'P':
        grade = 'PK'
    lowest_grades[j] = grade
    j += 1
    grade = 0

# Reset position
j = 0
# Find the highest grade taught
for x in highest_grades:
    for y in x:
        # Get rid of PK and K as they both evaluate to more then numerical
        if y != 'P' and y != 'K':
            if y > grade:
                grade = y
    # If it goes above 9 the program mistakes it as lower so check if grade = our last y if not add 10
    if grade != y and y != 'P' and y != 'K':
        # Convert y str to int to add 10
        y = int(y)
        y += 10
        # Reassign grade
        grade = y
    # Check if nothing higher then K or PK         
    if y == 'K':
        if highest_grades[j][0] == 'P':
            grade = 'PK'
        else:
            grade = 'K'
    highest_grades[j] = grade
    grade = 0
    j += 1

# Derive Starting hour
starting_hour = cps_dervive_dataframe.School_Hours

# Reset position
j = 0
# Find the Starting hour
for x in starting_hour:
    # We have to put this in a try block for when hours are present
    try:
        hour_strings = x.split()
        hour = hour_strings[0]
        meridiem = hour_strings[1][:2]
        start_time = hour+meridiem
        starting_hour[j] = start_time
    except:
        pass
    j+=1

# Add lowest Grade column to dataframe
cps_dataframe['Lowest_Grade_Offered'] = lowest_grades.values
# Add Highest Grade column to dataframe
cps_dataframe['Highest_Grade_Offered'] = highest_grades.values
# Add starting hour column to dataframe
cps_dataframe['Starting_Hour'] = starting_hour.values

# Get mean and sd of college Enrollment Rate for high schools
# Create new dataframe for only highschools
highschools_dataframe = cps_dataframe.copy()
# Delete non highschools
highschools_dataframe.drop(highschools_dataframe[highschools_dataframe.Is_High_School == False].index, inplace=True)
# Get mean of CER
college_enrollment_rate_mean = highschools_dataframe.College_Enrollment_Rate_School.mean()
# Get sd of CER
college_enrollment_rate_sd = highschools_dataframe.College_Enrollment_Rate_School.std()

# Get mean and sd of student_count_total for non-high schools
# Create new dataframe for only highschools
nonhighschools_dataframe = cps_dataframe.copy()
# Delete non highschools
nonhighschools_dataframe.drop(nonhighschools_dataframe[nonhighschools_dataframe.Is_High_School == True].index, inplace=True)
# Get mean of SCT
student_count_total_mean = nonhighschools_dataframe.Student_Count_Total.mean()
# Get sd of SCT
student_count_total_sd= nonhighschools_dataframe.Student_Count_Total.std()


# Output

# Header info
print("DATA-51100, SUMMER 2020")
print("Christian Nelson")
print("PROGRAMMING ASSIGNMENT #5\n")

# First 10 rows of the dataframe
print(cps_dataframe[:10])

# Print mean and sd of college Enrollment Rate
print(fm1.format(j=college_enrollment_rate_mean,i=college_enrollment_rate_sd))


# Print mean and sd of student_count_total
print(fm2.format(j=student_count_total_mean,i=student_count_total_sd))
