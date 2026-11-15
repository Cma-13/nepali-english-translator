// Small behaviours shared by every page. No libraries needed.

// Copy button: <button data-copy="#id-of-text">
document.addEventListener("click", (event) => {
    const button = event.target.closest("[data-copy]");
    if (!button) return;

    const text = document.querySelector(button.dataset.copy).innerText;
    navigator.clipboard.writeText(text)
        .then(() => flash(button, "Copied ✓", "is-ok"))
        .catch(() => flash(button, "Copy failed", "is-failed"));
});

function flash(button, label, className) {
    const original = button.textContent;
    button.textContent = label;
    button.classList.add(className);
    button.disabled = true;
    setTimeout(() => {
        button.textContent = original;
        button.classList.remove(className);
        button.disabled = false;
    }, 2000);
}

// Delete button asks once more before it deletes: <button data-confirm="Yes, delete">
document.addEventListener("click", (event) => {
    const button = event.target.closest("[data-confirm]");
    if (!button || button.classList.contains("confirming")) return;

    event.preventDefault();
    const original = button.textContent;
    button.textContent = button.dataset.confirm;
    button.classList.add("confirming");
    setTimeout(() => {
        button.textContent = original;
        button.classList.remove("confirming");
    }, 4000);
});

// Show a spinner while a slow form is being sent: <form data-loading="Translating…">
document.querySelectorAll("form[data-loading]").forEach((form) => {
    form.addEventListener("submit", () => {
        const button = form.querySelector("button[type=submit]");
        button.disabled = true;
        button.innerHTML = '<span class="spinner"></span>' + form.dataset.loading;
    });
});

// Live character count: <textarea maxlength="5000"> with <span data-count-for="textarea-id">
document.querySelectorAll("[data-count-for]").forEach((counter) => {
    const field = document.getElementById(counter.dataset.countFor);
    const update = () => {
        counter.textContent = field.value.length + " / " + field.maxLength;
    };
    field.addEventListener("input", update);
    update();
});

// The Preeti option only makes sense for Nepali → English.
const preetiRow = document.querySelector("[data-preeti-row]");
if (preetiRow) {
    const sync = () => {
        const nepaliSource = document.querySelector("input[name=direction]:checked")?.value === "ne_en";
        preetiRow.hidden = !nepaliSource;
        if (!nepaliSource) preetiRow.querySelector("input").checked = false;
    };
    document.querySelectorAll("input[name=direction]").forEach((radio) => radio.addEventListener("change", sync));
    sync();
}
