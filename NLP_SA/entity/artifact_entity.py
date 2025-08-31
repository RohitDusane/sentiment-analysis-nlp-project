

# -----------DATA INGESTION ARTIFACT -----------
from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    trained_file_path: str
    val_file_path: str  # this is actually validation file
    final_test_file_path: str  # NEW: true test set from original test.csv
    is_ingested: bool
    message: str
