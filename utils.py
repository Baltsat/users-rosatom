# Reduce dimensionality using PCA
from sklearn.decomposition import PCA


# Function to return the principal components
def get_pc(arr, n):
    pca = PCA(n_components=n)
    embeds_transform = pca.fit_transform(arr)
    return embeds_transform
