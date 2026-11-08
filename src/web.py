"""Web interface for managing warehouse storages."""

import math

from flask import (
    Blueprint,
    Flask,
    current_app,
    redirect,
    render_template_string,
    request,
    url_for,
)

from varasto import Varasto


PAGE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Warehouse</title>
  <style>
    :root { font-family: system-ui, sans-serif; color: #17241f; background: #f3f6f3; }
    body { max-width: 900px; margin: 0 auto; padding: 2rem 1rem; }
    h1 { margin-bottom: .25rem; } .muted { color: #58665f; }
    .panel, .storage { background: white; border: 1px solid #dce5de; border-radius: 12px; padding: 1.25rem; margin: 1rem 0; }
    .storages { display: grid; grid-template-columns: repeat(auto-fit,minmax(270px,1fr)); gap: 1rem; }
    .storage { margin: 0; } form { display: flex; flex-wrap: wrap; gap: .5rem; margin-top: 1rem; }
    input, button { font: inherit; padding: .55rem .7rem; border-radius: 7px; border: 1px solid #b9c8bf; }
    input[type=text] { flex: 1 1 150px; } button { background: #176b4b; color: white; border: 0; cursor: pointer; }
    .error { color: #a32828; } .flash { padding: .7rem; background: #e8f4ec; border-radius: 7px; }
  </style>
</head>
<body>
  <header><h1>Warehouse</h1><p class="muted">Manage storage capacity and stock.</p></header>
  {% for message in messages %}<p class="flash" role="status">{{ message }}</p>{% endfor %}
  {% if error %}<p class="error" role="alert">{{ error }}</p>{% endif %}
  <section class="panel" aria-labelledby="create-heading">
    <h2 id="create-heading">Create a storage</h2>
    <form action="{{ url_for('warehouse.create_storage') }}" method="post">
      <label>Name <input name="name" type="text" required maxlength="80"></label>
      <label>Capacity <input name="capacity" type="number" min="0" step="any" required></label>
      <button type="submit">Create storage</button>
    </form>
  </section>
  <section aria-labelledby="storages-heading">
    <h2 id="storages-heading">Storages</h2>
    {% if storages %}<div class="storages">
      {% for storage in storages %}<article class="storage">
        <h3>{{ storage.name }}</h3>
        <p>Balance: <strong>{{ '%.2f'|format(storage.inventory.saldo) }}</strong> / {{ '%.2f'|format(storage.inventory.tilavuus) }}</p>
        <p class="muted">Available capacity: {{ '%.2f'|format(storage.inventory.paljonko_mahtuu()) }}</p>
        <form action="{{ url_for('warehouse.change_stock', storage_id=storage.id) }}" method="post">
          <label>Quantity <input name="quantity" type="number" min="0" step="any" required></label>
          <button name="action" value="add" type="submit">Add stock</button>
          <button name="action" value="take" type="submit">Take stock</button>
        </form>
      </article>{% endfor %}
    </div>{% else %}<p class="muted">No storages yet. Create one to get started.</p>{% endif %}
  </section>
</body>
</html>"""

warehouse = Blueprint("warehouse", __name__)


def render_page(error=None, messages=()):
    """Render the storage dashboard and an optional validation message."""
    return render_template_string(
        PAGE,
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
