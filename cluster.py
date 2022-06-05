from tkinter import N
import hdbscan

from sklearn.cluster import AgglomerativeClustering


def pick_clusterer():
    pass


def tune_clusterers(df):
    pass


def fit_clusterers(df, target_cluster_min, target_cluster_max, min_cluster_size=20):
    out_df, clusterer = _fit_and_label_hdbscan_clusters(df, min_cluster_size=min_cluster_size)

    n_clusters = len(out_df) // target_cluster_max
    print(f"n_clusters: {n_clusters}")
    out_df, agg = _fit_and_label_agglomerative_clusters(out_df, n_clusters=n_clusters)

    return out_df, clusterer, agg


def _fit_and_label_hdbscan_clusters(df, min_cluster_size):
    out_df = df
    
    clusterer = hdbscan.HDBSCAN(min_cluster_size=min_cluster_size)

    clusterer.fit(df[['lat', 'lng']])

    out_df = out_df.assign(
        _hdbscan_cluster_id = clusterer.labels_
    )

    return out_df, clusterer


def _fit_and_label_agglomerative_clusters(df, n_clusters):
    agg = AgglomerativeClustering(n_clusters=n_clusters)
    X = df[['lat', 'lng']]

    out_df = df.copy()

    out_df = out_df.assign(
        _agg_cluster_id = agg.fit_predict(X)
    )

    return out_df, agg