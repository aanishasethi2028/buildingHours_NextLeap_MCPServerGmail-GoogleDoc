from googleapiclient.discovery import build
from auth import get_credentials


def append_to_doc(doc_id: str, content: str):
    """
    Appends text to the end of a Google Doc.
    """
    creds = get_credentials()
    service = build("docs", "v1", credentials=creds)

    # First, get the document to find out its current length
    # Alternatively, inserting at the end can be done using the `endOfSegmentLocation`.
    # Actually, we can just insert text using `endOfSegmentLocation` without fetching the document.

    requests = [
        {
            "insertText": {
                "location": {
                    "index": 1,  # Just appending to the beginning is easier, but if we want end, we need the doc length.
                },
                "text": content,
            }
        }
    ]

    # To append to the end, we need to fetch the document length
    document = service.documents().get(documentId=doc_id).execute()  # pylint: disable=no-member
    # Find the end index of the body
    content_elements = document.get("body", {}).get("content", [])
    if content_elements:
        end_index = content_elements[-1].get("endIndex") - 1
    else:
        end_index = 1

    requests = [
        {
            "insertText": {
                "location": {
                    "index": end_index,
                },
                "text": content + "\n",
            }
        }
    ]

    result = service.documents().batchUpdate(  # pylint: disable=no-member
        documentId=doc_id, body={"requests": requests}
    ).execute()

    return result
