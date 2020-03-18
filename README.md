# questionnaire_match
Used to match students to mentors given the results of a questionnaire.

## Inputs
All inputs are interpretted as csv
- s_input.txt
    - Each row represents the responses of one student
    - The formatting of each row is with each question demarcated by '()' and 
    separated by commas, and each possible response within each question is 
    separated by semicolons
- m_input.txt
    - Each row represents the responses of one mentor
    - The formatting is the same as with s_input.csv
- questions.txt
    - Each row represents a question
    - Each row contains information about the number of possible responses to 
    the question and the question's weight