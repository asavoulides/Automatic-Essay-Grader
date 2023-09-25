import os
import openai
import tkinter as tk
from tkinter import ttk

openai.api_key = "YOUR API KEY"

with open('.\prompts\content.txt', 'r') as content_file:
    content_prompt = content_file.read()

with open('.\prompts\grammar.txt', 'r') as grammar_file:
    grammar_prompt = grammar_file.read()

with open('.\prompts\structure.txt', 'r') as structure_file:
    structure_prompt = structure_file.read()

def gpt_req(str):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
              "role": "user",
              "content": str
            }
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    print(response['choices'][0]['message']['content'])
    return response['choices'][0]['message']['content']

def analyze_essay_gpt(essay_text):
    student_grade = student_grade_entry.get()

    return {
        'Grammar': gpt_req(f"{grammar_prompt}\n{essay_text}\n---ESSAY OVER--- \n Please note when grading: the student who wrote this essay is in {student_grade} Grade. You should take the grade level into account when grading."),
        'Content': gpt_req(f"{content_prompt}\n{essay_text}\n---ESSAY OVER--- \n Please note when grading: the student who wrote this essay is in {student_grade} Grade. You should take the grade level into account when grading."),
        'Structure': gpt_req(f"{structure_prompt}\n{essay_text}\n---ESSAY OVER--- \n Please note when grading: the student who wrote this essay is in {student_grade} Grade. You should take the grade level into account when grading.")
    }


def grade_essay():
    essay_text = essay_entry.get("1.0", tk.END)
    student_grade = student_grade_entry.get()
    grades = analyze_essay_gpt(essay_text)
    
    grammar_label.config(text=f"Grammar: {grades['Grammar']}")
    content_label.config(text=f"Content: {grades['Content']}")
    structure_label.config(text=f"Structure: {grades['Structure']}")

root = tk.Tk()
root.title("Essay Grader")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

essay_entry = tk.Text(frame, width=50, height=20)
essay_entry.grid(row=0, column=0, columnspan=4)

student_grade_entry = ttk.Entry(frame, width=10)
student_grade_entry.grid(row=1, column=0)
student_grade_entry_label = ttk.Label(frame, text="Enter Student Grade:")
student_grade_entry_label.grid(row=1, column=1)

grade_button = ttk.Button(frame, text="Grade Essay", command=grade_essay)
grade_button.grid(row=1, column=3)

grammar_label = ttk.Label(frame, text="Grammar:")
grammar_label.grid(row=2, column=0)
content_label = ttk.Label(frame, text="Content:")
content_label.grid(row=2, column=1)
structure_label = ttk.Label(frame, text="Structure:")
structure_label.grid(row=2, column=2)


root.mainloop()
