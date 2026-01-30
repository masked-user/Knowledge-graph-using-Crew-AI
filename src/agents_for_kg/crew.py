from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import FileReadTool
from typing import List
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

file_tool = FileReadTool(file_path="agents_for_kg/knowledge/rules_for_ontology.txt")


SystemPrompt = """You are an expert knowledge graph construction agent. Your task is to assist in building and refining knowledge graphs based on provided data and instructions. You have access to various tools to read files and extract information.
Use the tools wisely to gather necessary information and ensure the quality of the knowledge graph.
Always refer to the authoritative ontology and rules provided in 'rules_for_ontology.txt' when making decisions about the knowledge graph structure and content.   
 """

@CrewBase
class AgentsForKg():
    """AgentsForKg crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.comc/concepts/agents#agent-tools
    @agent
    def SchemaMapper(self) -> Agent:
        return Agent(
            config=self.agents_config['SchemaMapper'], # type: ignore[index]
            verbose=True,
            reasoning=True,  # Enable reasoning
            max_reasoning_attempts=3,
            system_template=SystemPrompt,
            toosls=[file_tool]  # Adding the file reading tool
        )
    
    @agent
    def EvidenceExtractor(self) -> Agent:
        return Agent(
            config=self.agents_config['EvidenceExtractor'], # type: ignore[index]
            verbose=True,
            reasoning=True,  # Enable reasoning
            max_reasoning_attempts=3,
            system_template=SystemPrompt,
            toosls=[file_tool]  # Adding the file reading tool
        )

    @agent
    def GraphLinker(self) -> Agent:
        return Agent(
            config=self.agents_config['GraphLinker'], # type: ignore[index]
            verbose=True,
            reasoning=True,  # Enable reasoning
            max_reasoning_attempts=3,
            system_template=SystemPrompt,
            toosls=[file_tool]  # Adding the file reading tool
        )

    @agent
    def VerificationCritic(self) -> Agent:
        return Agent(
            config=self.agents_config['VerificationCritic'], # type: ignore[index]
            verbose=True,
            reasoning=True,  # Enable reasoning
            max_reasoning_attempts=3,
            system_template=SystemPrompt,
            toosls=[file_tool]  # Adding the file reading tool
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def Ontology_Alignment(self) -> Task:
        return Task(
            config=self.tasks_config['Ontology_Alignment'], # type: ignore[index]
            output_file='aligned_ontology.json'
        )

    @task
    def Attribute_Extraction(self) -> Task:
        return Task(
            config=self.tasks_config['Attribute_Extraction'], # type: ignore[index]
            output_file='extracted_attributes.json'
        )
    
    @task
    def Relationship_Establishment(self) -> Task:
        return Task(
            config=self.tasks_config['Relationship_Establishment'], # type: ignore[index]
            output_file='established_relationships.json'
        )

    @task
    def Quality_Validation(self) -> Task:
        return Task(
            config=self.tasks_config['Quality_Validation'], # type: ignore[index]
            output_file='validated_attributes.json'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the AgentsForKg crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            memory=True,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
