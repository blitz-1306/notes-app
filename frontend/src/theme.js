const STORAGE_KEY = 'notes_theme';
export const THEMES = ['light', 'dark', 'system'];

export function getThemePref() {
  const v = localStorage.getItem(STORAGE_KEY);
  return THEMES.includes(v) ? v : 'system';
}

export function setThemePref(pref) {
  localStorage.setItem(STORAGE_KEY, pref);
  applyTheme();
}

function resolve(pref) {
  if (pref === 'system') {
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }
  return pref;
}

export function applyTheme() {
  document.documentElement.setAttribute('data-theme', resolve(getThemePref()));
}

export function initTheme() {
  applyTheme();
  const mql = window.matchMedia('(prefers-color-scheme: dark)');
  const onChange = () => {
    if (getThemePref() === 'system') applyTheme();
  };
  if (mql.addEventListener) mql.addEventListener('change', onChange);
  else mql.addListener(onChange);
}
