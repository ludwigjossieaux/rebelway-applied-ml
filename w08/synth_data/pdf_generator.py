from faker import Faker
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import random

fake = Faker()

def generate_cv_pdf(filename):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    
    # Fake personal information
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, fake.name())
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, f"Email: {fake.email()}")
    c.drawString(50, height - 100, f"Phone: {fake.phone_number()}")
    c.drawString(50, height - 120, f"Address: {fake.address().replace(chr(10), ', ')}")
    
    # Summary
    c.drawString(50, height - 160, "Summary:")
    c.drawString(70, height - 180, fake.paragraph(nb_sentences=3))
    
    # Work Experience
    c.drawString(50, height - 200, "Work Experience:")
    y = height - 240
    
    for _ in range(random.randint(1, 5)):
        c.drawString(70, y, f"{fake.job()} at {fake.company()} ({fake.date()} - {fake.date()})")
        y -= 20
        c.drawString(90, y, fake.paragraph(nb_sentences=2))
        y -= 40
        
    # Education
    c.drawString(50, y, "Education:")
    y -= 20
    for _ in range(random.randint(1, 3)):
        c.drawString(70, y, f"{fake.job()} Degree from {random.choice(['Harvard', 'MIT', 'Stanford', 'Yale'])} ({fake.date()} - {fake.date()})")
        y -= 20
        
    # Skills
    c.drawString(50, y, "Skills:")
    y -= 20
    skills = ["Python", "Data Analysis", "Machine Learning", "Project Management", "Team Leadership"]
    c.drawString(70, y, ", ".join(random.sample(skills, k=random.randint(2, len(skills)))))
    
    c.save()
    
for i in range(10):
    filename = f"CV_{i+1}.pdf"
    generate_cv_pdf(filename)
    print(f"Generated {filename}")
    
    # # Create a PDF canvas
    # c = canvas.Canvas("generated_cv.pdf", pagesize=A4)
    # width, height = A4

    # # Generate fake personal information
    # name = fake.name()
    # address = fake.address().replace("\n", ", ")
    # phone = fake.phone_number()
    # email = fake.email()
    # summary = fake.text(max_nb_chars=200)

    # # Draw personal information on the PDF
    # c.setFont("Helvetica-Bold", 20)
    # c.drawString(50, height - 50, name)

    # c.setFont("Helvetica", 12)
    # c.drawString(50, height - 80, f"Address: {address}")
    # c.drawString(50, height - 100, f"Phone: {phone}")
    # c.drawString(50, height - 120, f"Email: {email}")

    # c.setFont("Helvetica-Bold", 14)
    # c.drawString(50, height - 150, "Professional Summary")
    
    # c.setFont("Helvetica", 12)
    # text_object = c.beginText(50, height - 170)
    # text_object.textLines(summary)
    # c.drawText(text_object)

    # # Generate fake work experience
    # c.setFont("Helvetica-Bold", 14)
    # c.drawString(50, height - 250, "Work Experience")

    # y_position = height - 270
    # for _ in range(3):
    #     job_title = fake.job()
    #     company = fake.company()
    #     start_date = fake.date_between(start_date='-10y', end_date='-1y').strftime("%b %Y")
    #     end_date = fake.date_between(start_date='-1y', end_date='today').strftime("%b %Y")
    #     description = fake.text(max_nb_chars=150)

    #     c.setFont("Helvetica-Bold", 12)
    #     c.drawString(50, y_position, f"{job_title} at {company} ({start_date} - {end_date})")
    #     y_position -= 20

    #     c.setFont("Helvetica", 12)
    #     text_object = c.beginText(60, y_position)
    #     text_object.textLines(description)
    #     c.drawText(text_object)
    #     y_position -= 60

    # # Save the PDF
    # c.save()