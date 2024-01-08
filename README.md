# Py-TwelveLabs
Copyright © 2024 Minura Punchihewa

Py-TwelveLabs is a Python library for interacting with the TwelveLabs API.

## Installation
### With pip
```bash
pip install py_twelvelabs
```

## Usage

First, sign up for a TwelveLabs account [here](https://playground.twelvelabs.io/signup) and get your API key.

The API key can either be passed to the constructor directly or through the environment variable `TWELVE_LABS_API_KEY` like so:
```bash
export TWELVE_LABS_API_KEY=tlk_...
```

Then, import the library and create a client object:
```python
from py_twelvelabs import TwelveLabsAPIClient

client = TwelveLabsAPIClient()
# OR
client = TwelveLabsAPIClient(api_key='tlk_...')
```

### Indexes

#### Create an Index
```python
index_id = client.index.create(
    index_name='my_index',
    index_options=["visual", "conversation", "text_in_video", "logo"]
)
```

#### Get an Index
```python
index = client.index.get(index_id)
```

`index` will be an instance of the `Index` class.

#### List Indexes
```python
indexes = client.index.list()
```

`indexes` will be a list of `Index` objects.

#### Update an Index
```python
client.index.update(
    index_id=index_id,
    index_name='my_index_updated'
)
```

#### Delete an Index
```python
client.index.delete(index_id)
```

### Tasks

#### Create a Video Indexing Task
Create a task asynchronously:
```python
task_id = client.task.create_async(
    index_id=index_id,
    video_file='path/to/my/video.mp4'
)
```

`task_id` will be a string representing the ID of the task.

Create a task synchronously:
```python
task = client.task.create_sync(
    index_id=index_id,
    video_file='path/to/my/video.mp4'
)
```

`task` will be an instance of the `Task` class.

#### Get a Video Indexing Task
```python
task = client.task.get(task_id)
```

`task` will be an instance of the `Task` class.

#### List Video Indexing Tasks
```python
tasks = client.task.list()
```

`tasks` will be a list of `Task` objects.

#### Delete a Video Indexing Task
```python
client.task.delete(task_id)
```

### Search

#### Run a Search Query
```python
results = client.search.query(
    index_id=index_id,
    query='my search query',
    search_options=["visual", "conversation", "text_in_video", "logo"]
)
```