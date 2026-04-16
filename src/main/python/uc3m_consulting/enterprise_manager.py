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
        cif = True
        return cif

    def _is_valid_md5(self, s: str) -> bool:
        """Determines whether a string is a valid md5"""
        return isinstance(s, str) and bool(re.fullmatch(r"[a-fA-F0-9]{32}", s))

    def register_document(self, input_file: str):
        """Registers documents when valid inputs are passed"""
        # Load the file
        try:
            with open(input_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as exc:
            raise EnterpriseManagementException("The file is not JSON formatted.") from exc
        try:
            project_id = data["PROJECT_ID"]
            filename = data["FILENAME"]
        except Exception as exc:
            error_string = "JSON does not have the expected structure."
            raise EnterpriseManagementException(error_string) from exc

        if not self._is_valid_md5(project_id):
            raise EnterpriseManagementException("JSON has invalid values")
        if not re.fullmatch(r"[a-zA-Z0-9]{8}\.(pdf|docx|xlsx)", filename):
            raise EnterpriseManagementException("JSON has invalid values")
        # Create the document object and get the signature
        my_doc = ProjectDocument(project_id, filename)
        signature = my_doc.document_signature

        # Save to all_documents.json
        storage_file = "./output/all_documents.json"
        all_docs = []

        try:
            with open(storage_file, "r", encoding="utf-8") as f:
                all_docs = json.load(f)
        except FileNotFoundError:
            all_docs = []  # file doesn't exist yet → start fresh
        except json.JSONDecodeError as exc:
            raise EnterpriseManagementException("The file is not JSON formatted.") from exc

        all_docs.append(my_doc.to_json())

        try:
            with open(storage_file, "w", encoding="utf-8") as f:
                json.dump(all_docs, f, indent=4)
        except Exception as exc:
            raise EnterpriseManagementException("2 The file is not JSON formatted.") from exc

        return signature
