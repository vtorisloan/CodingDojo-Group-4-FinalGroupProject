from flask_app import app
from flask import flash, redirect, request, session
from flask_app.models.like import Likes


@app.post("/likes/watch")
def watch_likes():
    """This route processes an anime to our watch list"""

    Likes.watch_likes()

    if "user_id" not in session:
        flash("please log in. ", "login")
        return redirect("/")

    form_data = {
        "user_id": session["user_id"],
        "anime_id": request.form["anime_id"]
    }
    Likes.watch(form_data)
    return redirect("/likes")



@app.get("/watchlist/remove/<int:anime_id>/<int:user_id>")
def remove(anime_id, user_id):
    """This route removes an anime from our watch list"""
    if "user_id" not in session:
        flash("please log in. ", "login")
        return redirect("/")

    form_data = {
        "user_id": user_id,
        "anime_id": anime_id
    }
    Likes.remove(form_data)
    return redirect("/animes/all")

@app.get("/watchlist/add/<int:anime_id>/<int:user_id>")
def add(anime_id, user_id):
    """This route adds an anime to our watch list"""
    if "user_id" not in session:
        flash("please log in. ", "login")
        return redirect("/")

    form_data = {
        "user_id": user_id,
        "anime_id": anime_id,
        "watch_status": "watching"
    }
    Likes.add(form_data)
    return redirect("/animes/all")

