from langchain import PromptTemplate, SQLDatabase
from langchain.chains import APIChain, LLMMathChain, RetrievalQA, SQLDatabaseChain
from langchain.chains.api import podcast_docs
from langchain.chains.api.prompt import API_RESPONSE_PROMPT
from langchain.experimental.plan_and_execute import PlanAndExecute, load_agent_executor, load_chat_planner
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.chat_models import ChatOpenAI
from langchain.agents.tools import Tool
import os
from typing import List
from pathlib import Path
from dotenv import load_dotenv
from langchain.agents import AgentType
import pinecone
from api.api_docs import payment_docs

load_dotenv()

class PayAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0, openai_api_key=os.environ.get('OPENAI_API_KEY'))
        
    def retrieve_user_stories(self, index_name: str, query: str)-> str:
        pinecone.init(
            api_key=os.environ.get('PINECONE_API_KEY'),
            environment=os.environ.get('PINECONE_API_ENV')
        )

        embeddings = OpenAIEmbeddings()
        
        docsearch = Pinecone.from_existing_index(index_name, embeddings)

        template="""Based on the user request given {query}, select the user stories that best matches what 
        the user wants to perform. Else, if no user story matches, return 'No user story found'. 
        After selecting the stories, break it down into steps. """

        prompt = PromptTemplate(template=template, input_variables=["query"])
        chain_type_kwargs = {"prompt": prompt}
        flow_docs = RetrievalQA.from_chain_type(llm=self.llm, chain_type="stuff",  retriever=docsearch.as_retriever(), chain_type_kwargs=chain_type_kwargs)
        
        user_story = flow_docs.run(query)
        
        return user_story
    
    def create_api_call_tool(self):
        api_chain = APIChain.from_llm_and_api_docs(llm=self.llm, api_docs=payment_docs.PAYMENT_DOCS, verbose=True)
        tool = Tool(
                name = "API Call system",
                func=api_chain.run,
                description="Used to determine the API to call to run payment integrations based on the user stories given"
            )
        
        return tool
    
    def create_sql_query_tool(self):
        dburi = "sqlite:///payment.db"
        db = SQLDatabase.from_uri(dburi)
        sql_chain = SQLDatabaseChain(llm=self.llm, database=db, verbose=True)
        tool = Tool(
                name = "SQL Executer System",
                func=sql_chain.run,
                description="Useful to query payment information in the database and provide the answers back"
            )
        
        return tool
    
    # def create_math_calculator_tool(self):
    #     math_chain = LLMMathChain.from_llm(llm=self.llm, verbose=True)
    #     tool = Tool(
    #             name = "Math Calculation System",
    #             func=math_chain.run,
    #             description="Useful to calculate the math"
    #         )
        
    #     return tool
        
       
    def create_agent(self, tools: List[Tool]) ->PlanAndExecute:
        planner = load_chat_planner(llm=self.llm)
        executor = load_agent_executor(llm=self.llm, tools=tools, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, max_iterations=10, max_execution_time=10, early_stopping_method="generate", verbose=True)
        agent = PlanAndExecute(planner=planner, executor=executor, verbose=True)
        return agent

    def upload_stories(self, filename: str, index_name: str)-> None:
        
        destination_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'docs')
        doc_path = os.path.join(destination_folder, filename)

        loader = PyPDFLoader(doc_path)
        texts = loader.load_and_split(text_splitter=CharacterTextSplitter(chunk_size=1000, chunk_overlap=0))
        
        embeddings = OpenAIEmbeddings()
        
        pinecone.init(
            api_key=os.environ.get('PINECONE_API_KEY'),
            environment=os.environ.get('PINECONE_API_ENV')
        )

        index = Pinecone.from_documents(texts, embeddings, index_name=index_name)
            
    
    # def get_steps(self, query: str):
        
    #     action = self.db_chain.run(f"""
    #                     Based on the user request below,
    #                     retrieve the most probable action to take based on the action description
    #                     in the action table and return the action code. If there is no probable action to take,
    #                     return null:
                        
    #                     {query}
    #                     """)
        
    #     if not action:
    #         raise Exception("There is no relevant actions to take")
    
    #     self.db_chain.run(f"""
    #                     Based on the action selected, select the corresponding agent in the agent table
    #                     """)
        
    #     steps = self.db_chain.run(f"""
    #                     Based on the agent selected, get the agent steps and correlate them to the step codes 
    #                     in step table and retrieve the step's prompt templates in the order of the steps in the agent steps column. 
    #                     Combine the prompt templates into 1 continuous string
    #                     """)
        
    #     return steps 
    
    