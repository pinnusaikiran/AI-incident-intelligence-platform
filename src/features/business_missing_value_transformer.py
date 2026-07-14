from sklearn.base import BaseEstimator, TransformerMixin

class BusinessMissingValueTransformer(BaseEstimator, TransformerMixin):

    def __init__(self):
        self.replacement = {
            'location': 'Unknown_location',
            'category': 'Unknown_category',
            'subcategory': 'Unknown_subcategory',
            'u_symptom': 'Unknown_symptom',
            'assignment_group': 'Unknown_assignment_group',
            'assigned_to': 'Unknown_assigned_to',
            'caller_id': 'Unknown_caller_id',
            'opened_by': 'Unknown_opened_by'
        }

        self.missing_tokens = ['?', 'NA', 'N/A', None]

    def fit(self, X, y=None):

        missing_cols = []

        for col in self.replacement.keys():
            if col not in X.columns:
                missing_cols.append(col)

        if missing_cols:
            raise ValueError(
                f"Required missing columns are: {missing_cols}"
            )

        return self

    def transform(self, X):

        X_copy = X.copy()

        for col, replacement_value in self.replacement.items():

            X_copy[col] = X_copy[col].replace(
                self.missing_tokens,
                replacement_value
            )

        return X_copy