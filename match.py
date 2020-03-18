"""
match
"""
import csv
import os

TEST_FOLDER = os.path.dirname(os.path.abspath(__file__)) + "/tests"

class Person:
    def __init__(self):
        self.responses = []
        self.inGroup = False

class Student(Person):
    def __init__(self, id):
        Person.__init__(self)
        self.id = id
        self.pairs = []

class Mentor(Person):
    def __init__(self, id):
        Person.__init__(self)
        self.id = id

class Question:
    def __init__(self):
        self.n_responses = 0
        self.weight = 0

class Pair:
    def __init__(self, student, mentor):
        self.student = student
        self.mentor = mentor
        
        self.score = 0

class Group:
    MAX_STUDENTS = 3

    def __init__(self):
        self.students = []
        self.mentor = None

def add_student(responses, students, id):
    new_student = Student(id)
    # add all the responses for each question into the new student's responses
    for response in responses:
        # remove brackets from response
        response = response.strip("()")
        response_list = response.split(";")

        # convert everything to integers
        for index in range(len(response_list)):
            response_list[index] = int(response_list[index])

        new_student.responses.append(response_list)

    # add new student to students
    students.append(new_student)


def add_mentor(responses, mentors, id):
    new_mentor = Mentor(id)
    # add all the responses for each question into the new mentor's responses
    for response in responses:
        # remove brackets from response
        response = response.strip("()")
        response_list = response.split(";")
        
        # convert everything to integers
        for index in range(len(response_list)):
            response_list[index] = int(response_list[index])

        new_mentor.responses.append(response_list)

    # add new mentor to mentors
    mentors.append(new_mentor)

def add_question(row, questions):
    new_question = Question()
    new_question.n_responses = int(row[0])
    new_question.weight = int(row[1])
    
    questions.append(new_question)

def read_inputs(mentors, students, questions):
    # students
    student_id = 0
    with open(os.path.join(TEST_FOLDER,'s_input.txt')) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                # header row (do nothing)
                line_count = line_count + 1
            else:
                add_student(row, students, student_id)
                line_count = line_count + 1
            
                student_id = student_id + 1

    # mentors
    mentor_id = 0
    with open(os.path.join(TEST_FOLDER, 'm_input.txt')) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                # header row (do nothing)
                line_count = line_count + 1
            else:
                add_mentor(row, mentors, mentor_id)
                line_count = line_count + 1

                mentor_id = mentor_id + 1

    # questions
    with open(os.path.join(TEST_FOLDER, 'questions.txt')) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                # header row (do nothing)
                line_count = line_count + 1
            else:
                add_question(row, questions)
                line_count = line_count + 1


def generate_pairs(students, mentors, pairs):
    for student in students:
        for mentor in mentors:
            new_pair = Pair(student, mentor)
            pairs.append(new_pair)

def calculate_pair_score(pair, questions):
    # iterate through questions
    for question_i in range(len(questions)):
        matched_responses = 0
        # iterate through each possible response and compare between student/mentor
        for response_i in range(questions[question_i].n_responses):
            if pair.student.responses[question_i][response_i] == pair.mentor.responses[question_i][response_i]:
                matched_responses = matched_responses + 1

        # increment pair score
        pair.score = pair.score + matched_responses * questions[question_i].weight

def associate_pairs(pairs, students):
    for student in students:
        for pair in pairs:
            if pair.student == student:
                student.pairs.append(pair)

# need to double check references here (does updating pair.student update student?)
def generate_groups(groups, students):
    # iterate for the number of students in each group
    for n_students_in_group in range(Group.MAX_STUDENTS):
        # iterate through each student's pairs and find the highest scored pair
        optimal_pairs = []

        for student in students:
            mentor = None
            score = 0

            for pair in student.pairs:
                if (pair.score > score) and (pair.student.inGroup == False):
                    score = pair.score
                    mentor = pair.mentor
        
            # if mentor != None:
            optimal_pairs.append(Pair(student, mentor))

        # iterate through the highest scoring pairs per student by mentor and add
        # to groups
        for pair in optimal_pairs:
            # if initial
            if n_students_in_group == 0:
                if (pair.student.inGroup == False) and (pair.mentor.inGroup == False):
                    new_group = Group()
                    new_group.students.append(pair.student)
                    new_group.mentor = pair.mentor
                    groups.append(new_group)

                    pair.student.inGroup = True
                    pair.mentor.inGroup = True
            else:
                if pair.student.inGroup == False:
                    # get group with optimal mentor
                    for group in groups:
                        if pair.mentor == group.mentor:
                            group.students.append(pair.student)

                            pair.student.inGroup = True

def output_groups(groups):
    with open(os.path.join(TEST_FOLDER,'groups.csv'), mode='w') as groups_file:
        groups_writer = csv.writer(groups_file, delimiter=',')

        for group in groups:
            out_list = [group.mentor.id]
            for student in group.students:
                out_list.append(student.id)

            groups_writer.writerow(out_list)


def main():
    # initialise variables
    mentors = []
    students = []
    questions = []
    pairs = []
    groups = []

    # read inputs
    read_inputs(mentors, students, questions)

    # generate pairs
    generate_pairs(students, mentors, pairs)

    # calculate score for each pair
    for pair in pairs:
        calculate_pair_score(pair, questions)

    # associate pairs with each student
    associate_pairs(pairs, students)

    # generate groups based on optimal pairings for each student
    generate_groups(groups, students)

    # output groups   
    output_groups(groups)

if __name__ == '__main__':
    main()