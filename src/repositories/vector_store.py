import faiss
import numpy as np


class VectorStore:
    def __init__(self, dimension: int):
        self.index = faiss.IndexFlatL2(dimension)
        self.metadata = []

    def add(self, vectors, metadata):
        self.index.add(np.array(vectors).astype("float32"))
        self.metadata.extend(metadata)

    def search(self, query_vector, k=5):
        distances, indices = self.index.search(
            np.array([query_vector]).astype("float32"), k
        )

        results = []
        for idx in indices[0]:
            if idx < len(self.metadata):
                results.append(self.metadata[idx])

        return results