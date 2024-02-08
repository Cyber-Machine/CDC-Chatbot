# CDC-Chatbot

A sample chatbot showcasing RAG pipeline on CDC dataset.
![Interface](https://github.com/Cyber-Machine/CDC-Chatbot/assets/60005585/7588cae2-5275-47c4-ab12-eb7672cf4998)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Docker
- Docker Compose
- Poetry (Python dependency manager)

### Installation

1. Clone the repository

   ```bash
   git clone https://github.com/Cyber-Machine/CDC-Chatbot.git
   ```

2. Navigate to the project directory

   ```bash
   cd CDC-Chatbot
   ```

3. Export `TRUEFOUNDRY_API_KEY` to your environment variables.
   Find your API key by following [this](https://docs.truefoundry.com/docs/llm-gateway).

   ```bash
   export TRUEFOUNDRY_API_KEY=<YOUR_API_KEY>
   ```

   > **Note**: Add Truefoundry API Key in `cdc_bot` ENVIRONMENT variable, if you are planning to use docker-compose.

4. Install the project dependencies using Poetry

   ```bash
   pip install poetry
   poetry install
   ```

> [!NOTE]
> Make sure to run chromadb server at `localhost:8000`

**OR**

Start the application using Docker Compose

```bash
docker compose up
```

## Examples and Experimentations

Also checkout answers from RAG bot [here](EXAMPLES.md).
and few experimentations done [here](EXPERIMENTS.md).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
