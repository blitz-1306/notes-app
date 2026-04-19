import { useLang } from '../i18n.jsx';

function surround(textarea, before, after = before, placeholder = '') {
  if (!textarea) return;
  const { selectionStart: s, selectionEnd: e, value } = textarea;
  const selected = value.slice(s, e) || placeholder;
  const next = value.slice(0, s) + before + selected + after + value.slice(e);
  const cursorStart = s + before.length;
  const cursorEnd = cursorStart + selected.length;
  const inputEvent = new Event('input', { bubbles: true });
  const descriptor = Object.getOwnPropertyDescriptor(
    window.HTMLTextAreaElement.prototype, 'value'
  );
  descriptor.set.call(textarea, next);
  textarea.dispatchEvent(inputEvent);
  textarea.focus();
  textarea.setSelectionRange(cursorStart, cursorEnd);
}

function prefixLines(textarea, prefix) {
  if (!textarea) return;
  const { selectionStart: s, selectionEnd: e, value } = textarea;
  const lineStart = value.lastIndexOf('\n', s - 1) + 1;
  const lineEnd = (() => {
    const nl = value.indexOf('\n', e);
    return nl === -1 ? value.length : nl;
  })();
  const block = value.slice(lineStart, lineEnd);
  const prefixed = block.split('\n').map((l) => prefix + l).join('\n');
  const next = value.slice(0, lineStart) + prefixed + value.slice(lineEnd);
  const descriptor = Object.getOwnPropertyDescriptor(
    window.HTMLTextAreaElement.prototype, 'value'
  );
  descriptor.set.call(textarea, next);
  textarea.dispatchEvent(new Event('input', { bubbles: true }));
  textarea.focus();
  textarea.setSelectionRange(lineStart, lineStart + prefixed.length);
}

export default function MarkdownToolbar({ textareaRef }) {
  const { t } = useLang();
  const ta = () => textareaRef.current;

  const actions = [
    { label: 'B', title: t('editor.toolbarBold'), cls: 'tb-bold', onClick: () => surround(ta(), '**', '**', 'bold') },
    { label: 'I', title: t('editor.toolbarItalic'), cls: 'tb-italic', onClick: () => surround(ta(), '*', '*', 'italic') },
    { label: 'H', title: t('editor.toolbarHeading'), onClick: () => prefixLines(ta(), '## ') },
    { label: '•', title: t('editor.toolbarList'), onClick: () => prefixLines(ta(), '- ') },
    { label: '❝', title: t('editor.toolbarQuote'), onClick: () => prefixLines(ta(), '> ') },
    { label: '</>', title: t('editor.toolbarCode'), onClick: () => surround(ta(), '`', '`', 'code') },
    { label: '🔗', title: t('editor.toolbarLink'), onClick: () => surround(ta(), '[', '](https://)', 'text') },
  ];

  return (
    <div className="md-toolbar" role="toolbar" aria-label="Markdown toolbar">
      {actions.map((a) => (
        <button
          key={a.title}
          type="button"
          className={`tb-btn ${a.cls || ''}`}
          title={a.title}
          aria-label={a.title}
          onMouseDown={(e) => e.preventDefault()}
          onClick={a.onClick}
        >
          {a.label}
        </button>
      ))}
    </div>
  );
}
