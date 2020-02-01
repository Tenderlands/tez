from prediction import regressor, dictionary
from flask import Flask, render_template, url_for, flash, redirect, jsonify
from form import PredictionForm
from processLibrary import *

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'


@app.route("/", methods=['GET', 'POST'])
def home():
    form = PredictionForm()
    if form.validate_on_submit():
        prd = int(regressor.predict(
            SampleTranslator(form.Marka.data, form.Seri.data, form.Model.data, form.Yil.data, form.Yakit.data,
                             form.Vites.data, form.KM.data, form.Kasa_Tipi.data, form.Motor_Gucu.data,
                             form.Motor_Hacmi.data, form.Renk.data, form.Kimden.data, dictionary))[0])
        flash(
            f'Prediction for {form.Marka.data} {form.Seri.data} {form.Model.data} {form.Yil.data}, {form.Yakit.data}, \
                {form.Vites.data} vites, {form.KM.data} KM, {form.Kasa_Tipi.data}, {form.Motor_Gucu.data} HP, \
                {int(form.Motor_Hacmi.data)} cc, {form.Renk.data}, {form.Kimden.data} : \n\n{prd} TL', 'success')
        return redirect(url_for('home'))
    else:
        flash_errors(form)
    if(form.Marka.data != ""):
        seriList = []
        for seri in getDict()['Marka'][form.Marka.data]:
            seriList.append(seri)
        form.Seri.choices = processChoices(seriList)
        form.Seri.render_kw = {}
        if(form.Seri.data != ""):
            modelList = []
            for model in getDict()['Marka'][form.Marka.data][form.Seri.data]:
                modelList.append(model)
            form.Model.choices = processChoices(modelList)
            form.Model.render_kw = {}
    return render_template('index.html', form=form)


@app.route("/marka=<marka>")
def fill_seri(marka):
    seriDict = getDict()['Marka'][marka]
    seriList = [{"label": "Seçiniz", "value": ""}]
    for seri in seriDict:
        seriObj = {"label": seri, "value": seri}
        seriList.append(seriObj)
    return jsonify({"seriler": seriList})


@app.route("/marka=<marka>&seri=<seri>")
def fill_model(marka, seri):
    modelDict = getDict()['Marka'][marka][seri]
    modelList = [{"label": "Seçiniz", "value": ""}]
    for model in modelDict:
        modelObj = {"label": model, "value": model}
        modelList.append(modelObj)
    return jsonify({"modeller": modelList})


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'warning')

if __name__ == '__main__':
    app.run(debug=True)
