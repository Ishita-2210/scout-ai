import { useState } from "react";
import type { RefObject } from "react";
import { ArrowRight, Compass, X } from "lucide-react";
import { deleteAllData } from "../services/api";

export default function AboutDialog({
  dialogRef,
  busy,
  onDeleted,
  onError,
}: {
  dialogRef: RefObject<HTMLDialogElement | null>;
  busy: boolean;
  onDeleted: () => void;
  onError: (message: string) => void;
}) {
  const [confirmDelete, setConfirmDelete] = useState(false);
  const [deleting, setDeleting] = useState(false);
  async function removeData() {
    if (deleting || busy) return;
    setDeleting(true);
    try {
      await deleteAllData();
      onDeleted();
      dialogRef.current?.close();
    } catch (error) {
      onError(
        error instanceof Error
          ? error.message
          : "Your data could not be deleted. Please try again.",
      );
      dialogRef.current?.close();
    } finally {
      setDeleting(false);
      setConfirmDelete(false);
    }
  }
  return (
    <dialog
      ref={dialogRef}
      className="about-dialog"
      aria-labelledby="about-title"
      onClose={() => setConfirmDelete(false)}
      onClick={(event) => {
        if (event.target === event.currentTarget) dialogRef.current?.close();
      }}
    >
      <button
        className="icon-button dialog-close"
        onClick={() => dialogRef.current?.close()}
        aria-label="Close about Scout"
      >
        <X size={20} />
      </button>
      <Compass size={30} />
      <p className="eyebrow">EDUCATION, CONTINUED.</p>
      <h2 id="about-title">Meet your next step.</h2>
      <p>
        Scout helps displaced students and families reconnect with education:
        schools, scholarships, documents, housing, education rights, and
        learning support.
      </p>
      <h3>Make it personal, at your pace.</h3>
      <p>
        Share your city, grade, and what you need help with. Avoid passwords,
        identity numbers, or sensitive documents. Scout offers guidance; confirm
        important decisions with official sources.
      </p>
      <h3>Your conversations & privacy</h3>
      <p>
        This browser has an anonymous session. Conversations and basic details
        you share are stored on the server. Your questions and relevant recent
        context are sent to the AI provider. When live search is available,
        focused search terms are sent to the search provider. Use a private
        device and delete conversations with the trash control.
      </p>
      <p>
        Deleting a conversation removes its messages. Use “Delete all my data”
        to remove all conversations and remembered profile details from this
        session. Backups and provider records follow their own retention
        policies.
      </p>
      {confirmDelete ? (
        <div className="delete-confirmation">
          <p>
            This permanently removes your saved conversations and remembered
            details from Scout.
          </p>
          <button
            className="danger-button"
            disabled={deleting || busy}
            onClick={() => void removeData()}
          >
            {deleting ? "Deleting…" : "Confirm delete all my data"}
          </button>
          <button
            className="icon-button"
            disabled={deleting}
            onClick={() => setConfirmDelete(false)}
          >
            Keep my data
          </button>
        </div>
      ) : (
        <button
          className="danger-button"
          disabled={busy}
          onClick={() => setConfirmDelete(true)}
        >
          Delete all my data
        </button>
      )}
      <button
        className="dialog-done"
        onClick={() => dialogRef.current?.close()}
      >
        Got it <ArrowRight size={16} />
      </button>
    </dialog>
  );
}
