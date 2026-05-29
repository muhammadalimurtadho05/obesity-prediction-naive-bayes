from classifier.bayes_model import bayes_model

def tes(data):
    m_bayes_model = bayes_model()
    prediksi, proba = m_bayes_model.testing(data)
    return prediksi, proba
        