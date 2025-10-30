import os
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate

class RAGService:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        self.llm = ChatGroq(
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name="groq/compound"
        )

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )

        self.vectorstore = None
        self.qa_chain = None

    def load_collection(self, collection_name):
        collection_path = f"data/collections/{collection_name}"

        loader = DirectoryLoader(
            collection_path, 
            glob="**/*.md", 
            loader_cls=TextLoader,
            loader_kwargs={"encoding": "utf-8"}
        )

        documents = loader.load()

        if not documents:
            return False

        texts = self.text_splitter.split_documents(documents)

        self.vectorstore = FAISS.from_documents(texts, self.embeddings)

        template = """
            You are a helpful assistant that provides accurate answers based on the provided context.
            Use the following pieces of context to answer the question at the end.
            
            {context}
            
            Question: {question}"""
        
        prompt = PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )

        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff", ## stuff is used to send a question and receive a answer 
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": 5}), ## number of documents to retrieve
            chain_type_kwargs={"prompt": prompt}
        )

        return True
    
    def answer_question(self, question):
        ## Make question using the loaded collection
        if not self.qa_chain:
            return "No collection loaded."

        try:
            response = self.qa_chain.invoke({"query": question})
            return response["result"]
        except Exception as e:
            return f"Error occurred: {str(e)}"

