import { useEffect, useState } from "react";
import { CloseIcon } from "./Icons";

const emptyForm = {
  name: "",
  email: "",
  phone: "",
  grade: "",
};

export default function StudentModal({
  mode,
  initialStudent,
  isSaving,
  error,
  onClose,
  onSubmit,
}) {
  const [form, setForm] = useState(emptyForm);

  useEffect(() => {
    if (initialStudent) {
      setForm({
        name: initialStudent.name || "",
        email: initialStudent.email || "",
        phone: initialStudent.phone || "",
        grade: initialStudent.grade || "",
      });
      return;
    }

    setForm(emptyForm);
  }, [initialStudent]);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setForm((currentForm) => ({
      ...currentForm,
      [name]: value,
    }));
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    onSubmit({
      name: form.name.trim(),
      email: form.email.trim(),
      phone: form.phone.trim(),
      grade: form.grade.trim(),
    });
  };

  return (
    <div className="modal-overlay" role="dialog" aria-modal="true">
      <div className="modal-card">
        <div className="modal-header">
          <h2>{mode === "edit" ? "Edit Student" : "Add New Student"}</h2>
          <button
            type="button"
            className="icon-button"
            onClick={onClose}
            aria-label="Close modal"
          >
            <CloseIcon className="icon-md" />
          </button>
        </div>

        <form className="modal-form" onSubmit={handleSubmit}>
          <label className="field-group">
            <span>Full Name</span>
            <input
              name="name"
              placeholder="Jane Doe"
              value={form.name}
              onChange={handleChange}
              required
            />
          </label>

          <label className="field-group">
            <span>Email Address</span>
            <input
              name="email"
              type="email"
              placeholder="jane@example.com"
              value={form.email}
              onChange={handleChange}
              required
            />
          </label>

          <label className="field-group">
            <span>Phone Number</span>
            <input
              name="phone"
              placeholder="+1 (555) 000-0000"
              value={form.phone}
              onChange={handleChange}
              required
            />
          </label>

          <label className="field-group">
            <span>Grade / Class</span>
            <input
              name="grade"
              placeholder="e.g. 10th Grade"
              value={form.grade}
              onChange={handleChange}
              required
            />
          </label>

          {error ? <div className="auth-alert">{error}</div> : null}

          <div className="modal-actions">
            <button type="button" className="secondary-button" onClick={onClose}>
              Cancel
            </button>
            <button type="submit" className="primary-button" disabled={isSaving}>
              {isSaving
                ? mode === "edit"
                  ? "Updating..."
                  : "Adding..."
                : mode === "edit"
                  ? "Update Student"
                  : "Add Student"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
