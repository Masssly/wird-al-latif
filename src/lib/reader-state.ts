import { useCallback, useEffect, useState } from "react";
import { defaultWhen, type When } from "./wird";

/** Everything here stays on the reader's device (localStorage). No accounts, no tracking. */
export type Settings = {
  size: number; // 0..4
  theme: "system" | "light" | "dark";
  translit: boolean;
  meaning: boolean;
};
const DEFAULTS: Settings = { size: 1, theme: "system", translit: true, meaning: true };
const KEY = "wird:settings";

function load<T>(key: string, fallback: T): T {
  try {
    const v = localStorage.getItem(key);
    return v ? { ...fallback, ...JSON.parse(v) } : fallback;
  } catch {
    return fallback;
  }
}

export function applyTheme(theme: Settings["theme"]) {
  const dark =
    theme === "dark" || (theme === "system" && window.matchMedia("(prefers-color-scheme: dark)").matches);
  document.documentElement.classList.toggle("dark", dark);
}

export function useSettings() {
  const [settings, setSettings] = useState<Settings>(DEFAULTS);
  useEffect(() => setSettings(load(KEY, DEFAULTS)), []);
  const update = useCallback((patch: Partial<Settings>) => {
    setSettings((s) => {
      const next = { ...s, ...patch };
      localStorage.setItem(KEY, JSON.stringify(next));
      if (patch.theme) applyTheme(next.theme);
      return next;
    });
  }, []);
  return [settings, update] as const;
}

const today = () => new Date().toLocaleDateString("en-CA");

/** Tap counts for one sitting (today + morning/evening). */
export function useProgress(when: When) {
  const key = `wird:progress:${today()}:${when}`;
  const [counts, setCounts] = useState<Record<string, number>>({});
  useEffect(() => setCounts(load(key, {})), [key]);
  const save = (next: Record<string, number>) => {
    localStorage.setItem(key, JSON.stringify(next));
    return next;
  };
  const tap = useCallback(
    (id: string, max: number) =>
      setCounts((c) => save({ ...c, [id]: (c[id] ?? 0) >= max ? 0 : (c[id] ?? 0) + 1 })),
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [key],
  );
  const reset = useCallback(() => {
    localStorage.removeItem(key);
    setCounts({});
  }, [key]);
  return { counts, tap, reset };
}

export function useWhen() {
  const [when, setWhen] = useState<When>("morning");
  useEffect(() => setWhen(defaultWhen()), []);
  return [when, setWhen] as const;
}

export function useOnline() {
  const [online, setOnline] = useState(true);
  useEffect(() => {
    const up = () => setOnline(navigator.onLine);
    up();
    window.addEventListener("online", up);
    window.addEventListener("offline", up);
    return () => {
      window.removeEventListener("online", up);
      window.removeEventListener("offline", up);
    };
  }, []);
  return online;
}
