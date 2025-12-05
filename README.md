# Keyoku Python SDK

The official Python SDK for [Keyoku](https://keyoku.dev) - AI Memory Infrastructure.

## Installation

```bash
pip install keyoku
```

With framework integrations:

```bash
pip install keyoku[langchain]    # LangChain support
pip install keyoku[llamaindex]   # LlamaIndex support
pip install keyoku[crewai]       # CrewAI support
pip install keyoku[all]          # All integrations
```

## Quick Start

```python
from keyoku import Keyoku

# Initialize the client
client = Keyoku(api_key="your-api-key")

# Store a memory
job = client.remember("User prefers dark mode and uses VS Code")
job.wait()  # Wait for processing

# Search memories
memories = client.search("What editor does the user prefer?")
for memory in memories:
    print(f"{memory.content} (score: {memory.score:.2f})")
```

## Async Support

```python
from keyoku import AsyncKeyoku

async with AsyncKeyoku(api_key="your-api-key") as client:
    job = await client.remember("User likes Python")
    await job.wait()

    memories = await client.search("programming languages")
```

## Framework Integrations

### LangChain

```python
from keyoku.integrations.langchain import KeyokuMemory
from langchain.chains import ConversationChain
from langchain_openai import ChatOpenAI

memory = KeyokuMemory(api_key="your-api-key")

chain = ConversationChain(
    llm=ChatOpenAI(),
    memory=memory,
)
```

### LlamaIndex

```python
from keyoku.integrations.llamaindex import KeyokuVectorStore

vector_store = KeyokuVectorStore(api_key="your-api-key")
retriever = vector_store.as_retriever(similarity_top_k=5)
```

### CrewAI

```python
from keyoku.integrations.crewai import KeyokuCrewMemory
from crewai import Crew

memory = KeyokuCrewMemory(api_key="your-api-key")
crew = Crew(agents=[...], memory=memory)
```

## API Reference

### Memories

```python
# Store a memory
client.remember(content, session_id=None, agent_id=None)

# Search memories
client.search(query, limit=10, mode="hybrid", agent_id=None)

# List memories
client.memories.list(limit=50, offset=0)

# Get a memory
client.memories.get(memory_id)

# Delete a memory
client.memories.delete(memory_id)

# Delete all memories
client.memories.delete_all()

# Batch operations
client.memories.batch_create(contents)
client.memories.batch_delete(memory_ids)
```

### Knowledge Graph

```python
# Entities
client.entities.list()
client.entities.search(query)
client.entities.get(entity_id)
client.entities.relationships(entity_id)

# Relationships
client.relationships.list()
client.relationships.get(relationship_id)

# Graph traversal
client.graph.find_path(from_entity, to_entity, max_depth=5)
```

### Schemas

```python
client.schemas.list()
client.schemas.get(schema_id)
client.schemas.create(name, schema)
client.schemas.update(schema_id, name=None, schema=None)
client.schemas.delete(schema_id)
```

## Configuration

```python
client = Keyoku(
    api_key="your-api-key",
    base_url="https://api.keyoku.dev",  # Custom API URL
    timeout=30.0,                        # Request timeout
    entity_id="user-123",               # Multi-tenant isolation
)
```

## License

MIT
