from flask_wtf import *
from flask_wtf.file import FileField, FileAllowed
from wtforms import *
from wtforms.fields.html5 import DateField
from wtforms.validators import *


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=True)
    option_widget = widgets.CheckboxInput()

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

class TaskForm(Form):
    TaskPriority = StringField('Priority: ')
    TaskDescription = StringField('Description: ', validators = [DataRequired()])
    ExpectedStartDate = DateField('Expected Start Date: ')
    ExpectedEndDate = DateField('Expected End Date: ')
    ActualStartDate = DateField('Actual Start Date: ')
    ActualEndDate = DateField('Actual End Date:')
    Location = StringField('Location :' )
    AssignedTo = StringField('Assigned to: ')
    Deliverables = StringField('Deliverables: ')
    Status = SelectField('Status: ', choices = [('Scheduled','Scheduled'),('In Progress','In Progress'),('On Hold','On Hold'),('Canceled','Canceled'),('Complete','Complete')])
    Comments = TextAreaField('Comments: ')
    submit = SubmitField('Submit')