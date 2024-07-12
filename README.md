
# Civitai API Wrapper

A Python wrapper for the Civitai REST API, providing easy access to models, images, creators, tags, and more.

## Features

- List and search models with various filters
- Retrieve detailed information about specific models
- List and search images waith various filters
- List and search creators
- List and search tags
- Retrieve specific model versions

## Installation

Clone this repo and install the required dependencies using `pip`:

```bash
pip install -r requirements.txt
```

## Usage

### Initialization

Import what you need and initialize the `Civitai` client with your API key:

```python
from civitai_api import Civitai
from civitai_api.models import BaseModel, ModelType
from civitai_api.api.models import ModelSort, ModelPeriod

civitai = Civitai(api_key="nice try, fed")
```

### Listing Models

List models with various filters:

```python
#get top 5 loras created by RalFinger this year for sd15 with 'style' in the name
models = civitai.models.list_models(
        types=[ModelType.LORA],
        sort=ModelSort.HIGHEST_RATED,
        username='RalFinger',
        base_models=[BaseModel.SD_1_5, BaseModel.SD_1_5_LCM],
        query='style',
        page=1,
        period=ModelPeriod.YEAR,
        limit=5
    )

print("models:")
for model in models:
    print(model.name)
```


### Getting Model Details

Retrieve detailed information about a specific model:

```python
model = civitai.models.get_model(model_id=1102)
print(model.nsfw)
```

### Getting Images, Creators, ModelVersions, Tags

Retrieve information about images

```python
#get 4 images related to model 1102
images = civitai.images.list_images(model_id=1102, limit=4)
print("images:")
for image in images:
    print(image.url)

#get a model version
version = civitai.model_versions.get_model_version(version_id=1302)
print(version.name)

#query creators
creators = civitai.creators.list_creators(query='RalFinger')
for creator in creators:
    print(creator.modelCount)

#query tags
tags = civitai.tags.list_tags(query='celebrity')
for tag in tags:
    print(tag.name, tag.modelCount)
```
## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
