import fitz  # PyMuPDF
import re

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text

# Function to parse questions and answers
def parse_questions_answers(text):
    questions_answers = re.findall(r'(\d+\.\s.*?)(?=\d+\.|$)', text, re.DOTALL)
    qa_dict = {}
    for qa in questions_answers:
        question_num = re.match(r'(\d+)\.', qa).group(1)
        answers = re.findall(r'[A-D]\)\s.*', qa)
        qa_dict[question_num] = answers
    return qa_dict

# Function to read correct answers from TXT file
def read_correct_answers(txt_path):
    with open(txt_path, 'r') as file:
        correct_answers = {}
        for line in file:
            if line.strip():
                question, answer = line.strip().split(':')
                correct_answers[question.strip()] = answer.strip()
    return correct_answers

# Function to highlight correct answers in PDF
def highlight_correct_answers(pdf_path, correct_answers, output_pdf_path):
    doc = fitz.open(pdf_path)
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text("text")
        for question, correct_answer in correct_answers.items():
            question_pattern = re.compile(rf'{question}\.\s.*?([A-D]\)\s{correct_answer})', re.DOTALL)
            matches = question_pattern.findall(text)
            for match in matches:
                answer = match.strip()
                text_instances = page.search_for(answer)
                for inst in text_instances:
                    highlight = page.add_highlight_annot(inst)
                    highlight.update()
    doc.save(output_pdf_path)

# Main function to execute the workflow
def main(pdf_path, txt_path, output_pdf_path):
    text = extract_text_from_pdf(pdf_path)
    qa_dict = parse_questions_answers(text)
    correct_answers = read_correct_answers(txt_path)
    highlight_correct_answers(pdf_path, correct_answers, output_pdf_path)
    print(f"Correct answers highlighted and saved to {output_pdf_path}")

# Paths to the input files and output file
pdf_path = "input/practice test 3.pdf"
txt_path = "input/dapan.txt"
output_pdf_path = "highlighted_practice_test_3.pdf"

# Run the main function
main(pdf_path, txt_path, output_pdf_path)
