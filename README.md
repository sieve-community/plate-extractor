# Licens Plate Extraction 

Deployed on Sieve at `developer-sievedata-com/plate-extractor`. You can also deploy it yourself using `sieve model` inside this repo's directory.

### Create a workflow using this model

`pip install https://storage.googleapis.com/sieve-client-package/sievedata-0.0.1.3-py3-none-any.whl`

#### Python
```Python
from sieve.api.client import SieveClient, SieveProject
from sieve.types.api import *
cli = SieveClient()

proj = SieveProject(
    name="plate_extractor_project",
    fps=5,
    store_data=True,
    workflow=SieveWorkflow([
        SieveLayer(
            iteration_type=SieveLayerIterationType.video,
            models=[
                SieveModel(
                    name="developer-sievedata-com/plate-extractor",
                )
            ]
        )
    ])
)
proj.create()
```

#### YAML
```
# workflow.yaml
fps: 5
store_data: true
layers:
- iteration: "video"
  models: 
  - model_name: developer-sievedata-com/plate-extractor
```
`sieve projects my_plate_extractor create -wf workflow.yaml`