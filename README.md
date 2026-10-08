# ReefWatch Marine Conservation Digital Transformation

## Background

ReefWatch is a fictional marine conservation organisation created for this assessment. It
manages a growing network of reef monitoring centres. ReefWatch focuses on protecting
marine ecosystems through reef surveys, biodiversity monitoring, and environmental
conservation. With 30+ monitoring stations, they face challenges in managing survey
records, field equipment, and partner organisation information consistently.

### Currently:

- Each monitoring station uses different systems for survey and equipment
  management
- Partner organisation data is scattered across spreadsheets and emails
- Head office lacks real-time insights into equipment availability, marine survey
  activities, and partner organisation performance

ReefWatch is investing in a cloud-based solution to unify operations. Your task is to build a
proof-of-concept system for one monitoring station that integrates Azure SQL and Azure
Cosmos DB (NoSQL) with a Python application layer.

## Assessment Overview

This assessment evaluates your ability to:

- Design and implement SQL and NoSQL databases in Microsoft Azure (Free Tier).
- Develop a Python application that interacts with both databases.
- Document design decisions, testing, and outcomes in a professional report.

## Functional Requirements

Your Python application must include:

### 1. Core Features (Pass/Credit)

- **Survey Management**
  - Accept new marine survey records
  - Store survey details (researcher information, observed species, equipment used,
    survey costs) in Cosmos DB
- **Equipment Tracking**
  - Maintain equipment details in Cosmos DB (equipment name, category, replacement
    cost, available quantity)
  - Update equipment quantities when surveys are conducted
- **Partner Organisation Management**
  - Store partner organisation details in Cosmos DB (organisation name, contact
    information, conservation areas supported)
- **Daily Summary**
  - Date
  - Total surveys completed
  - Total survey costs
  - Most frequently observed marine species
  - Low-equipment alerts (optional for credit)
  - At the end of each day, generate and store a summary in Azure SQL
  - Prevent duplicate summaries for the same date

### 2. Advanced Features (Distinction/HD)

- Flask Web Interface for survey entry and summary reporting
- Automatic PDF generation for survey reports and daily summaries
- Deployment to Azure App Service for live demo
- Data Visualization (charts for survey trends)
- Role-based Access Control (admin vs field staff)

### 3. Database Requirements

- **Cosmos DB (NoSQL):**
  - Collection(s) for surveys, equipment, partner organisations
  - HINT: Schema optimised for queries
- **Azure SQL:**
  - Table for daily summaries
  - Use aggregate NOSQL queries for summaries (not Python loops)
  - Provide SQL scripts for schema creation

## Testing

Populate with:

- Multiple researchers and survey records
- At least 10 equipment items
- At least 3 partner organisations
- Several daily summaries

## Deliverables

### Report:

- **Title Page**
- **Table of Contents**
- **Introduction**
  - Brief description of the system’s purpose.
- **Database Design**
  - NoSQL schema design and rationale
  - SQL schema design and rationale
- **System Architecture**
  - Explanation of how the Python application interacts with
    both databases
- **Discussion**
  - Challenges, limitations, and key decisions made.
- **Testing**
  - Test plan, sample test cases, and outcomes (with screenshots where
    useful).
- **Reflection on Artificial Intelligence (AI) Use**
  - Briefly explain how AI tools were
    used during the planning, development, debugging, testing, documentation,
    or report-writing stages.
  - Include:
    - The AI tool(s) used
    - At least three detailed prompts and a brief summary of the
      corresponding outputs
    - How each output was applied, modified, or rejected
    - Any errors, limitations, or unsuitable suggestions identified
    - How AI-generated content was checked, tested, and verified
    - Where relevant, screenshots of AI prompts and outputs can be
      included to illustrate your reflection.
- **References**
  - Any external resources consulted.

### Python Application:

- Connection to both databases
- Implementation of required functionality
- In-code documentation (docstrings, comments)
- Submit as a single .py file or a compressed .zip with all supporting files
- **Must include:**
  - Ensure code runs in a fresh environment with minimal setup.

## Important Notes

- Use Azure Free Tier for all services.
- Configure IP range for your server: 0.0.0.0 to 255.255.255.255.
- Ensure correct access permissions so markers can verify your work.
