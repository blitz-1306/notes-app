import { beforeEach, describe, expect, it, vi } from 'vitest';

import { applyTheme, setThemePref } from './theme.js';

function mockPrefersDark(prefersDark) {
  window.matchMedia = vi.fn().mockImplementation((query) => ({
    matches: query.includes('dark') ? prefersDark : false,
    media: query,
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    addListener: vi.fn(),
    removeListener: vi.fn(),
    dispatchEvent: vi.fn(),
  }));
}

describe('theme', () => {
  beforeEach(() => {
    document.documentElement.removeAttribute('data-theme');
    localStorage.clear();
  });

  it('applies explicit light preference', () => {
    mockPrefersDark(true);
    setThemePref('light');
    expect(document.documentElement.getAttribute('data-theme')).toBe('light');
  });

  it('applies explicit dark preference', () => {
    mockPrefersDark(false);
    setThemePref('dark');
    expect(document.documentElement.getAttribute('data-theme')).toBe('dark');
  });

  it('resolves "system" to the OS preference', () => {
    mockPrefersDark(true);
    setThemePref('system');
    expect(document.documentElement.getAttribute('data-theme')).toBe('dark');

    mockPrefersDark(false);
    applyTheme();
    expect(document.documentElement.getAttribute('data-theme')).toBe('light');
  });
});
