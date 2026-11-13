import {requestJSON} from "/static/js/api.js";
import {busy, cell, emptyRow, message} from "/static/js/ui.js";

const select = document.querySelector("#report-kind");
const head = document.querySelector("#table-head");
const body = document.querySelector("#table-body");
const groupColumns = [
  {key: "name", title: "Группа"},
  {key: "student_count", title: "Студентов", className: "number"},
  {key: "grade_count", title: "Оценок", className: "number"},
  {key: "average_mark", title: "Средний балл", className: "number"},
];
const studentColumns = [
  {key: "name", title: "Студент"},
  {key: "group_name", title: "Группа"},
];
let loadedKind = null;

function render(kind, items) {
  const columns = kind === "groups" ? groupColumns : studentColumns;
  head.replaceChildren();
  for (const column of columns) {
    const th = document.createElement("th");
    th.scope = "col";
    th.textContent = column.title;
    th.className = column.className ?? "";
    head.append(th);
  }
  body.replaceChildren();
  if (!items.length) {
    emptyRow(body, columns.length);
    return;
  }
  for (const item of items) {
    const row = document.createElement("tr");
    for (const column of columns) {
      let value = item[column.key];
      if (column.key === "average_mark" && value !== null) {
        value = value.toLocaleString("ru-RU", {minimumFractionDigits: 2, maximumFractionDigits: 2});
      }
      row.append(cell(value, column.className));
    }
    body.append(row);
  }
}

async function load() {
  busy(true);
  message("Загрузка...");
  try {
    const params = new URLSearchParams({kind: select.value});
    const {kind, items} = await requestJSON("/api/reports?" + params);
    render(kind, items);
    loadedKind = kind;
    message();
  } catch (error) {
    if (loadedKind === null) emptyRow(body, 1, "Данные не загружены");
    else select.value = loadedKind;
    message(error.message, true);
  } finally {
    busy(false);
  }
}

select.addEventListener("change", load);
load();
