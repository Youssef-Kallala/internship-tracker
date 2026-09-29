from flask import Flask, render_template, request, redirect, url_for, jsonify
from database import *

app = Flask(__name__)

@app.route("/")
def home():
    apps = get_all_applications()
    selected_columns = get_home_columns()

    all_fields = ["Status", "Company", "Position", "Date Applied", "Deadline",
                  "Application Link", "Location", "Duration", "Salary"]

    date_from = request.args.get("date_from", "")
    date_to = request.args.get("date_to", "")

    apps_with_values = []
    for app in apps:
        fields = get_fields_and_values(app["id"])
        values = {field["field_name"]: field["value"] for field in fields}

        # Filter by date range
        date_applied = values.get("Date Applied", "")
        if date_from and date_applied and date_applied < date_from:
            continue
        if date_to and date_applied and date_applied > date_to:
            continue

        apps_with_values.append({"app": app, "values": values})

    # Sort by status group first, then by date applied ascending within each group
    status_order = {
        "Did not apply yet": 0,
        "Applied":           1,
        "Interviewed":       2,
        "Accepted":          3,
        "Rejected":          4,
    }

    def sort_key(item):
        status = item["values"].get("Status", "Applied")
        date = item["values"].get("Date Applied", "")
        priority = status_order.get(status, 1)
        if not date:
            date = "9999-12-31"
        return (priority, date)

    apps_with_values.sort(key=sort_key)

    # Compute statistics
    stats = {
        "total":        len(apps_with_values),
        "did_not_apply": sum(1 for a in apps_with_values if a["values"].get("Status") == "Did not apply yet"),
        "applied":      sum(1 for a in apps_with_values if a["values"].get("Status") == "Applied"),
        "interviewed":  sum(1 for a in apps_with_values if a["values"].get("Status") == "Interviewed"),
        "accepted":     sum(1 for a in apps_with_values if a["values"].get("Status") == "Accepted"),
        "rejected":     sum(1 for a in apps_with_values if a["values"].get("Status") == "Rejected"),
    }

    return render_template("home.html",
                           apps_with_values=apps_with_values,
                           selected_columns=selected_columns,
                           all_fields=all_fields,
                           date_from=date_from,
                           date_to=date_to,
                           stats=stats)

@app.route("/application/<int:app_id>")
def application(app_id):
    app_data = get_application(app_id)
    if not app_data:
        return "Application not found", 404
    fields = get_fields_and_values(app_id)
    return render_template("application.html", app=app_data, fields=fields)

@app.route("/add_application", methods=["POST"])
def add_application_route():
    name = request.form["name"]
    app_id = add_application(name)
    return redirect(url_for("application", app_id=app_id))

@app.route("/delete_application/<int:app_id>", methods=["POST"])
def delete_application_route(app_id):
    delete_application(app_id)
    return redirect(url_for("home"))

@app.route("/add_field/<int:app_id>", methods=["POST"])
def add_field_route(app_id):
    field_name = request.form["field_name"]
    field_type = request.form["field_type"]
    add_field(app_id, field_name, field_type)
    return redirect(url_for("application", app_id=app_id))

@app.route("/delete_field/<int:field_id>/<int:app_id>", methods=["POST"])
def delete_field_route(field_id, app_id):
    delete_field(field_id)
    return redirect(url_for("application", app_id=app_id))

@app.route("/update_value/<int:entry_id>/<int:app_id>", methods=["POST"])
def update_value_route(entry_id, app_id):
    new_value = request.form["value"]
    update_value(entry_id, new_value)
    return redirect(url_for("application", app_id=app_id))

@app.route("/home_columns")
def home_columns():
    columns = get_home_columns()
    return jsonify(columns)

@app.route("/add_home_column", methods=["POST"])
def add_home_column_route():
    field_name = request.form["field_name"]
    add_home_column(field_name)
    return redirect(url_for("home"))

@app.route("/remove_home_column", methods=["POST"])
def remove_home_column_route():
    field_name = request.form["field_name"]
    remove_home_column(field_name)
    return redirect(url_for("home"))

@app.route("/rename_application/<int:app_id>", methods=["POST"])
def rename_application_route(app_id):
    new_name = request.form["new_name"]
    rename_application(app_id, new_name)
    return redirect(url_for("application", app_id=app_id))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)