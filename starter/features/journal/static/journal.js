import {requestJSON} from "/static/js/api.js";
import {busy, cell, emptyRow, fillGroups, message} from "/static/js/ui.js";

const API = "/api/journal";
const groupSelect = document.querySelector("#journal-group");
const head = document.querySelector("#table-head");
const body = document.querySelector("#table-body");
const editor = document.querySelector("#editor");
const form = document.querySelector("#edit-form");
const markInput = document.querySelector("#grade-mark");
const deleteButton = document.querySelector("#delete-grade");

let journal = null;
let selection = null;

function saveGrade(payload) {
  return requestJSON(API + "/grades", "POST", payload);
}

function deleteGrade(studentId, subjectId) {
  return requestJSON(API + "/grades/" + studentId + "/" + subjectId, "DELETE");
}

function render() {
  const {students, subjects, grades} = journal;
  const columns = ["Студент", ...subjects.map((subject) => subject.name)];
  head.replaceChildren();
  for (const name of columns) {
    const heading = document.createElement("th");
    heading.scope = "col";
    heading.textContent = name;
    head.append(heading);
  }
  body.replaceChildren();
  if (!students.length) {
    emptyRow(body, columns.length, "В группе нет студентов");
    return;
  }

  const marks = new Map(grades.map((grade) => [grade.student_id + ":" + grade.subject_id, grade.mark]));
  for (const student of students) {
    const row = document.createElement("tr");
    row.append(cell(student.name));
    for (const subject of subjects) {
      const mark = marks.get(student.id + ":" + subject.id);
      const button = document.createElement("button");
      button.type = "button";
      button.className = "grade-button";
      button.classList.toggle("empty", mark === undefined);
      button.classList.toggle("failing", mark === 2);
      button.dataset.studentId = String(student.id);
      button.dataset.subjectId = String(subject.id);
      button.dataset.mark = mark === undefined ? "" : String(mark);
      button.textContent = mark ?? "—";
      button.setAttribute("aria-label", student.name + ", " + subject.name + ", " + (mark ?? "нет оценки"));
      const gradeCell = document.createElement("td");
      gradeCell.className = "grade-cell";
      gradeCell.append(button);
      row.append(gradeCell);
    }
    body.append(row);
  }
}

async function load(successText = "") {
  busy(true);
  message("Загрузка...");
  try {
    const params = new URLSearchParams({group_id: groupSelect.value});
    journal = await requestJSON(API + "?" + params);
    render();
    message(successText);
  } catch (error) {
    if (journal) groupSelect.value = String(journal.group.id);
    else emptyRow(body, 1, "Данные не загружены");
    message((successText ? successText + " Обновление журнала не удалось. " : "") + error.message, true);
  } finally {
    busy(false);
  }
}

async function start() {
  busy(true);
  message("Загрузка...");
  try {
    const {items} = await requestJSON("/api/groups");
    fillGroups(groupSelect, items);
    if (items.length) {
      await load();
    } else {
      emptyRow(body, 1, "Сначала добавьте группу");
      message();
    }
  } catch (error) {
    emptyRow(body, 1, "Данные не загружены");
    message(error.message, true);
  } finally {
    busy(false);
  }
}

function closeEditor() {
  editor.hidden = true;
  selection = null;
}

groupSelect.addEventListener("change", () => {
  closeEditor();
  load();
});

body.addEventListener("click", (event) => {
  const button = event.target.closest("button[data-student-id]");
  if (!button) return;
  const studentId = Number(button.dataset.studentId);
  const subjectId = Number(button.dataset.subjectId);
  const student = journal.students.find((item) => item.id === studentId);
  const subject = journal.subjects.find((item) => item.id === subjectId);
  selection = {student_id: studentId, subject_id: subjectId};
  markInput.value = button.dataset.mark;
  deleteButton.hidden = button.dataset.mark === "";
  document.querySelector("#grade-context").textContent = student.name + " · " + subject.name;
  editor.hidden = false;
  message();
  markInput.focus();
});

document.querySelector("#cancel-edit").addEventListener("click", () => {
  closeEditor();
  message();
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  if (selection === null) return;
  const payload = {...selection, mark: Number(markInput.value)};
  busy(true);
  try {
    await saveGrade(payload);
    closeEditor();
    await load("Оценка сохранена.");
  } catch (error) {
    message(error.message, true);
  } finally {
    busy(false);
  }
});

deleteButton.addEventListener("click", async () => {
  if (selection === null) return;
  busy(true);
  try {
    await deleteGrade(selection.student_id, selection.subject_id);
    closeEditor();
    await load("Оценка удалена.");
  } catch (error) {
    message(error.message, true);
  } finally {
    busy(false);
  }
});

start();
