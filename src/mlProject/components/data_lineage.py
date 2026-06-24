import os
import json
from datetime import datetime

class DataLineageEngine:
    def __init__(self, lineage_path="artifacts/data_lineage.json"):
        self.lineage_path = lineage_path
        self._init_lineage()

    def _init_lineage(self):
        if not os.path.exists(self.lineage_path):
            os.makedirs(os.path.dirname(self.lineage_path), exist_ok=True)
            initial_data = {
                "nodes": [
                    {"id": "kaggle_red_wine_csv", "label": "Kaggle Raw Wine Source", "type": "Datasource"},
                    {"id": "artifacts_data_ingestion", "label": "Ingested Raw CSV", "type": "Artifact"},
                    {"id": "train_csv", "label": "Transformation Split: Train Data", "type": "Dataset"},
                    {"id": "test_csv", "label": "Transformation Split: Test Data", "type": "Dataset"},
                    {"id": "model_trainer_run", "label": "Model Trainer Pipeline Run", "type": "Execution"},
                    {"id": "model_joblib", "label": "Active Production Model", "type": "Model"}
                ],
                "links": [
                    {"source": "kaggle_red_wine_csv", "target": "artifacts_data_ingestion", "label": "ingested_by"},
                    {"source": "artifacts_data_ingestion", "target": "train_csv", "label": "splitted_to"},
                    {"source": "artifacts_data_ingestion", "target": "test_csv", "label": "splitted_to"},
                    {"source": "train_csv", "target": "model_trainer_run", "label": "fed_into"},
                    {"source": "model_trainer_run", "target": "model_joblib", "label": "generated"}
                ]
            }
            with open(self.lineage_path, "w") as f:
                json.dump(initial_data, f, indent=2)

    def get_lineage_graph(self) -> dict:
        try:
            with open(self.lineage_path, "r") as f:
                return json.load(f)
        except Exception:
            return {"nodes": [], "links": []}

    def record_derivation(self, parent_id: str, child_id: str, label: str) -> bool:
        try:
            graph = self.get_lineage_graph()
            # Ensure nodes exist
            node_ids = [n["id"] for n in graph.get("nodes", [])]
            if parent_id not in node_ids:
                graph["nodes"].append({"id": parent_id, "label": parent_id, "type": "Dataset"})
            if child_id not in node_ids:
                graph["nodes"].append({"id": child_id, "label": child_id, "type": "Dataset"})
                
            graph["links"].append({
                "source": parent_id,
                "target": child_id,
                "label": label,
                "recorded_at": datetime.utcnow().isoformat()
            })
            with open(self.lineage_path, "w") as f:
                json.dump(graph, f, indent=2)
            return True
        except Exception:
            return False
