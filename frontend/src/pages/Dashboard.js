import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  createStudent,
  fetchStudents,
  getApiError,
  removeStudent,
  updateStudent,
} from "../api/scholarsyncApi";
import {
  CalendarIcon,
  EditIcon,
  FilterIcon,
  GradeIcon,
  LogoIcon,
  LogoutIcon,
  MailIcon,
  PhoneIcon,
  PlusIcon,
  SearchIcon,
  TrashIcon,
  UserIcon,
} from "../components/Icons";
import StudentModal from "../components/StudentModal";
import { clearStoredUser, getStoredUser } from "../utils/session";

function formatEnrollmentDate(dateString) {
  if (!dateString) {
    return "TODAY";
  }

  return new Date(dateString)
    .toLocaleDateString("en-US", {
      month: "short",
      day: "2-digit",
      year: "numeric",
    })
    .toUpperCase();
}

function buildInitials(name) {
  return (name || "S")
    .split(" ")
    .filter(Boolean)
    .slice(0, 2)
    .map((part) => part[0].toUpperCase())
    .join("");
}

export default function Dashboard() {
  const navigate = useNavigate();
  const [user] = useState(() => getStoredUser());
  const [students, setStudents] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [pageError, setPageError] = useState("");
  const [modalMode, setModalMode] = useState(null);
  const [activeStudent, setActiveStudent] = useState(null);
  const [modalError, setModalError] = useState("");
  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => {
    let isMounted = true;
    const timer = setTimeout(async () => {
      if (!user?.id) {
        return;
      }

      try {
        if (isMounted) {
          setPageError("");
          setIsLoading(true);
        }

        const data = await fetchStudents(user.id, searchTerm);

        if (isMounted) {
          setStudents(data);
        }
      } catch (requestError) {
        if (isMounted) {
          setPageError(getApiError(requestError, "Unable to load students"));
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    }, 180);

    return () => {
      isMounted = false;
      clearTimeout(timer);
    };
  }, [searchTerm, user?.id]);

  const openCreateModal = () => {
    setModalError("");
    setActiveStudent(null);
    setModalMode("create");
  };

  const openEditModal = (student) => {
    setModalError("");
    setActiveStudent(student);
    setModalMode("edit");
  };

  const closeModal = () => {
    setModalError("");
    setActiveStudent(null);
    setModalMode(null);
  };

  const refreshStudents = async () => {
    const data = await fetchStudents(user.id, searchTerm);
    setStudents(data);
  };

  const handleStudentSubmit = async (payload) => {
    setModalError("");
    setIsSaving(true);

    try {
      if (modalMode === "edit" && activeStudent) {
        await updateStudent(user.id, activeStudent.id, payload);
      } else {
        await createStudent(user.id, payload);
      }

      await refreshStudents();
      closeModal();
    } catch (requestError) {
      setModalError(getApiError(requestError, "Unable to save student"));
    } finally {
      setIsSaving(false);
    }
  };

  const handleDelete = async (student) => {
    const shouldDelete = window.confirm(`Delete ${student.name}?`);
    if (!shouldDelete) {
      return;
    }

    try {
      setPageError("");
      await removeStudent(user.id, student.id);
      await refreshStudents();
    } catch (requestError) {
      setPageError(getApiError(requestError, "Unable to delete student"));
    }
  };

  const handleLogout = () => {
    clearStoredUser();
    navigate("/");
  };

  const uniqueGrades = new Set(
    students.map((student) => student.grade.trim()).filter(Boolean)
  ).size;

  const recentStudents = students.filter((student) => {
    if (!student.created_at) {
      return false;
    }

    const createdAt = new Date(student.created_at);
    const thirtyDaysAgo = new Date();
    thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);
    return createdAt >= thirtyDaysAgo;
  }).length;

  return (
    <main className={`dashboard-page ${modalMode ? "modal-open" : ""}`}>
      <header className="dashboard-topbar">
        <div className="dashboard-shell topbar-content">
          <div className="brand-lockup">
            <div className="brand-logo">
              <LogoIcon className="icon-lg" />
            </div>
            <span className="brand-title">ScholarSync</span>
          </div>

          <div className="topbar-actions">
            <div className="user-pill">
              <span className="user-avatar">
                {buildInitials(user?.full_name || user?.username)}
              </span>
              <span>{user?.full_name || user?.username}</span>
            </div>
            <button
              type="button"
              className="icon-button logout-button"
              onClick={handleLogout}
              aria-label="Log out"
              title="Log out"
            >
              <LogoutIcon className="icon-md" />
            </button>
          </div>
        </div>
      </header>

      <section className="dashboard-shell dashboard-content">
        <div className="dashboard-toolbar">
          <label className="search-field">
            <SearchIcon className="icon-md search-icon" />
            <input
              type="text"
              placeholder="Search students by name, email or grade..."
              value={searchTerm}
              onChange={(event) => setSearchTerm(event.target.value)}
            />
          </label>

          <button type="button" className="primary-button dashboard-add" onClick={openCreateModal}>
            <PlusIcon className="icon-md" />
            <span>Add Student</span>
          </button>
        </div>

        <div className="stats-grid">
          <article className="stat-card">
            <div className="stat-icon indigo">
              <UserIcon className="icon-md" />
            </div>
            <div>
              <p>Total Students</p>
              <h3>{students.length}</h3>
            </div>
          </article>

          <article className="stat-card">
            <div className="stat-icon green">
              <CalendarIcon className="icon-md" />
            </div>
            <div>
              <p>Recently Added</p>
              <h3>{recentStudents}</h3>
            </div>
          </article>

          <article className="stat-card">
            <div className="stat-icon amber">
              <FilterIcon className="icon-md" />
            </div>
            <div>
              <p>Grades Tracked</p>
              <h3>{uniqueGrades}</h3>
            </div>
          </article>
        </div>

        {pageError ? <div className="auth-alert page-alert">{pageError}</div> : null}

        {isLoading ? (
          <div className="empty-state">
            <div className="empty-state-icon">
              <UserIcon className="icon-xl muted" />
            </div>
            <h2>Loading students...</h2>
            <p>Please wait while we fetch your student list.</p>
          </div>
        ) : students.length === 0 ? (
          <div className="empty-state">
            <div className="empty-state-icon">
              <UserIcon className="icon-xl muted" />
            </div>
            <h2>No students found</h2>
            <p>
              {searchTerm
                ? "Try a different search term or clear the filter."
                : "Get started by adding your first student."}
            </p>
            {!searchTerm ? (
              <button type="button" className="secondary-button" onClick={openCreateModal}>
                Add New Student
              </button>
            ) : null}
          </div>
        ) : (
          <div className="student-grid">
            {students.map((student) => (
              <article key={student.id} className="student-card">
                <div className="student-card-header">
                  <div className="student-initial">{buildInitials(student.name)}</div>
                  <div className="student-actions">
                    <button
                      type="button"
                      className="icon-button"
                      onClick={() => openEditModal(student)}
                      aria-label={`Edit ${student.name}`}
                    >
                      <EditIcon className="icon-sm" />
                    </button>
                    <button
                      type="button"
                      className="icon-button"
                      onClick={() => handleDelete(student)}
                      aria-label={`Delete ${student.name}`}
                    >
                      <TrashIcon className="icon-sm" />
                    </button>
                  </div>
                </div>

                <h3>{student.name}</h3>

                <div className="student-meta">
                  <div>
                    <MailIcon className="icon-sm" />
                    <span>{student.email}</span>
                  </div>
                  <div>
                    <PhoneIcon className="icon-sm" />
                    <span>{student.phone}</span>
                  </div>
                  <div>
                    <GradeIcon className="icon-sm" />
                    <span>Grade: {student.grade}</span>
                  </div>
                </div>

                <div className="student-footer">
                  <span>ENROLLED</span>
                  <span>{formatEnrollmentDate(student.enrolled_at || student.created_at)}</span>
                </div>
              </article>
            ))}
          </div>
        )}
      </section>

      {modalMode ? (
        <StudentModal
          mode={modalMode}
          initialStudent={activeStudent}
          error={modalError}
          isSaving={isSaving}
          onClose={closeModal}
          onSubmit={handleStudentSubmit}
        />
      ) : null}
    </main>
  );
}
