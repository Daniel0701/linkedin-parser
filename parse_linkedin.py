import os
import pdfplumber

filename = input("Enter the pdf of the LinkedIn profile: ").strip()

if not os.path.exists(filename):
    print("Error: File not found. Please try again.")
    exit()

# extract text from the pdf
with pdfplumber.open(filename) as pdf:
    text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])

# Debugging purposes: first 500 characters of the extracted text
# print(text[:500])

# split the text into lines
lines = text.split("\n")

# initialize storage values
name = ""
role = ""
about = []
experience = []
education = []
section = None

# parse through the text
for i, line in enumerate(lines):
    line = line.strip()

    if i == 2:
        name = line
        role = lines[i + 1] if i + 1 < len(lines) else "Role Not Found"

    # get section info
    elif "About" in line:
        section = "about"
    elif "Experience" in line:
        section = "experience"
    elif "Education" in line:
        section = "education"
    elif "Analytics" in line:
        section = None

    elif section == "education" and ("Skills" in line or "Activites" in line or "Certificates" in line or "Courses in line"):
        break

    # store data into corresponding section
    if section == "about":
        about.append(line)
    elif section == "experience":
        experience.append(line)
    elif section == "education":
        education.append(line)

# clean up a little
about_text = " ".join(about).strip()
experience_text = "\n".join(experience).strip()
education_text = "\n".join(education).strip()

output_file = filename.replace(".pdf", "_parsed.txt")

# Save extracted data into separate files
sections = {
    "name": name,
    "role": role,
    "about": about_text,
    "experience": experience_text,
    "education": education_text
}

# write to one txt file
with open(output_file, "w", encoding="utf-8") as file:
    file.write("=== LinkedIn Profile Data ===\n\n")
    file.write(f"Name: \n{name}\n")
    file.write(f"Role: \n{role}\n\n")
    if about_text:
        file.write("About Section:\n")
        file.write(about_text + "\n\n")
    if experience_text:
        file.write("Experience Section:\n")
        file.write(experience_text + "\n\n")
    if education_text:
        file.write("Education Section:\n")
        file.write(education_text + "\n\n")
