from flask import Flask, render_template, redirect, url_for, request
from modules import convert_to_dict, make_ordinal

from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
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
    # the choices are (value, label)
    category = RadioField('Choose a detail to search:', validators=[Required()], choices=[ ('President', 'President\'s Name, e.g. John'), ('Home-state', 'Home State, e.g. Virginia'), ('Occupation', 'Occupation, e.g. Lawyer'), ('College', 'College, e.g. Harvard')] )
    text = StringField('Type full or partial text to search for:', validators=[Required()] )
    submit = SubmitField('Search')

# first route

@app.route('/')
def index():
    ids_list = []
    name_list = []
    # fill one list with the number of each presidency and
    # fill the other with the name of each president
    for president in presidents_list:
        ids_list.append(president['Presidency'])
        name_list.append(president['President'])
        # zip() is a built-in function that combines lists
        # creating a new list of tuples
    pairs_list = zip(ids_list, name_list)
    # sort the list by the first item in each tuple, the number
    # pairs_list_sorted = sorted(pairs_list, key=lambda tup: int(tup[0]))
    return render_template('index.html', pairs=pairs_list, the_title="Presidents Index")

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

# third route

@app.route( '/search', methods=['GET', 'POST'] )
def search():
    # this is from the class above; form will go to the template
    form = SearchForm()
    message = ""
    # make three empty lists
    ids_list = []
    name_list = []
    pairs_list = []
    if request.method == "POST":
        # get the inputs from the form
        category = request.form.get("category")
        text = request.form.get("text")

        # loop to find ALL presidents who match inputs
        # but ONLY those who match
        for president in presidents_list:
            if text.lower() in president[category].lower():
                ids_list.append(president['Presidency'])
                name_list.append(president['President'])

        pairs_list = zip(ids_list, name_list)
        # the following is for cases where the search.html template is returned
        message = "Sorry, no match was found."
    # decide which route/template to use, based on search results
    if len(ids_list) == 1:
        return redirect( url_for('detail', num=ids_list[0] ) )
    elif len(ids_list) > 0:
        return render_template('index.html', pairs=pairs_list, the_title="Search Results")
    else:
        # the next return happens if method == "GET" or no match was found
        return render_template('search.html', form=form, message=message)

# keep this as is
if __name__ == '__main__':
    app.run(debug=True)
