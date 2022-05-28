import pandas as pd
import numpy as np
import Levenshtein
from sklearn.manifold import MDS
import argparse


def calc_emb_from_df(haiku_df) -> np.ndarray:
    haikus = haiku_df['本文']
    D = np.array([[Levenshtein.distance(haikus[i], haikus[j]) for j in range(len(haikus))]
                  for i in range(len(haikus))])  # create distance matrix
    embedding = MDS(n_components=2, dissimilarity='precomputed')
    D_transformed = embedding.fit_transform(D)  # embed 2-dim space
    return D_transformed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--search_file', type=str)
    args = ap.parse_args()

    word = args.search_file.split('_')[-1].split('.')[0]
    haiku_df = pd.read_csv(args.search_file)
    D_transformed = calc_emb_from_df(haiku_df)
    np.save(f'embed_sample/embed_{word}.npy', D_transformed)


if __name__ == '__main__':
    main()
