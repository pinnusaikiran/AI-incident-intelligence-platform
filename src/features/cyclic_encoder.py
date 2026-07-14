import calendar
import numpy as np
import pandas as pd
from pandas.api.types import is_object_dtype, is_string_dtype
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import check_is_fitted

class CyclicEncoder(BaseEstimator, TransformerMixin):
    """
    Parameters
    ----------
        cyclic_columns : dict, default=None
            Dictionary mapping cyclic feature names to their cycle lengths.

        drop_original : bool, default=True
            Whether to remove the original cyclic columns after encoding.

    Attributes
    ----------
        month_mapping : dict
        day_mapping : dict
        n_features_in_ : int
    """
    def __init__(self,cyclic_columns=None,drop_original=True):
        if cyclic_columns is None:
            self.cyclic_columns={
                'Hour':24,
                'Day_of_week':7,
                'Month':12
            }
        else:
            self.cyclic_columns=cyclic_columns

        self.drop_original=drop_original
        self.month_mapping={
            month:idx for idx,month in enumerate(calendar.month_name) if month
            }
        self.day_mapping={ 
            day:idx for idx,day in enumerate(calendar.day_name) if day
            }
        
        self.category_mappings = {
            "Month": self.month_mapping,
            "Day_of_week": self.day_mapping
        }
        
    
    def _validate_input(self,X):
        if not isinstance(X,pd.DataFrame):
            raise TypeError(f"Expected the pandas Dataframe to be, but got: {type(X).__name__} ")
    
    def _validate_columns(self,X):
        missing_columns=[col for col in self.cyclic_columns if col not in X.columns]
        if missing_columns:    
            raise ValueError(f"Required missing columns are: {missing_columns}") 

    def fit(self,X,y=None):
        self._validate_input(X)
        self._validate_columns(X)
        self.n_features_in_ = X.shape[1]
        return self

    def transform(self,X):
        self._validate_input(X)
        self._validate_columns(X)
        check_is_fitted(self, "n_features_in_")
        X_transformed=X.copy()

        for col, mapping in self.category_mappings.items():
            if col in self.cyclic_columns:
                if is_object_dtype(X_transformed[col]) or is_string_dtype(X_transformed[col]):
                    X_transformed[col] = X_transformed[col].map(mapping)

        for col,period in self.cyclic_columns.items():
                        
            numeric_values = pd.to_numeric(X_transformed[col],errors='raise')

            X_transformed[f'{col}_sin']=np.sin((2*np.pi*numeric_values)/period)
            X_transformed[f'{col}_cos']=np.cos((2*np.pi*numeric_values)/period)
            
        if self.drop_original:
            X_transformed=X_transformed.drop(columns=list(self.cyclic_columns.keys()),errors='ignore')

        return X_transformed
        
        
        