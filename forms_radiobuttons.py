from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField
from wtforms.validators import InputRequired

class NET_Difficulty_Form(FlaskForm):
    difficulty = RadioField(u'NET Architecture difficulty:'
                    ,choices=[
                        ('1', 'Basic (DV6, recommended Interface rank: 2)')
                        ,('2', 'Standard (DV8, recommended Interface rank: 4)')
                        ,('3', 'Uncommon (DV10, recommended Interface rank: 6)')
                        ,('4', 'Advanced (DV12, recommended Interface rank: 8)')
                    ]
                    ,validators=[InputRequired()]
                    ,render_kw={'class':'no_bullets'})
    # The 'no_bullets' class is used to remove the default bullet points from the radio buttons
    submit = SubmitField('Submit')