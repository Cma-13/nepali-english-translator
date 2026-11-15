// Small behaviours shared by every page. No libraries needed.

// Copy button: <button data-copy="#id-of-text">
document.addEventListener("click", (event) => {
    const button = event.target.closest("[data-copy]");
    if (!button) return;

    const source = document.querySelector(button.dataset.copy);
    const text = "value" in source ? source.value : source.innerText;
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

// Eye button on every password field: click to show or hide what you typed.
const EYE_OPEN = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7-10-7-10-7z"/><circle cx="12" cy="12" r="3"/></svg>';
const EYE_CLOSED = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M10.6 5.1A10.9 10.9 0 0 1 12 5c6.4 0 10 7 10 7a17.6 17.6 0 0 1-3.2 4.1M6.6 6.6C3.6 8.5 2 12 2 12s3.6 7 10 7a10.7 10.7 0 0 0 5.4-1.5"/><path d="M9.9 9.9a3 3 0 0 0 4.2 4.2"/><path d="M3 3l18 18"/></svg>';

document.querySelectorAll('input[type="password"]').forEach((input) => {
    const wrap = document.createElement("div");
    wrap.className = "password-wrap";
    input.before(wrap);
    wrap.append(input);

    const button = document.createElement("button");
    button.type = "button";
    button.className = "eye";
    button.innerHTML = EYE_OPEN;
    button.setAttribute("aria-label", "Show password");
    wrap.append(button);

    button.addEventListener("click", () => {
        const show = input.type === "password";
        input.type = show ? "text" : "password";
        button.innerHTML = show ? EYE_CLOSED : EYE_OPEN;
        button.setAttribute("aria-label", show ? "Hide password" : "Show password");
        input.focus();
    });
});

// Editable letter sheet: the box grows with its text, and "Save changes"
// only lights up once something was actually changed.
document.querySelectorAll("textarea[data-autosize]").forEach((field) => {
    const resize = () => {
        field.style.height = "auto";
        field.style.height = field.scrollHeight + "px";
    };
    const saveButton = document.querySelector(field.dataset.watchChanges);
    const original = field.value;

    field.addEventListener("input", () => {
        resize();
        if (saveButton) saveButton.disabled = field.value === original;
    });
    window.addEventListener("resize", resize);
    resize();
});
