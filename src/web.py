"""Web interface for managing warehouse storages."""

import math

from flask import (
    Blueprint,
    Flask,
    current_app,
    redirect,
    render_template,
    request,
    url_for,
)

from varasto import Varasto


warehouse = Blueprint("warehouse", __name__)


def render_page(error=None, messages=()):
    """Render the storage dashboard and an optional validation message."""
    return render_template(
        "warehouse.html",
        storages=current_app.config["STORAGES"],
        error=error,
        messages=messages,
    )


def parse_quantity(field):
    """Return a valid non-negative finite number from a form field."""
    try:
        quantity = float(request.form.get(field, ""))
    except ValueError:
        quantity = -1
    if quantity < 0 or not math.isfinite(quantity):
        quantity = -1
    return quantity


@warehouse.get("/")
def index():
    """Show all storages."""
    return render_page()


@warehouse.post("/storages")
def create_storage():  # pylint: disable=too-many-return-statements
    """Create a named storage with the submitted capacity."""
    name = request.form.get("name", "").strip()
    capacity = parse_quantity("capacity")
    if capacity < 0:
        return render_page("Enter a valid non-negative capacity."), 400
    if not name:
        return render_page("Storage name is required."), 400
    storage_id = current_app.config["NEXT_ID"]
    current_app.config["NEXT_ID"] += 1
    current_app.config["STORAGES"].append(
        {"id": storage_id, "name": name, "inventory": Varasto(capacity)}
    )
    return redirect(url_for("warehouse.index"), code=303)


@warehouse.post("/storages/<int:storage_id>/stock")
def change_stock(storage_id):  # pylint: disable=too-many-return-statements
    """Add or remove stock from an existing storage."""
    storage = find_storage(storage_id)
    if storage is None:
        return "Storage not found", 404
    quantity = parse_quantity("quantity")
    if quantity < 0:
        return render_page("Enter a valid non-negative quantity."), 400
    updated = update_stock(
        storage["inventory"], quantity, request.form.get("action")
    )
    if not updated:
        return render_page("Choose whether to add or take stock."), 400
    return redirect(url_for("warehouse.index"), code=303)


def find_storage(storage_id):
    """Find one storage by its identifier."""
    return next(
        (
            item
            for item in current_app.config["STORAGES"]
            if item["id"] == storage_id
        ),
        None,
    )


def update_stock(inventory, quantity, action):
    """Apply a stock action and report whether it was recognized."""
    if action == "add":
        inventory.lisaa_varastoon(quantity)
    elif action == "take":
        inventory.ota_varastosta(quantity)
    else:
        action = None
    return action is not None


def create_app():
    """Create the Flask application and its in-memory storage collection."""
    application = Flask(__name__)
    application.config["STORAGES"] = []
    application.config["NEXT_ID"] = 1
    application.register_blueprint(warehouse)
    return application


app = create_app()


if __name__ == "__main__":
    app.run(debug=True, port=5001)
