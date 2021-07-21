import json
import fire
from gcsfs import GCSFileSystem

def main(sentence: str, words_output_path):
    words = sentence.split()

    fs = GCSFileSystem()
    words_output_path = words_output_path.replace("/gcs/", "gs://")
    with fs.open(words_output_path, "w") as f:
        json.dump(words, f)

if __name__ == "__main__":
    fire.Fire(main)
