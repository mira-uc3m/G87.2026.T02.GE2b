"""Module """
import json
import os
import re
from . import ProjectDocument
from .enterprise_management_exception import EnterpriseManagementException

class EnterpriseManager:
    """Class for providing the methods for managing the orders"""
    def __init__(self):
        pass

    @staticmethod
    def validate_cif(cif: str):
        """RETURNs TRUE IF THE IBAN RECEIVED IS VALID SPANISH IBAN,
        OR FALSE IN OTHER CASE"""
        return True

    def is_valid_md5(self, s: str) -> bool:
        return isinstance(s, str) and bool(re.fullmatch(r"[a-fA-F0-9]{32}", s))

    def register_document(self, input_file: str):
        # Load the file
        try:
            with open(input_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            raise EnterpriseManagementException("The file is not JSON formatted.")
        try:
            project_id = data["PROJECT_ID"]
            filename = data["FILENAME"]
        except Exception:
            raise EnterpriseManagementException("JSON does not have the expected structure.")

        if not self.is_valid_md5(project_id):
            raise EnterpriseManagementException("JSON has invalid values")
        if not re.fullmatch(r"[a-zA-Z0-9]{8}\.(pdf|docx|xlsx)", filename):
            raise EnterpriseManagementException("JSON has invalid values")
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