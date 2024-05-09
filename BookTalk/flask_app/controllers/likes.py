# this will be from our new table called likes: will be a many to many and update the erd creating a new likes table and connecting it to the existing tables

from flask_app import app
from flask import flash, redirect, request, session
from flask_app.models.like import Like

@app.post("/like/create")
def create_like():
    """This route processes the new like"""

    if "user_id" not in session:
        flash("please log in. ", "login")
        return redirect('/')
    
    book_id = request.form['book_id']

    Like.create(request.form)
    return redirect(f"/books/{book_id}")
