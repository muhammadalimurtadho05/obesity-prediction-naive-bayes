import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score
)
import warnings
warnings.filterwarnings("ignore")

class bayes_model:
    def __init__(self):
        FILE_PATH = 'classifier/dataset/obesitas.xlsx'
        self.df = pd.read_excel(FILE_PATH)
        
    def labelEncoding(self):
        categorical_cols = [
            "Gender", "family_history_with_overweight", "FAVC",
            "CAEC", "SMOKE", "SCC", "CALC", "MTRANS"
        ]
        
        label_encoders = {}
        df_encoded = self.df.copy()
        for col in categorical_cols:
            le = LabelEncoder()
            df_encoded[col] = le.fit_transform(df_encoded[col].astype(str))
            label_encoders[col] = le
            # print(f"Encoding '{col}': {dict(zip(le.classes_, le.transform(le.classes_)))}")
        
        return label_encoders, df_encoded
    
    def training(self):
        TARGET_COL = "NObeyesdad"
        label_encoders, df_encoded = self.labelEncoding()
        X_train = df_encoded.drop(columns=[TARGET_COL])
        y_train_raw = df_encoded[TARGET_COL]
        le_target = LabelEncoder()
        y_train = le_target.fit_transform(y_train_raw)
        model = GaussianNB()
        model.fit(X_train, y_train)
        # print(f"Model dilatih dengan {X_train.shape[0]} data training.")
        
        return X_train, le_target, model
    
    def testing(self, sample_raw):
        
        label_encoders, df_encoded = self.labelEncoding()
        X_train, le_target, model = self.training()

        sample_encoded = {}
        for col, val in sample_raw.items():
            if col in label_encoders:
                sample_encoded[col] = label_encoders[col].transform([str(val)])[0]
            else:
                sample_encoded[col] = val

        sample_df = pd.DataFrame([sample_encoded])
        sample_df = sample_df[X_train.columns]   # pastikan urutan kolom sama

        # Prediksi
        prediksi_kode  = model.predict(sample_df)[0]
        prediksi_label = le_target.inverse_transform([prediksi_kode])[0]
        probabilitas   = model.predict_proba(sample_df)[0]

        # print("\nData Input:")
        # for k, v in sample_raw.items():
        #     print(f"  {k:<35}: {v}")

        # print(f"\nHasil Prediksi  : {prediksi_label}")
        # print("\nProbabilitas per kelas:")
        proba = {}
        for kelas, prob in zip(le_target.classes_, probabilitas):
            proba[kelas] = prob 
            # bar = "█" * int(prob * 40)
            # print(f"  {kelas:<15}: {prob * 100:6.2f}%  {bar}")
        
        # print(zip(le_target.classes_, probabilitas))
        return prediksi_label, proba
    
    def datasetsInfo(self):
        print("INFORMASI DATASET")
        print(f"Jumlah baris   : {self.df.shape[0]}")
        print(f"Jumlah kolom   : {self.df.shape[1]}")
        print(f"\nKolom-kolom    :\n{self.df.columns.tolist()}")
        print(f"\nDistribusi label (NObeyesdad):\n{self.df['NObeyesdad'].value_counts()}")
        print(f"\nCuplikan data:\n{self.df.head(3)}\n")
