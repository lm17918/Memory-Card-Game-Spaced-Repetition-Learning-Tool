# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull the llama3.2 model
ollama pull llama3.2

# Install Python requirements
pip install -r requirements.txt

pre-commit install