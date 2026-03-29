from pydantic import Field
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base

mcp = FastMCP("DocumentMCP", log_level="ERROR")


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}

@mcp.tool(
    name = "read_doc_contents",
    description = "Reads the contents of a document."
)
def read_doc(doc_id: str = Field(description="The ID of the document to read.")) -> str:
    """Reads a document."""
    if doc_id not in docs:
        raise ValueError(f"Document {doc_id} not found.")
    return docs[doc_id]
# TODO: Write a tool to edit a doc
@mcp.tool(
    name = "edit_doc",
    description = "Edits the contents by replacing a string in the document with content passed."
)
def edit_doc(doc_id: str = Field(description="The ID of the document to edit."), old_content: str = Field(description="The old content of the document."), new_content: str = Field(description="The new content of the document.")) -> str:
    """Edits a document."""
    if doc_id not in docs:
        raise ValueError(f"Document {doc_id} not found.")
    docs[doc_id] = docs[doc_id].replace(old_content, new_content)
    return f"Document {doc_id} has been updated."
@mcp.resource(
    "docs://documents",
    mime_type="application/json",
)
def list_docs() -> list[str]:
    """Returns a list of all document kys."""
    return list(docs.keys())
@mcp.resource(
    "docs://documents/{doc_id}",
    mime_type="plain/text",
)
def fetch_doc(doc_id: str) -> str:
    """Returns the contents of a document."""
    if doc_id not in docs:
        raise ValueError(f"Document {doc_id} not found.")
    return docs[doc_id]

@mcp.prompt(
    name="format",
    description="Formats a document."
)
def format_doc(doc_id: str=Field(description="The ID of the document to format.")) -> list[base.Message]:
    prompt = f"""
    Your goal is to reformat a document to be written with markdown syntax.

    The id of the document you need to reformat is:
    <document_id>
    {doc_id}
    </document_id>

    Add in headers, bullet points, tables, etc as necessary. Feel free to add in structure.
    Use the 'edit_document' tool to edit the document. After the document has been reformatted...
    """
    return [base.UserMessage(prompt)]
# TODO: Write a prompt to summarize a doc


if __name__ == "__main__":
    mcp.run(transport="stdio")
