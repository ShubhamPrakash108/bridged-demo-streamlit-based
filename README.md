# 🧠 Natural Language to Pinecone Query Agent

A powerful Streamlit application that bridges the gap between natural language queries and vector database searches. This intelligent agent converts your everyday questions into precise Pinecone queries, combining semantic search with metadata filtering for accurate results.

## 📸 Application Screenshots

### System Architecture
![System Flow Diagram](images/system-flow-diagram.svg)
*Complete system architecture showing data flow from CSV input to query results*

### Pinecone Console Setup
![Pinecone Console](images/pinecone-console.jpg)
*Initial Pinecone console showing empty project ready for index creation*

### Application Interface
![Streamlit Interface](images/streamlit-interface.jpg)
*Main application interface with configuration panel and query section*

### Data Upload Process
![Pinecone Index Created](images/pinecone-index-created.jpg)
*CSV data being processed and uploaded to Pinecone vector database*

### Query Processing
![Query Interface](images/query-interface.jpg)
*Natural language query being processed and results being displayed*

### Sample Data Structure
![Sample Data](images/sample-data-csv.jpg)
*Example CSV data structure with required columns and format*

### Query Results
![Query Results](images/query-results.jpg)
*Search results showing matched articles with complete metadata*

## 🚀 What This Project Does

The Pinecone Query Agent transforms natural language queries into sophisticated vector database searches by:

1. **Natural Language Processing**: Takes your plain English questions and understands what you're looking for
2. **Dual Query Generation**: Creates both semantic embeddings and metadata filters from your input
3. **Intelligent Filtering**: Automatically extracts filters like author names, publication dates, and tags
4. **Vector Search**: Performs similarity searches using sentence transformers
5. **Results Display**: Presents matching results with complete metadata in an intuitive interface

## 🎯 Key Features

### Smart Query Interpretation
- **Semantic Understanding**: Extracts the core topic from your query for vector similarity search
- **Metadata Filtering**: Automatically identifies and applies filters for authors, dates, tags, and more
- **Flexible Date Parsing**: Understands relative dates like "last year", "June 2023", "this month"

### Powered by AI
- **Google Gemini Integration**: Uses Gemini 2.5 Flash for intelligent query parsing
- **Sentence Transformers**: Employs 'all-MiniLM-L6-v2' for high-quality text embeddings
- **Pinecone Vector DB**: Leverages serverless vector database for fast, scalable search

### User-Friendly Interface
- **Streamlit Web App**: Clean, intuitive interface for easy interaction
- **Real-time Results**: Instant query processing and result display
- **Configurable Parameters**: Adjust search parameters like top-k results
- **Data Upload**: Simple CSV to vector database pipeline

## 🔍 How It Works

### 1. Data Processing Pipeline
```
CSV Data → JSON Conversion → Embedding Generation → Pinecone Format → Vector Database
```

![Sample Data Structure](images/sample-data-csv.jpg)

The system processes your CSV data through several stages:
- Converts CSV to structured JSON format
- Generates title embeddings using sentence transformers
- Formats data for Pinecone with proper metadata structure
- Uploads vectors to your Pinecone index

### 2. Query Processing
When you ask a question like: *"Show me articles by Jane Doe from last year about machine learning"*

![Query Processing](images/query-interface.jpg)

The system:
- **Extracts Metadata Filter**: `{"author": "Jane Doe", "published_year": 2024, "tags": {"$in": ["machine learning"]}}`
- **Creates Semantic Query**: `"machine learning articles"`
- **Generates Embedding**: Converts semantic query to vector representation
- **Searches Database**: Combines vector similarity with metadata filtering
- **Returns Results**: Displays matched articles with full metadata

### 3. Supported Query Types

**Author-based Queries**:
- "Find articles by John Smith"
- "What did Alice Johnson write about AI?"

**Date-based Queries**:
- "Show me posts from last year"
- "Articles published in June 2023"
- "Recent content from this month"

**Topic-based Queries**:
- "Find content about vector databases"
- "Show me machine learning research"

**Combined Queries**:
- "Alice's articles about NLP from 2024"
- "Recent posts by Bob on deep learning"

## 🏗️ System Architecture

![System Architecture Diagram](images/system-flow-diagram.svg)
*Detailed system architecture showing the complete data pipeline and query processing flow*

### Architecture Overview

The system follows a modern microservices-inspired architecture with clear separation of concerns:

**Data Processing Layer**:
- CSV ingestion and validation
- JSON transformation pipeline
- Embedding generation using Sentence Transformers
- Vector database formatting and upload

**AI Processing Layer**:
- Google Gemini 2.5 Flash for query interpretation
- Natural language to metadata filter conversion
- Semantic query extraction and processing
- Dual-path query execution (semantic + metadata)

**Interface Layer**:
- Streamlit web application
- Real-time query processing
- Interactive result visualization
- Configuration management

**Storage Layer**:
- Pinecone vector database (primary storage)
- Local JSON files (intermediate processing)
- In-memory query caching

### Core Components

**Frontend (app_sl.py)**:
- Streamlit interface for user interaction
- Configuration panels for Pinecone setup
- Query input and results display
- Data upload workflow

**Backend (utils.py)**:
- Data processing pipeline functions
- AI-powered query interpretation
- Vector database operations
- Embedding generation and management

### Data Schema
The system expects CSV data with these columns:
- `pageURL`: Unique identifier
- `title`: Article/content title
- `publishedDate`: Publication date (ISO format)
- `author`: Author name
- `tags`: List of tags (string representation of Python list)

### Vector Database Structure
Each record in Pinecone contains:
- **ID**: Unique identifier (pageURL)
- **Values**: 384-dimensional embedding vector
- **Metadata**: Title, author, publication date components, and tags

## 🤖 AI Integration

### Google Gemini 2.5 Flash
- Converts natural language to Pinecone metadata filters
- Extracts semantic meaning for vector search
- Handles complex temporal and categorical queries
- Adapts to different domains and topics

### Sentence Transformers
- Uses 'all-MiniLM-L6-v2' model for embeddings
- Generates 384-dimensional vectors
- Optimized for semantic similarity search
- Fast inference for real-time queries

## 📊 Example Workflows

### Data Upload Workflow
![Streamlit Interface](images/streamlit-interface.jpg)
*Main application interface showing the data upload and configuration options*

1. Prepare your CSV with required columns
2. Configure Pinecone settings (API key, index name, dimensions)
3. Click "Upload Data to Pinecone"
4. System processes and uploads your data automatically

![Pinecone After Upload](images/pinecone-index-created.jpg)
*Pinecone console showing successfully uploaded data*

### Query Workflow
![Query Interface](images/query-interface.jpg)
*Query input interface where users can enter natural language questions*

1. Enter your natural language query
2. Provide Pinecone credentials
3. Set desired number of results
4. View interpreted query structure
5. Browse matched results with metadata

![Query Results](images/query-results.jpg)
*Example results showing matched articles with metadata and relevance scores*

## 🔧 Technical Specifications

- **Vector Dimensions**: 384 (configurable)
- **Similarity Metrics**: Cosine, Euclidean, Dot Product
- **Cloud Provider**: AWS (configurable)
- **Region**: US-East-1 (configurable)
- **Embedding Model**: all-MiniLM-L6-v2
- **AI Model**: Google Gemini 2.5 Flash Preview

## 💡 Use Cases

- **Content Management**: Find specific articles in large content databases
- **Research Discovery**: Locate research papers by topic, author, or date
- **Knowledge Base Search**: Query organizational knowledge repositories
- **Blog/News Search**: Search through article collections with natural language
- **Academic Research**: Find papers and publications using conversational queries

This project demonstrates the power of combining large language models with vector databases to create intuitive, intelligent search experiences that understand context and intent.

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Pinecone account and API key
- Google AI API key (for Gemini integration)

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/ShubhamPrakash108/streamlit-based
   cd streamlit-based
   ```

2. **Create and Activate Virtual Environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   *Note: This may take some time as it installs several ML libraries including sentence-transformers and other dependencies.*

4. **Launch the Application**
   ```bash
   streamlit run app_sl.py
   ```

### Initial Setup Workflow

#### Step 1: Configure Pinecone
![Pinecone Console](images/pinecone-console.jpg)
*Initial Pinecone console before creating any indexes*

When the Streamlit app opens, you'll see the Pinecone Configuration panel on the left sidebar:

- **Pinecone API Key**: Enter your Pinecone API key (get it from [Pinecone Console](https://app.pinecone.io))
- **Index Name**: Choose a name for your index (e.g., "demo", "mydemosp")
- **Similarity Metric**: Select your preferred metric (cosine recommended)
- **Vector Dimension**: Keep as **384** (matches the embedding model dimensions)

#### Step 2: Upload Your Data
![Streamlit Interface](images/streamlit-interface.jpg)
*Main Streamlit interface showing configuration options and upload functionality*

1. Ensure your CSV data follows the required schema:
   ```csv
   pageURL,title,publishedDate,author,tags
   https://example.com/article1,Sample Article,2025-05-01T14:25:03.000000Z,Akainu,"[""#SuyashSharma"", ""#RCB"", ""#CricketHealth""]"
   ```

2. Click **"📦 Upload Data to Pinecone"**

3. The system will process your data through several stages:
   - Convert CSV to JSON format (`output.json`)
   - Generate embeddings (`encoded_output.json`)
   - Format for Pinecone (`pinecone_data.json`)
   - Upload to your Pinecone index

4. You can verify the upload by checking:
   - **Local files**: JSON files will appear in your working directory
   - **Pinecone Console**: Your index will show the uploaded vectors

![Pinecone Index Created](images/pinecone-index-created.jpg)
*Pinecone console showing successfully created index with uploaded data*

#### Step 3: Query Your Database
![Query Interface](images/query-interface.jpg)
*Query interface where users can input natural language questions*

1. **Enter your query** in natural language:
   - "Show me articles written by the author Akainu"
   - "Find posts about cricket from last year"
   - "What did Jane Doe write about IPL?"

2. **Provide credentials** (for security):
   - Enter your **API Key** again
   - Enter your **Index Name** again
   - Adjust **Number of results** (1-10)

3. **Run Query** and view results:
   - **Interpreted Query**: See how your natural language was converted to filters and semantic search
   - **Results**: Browse matched articles with full metadata

![Query Results](images/query-results.jpg)
*Example of query results with complete metadata and relevance scores*

### Example Data Structure
![Sample Data CSV](images/sample-data-csv.jpg)
*Example CSV data structure showing the required columns and format*

The system expects CSV data like this:
```csv
pageURL,title,publishedDate,author,tags
https://example.com/article1,Sample Article,2025-05-01T14:25:03.000000Z,Akainu,"[""#SuyashSharma"", ""#RCB"", ""#CricketHealth""]"
```

### Security Features
- **Double Authentication**: Users must enter API credentials twice (setup + query) for enhanced security
- **No Persistent Storage**: API keys are not stored in the application
- **Direct Index Access**: Queries go directly to your Pinecone index with your credentials

### Sample Query Examples
Based on the provided data, try these queries:
- "Show me articles written by the author Akainu"
- "Find cricket articles by Jane Doe from 2025"
- "What did Mary Poppins write about IPL?"
- "Show me recent articles about Vaibhav Suryavanshi"

### Troubleshooting
- **No Index Found**: Make sure you've uploaded data first and the index name matches
- **No Results**: Check if your query matches the available data and authors
- **API Errors**: Verify your Pinecone API key is valid and has proper permissions
- **Dimension Mismatch**: Ensure vector dimension is set to 384

The application will show you the interpreted query structure so you can understand how your natural language was processed into database filters and semantic search terms.

## 📈 Project Impact

This Natural Language to Pinecone Query Agent represents a significant advancement in making vector databases accessible to non-technical users. By combining the power of large language models with efficient vector search, it creates an intuitive bridge between human language and sophisticated database queries.

### Key Achievements:
- **Simplified Vector Search**: Makes complex vector database operations accessible through natural language
- **Intelligent Query Processing**: Automatically extracts both semantic meaning and structured filters
- **Real-time Performance**: Delivers fast query results with immediate feedback
- **Scalable Architecture**: Built on cloud-native technologies for production deployment

The project showcases the potential of AI-powered interfaces to democratize advanced database technologies, making them usable for content discovery, research, and knowledge management across various domains.
