// A line that slides in over the viewport when something needs saying out loud
// — today only the check rejecting a formula, where the reason is in the chat
// but the operator is probably looking at the bench. It says what it understood
// and what it needs, and goes away on its own.
import { useEffect } from "react";

const DISMISS_MS = 9000;

export default function Toast({ toast, onDismiss }) {
  useEffect(() => {
    if (!toast) return undefined;
    const timer = setTimeout(onDismiss, DISMISS_MS);
    return () => clearTimeout(timer);
  }, [toast, onDismiss]);

  if (!toast) return null;
  return (
    <div className={`toast toast--${toast.level ?? "warn"}`} role="status">
      <div className="toast__body">
        <p className="toast__title">{toast.title}</p>
        {toast.lines?.length ? (
          <ul className="toast__lines">
            {toast.lines.map((line) => (
              <li key={line}>{line}</li>
            ))}
          </ul>
        ) : null}
        {toast.ask ? <p className="toast__ask">{toast.ask}</p> : null}
      </div>
      <button type="button" className="toast__close" onClick={onDismiss} aria-label="Dismiss">
        ×
      </button>
    </div>
  );
}
