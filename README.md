# Travel-Adviser
Travel Adviser project utilizing GPT4All, LangChain and Neo4j for intelligent vacation planning, managing and analyzing travel data to provide personalized recommendations and itineraries. This application designed to provide personalized travel recommendations using advanced AI models. The application features a robust API and an interactive user interface, leveraging machine learning techniques to enhance user experience.

## Features

- **Intelligent Travel Recommendations**: Uses large language models and similarity algorithms to suggest travel destinations.
- **Interactive UI**: A user-friendly interface for engaging with travel advice and exploring various options.
- **Scalable Architecture**: Built using containerized microservices for easy deployment and scaling.

## Project Structure

- **api/**: Contains the backend API built with Python.
  - **src/components/**: Core components for classification and result generation.
  - **src/embedding/**: Modules for different embedding techniques (e.g., OpenAI, GPT4ALL).
  - **src/llm/**: Interface for large language models.
  - **requirements.txt**: Python dependencies.
  - **Dockerfile**: Configuration for Dockerizing the API service.

- **ui/**: Contains the frontend code, built with modern JavaScript frameworks.
  - **src/chat-with-kg/**: Main components for chat functionality.
  - **Dockerfile**: Configuration for Dockerizing the frontend service.

- **downloader/**: Scripts and configuration for downloading necessary data.
  - **download_files.sh**: Shell script for data retrieval.

- **nginx/**: Configuration for the Nginx web server to route requests.

## API Documentations
For detailed API documentation and to explore the available endpoints interactively, please visit our Postman workspace: [Travel Adviser AI Assistant on Postman](https://www.postman.com/abowfzl/workspace/travel-adviser/overview). This workspace provides comprehensive examples and allows you to test the API endpoints directly, facilitating a smooth integration process.

## Getting Started

### Prerequisites

- Docker and Docker Compose installed on your machine.
- API keys and other credentials for external services (e.g., OpenAI).

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Travel-Adviser
   ```

2. **Set up environment variables**:
   - Copy `.env.example` to `.env` in the `ui` directory and fill in the necessary values.
   - Copy `.env.example` to `.env` in the root of project and fill in the necessary values.

3. **Build and run the services**:
   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   - Open your browser and go to `http://localhost` to access the project.
   - The API will be running on `http://localhost:8000`.
   - The UI will be running on `http://localhost:4173`.

### Usage

- Use the chat interface to interact with the travel adviser.
- Explore suggested travel destinations based on your input.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch.
3. Make your changes and commit them.
4. Push your changes to your fork.
5. Submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For questions or feedback, please reach out to [abowfzl@gmail.com](mailto:abowfzl@gmail.com).
