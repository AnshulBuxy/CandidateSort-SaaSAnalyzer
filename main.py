import streamlit as st
import re
import requests
import pdfplumber
from io import BytesIO
from openai import OpenAI
import os
import requests
from bs4 import BeautifulSoup
from langchain.document_loaders import WebBaseLoader
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from email.message import EmailMessage
import numpy as np
import os
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from openai import OpenAI as OpenAIApi
from langchain import OpenAI as LangchainOpenAI
import ssl
import smtplib
# Sample job descriptions (4 roles)
job_descriptions = [
    """
    Mobile application developer:
    Your role
    ● Help drive the development cycle by having the responsibility of driving features from
    the early stages all the way to production
    ● Take ownership of the work you're doing, from active participation with partners, to
    prioritization and effort estimation, to writing well-tested code
    ● Bring others along with you, as you communicate decisions and challenges, mentor
    junior developers, and consistently help us hit the next bar of excellence

    ● Help us see trends in maintenance issues, proposing wider-scope solutions to ensure we
    fix problematic spaces once and for all
    ● As a valued team member, you will bring ideas forward to refine processes

    Your experience
    ● Some experience in Kotlin or Java or Swift
    ● Experience with mobile design and architectural patterns
    ● Working in agile methodology
    ● Developed one or more apps on the Google Play Store or Apple App Store
    ● Passion for design, UI, and UX
    ● Bachelor degree in computer science or related engineering field or equivalent work
    experience
    """,
    """
   Full Stack developer:
    Your role
    ● Follow and promote best practices to solve high complexity challenges by building
    reliable, performant and elegant solutions that are easy to work with
    ● Own the technical output and standards for the team, ensuring software engineering and
    operational excellence
    ● Ideate, prototype, plan and deliver exciting capabilities
    ● Build proof of concepts to help craft the future success of our product

    ● Deliver reliable software through continuous integration, automated testing, and in-depth
    code & design reviews

    Your experience
    ● Software development experience, full-stack & product focused work experience
    preferred
    ● Solid skills in writing efficient, performant and extensible code using the right tools and
    patterns to implement the functionalities that add value to our customers
    ● Work in an agile setup using continuous deployment and delivery
    ● Maintain a high bar for quality through improving best practices, producing exemplary
    code, documentation, automated tests and thorough and precise monitoring
    ● Knowledge of software design and scalable architecture
    ● Experience with relational databases like PostgreSQL, MySQL, etc
    ● Experience with AWS cloud
    ● Experience with ReactJS or AngularJS
    ● Both backend and front end experience are preferred
    ● Independent, fast learner, and excited about learning new technologies
    """,
    """
    AI ML Engineer:
    Your role
    ● Developing algorithms and Machine Learning systems that connect users across the
    Jazzee marketplace; from students looking for their first jobs and internships to
    employers sourcing candidates for high-priority roles.
    ● Work with founders in driving new user experiences through Machine Learning and
    Natural Language Processing and build experiments that drive key product decisions.

    ● Work with data to create models, perform statistical analysis, and train and retrain models
    to optimize performance. Responsibilities will involve designing and constructing
    sophisticated machine learning models, as well as refining and updating existing systems.
    ● Goal is to build efficient self-learning applications and contribute to advancements in
    artificial intelligence.

    Your experience
    ● Coursework or projects in AI/ML.
    ● Ability to write robust code in Python, Java and R.
    ● End-to-End experience building web-scale AI systems, feature stores, microservices.
    ● Background in one or more of the following areas of machine learning:
    recommendations, optimization, natural language processing (NLP), deep learning,
    LLMs, explainable AI.
    ● Familiarity with machine learning frameworks (like Keras or PyTorch) and libraries (like
    scikit-learn).
    ● Experience building applications atop of IaaS (Google Cloud Platform, Amazon Web
    Services, Azure Cloud Services, etc.).
    ● Experience working directly with cross-functional teams such as product management,
    analytics, engineering, and design.
    ● Excellent communication skills — ability to succinctly communicate results and tell
    compelling stories.
    ● Bachelor degree in computer science or related engineering field or equivalent work
    experience, MS/Ph.D. in Machine Learning, Statistics or a related field.
    """,
    """
    Marketing Analyst:
    Your role
    ● Full-stack product marketing; Inbound strategy to inform the product experience and
    outbound strategy to drive awareness, acquisition, and retention (holistic Go To Market
    plan)
    ● Be the voice of the customer back —bringing in insights from direct client interactions,
    conferences, events, as well as deep customer and competitive research and analysis
    ● Work closely with the founders of Jazzee to optimize the customer
    experience—continuously test, refine and optimize the client experience and drive back
    recommendations
    ● Be the products’ subject matter expert so we can ideate and accelerate the growth of the
    business. Be ready to create content, inform landing pages, collaborate on webinars, plan
    events, and help formulate other demand generation tactics that effectively promote
    Jazzee’s paid employer and student offerings
    ● Support demand generation programs and employer and student marketing programs with
    product information (messaging, product features and capabilities) designed to increase
    market and revenue penetration

    Your experience
    ● Experience working in a strategic role in a Marketing organization
    ● Experience working with top brands to optimize their marketing strategy
    ● Ability to build actionable insights from analytics and research data
    ● Independent, fast learner, and excited about learning new industries
    """
]
CHECKLIST=[
'''
Agreement scope

Authorized means of obtaining and using services
Permissible SaaS services and the scope of access
Number of permitted users or access restrictions.
Specific business areas or markets may be subject to restrictions.
How users can utilize the product with each change in scope and permissions granted.''',
'''
Subscription and pricing plans
Subscription and Pricing Plans clause in a SaaS license agreement mainly covers the

Vendor's subscription details
Pricing structure, and
Service delivery.''',

'''
Service Level agreements
A SaaS service level agreement (SLA) can be used as a stand-alone document or as part of an elaborate SaaS provider agreement. It specifies the extent of support and service a SaaS provider commits to offering the customer.''',

'''
Data ownership and security
Both vendors and users will generate large amounts of sensitive data when using software. A data ownership and security clause is critical for clarifying the ownership of data gathered by the software company, especially given the SaaS providers' role in storing client data.''',

'''
Liability
The Limitation of Liability (LOL) clause protects the vendor against potential compensating claims in the event of contract breaches. This provision, included in the final agreement, limits the buyer's ability to demand particular damages if the SaaS service fails, thereby shielding the vendor from legal ramifications.''',

'''
Terma and Auto-Renewal
This clause serves as the contract's lifeline, laying forth the terms of the agreement and the procedures for renewing, suspending, or terminating the account. Most SaaS companies now favor evergreen renewals, which automatically renew the agreement unless the subscriber cancels it before a certain date.''',

'''
Customer support and maintenance
The SaaS agreement's customer support and maintenance provision specifies the accessible support channels, which include a dedicated help center, an email ticketing system, and phone support during business hours. It indicates the desired response time as well as the team in charge of handling client concerns.

The clause also includes support services and maintenance provisions, outlining any applicable service guarantees. This comprehensive provision assures that the SaaS vendor is committed to delivering timely and effective support for their services.''',

'''
Product Modifications
Product Modification clause in a SaaS agreement specifies the provider's right to modify or stop the software, including any related plans and pricing, with or without advance notification. It also describes the procedures for contacting customers about changes in functionality, pricing, or terms of service.

This clause is important because it notifies customers of prospective product and pricing changes, ensuring transparency and managing expectations.''',
'''
  "License Scope": {
        "Common Vendor Preferences": "A narrow scope, limited to specified named users, to be used only internally within the customer entity. Standard license restrictions (e.g., no reverse engineering, reselling, using competitively, etc.).",
        "Common Customer Preferences": "A broader scope, to include possible use by subsidiaries, affiliates and contractors. Fewer license restrictions, that are fair and reasonable."
    }''',

 '''
  "Payment Terms": {
        "Common Vendor Preferences": "Payment in advance. Shorter payment terms (e.g., net 30 after invoice date). Right to charge interest and collection costs for late payments.",
        "Common Customer Preferences": "Payment in arrears. Longer payment terms with right to dispute payments in good faith (e.g., net 60 after receipt of undisputed invoice). Avoid interest and penalties; or minimize their impact via a written notice requirement and cure periods before any interest or penalties can begin."
    },''',
  '''
    "Service Level Agreement (SLA)": {
        "Common Vendor Preferences": "Reasonable SLAs (if any). Include 'commercially reasonable efforts' standard, and manageable targets, as well as exceptions for things beyond vendor’s control (e.g., general internet issues).",
        "Common Customer Preferences": "Robust SLAs, including a right to service credits or refunds for excessive downtime, as well as a right to terminate after a certain number (or length) of incidents."
    }''',
'''
    "Use of Data/ Data Rights": {
        "Common Vendor Preferences": "Rights to use customers’ aggregated, anonymized usage data, especially when such data is needed to train vendor AI.",
        "Common Customer Preferences": "Retain all rights to its data; or grant limited rights to vendor for the use aggregated and anonymized data only."
    }
''',
    '''
    "Data Privacy Addendum (DPA)": {
        "Common Vendor Preferences": "Reasonable DPA that meets the requirements of applicable privacy laws.",
        "Common Customer Preferences": "DPA that requires prompt vendor notice (e.g., 48 hours) in the event of not only an actual security breach, but also any suspected or alleged security breaches; quick remediation (at vendor expense); termination rights for customer; and indemnity for security breach with either unlimited liability or a higher 'super-cap.'"
    }''',
    '''
    "Reps and Warranties": {
        "Common Vendor Preferences": "Standard, but narrow, vendor reps and warranties, such as a representation that vendor’s services will substantially comply with the documentation.",
        "Common Customer Preferences": "Standard, but broader, vendor reps and warranties, e.g., that vendor will comply with applicable laws and industry standards, confidentiality and privacy protections, IP rights (non-infringement), etc."
    }''',
    '''
    "Indemnities": {
        "Common Vendor Preferences": "Offer only basic indemnities (e.g., non-infringement), if any, to customer and include exceptions for modification or misuse of the Services. If possible, secure indemnities from the customer regarding its IP rights to any data or content being shared with vendor.",
        "Common Customer Preferences": "No indemnities given to vendor; or give indemnities with a narrow scope (and include exceptions for modification or misuse of your content or data). Robust indemnities from vendor (e.g., non-infringement, confidentiality & privacy, injury to persons or property, arising from any material breach, etc.)."
    }
    ''',
    '''
    "Limitation on Liability": {
        "Common Vendor Preferences": "Limit vendor liability. May give a 'super cap' for certain issues, like indemnity, IP violations, and confidentiality/privacy.",
        "Common Customer Preferences": "Uncapped vendor liability, if possible, especially for issues such as indemnities, IP violations, and confidentiality or privacy breaches. May accept super caps if they are reasonable, based on the scope of possible harm, not necessarily proportional to the size of the deal."
    }''',
    '''
    "Termination Rights": {
        "Common Vendor Preferences": "Limited termination rights for the customer, and no obligation to provide refunds, or refunds only in very limited circumstances.",
        "Common Customer Preferences": "Broad termination rights (e.g., due to vendor breach, SLA failures, privacy issues, decrease in service features or functionality, chronic issues, and, if possible, for convenience); with rights to pro-rata refund, if possible."
    }''',
    '''
    "Renewal": {
        "Common Vendor Preferences": "Auto-renewals for reduced churn.",
        "Common Customer Preferences": "Auto-renewal may be acceptable, but only with reasonable opt out dates for customer to avoid paying for an unwanted renewal term."
    }''',
    '''
    "Notice Periods": {
        "Common Vendor Preferences": "Short notice periods (5-10 days) for things like your notice to customer for non-payment; and longer notice requirements for others such as customer’s notice to you (e.g., 60-90 days prior) to opt out of auto renewal.",
        "Common Customer Preferences": "Shorter notice requirements for things relating to customer rights. Longer notice periods for any provisions giving the vendor a right to pursue remedies against customer."
    }''',
    '''
    "Insurance": {
        "Common Vendor Preferences": "Vendor insurance requirements match scope of vendor’s current policies and would not require to you obtain incremental or custom insurance for this transaction.",
        "Common Customer Preferences": "Vendor insured for general liability, errors & omissions/professional liability, cyber liability, and workmen’s comp. Plus, an umbrella policy and other applicable coverage based on circumstances (car, shipping, air, etc.)."
    }''',
    '''
    "Publicity": {
        "Common Vendor Preferences": "Right to use customer’s name, and possibly logo, in vendor marketing, or at least in list of customers.",
        "Common Customer Preferences": "Right to approve any use of customer name or logos, including prior approval of use in lists of clients."
    }''',
    '''
    "Assignment": {
        "Common Vendor Preferences": "Vendor assignment rights only; customer cannot assign.",
        "Common Customer Preferences": "Mutual restriction of assignment, with a mutual exception for M&A activity or reorganizations."
    }''']

openai_key = "Your API Key"
client = OpenAI(api_key=openai_key)
# Set page configuration and theme options
def analyze_t_and_c(t_and_c_text):
    # Generate a detailed prompt for the model to follow
    prompt = f"""
    You are a legal expert specializing in SaaS contracts. Your task is to read the following terms and conditions and identify potential risks to the buyer. Please flag the risks based on this checklist:

    {', '.join(CHECKLIST)}

    Use the above CHECKLIST texts as your base for terms and conditons after reading the below T&C Document quickly flag the redlines for the same so customers can make an informed decision about their purchases.Make it shorter and more understable for the client by highlighting the more important points on top.
     T&C Document:
    {t_and_c_text}
    """

    # Call OpenAI API with the prompt
    response = client.chat.completions.create(
      model="gpt-4o",
      messages=[
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": prompt}
  ]
)
    # Return the flagged risks
    return response.choices[0].message

def format_terms_conditions(input_text):
    sections = input_text.strip().split("\n\n")  # Split by double new lines for sections
    formatted_text = ""

    for section in sections:
        lines = section.strip().split("\n")
        title = lines[0].strip()  # The first line is the section title
        formatted_text += f"### {title}\n"

        for line in lines[1:]:
            line = line.strip()
            if "Risks:" in line:
                formatted_text += "**Risks:**\n"  # Identify risks heading
            elif line.startswith("-"):
                formatted_text += f"- {line[1:].strip()}\n"  # Format list items
            else:
                formatted_text += f"{line}\n"

        formatted_text += "\n"  # Add a newline after each section

    return formatted_text
st.set_page_config(
    page_title="Chatbot Suite",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS to style the app (for background color and hover effects)
st.markdown(
    """
    <style>
    .main {
        background-color: #00000;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
        border-radius: 8px;
    }
    .stButton>button:hover {
        background-color: #45a049;
        color: white;
        transform: scale(1.02);
        transition: all 0.3s ease;
    }
    </style>
    """, unsafe_allow_html=True
)

# Function for SaaS T&C analysis chatbot
def saas_tc_analysis():
    st.subheader("🔍 SaaS T&C Analysis")
    st.write("Analyze potential and risky points in the terms and conditions.")
    
    with st.expander("Instructions"):
        st.write("""
            1. Enter the URL of the SaaS Terms & Conditions.
            2. Click on 'Analyze' to view potential risks.
        """)
    
    # URL input for the terms and conditions webpage
    with st.container():
        url = st.text_input("Enter the URL of SaaS Terms & Conditions:")
        analyze_button = st.button("Analyze")
    
    if analyze_button and url:
        st.success(f"Analyzing T&C for: {url}")
        extracted_texts = ""
        def extract_text_from_url(url):
                response = requests.get(url)
                if response.status_code != 200:
            #print(f"Failed to retrieve the page: {url}")
                    return None
                soup = BeautifulSoup(response.content, 'html.parser')
                return soup.get_text(separator="\n", strip=True)

# Example URLs for SaaS T&C documents
        urls = [url]    

        for url in urls:
            #print(f"Extracting text from: {url}")
                text = extract_text_from_url(url)
                if text:
                    extracted_texts+=text
        st.session_state.url = "" # Reset the URL input field
    
        sample_t_and_c =extracted_texts
        risks = analyze_t_and_c(sample_t_and_c)
        formatted_output = format_terms_conditions(risks.content)
        st.markdown(formatted_output)
        # Simulating analysis process with a progress bar

# Function for Candidate Shortlister chatbot
import streamlit as st
import pandas as pd


def candidate_shortlister(email,password,send_email):
    st.subheader("📄 Candidate Shortlister")
    st.write("Upload an Excel sheet to sort candidates.")

    with st.expander("Instructions", expanded=True):
                        st.write("""
                            1. Upload a CSV File (.csv format) with candidate information.
                            2. Click on 'Sort Candidates' to see the results.
                        """)

                        # CSV structure example as a DataFrame
                        csv_structure = pd.DataFrame({
                            "Name": ["John Doe", "Jane Smith"],
                            "Email": ["johndoe@example.com", "janesmith@example.com"],
                            "Resume_link(Google Drive Link)": ["drive/abc", "drive/sdf"],
                            
                        })

                        st.write("**CSV File Structure:**")
                        st.write("The CSV file should contain the following columns:")
                        st.table(csv_structure) 

    # File uploader for a single Excel sheet input
    uploaded_file = st.file_uploader("Upload CSV sheet", type=["csv"])
    sort_button = st.button("Sort Candidates")

    if sort_button and uploaded_file:
        st.success(f"Uploaded the Excel sheet: {uploaded_file.name}")
        
        # Read the uploaded Excel file into a pandas DataFrame
        df = pd.read_csv(uploaded_file)
        list_email = df.iloc[:,1].tolist()
        list_drive = df.iloc[:,2].tolist()
        list_name = df.iloc[:,0].tolist()
        list_id =[]
        for i in range(len(list_drive)):
            url =list_drive[i]
            file_id = url.split("id=")[-1]
            list_id.append(file_id)

        def extract_text_from_pdf_url(url):
            response = requests.get(url)
            response.raise_for_status()  # Ensure we got a valid response

    # Create a BytesIO object from the response content
            pdf_stream = BytesIO(response.content)

    # Use pdfplumber to open the PDF file from the BytesIO object
            with pdfplumber.open(pdf_stream) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text()
            return text
        
        text=[]
        for i in list_id:
            url =f'https://drive.usercontent.google.com/uc?id={i}&export=download'
            text1 = extract_text_from_pdf_url(url)
            text.append(text1)
        
        def filter_resume_for_role_using_ai(resume_text, job_description):
            """
            Use OpenAI to match resume sections with a specific job description.
            """
            # Step 1: Extract resume sections using OpenAI


            # Step 3: Create a prompt to evaluate the resume for the given job role
            prompt = f"""
            You are a resume evaluation assistant.
            Evaluation criteria
            1.See if project matches with the wrok required by the company as mentioned in job description.Projects should not be very basic and common.From projects is should be felt that person has decent knowledge in the required field
            2.Match skills section.
            3.Cgpa criteria>7.5



            Given the job descriptions: {job_descriptions},
            and a resume :

            {resume_text}

        On the basis of all evaluation criterion . Return the shortlisted role name or "no" if not shortlisted.No extra details.
        give only the shortlisted role name.if it is not shortlisted print no
            """
            #client = OpenAI(api_key=openai_key)

            completion = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert in evaluating resumes."},
                    {"role": "user", "content": prompt}
                ]
            )

            # Extract the response content
            response_content = completion.choices[0].message.content
            return response_content
        
        def filter_resume_for_multiple_roles_using_ai(resume_text, job_descriptions):
            """
            Filter resume against multiple job descriptions using AI.
            Return a shortlist of roles the candidate is a good match for.
            """
            shortlisted_roles = []

            for i, job_description in enumerate(job_descriptions):
                result = filter_resume_for_role_using_ai(resume_text, job_description)
                print(f"Result for Job Role {i+1}:\n", result)

                # Check if the result contai-ns a positive match without parsing a score
                if "Yes" in result:  # Modify this condition based on the expected output format
                    shortlisted_roles.append()
                else:
                    shortlisted_roles.append("No")
                break

            return shortlisted_roles
        
        role=[]
            
        for i in text:
            shortlisted_roles = filter_resume_for_role_using_ai(i, job_descriptions)
            role.append(shortlisted_roles)
        mail=[]
        if send_email:
            sender_email = email
            email_password = password
            
            for i in range(len(list_email)):
                receiver_email = f"{list_email[i]}"
                subject = "Jazzee Hi"
                body = f'''Dear {list_name[i]},
                    I hope this message finds you well.
                    We are pleased to inform you that your resume has been shortlisted for the {role[i]}. We appreciate the time and effort you put into your application and are impressed with your qualifications.
                    Our team will be in touch soon to provide further details regarding the next steps. If you have any questions in the meantime, please feel free to reach out.

                    Thank you for your interest in joining our team. We look forward to speaking with you soon!

                    Best regards,
                    Kushal Bansal
                    Jazzee'''

                em = EmailMessage()
                em["From"] = sender_email
                em["To"] = receiver_email
                em["Subject"] = subject
                em.set_content(body)

                context = ssl.create_default_context()
                # if(role[i]!="no" or role[i]!="No" or role[i]!="NO" or role[i]!="nO"):
                #     with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
                #         smtp.login(sender_email, email_password)
                #         smtp.sendmail(sender_email, receiver_email, em.as_string())
                #         mail.append(f"Email sent to {receiver_email}")
                if(role[i]!="no" or role[i]!="No" or role[i]!="NO" or role[i]!="nO"):
                    try:
                        # SMTP login and email sending process
                        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
                            smtp.login(sender_email, email_password)
                            smtp.sendmail(sender_email, receiver_email, em.as_string())
                            mail.append(f"Email sent to {receiver_email}")

                    except smtplib.SMTPAuthenticationError:
                        # Catch incorrect password error
                        st.warning("❗ Password is incorrect. unable to send the mail.")
                        return  # Exit the function to avoid continuing further if authentication fails
                    except Exception as e:
                        # Catch any other potential SMTP-related errors
                        st.warning(f"An error occurred: {e}")
                        return
                        
                else:
                    mail.append("Not selected")
        
            # Simulating shortlisting process with a progress bar
        with st.spinner('Shortlisting candidates...'):
            import time
            time.sleep(1)
            st.info("✅ **Candidate Shortlisting Complete!**")
            st.write("Below is the table with candidate names and their respective roles:")
            selected=[]
            roles=[]
            for i in range(len(list_email)):
                    selected.append(list_name[i])
                    if(role[i]!="no" or role[i]!="No" or role[i]!="NO" or role[i]!="nO"): 
                        roles.append(role[i])
                    else:
                        roles.append("Not Shortlisted")
                # Display a table with candidate names and their roles
            if not mail:
                candidate_data = pd.DataFrame({
                            'Name': selected,
                            'Role': roles,
                        })
            else:
                candidate_data = pd.DataFrame({
                            'Name': selected,
                            'Role': roles,
                            "status":mail
                        })
            st.table(candidate_data)
            st.progress(100)
                
        # Simulating shortlisting process with a progress bar
        # with st.spinner('Shortlisting candidates...'):
        #     import time
        #     time.sleep(2)
            
        #     # Simulated output: Here you can implement your shortlisting logic
        #     st.info("✅ **Candidate Shortlisting Complete!**")
        #     st.write("Top Candidates: John Doe, Jane Smith")
        #     st.progress(100)
class Chatbot:
    def __init__(self, memory_limit=5):
        self.memory = []
        self.memory_limit = memory_limit

    def _add_to_memory(self, user_input, bot_response):
        # Add the user input and bot response to memory
        self.memory.append({"role": "user", "content": user_input})
        self.memory.append({"role": "assistant", "content": bot_response})

        # Maintain memory limit
        if len(self.memory) > self.memory_limit * 2:
            self.memory = self.memory[-self.memory_limit * 2:]

    def _build_prompt(self):
        # Build the prompt from memory
        messages = [{"role": "system", "content": "You are a helpful assistant."}]
        messages.extend(self.memory)
        return messages

    def chat(self, user_input):
        # Build the prompt for the API
        prompt = self._build_prompt()
        prompt.append({"role": "user", "content": user_input})

        # Get the response from OpenAI's API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=prompt
        )

        bot_response = response.choices[0].message.content

        # Add the conversation to memory
        self._add_to_memory(user_input, bot_response)

        return bot_response
def student():
    st.subheader("🎓 Student Chatbot")
    

####################################################################

    
    
    # Initialize session state to store chat history
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
    chatbot = Chatbot(memory_limit=5)
    # Chat input box
    user_input = st.text_input("You:", placeholder="Type your message here...")

    # When the user sends a message
    if user_input:
        # Add user message to history
        st.session_state['chat_history'].append({"role": "user", "message": user_input})
        
        # Generate a response (for now, just echoing the user input as a placeholder)
        bot_response = chatbot.chat(user_input)
        st.session_state['chat_history'].append({"role": "bot", "message": bot_response})

    # Display the chat history
    for chat in st.session_state['chat_history']:
        if chat['role'] == 'user':
            st.markdown(f"**You:** {chat['message']}")
        else:
            st.markdown(f"**Chatbot:** {chat['message']}")
# Main function to display the website structure
def main():
    # Sidebar for navigation
    st.sidebar.title("⚙️ Chatbot Suite")
    st.sidebar.write("Select the task you want to perform:")

    # Option selection using the sidebar


# Sidebar with select box instead of radio buttons
    
    option = st.sidebar.radio("", ('SaaS T&C Analysis', 'Candidate Shortlister', 'Student'))

   
    tab1, tab2 = st.tabs(["💬 Chatbot Suite", "About"])

    with tab1:
        st.title("Welcome to the Chatbot Suite")
        st.write("Choose the task you want to perform from the sidebar.")

        # Load the respective chatbot interface based on user's choice
        if option == 'SaaS T&C Analysis':
            saas_tc_analysis()

        elif option == 'Candidate Shortlister':
            # Ask user if they want to send emails to candidates
            send_email = st.radio("Do you want to send emails to the candidates?", ('Yes', 'No'))

            if send_email == 'Yes':
                # Ask for email and password
                email = st.text_input("Gmail", placeholder="Enter your Gmail")
                password = st.text_input("Security Password", type="password", placeholder="Enter your password")
                
                st.write("Press enter to proceed with Candidate Shortlister.")
                # Instructions on how to generate a password
                with st.expander("🔐 How to generate a Security password?",expanded=True):
                    st.write("""
                    - Step 1: Go to your Google Account settings.
                    - Step 2: Under 'Security', find 'App passwords' (you may need to enable 2-step verification first).
                    - Step 3: Generate an app password for 'Candidate Shortlister'.
                    - Step 4: Copy and paste the generated password here.
                    - Note: This ensures secure access without using your regular account password.
                    """)

                # Validation message
                if not email or not password:
                    st.warning("❗ Please provide Gmail and Password to proceed with Candidate Shortlister.")
                else:
                    candidate_shortlister(email, password,send_email=True)

            else:
                candidate_shortlister(None, None, send_email=False)
        elif option == 'Student':
            student()

    with tab2:
        st.subheader("ℹ️ About This App")
        st.write("""
            This app integrates two chatbots:
            1. SaaS T&C Analyzer: Helps you identify potential risks in terms and conditions.
            2. Candidate Shortlister: Allows you to upload resumes and sort the top candidates.
            
            Built using Streamlit for an interactive and seamless user experience.
        """)


# Run the Streamlit app
if __name__ == '__main__':
    main()
