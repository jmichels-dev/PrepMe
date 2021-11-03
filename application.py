import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash


from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///prepme.db")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        # Adding user's username and hashed password to the database
        username = request.form.get("username")
        password = request.form.get("password")
        hash_pass = generate_password_hash(password)
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash_pass)
        return redirect("/")

    else:
        
        # Passing current users to Javascript to detect duplicates
        users_d = db.execute("SELECT username FROM users")
        users = []
        users = [0 for i in range(len(users_d))]
        for i in range(0, len(users_d)):
            users[i] = users_d[i]['username']

        # Display registration page to user
        return render_template("register.html", users=users)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)
        
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html", users=users)

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/")
@login_required
def index():
    """Show user's profile"""

    # Getting user's classes, tests, and recommendation from database
    transcript = db.execute("SELECT * FROM classes WHERE user_id=?", session["user_id"])
    tests = db.execute("SELECT * FROM tests WHERE user_id=?", session["user_id"])
    recommendations = db.execute("SELECT * FROM recommendations WHERE user_id=?", session["user_id"])
    return render_template("index.html", transcript=transcript, tests=tests, recommendations=recommendations)

@app.route("/edit_classes", methods=["GET", "POST"])
def edit_classes():
    """Update user's class info"""
    if request.method == "POST":

        # Getting information from user input to add/remove classes from database
        user_id = session["user_id"]
        name = request.form.get("title")
        class_type = request.form.get("type")
        honors = request.form.get("honors")
        grade = request.form.get("grade")
        classr = request.form.get("classr")

        # If user inputted a class, add it to database
        if name:
            db.execute("INSERT INTO classes (user_id, name, type, honors, grade) VALUES (?, ?, ?, ?, ?)", user_id, name, class_type, honors, grade)

        # If user selected a class to be removed, remove it from the database
        if classr:
            db.execute("DELETE FROM classes WHERE user_id = ? AND name = ?", user_id, classr)

        # Redirect user to homepage
        return redirect("/")

    else:

        # Pass user's current classes in case user wants to remove a class
        classes = db.execute("SELECT * FROM classes WHERE user_id=?", session["user_id"])

        # Direct user to edit classes page
        return render_template("edit_classes.html", classes=classes)

@app.route("/edit_test_scores", methods=["GET", "POST"])
def edit_test_scores():
    """Update user's test score info"""
    if request.method == "POST":

        # Getting information from user input to add/remove tests from database
        user_id = session["user_id"]
        test = request.form.get("test")
        ssubject = request.form.get("ssubject")
        asubject = request.form.get("asubject")
        score = request.form.get("score")
        scorew = request.form.get("scorew")
        rtest = request.form.get("testr")
        subrs = request.form.get("subrs")
        subra = request.form.get("subra")

        # If no subject was selected, list subject as N/a in table
        if not ssubject and not asubject:
            subject = "N/a"

        # If there was not a SAT Subject test subject selected, set subject to be entered to an AP Test subject
        elif not ssubject:
            subject = asubject

        # If there was not an AP Test subject selected, set subject to be entered to an SAT Subject Test subject
        else:
            subject = ssubject

        # If there was no writing score inputted, list writing score as N/a in table
        if not scorew:
            scorew = "N/a"

        # If there was a test inputted to be added, add the test to user's database
        if test:
            db.execute("INSERT INTO tests (user_id, type, subject, score, scorew) VALUES (?, ?, ?, ?, ?)", user_id, test, subject, score, scorew)

        # If there was a test selected to be removed, remove test from user's database
        if rtest:

            # Distinguishes between SAT Subject Tests/AP Tests and all other types of tests
            if subrs or subra:
                if not subrs:
                    subr = subra
                else:
                    subr = subrs
                db.execute("DELETE FROM tests WHERE user_id = ? AND type = ? AND subject = ?", user_id, rtest, subr)
            else:
                db.execute("DELETE FROM tests WHERE user_id = ? AND type = ?", user_id, rtest)

        # Redirect user to homepage
        return redirect("/")

    else:

        # Pass user's current tests in case user wants to remove a test
        tests = db.execute("SELECT * FROM tests WHERE user_id=?", session["user_id"])

        # Direct user to edit tests page
        return render_template("edit_test_scores.html", tests=tests)

@app.route("/edit_recommendations", methods=["GET", "POST"])
def edit_recommendations():
    """Update user's recommendation info"""
    if request.method == "POST":

        # Getting information from user input to add/remove recommendations from database
        user_id = session["user_id"]
        recommender = request.form.get("recommender")
        relationship = request.form.get("relationship")
        strength = request.form.get("strength")
        recr = request.form.get("recr")

        # If there was a recommendation inputted to be removed, removes recommendation from user's database
        if recr:
            db.execute("DELETE FROM recommendations WHERE user_id = ? AND recommender = ?", user_id, recr)

        # If there was a recommendation inputted to be added, adds recommendation to user's database
        if recommender:
            db.execute("INSERT INTO recommendations (user_id, recommender, relationship, strength) VALUES (?, ?, ?, ?)", user_id, recommender, relationship, strength)

        # Redirect user to homepage
        return redirect("/")

    else:

        # Pass user's current recommendations in case user wants to remove a recommendation
        recommendations = db.execute("SELECT * FROM recommendations WHERE user_id=?", session["user_id"])

        # Direct user to edit recommendations page
        return render_template("edit_recommendations.html", recommendations=recommendations)

@app.route("/rate_application")
def rate_application():
    """Rate user's current application credentials"""

    # Getting user's class counts for rating algorithm
    science = db.execute("SELECT COUNT(type) FROM classes WHERE user_id=? AND type=?", session["user_id"], "Science")
    math = db.execute("SELECT COUNT(type) FROM classes WHERE user_id=? AND type=?", session["user_id"], "Math")
    english = db.execute("SELECT COUNT(type) FROM classes WHERE user_id=? AND type=?", session["user_id"], "English")
    history = db.execute("SELECT COUNT(type) FROM classes WHERE user_id=? AND type=?", session["user_id"], "History")
    for_lang = db.execute("SELECT COUNT(type) FROM classes WHERE user_id=? AND type=?", session["user_id"], "Foreign Language")
    extra = db.execute("SELECT COUNT(type) FROM classes WHERE user_id=? AND (type=? OR type=? OR type=?)", session["user_id"], "Music", "Art", "Other")

    # Getting user's number of honors/AP/IB classes taken info for rating algorithm
    honors = db.execute("SELECT COUNT(honors) FROM classes WHERE user_id=? AND honors=?", session["user_id"], "Honors")
    AP = db.execute("SELECT COUNT(honors) FROM classes WHERE user_id=? AND honors=?", session["user_id"], "AP")
    IB = db.execute("SELECT COUNT(honors) FROM classes WHERE user_id=? AND honors=?", session["user_id"], "IB")
    no_h = db.execute("SELECT COUNT(honors) FROM classes WHERE user_id=? AND honors=?", session["user_id"], "--")

    # Getting user's grades and total number of classes for gpa calculation
    grade_ap = db.execute("SELECT COUNT(grade) FROM classes WHERE user_id=? AND grade=?", session["user_id"], "a+")
    grade_a = db.execute("SELECT COUNT(grade) FROM classes WHERE user_id=? AND grade=?", session["user_id"], "a")
    grade_am = db.execute("SELECT COUNT(grade) FROM classes WHERE user_id=? AND grade=?", session["user_id"], "a-")
    grade_bp = db.execute("SELECT COUNT(grade) FROM classes WHERE user_id=? AND grade=?", session["user_id"], "b+")
    grade_b = db.execute("SELECT COUNT(grade) FROM classes WHERE user_id=? AND grade=?", session["user_id"], "b")
    grade_bm = db.execute("SELECT COUNT(grade) FROM classes WHERE user_id=? AND grade=?", session["user_id"], "b-")
    grade_cp = db.execute("SELECT COUNT(grade) FROM classes WHERE user_id=? AND grade=?", session["user_id"], "c+")
    grade_c = db.execute("SELECT COUNT(grade) FROM classes WHERE user_id=? AND grade=?", session["user_id"], "c")
    grade_cm = db.execute("SELECT COUNT(grade) FROM classes WHERE user_id=? AND grade=?", session["user_id"], "c-")
    grade_dp = db.execute("SELECT COUNT(grade) FROM classes WHERE user_id=? AND grade=?", session["user_id"], "d+")
    grade_d = db.execute("SELECT COUNT(grade) FROM classes WHERE user_id=? AND grade=?", session["user_id"], "d")
    grade_dm = db.execute("SELECT COUNT(grade) FROM classes WHERE user_id=? AND grade=?", session["user_id"], "d-")
    grade_f = db.execute("SELECT COUNT(grade) FROM classes WHERE user_id=? AND grade=?", session["user_id"], "f")
    class_count = db.execute("SELECT COUNT(*) FROM classes WHERE user_id=?", session["user_id"])

    # Calculating user's gpa
    if class_count[0]["COUNT(*)"] == 0:
        gpa = "no"
    else:
        gpa = (((grade_ap[0]["COUNT(grade)"] + grade_a[0]["COUNT(grade)"]) * 4.0) + (grade_am[0]["COUNT(grade)"] * 3.7) + (grade_bp[0]["COUNT(grade)"] * 3.3) + (grade_b[0]["COUNT(grade)"] * 3.0) + (grade_bm[0]["COUNT(grade)"] * 2.7) + (grade_cp[0]["COUNT(grade)"] * 2.3) + (grade_c[0]["COUNT(grade)"] * 2.0) + (grade_cm[0]["COUNT(grade)"] * 1.7) + (grade_dp[0]["COUNT(grade)"] * 1.3) + (grade_d[0]["COUNT(grade)"] * 1.0) + (grade_dm[0]["COUNT(grade)"] * 0.7) + (grade_f[0]["COUNT(grade)"] * 0.0)) / (class_count[0]["COUNT(*)"])

    # Calculating user's honors ratio, ratio of honors-level or above classes vs total number of classes taken
    if class_count[0]["COUNT(*)"] == 0:
        honors_ratio = "no"
    else:
        honors_ratio = (honors[0]["COUNT(honors)"] + AP[0]["COUNT(honors)"] + IB[0]["COUNT(honors)"]) / class_count[0]["COUNT(*)"]

    # Getting user's best ACT score, converting it into an integer used to categorize test score and compare to best SAT score
    act = db.execute("SELECT MAX(score) FROM tests WHERE user_id=? AND (type=? OR type=?)", session["user_id"], "ACT", "ACT w/ Writing")
    if not act[0]["MAX(score)"]:
        act = None
    elif act[0]["MAX(score)"] <= 36 and act[0]["MAX(score)"] >= 32:
        act = 32
    elif act[0]["MAX(score)"] <= 31 and act[0]["MAX(score)"] >= 27:
        act = 27
    elif act[0]["MAX(score)"] <= 26 and act[0]["MAX(score)"] >= 24:
        act = 24
    elif act[0]["MAX(score)"] <= 23 and act[0]["MAX(score)"] >= 21:
        act = 21
    else:
        act = 0

    # Getting user's best ACT writing score, converting it into an integer on SAT writing score scale, used to categorize writing score and compare to best SAT writing score
    # Conversions based on percentile values of ACT (https://blog.prepscholar.com/whats-an-average-act-writing-score) and SAT (https://www.compassprep.com/sat-essay-scores-explained/) writing scores
    actw = db.execute("SELECT MAX(scorew) FROM tests WHERE user_id=? AND type=?", session["user_id"], "ACT w/ Writing")
    if not actw[0]["MAX(scorew)"]:
        actw = None
    elif actw[0]["MAX(scorew)"] <= 12 and actw[0]["MAX(scorew)"] >= 8:
        actw = 6
    elif actw[0]["MAX(scorew)"] <= 7 and actw[0]["MAX(scorew)"] >= 5:
        actw = 4
    else:
        actw = 0

    # Getting user's best SAT score, converting it into an integer on ACT scale used to categorize test score and compare to best ACT score
    # Conversions found from official ACT concordance tables: https://www.act.org/content/dam/act/unsecured/documents/ACT-SAT-Concordance-Tables.pdf
    sat = db.execute("SELECT MAX(score) FROM tests WHERE user_id=? AND (type=? OR type=?)", session["user_id"], "SAT", "SAT w/ Writing")
    if not sat[0]["MAX(score)"]:
        sat = None
    elif sat[0]["MAX(score)"] <= 1600 and sat[0]["MAX(score)"] >= 1420:
        sat = 32
    elif sat[0]["MAX(score)"] <= 1410 and sat[0]["MAX(score)"] >= 1260:
        sat = 27
    elif sat[0]["MAX(score)"] <= 1250 and sat[0]["MAX(score)"] >= 1160:
        sat = 24
    elif sat[0]["MAX(score)"] <= 1150 and sat[0]["MAX(score)"] >= 1060:
        sat = 21
    else:
        sat = 0

    # Getting user's best SAT writing score, converting it into an integer on SAT writing score scale, used to categorize writing score and compare to best ACT writing score
    satw = db.execute("SELECT MAX(scorew) FROM tests WHERE user_id=? AND type=?", session["user_id"], "SAT w/ Writing")
    if not satw[0]["MAX(scorew)"]:
        satw = None
    elif satw[0]["MAX(scorew)"] <= 8 and satw[0]["MAX(scorew)"] >= 6:
        satw = 6
    elif satw[0]["MAX(scorew)"] <= 5 and satw[0]["MAX(scorew)"] >= 4:
        satw = 4
    else:
        satw = 0

    # Determines best SAT or ACT score
    if not sat and not act:
        best_test = "no"
    elif not sat and act:
        best_test = act
    elif not act and sat:
        best_test = sat
    elif sat > act:
        best_test = sat
    elif sat < act:
        best_test = act
    else:
        best_test = sat

    # Determines best SAT or ACT writing score
    if not satw and not actw:
        best_write = "no"
    elif not satw and actw:
        best_write = actw
    elif not actw and satw:
        best_write = satw
    elif satw > actw:
        best_write = satw
    elif satw < actw:
        best_write = actw
    else:
        best_write = satw

    # Getting number of SAT Subject tests and AP Tests user has taken
    sats = db.execute("SELECT COUNT(type) FROM tests WHERE user_id=? AND type=?", session["user_id"], "SAT Subject Test")
    ap = db.execute("SELECT COUNT(type) FROM tests WHERE user_id=? AND type=?", session["user_id"], "AP Test")

    # Getting user's recommendation information for rating algorithm
    rec_number = db.execute("SELECT COUNT(recommender) FROM recommendations WHERE user_id=?", session["user_id"])
    rec_score = db.execute("SELECT SUM(strength) FROM recommendations WHERE user_id=?", session["user_id"])

    # Calculating user's average recommendation
    if rec_number[0]["COUNT(recommender)"] == 0:
        rec_avg = "no"
    else:
        rec_avg = float(rec_score[0]["SUM(strength)"])/rec_number[0]["COUNT(recommender)"]

    # Directing user to their rated application
    return render_template("rate_application.html", science=science[0]["COUNT(TYPE)"], math=math[0]["COUNT(TYPE)"], english=english[0]["COUNT(TYPE)"], history=history[0]["COUNT(TYPE)"], for_lang=for_lang[0]["COUNT(TYPE)"], extra=extra[0]["COUNT(TYPE)"], AP=AP[0]["COUNT(honors)"], gpa=gpa, best_test=best_test, best_write=best_write, sats=sats[0]["COUNT(TYPE)"], rec_avg=rec_avg, honors_ratio=honors_ratio)

@app.route("/resume_tips")
def resume_tips():
    """Provides applicants with resume tips"""
    # Directing user to resume tips page
    return render_template("resume_tips.html")

@app.route("/about_me")
def about_me():
    """About the Developer"""
    # Directing user to about me page
    return render_template("about_me.html")