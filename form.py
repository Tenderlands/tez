from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, SubmitField, FloatField
from wtforms.validators import DataRequired, Length, NumberRange
from processLibrary import getDict, processChoices


class NonValidatingSelectField(SelectField):
    def pre_validate(self, form):
        pass


class VolumeField(FloatField):
    def process_formdata(self, valuelist):
        if valuelist:
            try:
                self.data = float(valuelist[0].replace(',', '.'))
            except ValueError:
                self.data = None
                raise ValueError(self.gettext('Not a valid float value'))

    def pre_validate(self, form):
        if self.data < 7:
            self.data *= 1000
            FloatField.pre_validate(self, form)


class PredictionForm(FlaskForm):
    Dict = getDict()
    markaList = []
    for marka in Dict['Marka']:
        markaList.append(marka)
    Marka = SelectField(u'Marka', choices=processChoices(markaList),default="", validators=[DataRequired()],render_kw={"onchange":"this.form.set_seri()"})
    Seri = NonValidatingSelectField(u'Seri', choices=[], coerce=str, render_kw={'disabled': 'disabled'})
    Model = NonValidatingSelectField(u'Model', choices=[], coerce=str, render_kw={'disabled': 'disabled'})
    Yil = IntegerField(u'Yıl', validators=[DataRequired(),NumberRange(min=1974, max=2020)])
    Yakit = SelectField(u'Yakıt', choices=processChoices(Dict['Yakıt']), validators=[DataRequired()])
    Vites =SelectField(u'Vites', choices=processChoices(Dict['Vites']), validators=[DataRequired()])
    KM = IntegerField(u'KM', validators=[DataRequired()])
    Kasa_Tipi = SelectField(u'Kasa Tipi', choices=processChoices(Dict['Kasa_Tipi']), validators=[DataRequired()])
    Motor_Gucu = IntegerField(u'Motor Gücü', validators=[DataRequired()])
    Motor_Hacmi = VolumeField(u'Motor Hacmi', validators=[DataRequired()])
    Renk = SelectField(u'Renk', choices=processChoices(Dict['Renk']), validators=[DataRequired()])
    Kimden = SelectField(u'Kimden', choices=processChoices(Dict['Kimden']), validators=[DataRequired()])
    Submit = SubmitField('Predict')
