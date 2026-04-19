import { LANGS, useLang } from '../i18n.jsx';

const FLAGS = { en: '🇬🇧', ru: '🇷🇺' };

export default function LanguageToggle() {
  const { lang, setLang, t } = useLang();

  const cycle = () => {
    const next = LANGS[(LANGS.indexOf(lang) + 1) % LANGS.length];
    setLang(next);
  };

  return (
    <button
      type="button"
      className="lang-toggle"
      onClick={cycle}
      title={`Language: ${t(`lang.label.${lang}`)} · click to change`}
      aria-label={`Language: ${t(`lang.label.${lang}`)}, click to change`}
    >
      <span className="theme-icon">{FLAGS[lang]}</span>
      <span className="lang-label">{t(`lang.label.${lang}`)}</span>
    </button>
  );
}
