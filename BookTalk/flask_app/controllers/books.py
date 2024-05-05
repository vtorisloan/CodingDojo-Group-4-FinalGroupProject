from flask_app import app
from flask_app.models.book import Book
from flask_app.models.user import User
from flask_app.models.like import Likes
from flask import flash, render_template, redirect, request, session


@app.route('/book/all')
def book():
    """This route displays all book"""

    if "user_id" not in session: 
        flash("please log in. ", "login")
        return redirect('/')
    
    book = Book.find_all_with_users()
    user_watchlist = Likes.get_all_by_id(session["user_id"])
    # print("\n\n\n\nline18 user_watchlist", user_watchlist   )
    user = User.find_by_id(session["user_id"])
    # context = {"book": book, "user": user}
    return render_template("dashboard.html", user=user, book=book, user_watchlist=user_watchlist)

@app.get("/book/new")
def new_book():
    """This route displays the new book form"""

    if "user_id" not in session:
        flash("please log in. ", "login")
        return redirect('/')
    
    user = User.find_by_id(session["user_id"])
    # context = {"user": user}
    return render_template("newbook.html", user=user)
    

@app.post('/book/create')
def create_book():
    """This route  processes the book form"""

    if "user_id" not in session:
        flash("please log in. ", "login")
        return redirect('/')
    
    if not Book.form_is_valid(request.form):
        return redirect("/book/new")
    
    if Book.count_by_title(request.form["title"]) >= 1:
        # session["comment"] = request.form["comment"]
        flash("Book already exists", "error")    
        return redirect("/book/new")
    
    book_id = Book.create(request.form)

    data = {
        "book_id": book_id,
        "user_id": session["user_id"],
        # "watch_status": "Watching"
    }

    Book.add_to_watchlist(data)

    
    return redirect("/book/all")


@app.get('/book/<int:book_id>')
def book_profile(book_id):
    """This route displays the one book's details"""

    if "user_id" not in session:
        flash("please log in. ", "login")
        return redirect('/')
    
    book = Book.find_by_id_with_users(book_id)
    user = User.find_by_id(session["user_id"])

    return render_template("profile.html", user=user, book=book)

@app.get('/book/<int:book_id>/edit')
def edit_book(book_id):
    """This route displays the edit book form"""

    if "user_id" not in session:
        flash("please log in. ", "login")
        return redirect('/')
    
    book = Book.find_by_id(book_id)
    user = User.find_by_id(session["user_id"])
    return render_template("editbook.html", user=user, book=book)

@app.post('/book/update')
def update_book():
    """this route processes the book edit"""
   

    if "user_id" not in session:
        flash("please log in. ", "login")
        return redirect('/')
    
    book_id = request.form["book_id"]
    if not Book.form_is_valid(request.form):
        return redirect(f'/book/{book_id}/edit')
    
    Book.update_by_id(request.form)
    return redirect(f'/book/{book_id}')

@app.post('/book/<int:book_id>/delete')
def delete_book(book_id):
    """This route deletes an book form"""

    if "user_id" not in session:
        flash("please log in. ", "login")
        return redirect('/')
    
    Book.delete_by_id(book_id)
    return redirect('/book/all')