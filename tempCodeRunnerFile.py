from flask import Flask, render_template, jsonify, request
import course_selector

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get_courses", methods=["POST"])
def get_courses():
    gen_ed_requirement = request.form.get("gen_ed_requirement")
    start_time_str = request.form.get("start_time")
    end_time_str = request.form.get("end_time")
    day_input = request.form.get("day")

    # Validation for received data
    if (
        not gen_ed_requirement
        or not start_time_str
        or not end_time_str
        or not day_input
    ):
        return jsonify({"error": "Missing or invalid inputs"}), 400

    try:
        results = course_selector.select_courses_based_on_requirements(
            gen_ed_requirement, start_time_str, end_time_str, day_input
        )
        return jsonify(results)
    except Exception as e:
        print(f"Error: {e}")  # This will print the actual error message
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
