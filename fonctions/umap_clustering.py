import umap
import numpy as np

reducer = umap.UMAP()
embedding = reducer.fit_transform(np.eye(100))
print(np.eye(100).shape)
print(embedding.shape)