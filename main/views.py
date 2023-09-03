from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
import chromadb


def home(request):
    chroma_client = chromadb.Client()

    collection = chroma_client.create_collection(name="my_collection")

    collection.add(
        documents=["This is a document", "This is another document"],
        metadatas=[{"source": "my_source"}, {"source": "my_source"}],
        ids=["id1", "id2"]
    )

    results = collection.query(
        query_texts=["This is a query document"],
        n_results=2
    )

    print(results)
    return HttpResponse("hello world i love you")
