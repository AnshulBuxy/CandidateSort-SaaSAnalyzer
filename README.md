# Jazzee Project

### Collaborators:
- **Anshul Buxy - 21ce02014@iitbbs.ac.in**
- **Jatin Sahu - 21ce02010@iitbbs.ac.in**
- **Kushak Bansal - 21ce02008@iitbbs.ac.in**

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Setup and Installation](#setup-and-installation)
4. [How to Run](#how-to-run)
5. [Screenshots](#screenshots)
6. [Technologies Used](#technologies-used)


---

## Project Overview
The **Jazzee Project** is a multipurpose tool that provides three core functionalities:
1. **Candidate Shortlisting**: A tool that helps in shortlisting candidates based on predefined criteria.
2. **SaaS T&C Analysis**: Analyze the terms and conditions of SaaS contracts to extract meaningful information.
3. **Student Chatbot**: A chatbot designed for student assistance, which maintains a history of chat interactions.

---

## Features
- **Candidate Shortlisting**: Upload a CSV file of candidate data and get a sorted list of shortlisted candidates based on specific criteria.
- **SaaS T&C Analysis**: Analyze and extract key points from SaaS Terms and Conditions.
- **Student Chatbot**: Chat with a bot designed to answer student queries and view the chat history.

---

## Setup and Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/AnshulBuxy/Jazzee-Project.git
   cd Jazzee-Project

2. ```bash
   pip install -r requirements.txt
   streamlit run main.py
3. Put OPEN_API_KEY in main.py line number 253
   !(https://github.com/AnshulBuxy/Jazzee-Project/blob/ca64f341b213252f1677894714a2c12a22e08ef3/%7B49A5C78E-71F0-43D9-98FD-E2E356FEC544%7D.png)

## Screenshots

### Streamlit App Interface:
### Candidate Shortlisting Output:
Here is an example of the output generated after shortlisting candidates from the uploaded CSV file:
![Candidate Shortlisting Output](https://github.com/AnshulBuxy/Jazzee-Project/blob/4d85912e1d801ae0381c4bc45d0c4ecf6d56758f/%7BAE8E2FC1-9A25-4832-97D0-04D92F7B5EDF%7D.png)

### SaaS T&C Analysis Output:
An output view from the analysis of SaaS Terms and Conditions:
![SaaS T&C Analysis Output](https://github.com/AnshulBuxy/Jazzee-Project/blob/4d85912e1d801ae0381c4bc45d0c4ecf6d56758f/%7BA16B5444-386C-4047-9EDE-11B7C9BC7413%7D.png)

### Student Chatbot Interface:
Below is the chatbot interface designed for students, which also shows the chat history:
![Student Chatbot Interface](https://github.com/AnshulBuxy/Jazzee-Project/blob/8ad40b486251db7d300dedbf77e986703ff3088e/%7B502DA6E9-F2EE-4AAA-A605-310EE367096B%7D.png)

---

## Technologies Used
- **Python**: Core programming language.
- **Streamlit**: Web framework for the frontend.
- **Natural Language Processing**: For analyzing SaaS T&C documents.
- **Machine Learning**: Applied in candidate shortlisting and chatbot functionalities.
