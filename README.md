# CDP Support Agent Chatbot

A chatbot that answers "how-to" questions related to Customer Data Platforms (CDPs): Segment, mParticle, Lytics, and Zeotap.

## Build and Setup Instructions

### Prerequisites

- Python 3.13
- Git
- Internet connection (for initial documentation fetching)

### 1. Clone the Repository

```bash
git clone https://github.com/SuprHUlk/chat-bot.git
cd chat-bot
```

### 2. Create a Virtual Environment

```bash
# Windows
python -m venv .venv

# macOS/Linux
python3 -m venv .venv
```

### 3. Activate the Virtual Environment

```bash
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Fetch Documentation

This step downloads and processes documentation from the supported CDP platforms:

```bash
python src/fetch_docs.py
```

You can also fetch documentation for a specific CDP:

```bash
python src/fetch_docs.py --cdp segment
python src/fetch_docs.py --cdp mparticle
python src/fetch_docs.py --cdp lytics
python src/fetch_docs.py --cdp zeotap
```

## Running the Application

### Web Interface (Recommended)

The web interface provides the most user-friendly experience:

```bash
python src/web_app.py
```

The web interface will be available at `http://localhost:8000`.

### Command-line Interface

For a terminal-based experience:

```bash
python src/cli.py
```

### API Server

To run just the API server (useful for integration with other applications):

```bash
python src/run_server.py
```

The API will be available at `http://localhost:8000`.

#### API Endpoints

- `POST /ask`: Ask a question
  - Request body: `{"text": "How do I set up a new source in Segment?"}`
  - Response: `{"response": "..."}`

- `GET /health`: Health check
  - Response: `{"status": "healthy"}`

## Features

- Answers "how-to" questions about CDP platforms
- Extracts relevant information from official documentation
- Handles variations in questions, including long questions
- Provides structured, helpful responses with source references
- Filters out irrelevant questions
- Web interface for easy interaction
- Cross-CDP comparisons for feature evaluation
- Advanced "how-to" questions with detailed step-by-step instructions

## Supported CDPs

- [Segment](https://segment.com/docs/)
- [mParticle](https://docs.mparticle.com/)
- [Lytics](https://docs.lytics.com/)
- [Zeotap](https://docs.zeotap.com/home/en-us/)

## Project Structure

```
.
├── data/
│   └── docs/           # Processed documentation files
├── src/
│   ├── api.py          # FastAPI web interface
│   ├── chatbot.py      # Core chatbot logic
│   ├── cli.py          # Command-line interface
│   ├── document_processor.py  # Documentation fetching and processing
│   ├── fetch_docs.py   # Script to fetch documentation
│   ├── indexer.py      # Document indexing and search
│   ├── run_server.py   # Script to run the API server
│   ├── test_all.py     # Consolidated test script with menu interface
│   ├── web_app.py      # Web application server
│   └── static/         # Static files for the web interface
│       ├── index.html  # HTML for the web interface
│       ├── styles.css  # CSS for the web interface
│       └── script.js   # JavaScript for the web interface
└── requirements.txt    # Python dependencies
```

## Testing

### Interactive Testing

Run the consolidated test script with an interactive menu:

```bash
python src/test_all.py
```

### Command-line Testing Options

You can also run specific test modes directly:

```bash
python src/test_all.py --mode basic      # Test basic CDP questions
python src/test_all.py --mode comparison # Test comparison questions
python src/test_all.py --mode lytics     # Debug Lytics question
python src/test_all.py --mode custom     # Test a custom question
python src/test_all.py --mode single     # Test a single predefined question
python src/test_all.py --mode all        # Run all tests
```

The test script provides a user-friendly interface to test all aspects of the chatbot and can save test results to JSON files for further analysis.

## Production Deployment Considerations

For production deployment, consider:

1. Using a production WSGI server like Gunicorn:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -k uvicorn.workers.UvicornWorker src.api:app
   ```

2. Setting up a reverse proxy (Nginx/Apache) in front of the application
3. Implementing proper logging and monitoring
4. Setting up CI/CD pipelines for automated testing and deployment

## Non-Functional Aspects

### Security Considerations

- **Input Validation**: The application validates and sanitizes all user inputs to prevent injection attacks.
- **Rate Limiting**: Consider implementing rate limiting for the API endpoints in production.
- **HTTPS**: Always use HTTPS in production environments.
- **Environment Variables**: Sensitive configuration should be stored in environment variables, not in code.

### Performance Optimizations

- **TF-IDF Vectorization**: The chatbot uses TF-IDF vectorization for efficient document search.
- **Caching**: Document indexing results are cached to improve response times.
- **Asynchronous Processing**: The FastAPI implementation supports asynchronous request handling.
- **Efficient Text Processing**: The application uses optimized text processing algorithms to minimize response time.

### Scalability

- The application architecture separates concerns (document processing, indexing, API) to allow for independent scaling.
- The stateless nature of the API allows for horizontal scaling behind a load balancer.
- Document processing is designed to handle large volumes of documentation efficiently.

### Accessibility

- The web interface is designed with accessibility in mind, using semantic HTML and proper contrast ratios.
- Keyboard navigation is supported throughout the interface.

## Example Questions

### Basic Questions

- "How do I set up a new source in Segment?"
- "How can I create a user profile in mParticle?"
- "How do I build an audience segment in Lytics?"
- "How can I integrate my data with Zeotap?"

### Advanced Questions

- "How does Segment's audience creation process compare to Lytics'?"
- "What are the differences between mParticle and Zeotap for identity resolution?"
- "Which CDP has better data governance features, Segment or mParticle?"
- "Compare the implementation complexity of Segment vs Lytics"

## Troubleshooting

### Common Issues

1. **Documentation Fetching Fails**:
   - Check your internet connection
   - Verify that the CDP documentation URLs haven't changed
   - Try fetching documentation for each CDP individually

2. **Application Won't Start**:
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Verify that the virtual environment is activated
   - Check for port conflicts on 8000

3. **Slow Response Times**:
   - The first few queries might be slower as the TF-IDF model initializes
   - Ensure your system meets the minimum requirements

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add some amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## License

This project is for educational purposes only. 