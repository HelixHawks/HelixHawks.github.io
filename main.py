from flask import Flask, render_template, request, jsonify
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
#from keras.models import load_model
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TextClassificationPipeline
import random

app = Flask(__name__, template_folder='templates', static_folder='static')

tokenizer = AutoTokenizer.from_pretrained('your-model-name')
model = AutoModelForSequenceClassification.from_pretrained('your-model-name')



@app.route("/")
def home():
  return render_template('index.html')


@app.route('/', methods=['GET', 'POST'])
def resume_form():
  if request.method == 'POST':
    name = request.form['name']
    title = request.form['title']
    address = request.form['address']
    phone = request.form['phone']
    email = request.form['email']
    summary_text = request.form['summary']
    work_exp_text = request.form['work_experience']
    education_text = request.form['education']
    references_text = request.form['references']
    skills_text = request.form['skills']
    job_title_text = request.form['job_title']
    awards_honors_text = request.form['awards_honors']

    create_resume(name, title, address, phone, email, summary_text,
                  work_exp_text, education_text, references_text, skills_text,
                  job_title_text, awards_honors_text)

    return "Resume created successfully!"

  return render_template('resume_form.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.route('/submit', methods=['POST'])
def generate_text():
    input_prompt = request.form['tbuser']
    # Generate text based on the input prompt using the loaded model
    generated_text = generate(input_prompt)
    return jsonify({'generated_text': generated_text})

def generate(input_prompt):
    # Use the loaded model to generate text based on the input prompt
    # You can preprocess the input, tokenize it using the model's tokenizer,
    # feed it to the model for text generation, and process the generated output
    # Return the generated text
    return "Generated text"  # Replace with your generated text


def create_resume(name, title, address, phone, email, summary_text,
                  work_exp_text, education_text, references_text, skills_text,
                  job_title_text, awards_honors_text):
  styles = getSampleStyleSheet()
  header_style = ParagraphStyle('header',
                                parent=styles['Heading1'],
                                fontSize=18,
                                spaceAfter=20)
  subheader_style = ParagraphStyle('subheader',
                                   parent=styles['Heading2'],
                                   fontSize=12,
                                   spaceAfter=10)
  content_style = ParagraphStyle('content',
                                 parent=styles['BodyText'],
                                 fontSize=11,
                                 spaceAfter=5)

  doc = SimpleDocTemplate("resume.pdf", pagesize=letter)
  story = []

  header = create_header(name, header_style)
  story.append(header)

  contact = create_contact_info(title, address, phone, email, content_style)
  story.append(contact)

  summary = create_section_header("Summary", subheader_style)
  story.append(summary)

  summary_paragraph = create_paragraph(summary_text, content_style)
  story.append(summary_paragraph)

  work_experience = create_section_header("Work Experience", subheader_style)
  story.append(work_experience)

  work_exp_paragraph = create_paragraph(work_exp_text, content_style)
  story.append(work_exp_paragraph)

  education = create_section_header("Education", subheader_style)
  story.append(education)

  education_paragraph = create_paragraph(education_text, content_style)
  story.append(education_paragraph)

  references = create_section_header("References", subheader_style)
  story.append(references)

  references_paragraph = create_paragraph(references_text, content_style)
  story.append(references_paragraph)

  skills = create_section_header("Skills", subheader_style)
  story.append(skills)

  skills_paragraph = create_paragraph(skills_text, content_style)
  story.append(skills_paragraph)

  job_title = create_section_header("Job Title", subheader_style)
  story.append(job_title)

  job_title_paragraph = create_paragraph(job_title_text, content_style)
  story.append(job_title_paragraph)

  awards_honors = create_section_header("Awards and Honors", subheader_style)
  story.append(awards_honors)

  awards_honors_paragraph = create_paragraph(awards_honors_text, content_style)
  story.append(awards_honors_paragraph)

  doc.build(story)


def create_header(name, style):
  header_text = f"<b>{name}</b>"
  header = Paragraph(header_text, style)
  return header


def create_contact_info(title, address, phone, email, style):
  contact_info = f"<b>{title}</b><br/>" \
                 f"{address}<br/>" \
                 f"{phone}<br/>" \
                 f"{email}"
  contact = Paragraph(contact_info, style)
  return contact


def create_section_header(text, style):
  section_header = Paragraph(f"<b>{text}</b>", style)
  return section_header


def create_paragraph(text, style):
  paragraph = Paragraph(text, style)
  return paragraph


def runModel(inputText):
  #add the model code here
  return inputText


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=random.randint(2000, 9000))
'''from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

styles = getSampleStyleSheet()

header_style = ParagraphStyle(
    'header',
    parent=styles['Heading1'],
    fontSize=18,
    spaceAfter=20
)

subheader_style = ParagraphStyle(
    'subheader',
    parent=styles['Heading2'],
    fontSize=12,
    spaceAfter=10
)

content_style = ParagraphStyle(
    'content',
    parent=styles['BodyText'],
    fontSize=11,
    spaceAfter=5
)


def create_resume():
    doc = SimpleDocTemplate("resumeexample4.pdf", pagesize=letter)
    story = []

    header = create_header("John Doe")
    story.append(header)

    contact = create_contact_info("Software Engineer", "123 Main St, City, State",
                                  "(123) 456-7890", "john.doe@example.com")
    story.append(contact)

    summary = create_section_header("Summary")
    story.append(summary)

    summary_text = "A highly motivated software engineer with experience in web development and strong problem-solving skills."
    summary_paragraph = create_paragraph(summary_text)
    story.append(summary_paragraph)

    work_experience = create_section_header("Work Experience")
    story.append(work_experience)

    work_exp_text = "<b>Software Developer</b><br/>" \
                    "ABC Company, City<br/>" \
                    "June 2018 - Present<br/><br/>" \
                    "Responsibilities:<br/>" \
                    "- Developed and maintained web applications using Python and Django<br/>" \
                    "- Collaborated with cross-functional teams to deliver high-quality software"
    work_exp_paragraph = create_paragraph(work_exp_text)
    story.append(work_exp_paragraph)

    education = create_section_header("Education")
    story.append(education)

    education_text = "<b>Bachelor of Science in Computer Science</b><br/>" \
                     "XYZ University, City<br/>" \
                     "May 2018"
    education_paragraph = create_paragraph(education_text)
    story.append(education_paragraph)

    references = create_section_header("References")
    story.append(references)

    references_text = "Available upon request"
    references_paragraph = create_paragraph(references_text)
    story.append(references_paragraph)

    skills = create_section_header("Skills")
    story.append(skills)

    skills_text = "- Python\n" \
                  "- Django\n" \
                  "- HTML/CSS\n" \
                  "- JavaScript"
    skills_paragraph = create_paragraph(skills_text)
    story.append(skills_paragraph)

    job_title = create_section_header("Job Title")
    story.append(job_title)

    job_title_text = "Software Engineer"
    job_title_paragraph = create_paragraph(job_title_text)
    story.append(job_title_paragraph)

    awards_honors = create_section_header("Awards and Honors")
    story.append(awards_honors)

    awards_honors_text = "- Outstanding Achievement Award, ABC Company, 2020"
    awards_honors_paragraph = create_paragraph(awards_honors_text)
    story.append(awards_honors_paragraph)

    doc.build(story)

def create_header(name):
    header_text = f"<b>{name}</b>"
    header = Paragraph(header_text, header_style)
    return header

def create_contact_info(title, address, phone, email):
    contact_info = f"<b>{title}</b><br/>" \
                   f"{address}<br/>" \
                   f"{phone}<br/>" \
                   f"{email}"
    contact = Paragraph(contact_info, content_style)
    return contact

def create_section_header(text):
    section_header = Paragraph(f"<b>{text}</b>", subheader_style)
    return section_header

def create_paragraph(text):
    paragraph = Paragraph(text, content_style)
    return paragraph

create_resume()'''
