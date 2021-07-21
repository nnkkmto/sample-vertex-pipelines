import os
import glob
import yaml
import kfp
from kfp.v2.compiler import Compiler
from kfp.v2.google.client import AIPlatformClient


PROJECT_ID = os.environ["PROJECT_ID"]
REGION = "asia-east1"
SERVICE_ACCOUNT = "your-service-account@{project_id}.iam.gserviceaccount.com"
PIPELINE_ROOT = "gs://your-bucket/pipeline_root"

# define pipeline
@kfp.dsl.pipeline(name="sample-pipeline", description="sample pipeline")
def pipeline(sentence: str):
    components_store = kfp.components.ComponentStore(local_search_paths=["component"])

    split_sentence_op = components_store.load_component('split_sentence')
    split_sentence = split_sentence_op(sentence=sentence)

    with kfp.dsl.ParallelFor(split_sentence.outputs["words"]) as word:
        print_word_op = components_store.load_component('print_word')
        print_word = print_word_op(word=word)


def override_components(project_id):
    component_files = glob.glob('component/*/component.yaml')
    for component_file in component_files:
        with open(component_file, 'r') as f:
            data = yaml.safe_load(f)
        data["implementation"]["container"]["image"] = data["implementation"]["container"]["image"].format(
            project_id=project_id)
        with open(component_file, "w") as f:
            yaml.dump(data, f)


override_components(PROJECT_ID)

# compile pipeline
Compiler().compile(
    pipeline_func=pipeline,
    package_path="pipeline.json"
)

api_client = AIPlatformClient(project_id=PROJECT_ID, region=REGION)
_ = api_client.create_run_from_job_spec(
    "pipeline.json",
    pipeline_root=PIPELINE_ROOT,
    service_account=SERVICE_ACCOUNT.format(project_id=PROJECT_ID),
    enable_caching=True,
    parameter_values={
        "sentence": "Hello Vertex Pipelines"
    }
)