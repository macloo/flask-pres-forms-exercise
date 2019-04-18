from flask import Flask, render_template, redirect, url_for, request
from modules import convert_to_dict, make_ordinal

from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from wtforms.validators import Required

app = Flask(__name__)

# Flask-WTF requires an encryption key - the string can be anything
app.config['SECRET_KEY'] = 'C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb'

# Flask-Bootstrap requires this line
Bootstrap(app)

# create a list of dicts
presidents_list = convert_to_dict("presidents.csv")

# with Flask-WTF, each web form is represented by a class
# "SearchForm" can change; "(FlaskForm)" cannot
class SearchForm(FlaskForm):
    # the choices are (option, string)
    pres_choice = SelectField('Select from this list')
    submit = SubmitField('Search')


# first route

@app.route('/', methods=['GET', 'POST'] )
def index():
    # make three empty lists
    ids_list = []
    name_list = []
    pairs_list = []
    # fill one list with the number of each presidency and
    # fill the other with the name of each president
    for president in presidents_list:
        ids_list.append(president['Presidency'])
        name_list.append(president['President'])
        # zip() is a built-in function that combines lists
        # creating a new list of tuples
    pairs_list = zip(ids_list, name_list)

    # this is from the class above; form will go to the template
    form = SearchForm()
    # this is how we auto-populate a select menu in a form
    form.pres_choice.choices = [ (p[0], p[1]) for p in pairs_list ]

    # if page opened by form submission, redirect to detail page
    if request.method == "POST":
        # get the input from the form
        pres_choice = request.form.get("pres_choice")
        return redirect( url_for('detail', num=pres_choice ) )

    # no else - just do this by default
    return render_template('search2.html', form=form)


# second route

@app.route('/president/<num>')
def detail(num):
    for president in presidents_list:
        if president['Presidency'] == num:
            pres_dict = president
            break
    # a little bonus function, imported
    ord = make_ordinal( int(num) )
    return render_template('president.html', pres=pres_dict, ord=ord, the_title=pres_dict['President'])


# keep this as is
if __name__ == '__main__':
    app.run(debug=True)
