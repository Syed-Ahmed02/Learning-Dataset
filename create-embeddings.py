#Resouces: https://www.datacamp.com/code-along/retrieval-augmented-generation-openai-api-pinecone

import pandas as pd
from langchain_community.document_loaders import DataFrameLoader
import tiktoken
import os
import pinecone
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

load_dotenv()

learning_raw = pd.read_csv("dataset_cleaned.csv")

# Print the head of movies_raw

learning = learning_raw.rename(columns = {
    "Repo": "repository",
    "Text": "title",
    "URL": "url"
})

learning["source"] = "https://github.com/" + learning["repository"]

learning["page_content"] = "Title: " + learning["title"] + "\n" + \
                         "Url: " + learning["url"] 
                         
                         
learning= learning[["source", "page_content"]]

docs = DataFrameLoader(
    learning,
    page_content_column="page_content",
).load()

# Print the first 3 documents and the number of documents
print(f"First 3 documents: {docs[:3]}")
print(f"Number of documents: {len(docs)}")



# Create the encoder
encoder = tiktoken.get_encoding("cl100k_base")

# Create a list containing the number of tokens for each document
tokens_per_doc = [len(encoder.encode(doc.page_content)) for doc in docs]

# Show the estimated cost, which is the sum of the amount of tokens divided by 1000, times $0.0001
total_tokens = sum(tokens_per_doc)
cost_per_1000_tokens = 0.0001
cost =  (total_tokens / 1000) * cost_per_1000_tokens
print(cost)


pinecone_api_key = os.getenv("PINECONE_API_KEY")
pc = pinecone.Pinecone(api_key=pinecone_api_key)


index_name = "roadmap-gpt"

# List the names of available indexes. Assign to existing_index_names.
existing_index_names = [idx.name for idx in pc.list_indexes().indexes]

# First check that the given index does not exist yet
if index_name not in existing_index_names:
    # Create the 'imbd-movies' index with cosine metric, 1536 dims, serverless spec: aws in us-east-1
    pc.create_index(
        name=index_name,
        metric='cosine',
        dimension=1536,
        spec=pinecone.ServerlessSpec(cloud="aws", region="us-east-1")
    )



embeddings = OpenAIEmbeddings()

# Create an index from its name
index = pc.Index(index_name)

# Count the number of vectors in the index
n_vectors = index.describe_index_stats()['total_vector_count']
print(f"There are {n_vectors} vectors in the index already.")

# Check if there is already some data in the index on Pinecone
if n_vectors > 0:
    # If there is, get the documents to search from the index. Assign to docsearch.
    docsearch = PineconeVectorStore.from_existing_index(index_name, embeddings)
else:
    # If not, fill the index from the documents and return those docs to assign to docsearch
    docsearch = PineconeVectorStore.from_documents(docs, embeddings, index_name=index_name)

# Define a question about learning to ask
question = "How do I learn Machine learning?"
    
# Convert the vector database to a retriever and get the relevant documents for a question
print("These are the documents most relevant to the question:")
print(docsearch.as_retriever().invoke(question))