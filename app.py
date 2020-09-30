import os
from flask import Flask, render_template, redirect, request, url_for, flash
from flask_pymongo import PyMongo
from pymongo import ASCENDING, DESCENDING
from bson.objectid import ObjectId


app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'jargon_buster'
app.config['MONGO_URI'] = 'mongodb+srv://root:rootUser@myfirstcluster-lrum9.mongodb.net/jargon_buster?retryWrites=true&w=majority'

mongo = PyMongo(app)


@app.route('/')

#Get all terms
@app.route('/get_jargon')
def get_jargon():
    jargons = list(mongo.db.jargon.find())
    if 'jargon_search' in request.args:
        query = request.args['jargon_search']
        new_jargon_list = []
        for jargon in jargons:
            if jargon['jargon_name'].find(query) != -1:
                new_jargon_list.append(jargon)
        return render_template('search.html', jargons=new_jargon_list)

    elif 'sort' in request.args:
        if request.args['sort'] == 'asc':
            new_jargon_list = list(mongo.db.jargon.find().sort('jargon_name', ASCENDING))
            return render_template('recipes.html', recipes=new_jargon_list)
        elif request.args['sort'] == 'dsc':
            new_jargon_list = list(mongo.db.recipes.find().sort('jargon_name', DESCENDING))
            return render_template('search.html', jargons=new_jargon_list)

    return render_template('jargon.html', jargons=jargons)


@app.route('/add_jargon')
def add_jargon():
    return render_template('addjargon.html',
                           categories=mongo.db.categories.find())

# Adds a new definition to the database.
@app.route('/insert_jargon', methods=['POST'])
def insert_jargon():
    jargon = mongo.db.jargon
    jargon.insert_one(request.form.to_dict())
    return redirect(url_for('get_jargon'))


@app.route('/edit_jargon/<jargon_id>')
def edit_jargon(jargon_id):
    the_jargon = mongo.db.jargon.find_one({"_id": ObjectId(jargon_id)})
    all_categories = mongo.db.categories.find()
    return render_template('editjargon.html', jargon=the_jargon,
                           categories=all_categories)


@app.route('/update_jargon/<jargon_id>', methods=["POST"])
def update_jargon(jargon_id):
    jargon = mongo.db.jargon
    jargon.update({'_id': ObjectId(jargon_id)},
                  {
            'jargon_name': request.form.get('jargon_name'),
            'category_name': request.form.get('category_name'),
            'description': request.form.get('description')
                })
    return redirect(url_for('get_jargon'))


@app.route('/delete_jargon/<jargon_id>')
def delete_jargon(jargon_id):
    mongo.db.jargon.remove({'_id': ObjectId(jargon_id)})
    return redirect(url_for('get_jargon'))


@app.route('/get_categories')
def get_categories():
    return render_template('categories.html',
                           categories=mongo.db.categories.find())


@app.route('/delete_category/<category_id>')
def delete_category(category_id):
    mongo.db.categories.remove({'_id': ObjectId(category_id)})
    return redirect(url_for('get_categories'))


@app.route('/edit_category/<category_id>')
def edit_category(category_id):
    return render_template('editcategory.html',
    category=mongo.db.categories.find_one({'_id': ObjectId(category_id)}))


@app.route('/update_category/<category_id>', methods=['POST'])
def update_category(category_id):
    mongo.db.categories.update(
        {'_id': ObjectId(category_id)},
        {'category_name': request.form.get('category_name')})
    return redirect(url_for('get_categories'))


@app.route('/insert_category', methods=['POST'])
def insert_category():
    category_doc = {'category_name': request.form.get('category_name')}
    mongo.db.categories.insert_one(category_doc)
    return redirect(url_for('get_categories'))


@app.route('/add_category')
def add_category():
    return render_template('addcategory.html')


if __name__ == '__main__':
    app.run(host=os.environ.get('IP', '0.0.0.0'),
            port=int(os.environ.get('PORT', '5000')),
            debug=True)
