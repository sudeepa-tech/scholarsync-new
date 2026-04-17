function iconProps(className) {
  return {
    className,
    fill: "none",
    stroke: "currentColor",
    strokeLinecap: "round",
    strokeLinejoin: "round",
    strokeWidth: 1.8,
  };
}

export function LogoIcon({ className = "" }) {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true" {...iconProps(className)}>
      <path d="M3 8.75 12 4l9 4.75L12 13.5 3 8.75Z" />
      <path d="M7 10.8v4.6c0 .5 2.24 2.6 5 2.6s5-2.1 5-2.6v-4.6" />
    </svg>
  );
}

export function SearchIcon({ className = "" }) {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true" {...iconProps(className)}>
      <circle cx="11" cy="11" r="6.5" />
      <path d="m16 16 4.5 4.5" />
    </svg>
  );
}

export function PlusIcon({ className = "" }) {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true" {...iconProps(className)}>
      <path d="M12 5v14M5 12h14" />
    </svg>
  );
}

export function UserIcon({ className = "" }) {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true" {...iconProps(className)}>
      <circle cx="12" cy="8" r="3.6" />
      <path d="M5.5 19a6.5 6.5 0 0 1 13 0" />
    </svg>
  );
}

export function CalendarIcon({ className = "" }) {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true" {...iconProps(className)}>
      <path d="M7 3.5v3M17 3.5v3M4 9h16" />
      <rect x="4" y="5.5" width="16" height="14" rx="2.5" />
    </svg>
  );
}

export function FilterIcon({ className = "" }) {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true" {...iconProps(className)}>
      <path d="M4 5h16l-6 7v5l-4 2v-7L4 5Z" />
    </svg>
  );
}

export function MailIcon({ className = "" }) {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true" {...iconProps(className)}>
      <rect x="3.5" y="5.5" width="17" height="13" rx="2.5" />
      <path d="m5.5 8 6.5 5 6.5-5" />
    </svg>
  );
}

export function PhoneIcon({ className = "" }) {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true" {...iconProps(className)}>
      <path d="M7.5 4.5c.7-.4 1.9.4 2.7 2l.5 1c.3.7.2 1.5-.3 2.1l-1.2 1.2c1.2 2.1 3 3.9 5.1 5.1l1.2-1.2c.6-.6 1.5-.7 2.1-.3l1 .5c1.6.8 2.4 2 2 2.7l-.5 1c-.6 1.3-2.1 2-3.5 1.7-7.2-1.5-12.8-7.1-14.3-14.3-.3-1.4.4-2.9 1.7-3.5l1-.5Z" />
    </svg>
  );
}

export function GradeIcon({ className = "" }) {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true" {...iconProps(className)}>
      <path d="M3.5 10 12 5l8.5 5L12 15l-8.5-5Z" />
      <path d="M7 12.2v3.6c0 .6 2.2 2.7 5 2.7s5-2.1 5-2.7v-3.6" />
    </svg>
  );
}

export function EditIcon({ className = "" }) {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true" {...iconProps(className)}>
      <path d="m4 20 4.2-1 9.6-9.6a2.1 2.1 0 0 0-3-3L5.2 16 4 20Z" />
      <path d="m13.5 7.5 3 3" />
    </svg>
  );
}

export function TrashIcon({ className = "" }) {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true" {...iconProps(className)}>
      <path d="M4.5 7.5h15" />
      <path d="M9.5 4.5h5l.8 1.5h3.2v2l-1 10.2a2 2 0 0 1-2 1.8H8.5a2 2 0 0 1-2-1.8L5.5 8V6h3.2l.8-1.5Z" />
      <path d="M10 10.5v5.5M14 10.5v5.5" />
    </svg>
  );
}

export function LogoutIcon({ className = "" }) {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true" {...iconProps(className)}>
      <path d="M9 5.5H6A2.5 2.5 0 0 0 3.5 8v8A2.5 2.5 0 0 0 6 18.5h3" />
      <path d="M13 8.5 18 12l-5 3.5" />
      <path d="M9.5 12H18" />
    </svg>
  );
}

export function CloseIcon({ className = "" }) {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true" {...iconProps(className)}>
      <path d="M6 6 18 18M18 6 6 18" />
    </svg>
  );
}
