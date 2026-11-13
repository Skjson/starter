import {requestJSON} from "/static/js/api.js";
import {actions, busy, cell, emptyRow, fillGroups, message} from "/static/js/ui.js";

const API = "/api/students";
const body = document.querySelector("#table-body");
const search = document.querySelector("#student-search");
const groupFilter = document.querySelector("#group-filter");
const editor = document.querySelector("#editor");
const form = document.querySelector("#edit-form");
const idInput = document.querySelector("#record-id");
const nameInput = document.querySelector("#record-name");
const groupInput = document.querySelector("#record-group");
const emailInput = document.querySelector("#record-email");
const confirmation = document.querySelector("#confirmation");

let items = [];
let pendingId = null;
let loaded = false;

function saveRecord(recordId, payload) {
  const url = recordId === null ? API : API + "/" + recordId;
  return requestJSON(url, "POST", payload);
}

function deleteRecord(recordId) {
  return requestJSON(API + "/" + recordId, "DELETE");
}

function render() {
  const query = search.value.trim().toLowerCase();
  const groupId = groupFilter.value;
  const visible = items.filter((item) =>
    (!groupId || String(item.group_id) === groupId) && item.name.toLowerCase().includes(query)
  );
  body.replaceChildren();
  if (!visible.length) {
    emptyRow(body, 4, "Студенты не найдены");
    return;
  }
  for (const item of visible) {
    const row = document.createElement("tr");
    const actionCell = document.createElement("td");
    actionCell.append(actions(item.id));
    row.append(cell(item.name), cell(item.group_name), cell(item.email), actionCell);
    body.append(row);
  }
}

async function load(successText = "") {
  busy(true);
  message("Загрузка...");
  try {
    const [students, groups] = await Promise.all([requestJSON(API), requestJSON("/api/groups")]);
    fillGroups(groupFilter, groups.items, true);
    fillGroups(groupInput, groups.items);
    items = students.items;
    loaded = true;
    render();
    message(successText);
  } catch (error) {
    if (!loaded) emptyRow(body, 4, "Данные не загружены");
    message((successText ? successText + " Обновление списка не удалось. " : "") + error.message, true);
  } finally {
    busy(false);
  }
}

function openEditor(item = null) {
  if (!groupInput.options.length) {
    message("Сначала добавьте группу.", true);
    return;
  }
  form.reset();
  idInput.value = item ? String(item.id) : "";
  nameInput.value = item ? item.name : "";
  emailInput.value = item?.email ?? "";
  groupInput.value = item ? String(item.group_id) : groupFilter.value || groupInput.options[0].value;
  document.querySelector("#editor-title").textContent = item ? "Изменение студента" : "Добавление студента";
  confirmation.hidden = true;
  pendingId = null;
  editor.hidden = false;
  message();
  nameInput.focus();
}

search.addEventListener("input", render);
groupFilter.addEventListener("change", render);
document.querySelector("#add-record").addEventListener("click", () => openEditor());
document.querySelector("#cancel-edit").addEventListener("click", () => {
  editor.hidden = true;
  message();
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const recordId = idInput.value ? Number(idInput.value) : null;
  const payload = {name: nameInput.value, group_id: Number(groupInput.value), email: emailInput.value};
  busy(true);
  try {
    await saveRecord(recordId, payload);
    editor.hidden = true;
    form.reset();
    await load("Изменения сохранены.");
  } catch (error) {
    message(error.message, true);
  } finally {
    busy(false);
  }
});

body.addEventListener("click", (event) => {
  const button = event.target.closest("button[data-action]");
  if (!button) return;
  const item = items.find((record) => record.id === Number(button.dataset.id));
  if (!item) return;
  if (button.dataset.action === "edit") {
    openEditor(item);
    return;
  }
  pendingId = item.id;
  editor.hidden = true;
  confirmation.hidden = false;
  document.querySelector("#confirmation-text").textContent =
    "Удалить «" + item.name + "»? Будет удалено оценок: " + item.grade_count + ".";
  message();
});

document.querySelector("#cancel-delete").addEventListener("click", () => {
  pendingId = null;
  confirmation.hidden = true;
  message();
});

document.querySelector("#confirm-delete").addEventListener("click", async () => {
  if (pendingId === null) return;
  busy(true);
  try {
    await deleteRecord(pendingId);
    pendingId = null;
    confirmation.hidden = true;
    await load("Студент удалён.");
  } catch (error) {
    message(error.message, true);
  } finally {
    busy(false);
  }
});

load();
