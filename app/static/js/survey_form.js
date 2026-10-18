/* Survey entry form: add/remove species and equipment rows plus a few sensible defaults. */
(function () {
  const form = document.getElementById("survey-form");
  if (!form) return;

  // Default the date to today in the browser's own timezone (YYYY-MM-DD) and block future dates.
  const dateInput = form.elements["surveyDate"];
  const today = new Date().toLocaleDateString("en-CA");
  dateInput.max = today;
  if (!dateInput.value) dateInput.value = today;

  // Cap an equipment quantity at the stock available for the chosen item.
  function syncQuantity(row) {
    const select = row.querySelector("select");
    const qty = row.querySelector('input[name="equipment_qty"]');
    const option = select.selectedOptions[0];
    if (select.value && option && option.dataset.available) {
      qty.max = option.dataset.available;
    } else {
      qty.removeAttribute("max");
    }
    qty.required = Boolean(select.value); // a quantity is only needed once an item is chosen
  }

  function addRow(kind) {
    const template = document.getElementById(kind + "-template");
    const container = document.getElementById(kind + "-rows");
    container.appendChild(template.content.cloneNode(true));
    container.lastElementChild.querySelector("input, select").focus();
  }

  function removeRow(row) {
    const container = row.parentElement;
    if (container.id === "species-rows" && container.children.length === 1) {
      // A survey needs at least one species, so clear the last row instead of removing it.
      row.querySelectorAll("input").forEach((input) => (input.value = ""));
    } else {
      row.remove();
    }
  }

  // One listener per event type handles every row, including rows added later.
  form.addEventListener("click", (event) => {
    const add = event.target.closest("[data-add]");
    if (add) return addRow(add.dataset.add);
    const remove = event.target.closest("[data-remove]");
    if (remove) removeRow(remove.closest(".repeat-row"));
  });

  form.addEventListener("change", (event) => {
    if (event.target.matches('select[name="equipment_id"]')) {
      syncQuantity(event.target.closest(".repeat-row"));
    }
  });

  form.querySelectorAll("#equipment-rows .repeat-row").forEach(syncQuantity);

  // Stop a double click from saving the survey (and taking the stock) twice.
  const saveButton = document.getElementById("save-survey");
  form.addEventListener("submit", () => {
    saveButton.disabled = true;
  });
  window.addEventListener("pageshow", () => {
    saveButton.disabled = false; // re-enable if the user comes back with the browser's Back button
  });
})();
