from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages, session, make_response, jsonify

app = Flask(__name__)
app.secret_key = "your_secret_key"

WORD_LIST_FILE = "word_list.txt"

# Read words from the word list file
def read_word_list():
    with open(WORD_LIST_FILE, 'r') as f:
        return [line.strip() for line in f.readlines()]

# Write words to the word list file
def write_word_list(words):
    with open(WORD_LIST_FILE, 'w') as f:
        for word in words:
            f.write(f"{word}\n")

# Display the main page with word list
@app.route('/')
def index():
    word_list = read_word_list()
    return render_template('index.html', word_list=word_list)

# Practise page for testing user's spelling
@app.route("/practise", methods=["GET", "POST"])
def practise():
    word_list = read_word_list()

    # Initialize session variables if not already set
    if 'current_word_index' not in session:
        session['current_word_index'] = 0
    if "correct" not in session:
        session["correct"] = 0
    if "total_attempts" not in session:
        session["total_attempts"] = 0

    # Process user's input and update session variables
    if request.method == "POST":
        user_input = request.form["user_input"]
        correct_word = request.form["correct_word"]

        if user_input == correct_word:
            session["correct"] += 1
            response_data = {"status": "success", "message": "Correct!"}
            cookie_sound = "correct"
        else:
            response_data = {"status": "danger", "message": f"Oops! That's wrong. The correct spelling is '{correct_word}'"}
            cookie_sound = "incorrect"

        session["total_attempts"] += 1
        session['current_word_index'] += 1

        if session['current_word_index'] >= len(word_list):
            session['current_word_index'] = 0

        next_word = word_list[session['current_word_index']]
        response = jsonify({"score": f'{session["correct"]}/{session["total_attempts"]}', "sound": cookie_sound, "response_data": response_data, "next_word": next_word})
        return response

    word = word_list[session['current_word_index']]
    return render_template("practise.html", word=word)

# Update word list page
@app.route('/update_word_list', methods=['GET', 'POST'])
def update_word_list():
    if request.method == 'POST':
        words = request.form['words'].splitlines()
        write_word_list(words)
        return redirect(url_for('index'))

    current_words = '\n'.join(read_word_list())
    return render_template('update_word_list.html', current_words=current_words)

# Reset user's score and redirect to index
@app.route("/reset_score", methods=["POST"])
def reset_score():
    session["correct"] = 0
    session["total_attempts"] = 0
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
