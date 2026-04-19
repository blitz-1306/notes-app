import { useEffect } from 'react';

const EDITABLE_TAGS = new Set(['INPUT', 'TEXTAREA', 'SELECT']);

function isEditable(target) {
  if (!target) return false;
  if (EDITABLE_TAGS.has(target.tagName)) return true;
  return target.isContentEditable === true;
}

export function useShortcuts(handlers) {
  useEffect(() => {
    const onKeyDown = (e) => {
      const mod = e.metaKey || e.ctrlKey;

      // Cmd/Ctrl+S: save. Works even while editing the note body.
      if (mod && !e.shiftKey && !e.altKey && e.key.toLowerCase() === 's' && handlers.onSave) {
        e.preventDefault();
        handlers.onSave();
        return;
      }

      if (isEditable(e.target)) return;

      // Plain-key shortcuts (only when not typing in an input).
      if (!mod && !e.altKey && !e.shiftKey) {
        if (e.key === 'n' && handlers.onNewNote) {
          e.preventDefault();
          handlers.onNewNote();
          return;
        }
        if (e.key === '/' && handlers.onFocusSearch) {
          e.preventDefault();
          handlers.onFocusSearch();
          return;
        }
      }
      if (e.key === '?' && handlers.onShowHelp) {
        e.preventDefault();
        handlers.onShowHelp();
        return;
      }
      if (e.key === 'Escape' && handlers.onEscape) {
        handlers.onEscape();
      }
    };

    window.addEventListener('keydown', onKeyDown);
    return () => window.removeEventListener('keydown', onKeyDown);
  }, [handlers]);
}
