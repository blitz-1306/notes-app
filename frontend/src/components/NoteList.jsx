import { useLang } from '../i18n.jsx';

export default function NoteList({
  notes,
  selectedId,
  onSelect,
  bulkMode = false,
  selectedIds = new Set(),
  onToggleSelect,
}) {
  const { t } = useLang();
  if (!notes.length) {
    return (
      <div className="empty-state" style={{ padding: '1.5rem' }}>
        <p style={{ fontSize: '0.9rem', margin: 0 }}>{t('notes.noMatch')}</p>
      </div>
    );
  }
  return (
    <ul className="note-list">
      {notes.map((n) => {
        const isSelected = n.id === selectedId;
        const isChecked = selectedIds.has(n.id);
        const isPinned = Boolean(n.pinned_at);
        const isArchived = Boolean(n.archived_at);
        const classes = [
          'note-item',
          isSelected ? 'selected' : '',
          isArchived ? 'archived' : '',
          isChecked ? 'checked' : '',
        ].filter(Boolean).join(' ');

        const onClick = () => {
          if (bulkMode) onToggleSelect?.(n.id);
          else onSelect(n);
        };

        return (
          <li key={n.id} className={classes} onClick={onClick}>
            {bulkMode && (
              <input
                type="checkbox"
                checked={isChecked}
                onChange={() => onToggleSelect?.(n.id)}
                onClick={(e) => e.stopPropagation()}
                className="note-item-checkbox"
              />
            )}
            <div className="note-item-body">
              <div className="note-item-title">
                {isPinned && <span className="pin-ind" title={t('notes.pinned')}>📌</span>}
                {n.title}
              </div>
              <div className="note-item-meta">
                {n.note_date && <span className="date-pill">📅 {n.note_date}</span>}
                {(n.tags || []).slice(0, 3).map((tag) => (
                  <span key={tag} className="tag">#{tag}</span>
                ))}
              </div>
            </div>
          </li>
        );
      })}
    </ul>
  );
}
