import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM

# Load environment variables
load_dotenv()
api_key = os.getenv("VENICE_API_KEY")

# Configuration for Venice AI instances
# Venice AI uses OpenAI-compatible API
venice_base_url = "https://api.venice.ai/api/v1"

# Instance 1: Llama 3.3 70b
llama_llm = LLM(
    model="venice/llama-3.3-70b",
    base_url=venice_base_url,
    api_key=api_key,
    temperature=0.7
)

# Instance 2: Qwen 3 VL
qwen_llm = LLM(
    model="venice/qwen3-vl-235b-a22b",
    base_url=venice_base_url,
    api_key=api_key,
    temperature=0.7
)

# Define Agents
researcher = Agent(
    role='Security Researcher',
    goal='Identify potential vulnerabilities in a system',
    backstory='You are an expert in cybersecurity with years of experience in penetration testing.',
    allow_delegation=False,
    llm=llama_llm,
    verbose=True
)

analyst = Agent(
    role='Compliance Analyst',
    goal='Assess the impact of security vulnerabilities on compliance standards',
    backstory='You specialize in legal and regulatory compliance for whistleblowing platforms.',
    allow_delegation=False,
    llm=qwen_llm,
    verbose=True
)

# Define Tasks
task1 = Task(
    description='Analyze the risk of local file storage for whistleblower evidence.',
    expected_output='A brief summary of risks associated with storing evidence in /tmp.',
    agent=researcher
)

task2 = Task(
    description='Evaluate if /tmp storage meets GDPR data protection standards based on the researcher\'s report.',
    expected_output='A determination on GDPR compliance.',
    agent=analyst
)

# Create Crew
crew = Crew(
    agents=[researcher, analyst],
    tasks=[task1, task2],
    process=Process.sequential,
    verbose=True
)

if __name__ == "__main__":
    print("### Starting CrewAI Verification with Venice AI ###")
    result = crew.kickoff()
    print("\n### Final Result ###\n")
    print(result)
