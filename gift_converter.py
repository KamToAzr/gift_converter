import pandas as pd
import re
import os

def parse_questions(input_text):
    # Extract questions and answers using regular expressions
    pattern = re.compile(r"^(.*?)\nA\) (.*?)\nB\) (.*?)\nC\) (.*?)\nD\) (.*?)\nAnswer: ([ABCD])\n", re.MULTILINE)
    questions = pattern.findall(input_text)

    # Create a DataFrame to store and manipulate data
    columns = ['question', 'option_a', 'option_b', 'option_c', 'option_d', 'answer']
    df = pd.DataFrame(questions, columns=columns)
    return df

def to_gift_format(df, category="PLACEHOLDER"):
    gift_text = [f"$CATEGORY: {category}\n"]
    for index, row in df.iterrows():
        question_number = index + 1

        options = {
            'A': row['option_a'],
            'B': row['option_b'],
            'C': row['option_c'],
            'D': row['option_d']
        }

        gift_question = f"::Q{question_number:02}:: {row['question']} {{\n"
        for key, option in options.items():
            if key == row['answer']:
                gift_question += f"={option}\n"
            else:
                gift_question += f"~{option}\n"
        gift_question += "}\n"
        gift_text.append(gift_question)
    return "\n".join(gift_text)

def main(input_file_path):
    # Read the input text file
    with open(input_file_path, 'r') as file:
        input_text = file.read()

    df_questions = parse_questions(input_text)

    category = input("Please enter the category for the GIFT file: ")

    gift_formatted_text = to_gift_format(df_questions, category)

    output_file_path = os.path.splitext(input_file_path)[0] + "_output.txt"

    with open(output_file_path, 'w') as file:
        file.write(gift_formatted_text)

    print("Conversion to GIFT format completed successfully.")
    print(f"Output file created at: {output_file_path}")

input_file_path = 'input.txt'
main(input_file_path)
