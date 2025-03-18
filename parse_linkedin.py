from bs4 import BeautifulSoup

filename = input("Please enter the name of the LinkedIn HTML file:").strip()

# Try to open the file
try:
    with open(filename, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    # Get name
    name_tag = soup.find("h1")
    name = name_tag.text.strip() if name_tag else "No name found"

    # Get summary
    summary_tag = soup.find(class_="summary")
    summary = summary_tag.text.strip() if summary_tag else "No summary found"

    # Get work experience information
    experience_section = soup.find_all("section")
    work_experience = []

    for section in experience_section:
        if "Experience" in section.text:
            jobs = section.find_all("li")
            for job in jobs:
                job_title = job.find("h3").text.strip() if job.find("h3") else "Unknown Job Title"
                company = job.find("p").text.strip() if job.find("p") else "Unknown Company"
                work_experience.append(f"{job_title} at {company}")

    print(f"Name: {name}")
    print(f"Summary: {summary}\n")
    print("Work Experience:")
    for job in work_experience:
        print(f"- {job}")

except FileNotFoundError:
    print("Error: The file was not found. Please check the filename and try again.")