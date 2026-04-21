import pandas as pd
import os

class DataCleaner:
    def __init__(self,file_path,missing = 'drop',duplicates = True,show_log = False,show_corr = True):
        self.file_path = file_path
        self.missing = missing
        self.duplicates = duplicates
        self.show_log = show_log
        self.show_corr = show_corr

    def _log(self, message):
        if self.show_log:
            print(f'[DataCleaner INFO]: {message}')

    def load_data(self):

        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f'File not found: {self.file_path}')


        self._log(f'Loading Data from {self.file_path}')

            # redaing data of different files
        if self.file_path.endswith('.csv'):
            df = pd.read_csv(self.file_path)
        elif self.file_path.endswith('.xlsx'):
            df =  pd.read_excel(self.file_path)
        elif self.file_path.endswith('.json'):
            df = pd.read_json(self.file_path)
        else:
            raise ValueError('Unsupported file format. Please provide a CSV, Excel, or JSON file.')
        
        self._log(f'Data loaded sucessfully with shape {df.shape}')

        return df
    
    def remove_duplicates(self,df):
        if self.duplicates:
            before = df.shape[0]
            df = df.drop_duplicates()
            after = df.shape[0]

            self._log(f'Removed {before - after} duplicate rows')
            self._log(f'Current data shape: {df.shape}')
        else:
            self._log('Duplicates removal skipped')

        return df
    
    def handle_missing_values(self, df):
        self._log(f'Handling missing values using: {self.missing}')
        if self.missing == 'drop':
            df = df.dropna()
        elif self.missing == 'mean':
            df =  df.fillna(df.select_dtypes(include = ['number']).mean())
        elif self.missing == 'median':
            df = df.fillna(df.select_dtypes(include  = ['number']).median())
        else:
            raise ValueError("Invalid missing value")
        
        return df

    def show_correlation(self,df):
        if not self.show_corr :
            return 
        corr_matrix = df.corr(numeric_only = True)
        print("\nCorrelation Matrix\n")
        print(corr_matrix.round(2))
        return

    def clean(self):

        try:
            df = self.load_data()
            df = self.remove_duplicates(df)
            df = self.handle_missing_values(df)
            self.show_correlation(df)
            self._log('Cleaning complete')

            return df
        except Exception as e:
            self._log(f'[Error]: {e}')
            return None 