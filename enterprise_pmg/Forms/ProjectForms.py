from flask_wtf import *
from flask_wtf.file import FileField, FileAllowed
from wtforms import *
from wtforms.fields.html5 import DateField
from wtforms.validators import *


class ProjectForm(Form):
    ProjectCode = StringField('Project Code:',  validators = [DataRequired()])
    ProjectStartDate = DateField('Start Date:',   validators = [DataRequired()])
    ProjectEndDate = DateField('End Date:', validators = [DataRequired()])
    Location = StringField('Location:')
    FundingSource = StringField('Funding Source:')
    TotalBudget = StringField('Total Budget:')
    Currency = StringField('Currency:', validators = [Length(max = 3)])
    Managers = StringField('Project Managers:', validators = [DataRequired()])
    StakeHolders = StringField('Stakeholders:')
    Description = TextAreaField('Description:')
    Log = TextAreaField('Project Log:')
    submit = SubmitField('Submit')