import json
import streamlit as st
from utils import (
    natural_language_to_pinecone_format,
    natural_language_to_sematic_meaning,
    query_database_custom,
    data_creation,
    embeddings_creation,
    convert_to_pinecone_format,
    data_to_vector_db
)

st.set_page_config(page_title="Pinecone Query Agent", layout="wide")
st.title("🧠 Natural Language to Pinecone Query Agent")

st.sidebar.header("🔧 Pinecone Configuration")
api_key = st.sidebar.text_input("Pinecone API Key", type="password")
index_name = st.sidebar.text_input("Index Name", value="demo")
metric = st.sidebar.selectbox("Similarity Metric", ["cosine", "euclidean", "dotproduct"])
dimension = st.sidebar.number_input("Vector Dimension", min_value=1, value=384)
run_setup = st.sidebar.button("📦 Upload Data to Pinecone")

if run_setup:
    if not api_key.strip():
        st.sidebar.warning("Please provide a valid API key.")
    else:
        with st.spinner("Processing and uploading data..."):
            data_creation("./data/sample_data - itg_sports.csv.csv")
            embeddings_creation()
            convert_to_pinecone_format()
            data_to_vector_db(
                api_key=api_key,
                index_name=index_name,
                metric=metric,
                dimension=dimension
            )
        st.sidebar.success("✅ Data uploaded to Pinecone!")

st.subheader("🔍 Query Your Vector Database")

user_query = st.text_input("Enter your query:", placeholder="e.g. Show me all articles by Jane Doe")
index_name = st.text_input("Enter your index_name:", placeholder="e.g. demo")
api_key = st.text_input("Enter your API_KEY:", type="password")
top_k = st.slider("Number of results to retrieve", 1, 10, 3)

if st.button("Run Query"):
    if not user_query.strip():
        st.warning("Please enter a query first.")
    elif not api_key.strip():
        st.error("API key is required to query the database.")
    else:
        with st.spinner("Querying Pinecone..."):
            filter_response = natural_language_to_pinecone_format(user_query)
            semantic_response = natural_language_to_sematic_meaning(user_query)

            st.subheader("🧠 Interpreted Query")
            st.json({
                "filter": json.loads(filter_response),
                "semantic_query": semantic_response.strip().replace('"', '')
            })

            st.subheader("Results from Pinecone")
            response = query_database_custom(user_query, api_key, top_k, index_name)
            if response.matches:
                for i, match in enumerate(response.matches, 1):
                    with st.expander(f"Result {i}"):
                        st.json(match.metadata)
            else:
                st.write("No results found.")

