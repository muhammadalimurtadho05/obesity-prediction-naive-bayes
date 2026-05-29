from django.shortcuts import render, redirect
from classifier.tes_data import tes

def halaman_utama(request):
    return render(request, 'index.html', {'nama': 'Django'})

def test(request):
    return render(request, 'test.html', {'nama': 'Django'})

def hasil(request):
    if request.method == "POST":
        test_raw = {
            "Gender": request.POST.get('gender'),
            "Age": float(request.POST.get('age')),
            "Height":float(request.POST.get('height')),
            "Weight": float(request.POST.get('weight')),
            "family_history_with_overweight": request.POST.get('family_history_with_overweight'),
            "FAVC": request.POST.get('favc'),
            "FCVC": float(request.POST.get('fcvc')),
            "NCP": float(request.POST.get('ncp')),
            "CAEC": request.POST.get('caec'),
            "SMOKE": request.POST.get('smoke'),
            "CH2O": float(request.POST.get('ch2o')),
            "SCC": request.POST.get('scc'),
            "FAF": float(request.POST.get('faf')),
            "TUE": float(request.POST.get('tue')),
            "CALC": request.POST.get('calc'),
            "MTRANS": request.POST.get('mtrans')
        }
        prediksi, proba = tes(test_raw)
        return render(request, 'hasil.html', {'prediksi': prediksi, 'proba' : proba, 'sample_raw': test_raw})
    else:
        return redirect('/test')
    
    
