import pandas as pd
import ast
import json
from sentence_transformers import SentenceTransformer
from datetime import datetime
from pinecone import Pinecone, ServerlessSpec
import json
import os
import google.generativeai as genai


def data_creation(data_frame_path):
    df = pd.read_csv(data_frame_path)
    # print(df.head())
    # print(df.shape)
    # print(df.columns)

    data = []

    for index, row in df.iterrows():
        tags_str = row['tags'].strip()  # Remove leading/trailing whitespace/newlines
        data_imm = {
            "id": row['pageURL'],
            "title": row['title'],
            "metadata": {
                "published_date": row['publishedDate'],
                "author": row['author'],
                "tags": ast.literal_eval(tags_str)
            }
        }
        data.append(data_imm)
        # print(data_imm)

    with open('output.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print("Data saved to output.json")


def embeddings_creation():
    with open('output.json', 'r') as f:
        data = json.load(f)

    model = SentenceTransformer('all-MiniLM-L6-v2')
    titles = [item['title'] for item in data]
    embeddings = model.encode(titles)

    output_data = []
    for item, embedding in zip(data, embeddings):
        item_copy = item.copy()
        item_copy['title_embedding'] = embedding.tolist()
        output_data.append(item_copy)

    with open('encoded_output.json', 'w') as f:
        json.dump(output_data, f, indent=4)




def convert_to_pinecone_format():
    with open('encoded_output.json') as f:
        data = json.load(f)

    output = []

    for item in data:
        try:
            d = datetime.fromisoformat(item['metadata']['published_date'].replace('Z', '+00:00'))
            y, m, d_ = d.year, d.month, d.day
        except:
            y = m = d_ = None

        output.append({
            "id": item['id'],
            "values": item['title_embedding'],
            "metadata": {
                "title": item['title'],
                "published_date": item['metadata']['published_date'],
                "published_year": y,
                "published_month": m,
                "published_day": d_,
                "author": item['metadata']['author'],
                "tags": item['metadata']['tags']
            }
        })

    with open('pinecone_data.json', 'w') as f:
        json.dump(output, f, indent=2)

    print(f"Converted {len(output)} items to Pinecone format") 
    # print(json.dumps(output[0], indent=2)) 


def data_to_vector_db(api_key, index_name, metric, dimension=384, cloud="aws", region="us-east-1"):
    pc = Pinecone(api_key=api_key)

    if not pc.list_indexes() or index_name not in pc.list_indexes():
        pc.create_index(
            name=index_name,
            dimension=dimension,
            metric=metric,
            spec=ServerlessSpec(cloud=cloud, region=region)
        )
        print(f"Index '{index_name}' created with dimension={dimension} and metric='{metric}'.")
    else:
        print(f"Index '{index_name}' already exists.")

    index = pc.Index(index_name)

    with open("pinecone_data.json", "r") as f:
        items = json.load(f)

    vectors = [
        {
            "id": item["id"],
            "values": item["values"],
            "metadata": item.get("metadata", {})
        }
        for item in items
    ]

    index.upsert(vectors=vectors)
    print("Data uploaded successfully.")


def natural_language_to_pinecone_format(instruction_of_user):
   api_key="AIzaSyAIZuyNcQS38wZzO5uEJyReJ4nW87jJM2s"
   SYSTEM_INSTRUCTIONS = """
You are a Natural Language to Pinecone Query Agent. Convert user queries to Pinecone metadata filters.

SCHEMA:
- published_year: int
- published_month: int  
- published_day: int
- author: string
- tags: array

SYNTAX:
- Equality: "field": value
- Arrays: "field": {"$in": ["value1", "value2"]}
- Ranges: "field": {"$gte": start, "$lt": end}

CURRENT DATE: May 31, 2025

PARSING:
- "last year" = published_year: 2024
- "this year" = published_year: 2025
- "June 2023" = published_year: 2023, published_month: 6
- Month names: January=1, February=2, March=3, April=4, May=5, June=6, July=7, August=8, September=9, October=10, November=11, December=12

EXAMPLES:

Input: "Show me articles by Alice Zhang from last year about machine learning"
Output:
{
 "author": "Alice Zhang",
 "published_year": 2024,
 "tags": {"$in": ["machine learning"]}
}

Input: "Find posts tagged with 'LLMs' published in June, 2023"
Output:
{
 "tags": {"$in": ["LLMs"]},
 "published_year": 2023,
 "published_month": 6
}

Input: "Anything by John Doe on vector search?"
Output:
{
 "author": "John Doe",
 "tags": {"$in": ["vector search"]}
}
REMEMBER THAT THE USER INPUT MIGHT BE FROM DIFFERENT TOPIC OR DIFFERENT FIELD. USE YOU INTELLIGENCE TO GIVE THE BEST POSSIBLE OUTPUT. 
I HAVE JUST GIVEN SOME EXAMPLES.
Return only JSON. No markdown. No explanations.
"""

   genai.configure(api_key=api_key)

   model = genai.GenerativeModel(
       model_name="gemini-2.5-flash-preview-05-20",
       system_instruction=SYSTEM_INSTRUCTIONS
   )

   response = model.generate_content(instruction_of_user)
   return response.text


def natural_language_to_sematic_meaning(input):
   api_key="AIzaSyAIZuyNcQS38wZzO5uEJyReJ4nW87jJM2s"
   SYSTEM_INSTRUCTIONS = """
You are a semantic query extractor for a vector search system.

Your only task is to extract the core topic or subject from a user's natural language query. This semantic phrase will be used for vector similarity search.

Instructions:
- Ignore all metadata like author names, publication dates, or tags unless they are part of the actual search topic.
- Focus only on the main idea or topic the user is trying to find content about.
- Your output must be a concise search phrase (ideally 3 to 7 words).
- Only return a quoted string with the semantic query.
- DO NOT return anything else—no explanations, no formatting, no extra text.

Examples:

User Input: "Show me articles by Alice Zhang from last year about machine learning"  
Output: "machine learning articles"

User Input: "Find posts tagged with ‘LLMs’ published in June, 2023."  
Output: "LLM posts"

User Input: "Anything by John Doe on vector search?"  
Output: "vector search content"

User Input: "I want research on retrieval-augmented generation."  
Output: "retrieval-augmented generation research"

REMEMBER THAT THE USER INPUT MIGHT BE FROM DIFFERENT TOPIC OR DIFFERENT FIELD. USE YOU INTELLIGENCE TO GIVE THE BEST POSSIBLE OUTPUT. 
I HAVE JUST GIVEN SOME EXAMPLES.
---

Now process the next input.  
Only return a quoted string.

"""

   genai.configure(api_key=api_key)

   model = genai.GenerativeModel(
       model_name="gemini-2.5-flash-preview-05-20",
       system_instruction=SYSTEM_INSTRUCTIONS
   )

   response = model.generate_content(input)
   return response.text



def query_database_hardcoded():
    model = SentenceTransformer('all-MiniLM-L6-v2')

    pc = Pinecone(api_key="pcsk_4Z6Fn5_PJpZMZFg4jvSDiSUGRi8ZbwX5dq79pXK69yvEbGyiw9T7rbZASZkKwWGwHbNLWu") 
    index_name = "demo"  
    index = pc.Index(index_name)

    user_input = "Show me the article about Vaibhav Suryavanshi's duck after hundred in IPL 2025 by Jane Doe"
    metadata_filter = {
        "author": "Jane Doe",
        "published_year": 2025,
        "tags": {
            "$in": ["#VaibhavSuryavanshi", "#IPL2025"]
        }
    }

    semantic_query = "Vaibhav Suryavanshi IPL 2025 duck after hundred"
    query_vector = model.encode(semantic_query).tolist()

    response = index.query(
        vector=query_vector,
        top_k=5,
        filter=metadata_filter,
        include_metadata=True
    )

    print("Metadata Filter:", json.dumps(metadata_filter, indent=2))
    print("Semantic Query:", semantic_query)
    print("\nResults:")
    for match in response['matches']:
        print(json.dumps(match['metadata'], indent=2))


# def query_database_custom(user_input,k=5):
#     model = SentenceTransformer('all-MiniLM-L6-v2')

#     pc = Pinecone(api_key="pcsk_4Z6Fn5_PJpZMZFg4jvSDiSUGRi8ZbwX5dq79pXK69yvEbGyiw9T7rbZASZkKwWGwHbNLWu") 
#     index_name = "demo"  
#     index = pc.Index(index_name)
#     metadata_filter = natural_language_to_pinecone_format(user_input)
#     # metadata_filter = {
#     #     "author": "Jane Doe",
#     #     "published_year": 2025,
#     #     "tags": {
#     #         "$in": ["#VaibhavSuryavanshi", "#IPL2025"]
#     #     }
#     # }
#     print(metadata_filter)
#     metadata_filter = json.loads(metadata_filter)
#     semantic_query = natural_language_to_sematic_meaning(user_input)
    
#     print(semantic_query)
#     query_vector = model.encode(semantic_query).tolist()

#     response = index.query(
#         vector=query_vector,
#         top_k=k,
#         filter=metadata_filter,
#         include_metadata=True
#     )

#     print("Metadata Filter:", json.dumps(metadata_filter, indent=2))
#     print("Semantic Query:", semantic_query)
#     print("\nResults:")
#     for match in response['matches']:
#         print(json.dumps(match['metadata'], indent=2))






def query_database_custom(user_input,api_key, k=5, index_name="demo"):
    model = SentenceTransformer('all-MiniLM-L6-v2')

    pc = Pinecone(api_key=api_key) 
    index = pc.Index(index_name)

    metadata_filter = natural_language_to_pinecone_format(user_input)
    metadata_filter = json.loads(metadata_filter)

    semantic_query = natural_language_to_sematic_meaning(user_input)
    semantic_query = semantic_query.strip('"')

    query_vector = model.encode(semantic_query).tolist()

    response = index.query(
        vector=query_vector,
        top_k=k,
        filter=metadata_filter,
        include_metadata=True
    )

    print("Metadata Filter:", json.dumps(metadata_filter, indent=2))
    print("Semantic Query:", semantic_query)
    print("\nResults:")
    for match in response['matches']:
        print(json.dumps(match['metadata'], indent=2))

    return response
