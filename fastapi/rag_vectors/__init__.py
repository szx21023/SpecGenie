async def init_app(app):
    # services/embedding.py
    from typing import List

    class EmbeddingClient:
        """
        傳入你現有的 openai client（如 app.state.openai_client）
        """
        def __init__(self, client, model: str = "text-embedding-3-small"):
            self.client = client
            self.model = model

        def embed_one(self, text: str) -> List[float]:
            resp = self.client.embeddings.create(
                model=self.model,
                input=[text]
            )
            return resp.data[0].embedding

        def embed_batch(self, texts: List[str]) -> List[List[float]]:
            resp = self.client.embeddings.create(
                model=self.model,
                input=texts
            )
            return [d.embedding for d in resp.data]

    app.state.embedding_client = EmbeddingClient(app.state.openai_client)

