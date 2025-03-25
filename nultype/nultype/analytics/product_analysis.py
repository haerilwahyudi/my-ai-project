import pandas as pd
from sklearn.decomposition import PCA
from typing import Tuple

class ProductAnalyzer:
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.pca = PCA(n_components=2)
        
    def analyze_sales_trends(self) -> Tuple[pd.DataFrame, dict]:
        """Analyze product sales trends with seasonality detection"""
        trends = (
            self.data
            .groupby('product_category')
            .agg({
                'sales': ['mean', 'std'],
                'price': 'median'
            })
        )
        
        pca_features = self.pca.fit_transform(
            self.data[['sales', 'price', 'rating']]
        )
        
        return trends, {
            'pca_explained_variance': self.pca.explained_variance_ratio_,
            'pca_components': self.pca.components_
        }
