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
    model="openai/llama-3.3-70b",
    base_url=venice_base_url,
    api_key=api_key,
    temperature=0.7
)

# Instance 2: Qwen 3 VL
qwen_llm = LLM(
    model="openai/qwen3-vl-235b-a22b",
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

summary_agent = Agent(
    role='Report Specialist',
    goal='Create a professional and concise police report based on provided evidence and whistleblower intent.',
    backstory='You are a veteran police officer with expertise in drafting formal reports that are clear, factual, and actionable for investigators.',
    allow_delegation=False,
    llm=llama_llm,
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

def generate_police_report(evidence_analysis: str):
    """
    Triggers CrewAI to generate a police report based on the provided evidence analysis.
    """
    report_task = Task(
        description=f'Based on the following extracted evidence: "{evidence_analysis}", create a formal police report. '
                    f'The report should include: Date/Time (placeholder), Evidence Summary, and Potential Category of Crime.',
        expected_output='A structured, professional police report in markdown format.',
        agent=summary_agent
    )
    
    report_crew = Crew(
        agents=[summary_agent],
        tasks=[report_task],
        process=Process.sequential,
        verbose=True
    )
    
    return report_crew.kickoff()

if __name__ == "__main__":
    print("### Starting CrewAI Verification with Venice AI ###")
    result = crew.kickoff()
    print("\n### Final Result ###\n")
    print(result)
