"""Module """
import json
import os
from . import ProjectDocument

class EnterpriseManager:
    """Class for providing the methods for managing the orders"""
    def __init__(self):
        pass

    @staticmethod
    def validate_cif(cif: str):
        """RETURNs TRUE IF THE IBAN RECEIVED IS VALID SPANISH IBAN,
        OR FALSE IN OTHER CASE"""
        return True

    def register_document(self, input_file: str):
        # Load the file
        with open(input_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        project_id = data["PROJECT_ID"]
        filename = data["FILENAME"]

        # Create the document object and get the signature
        my_doc = ProjectDocument(project_id, filename)
        signature = my_doc.document_signature

        # Save to all_documents.json
        storage_file = "all_documents.json"
        all_docs = []
        if os.path.exists(storage_file):
            with open(storage_file, "r") as f:
                all_docs = json.load(f)

        all_docs.append(my_doc.to_json())

        with open(storage_file, "w") as f:
            json.dump(all_docs, f, indent=4)

        return signature