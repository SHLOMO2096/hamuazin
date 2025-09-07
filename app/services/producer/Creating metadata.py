import pathlib



def create_metadata_file(file_path: str, metadata: dict) -> None:
    """Create a metadata file for a given file path."""
    metadata_file = pathlib.Path(file_path).with_suffix(".meta.json")
    with metadata_file.open("w") as f:
        json.dump(metadata, f)