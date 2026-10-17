import { Link } from "@tanstack/react-router";
import { Drawer } from "vaul";
import type { Settings } from "@/lib/reader-state";
import { getLang, LANG_ORDER } from "@/lib/wird";
import { Legend } from "./Legend";
import { StatusBadge } from "./StatusBadge";

type Props = {
  open: boolean;
  onOpenChange: (o: boolean) => void;
  settings: Settings;
  update: (p: Partial<Settings>) => void;
  current: string;
};

const SIZES = ["S", "M", "L", "XL", "XXL"];

export function ReaderSettings({ open, onOpenChange, settings, update, current }: Props) {
  return (
    <Drawer.Root open={open} onOpenChange={onOpenChange}>
      <Drawer.Portal>
        <Drawer.Overlay className="fixed inset-0 z-40 bg-foreground/30" />
        <Drawer.Content className="fixed inset-x-0 bottom-0 z-50 flex max-h-[88dvh] flex-col rounded-t-3xl bg-card outline-none">
          <div className="mx-auto mt-3 h-1.5 w-12 shrink-0 rounded-full bg-border" />
          <div className="mx-auto w-full max-w-md overflow-y-auto px-5 pt-4 pb-safe">
            <Drawer.Title className="font-serif text-xl font-bold">Reading settings</Drawer.Title>
            <Drawer.Description className="sr-only">Text size, theme, language and colour legend</Drawer.Description>

            <Group label="Text size">
              <div className="grid grid-cols-5 gap-1 rounded-full bg-muted p-1">
                {SIZES.map((s, i) => (
                  <Seg key={s} active={settings.size === i} onClick={() => update({ size: i })}>
                    {s}
                  </Seg>
                ))}
              </div>
            </Group>

            <Group label="Show">
              <Toggle label="Transliteration" on={settings.translit} onChange={(v) => update({ translit: v })} />
              <Toggle label="Meaning" on={settings.meaning} onChange={(v) => update({ meaning: v })} />
            </Group>

            <Group label="Theme">
              <div className="grid grid-cols-3 gap-1 rounded-full bg-muted p-1">
                {(["system", "light", "dark"] as const).map((t) => (
                  <Seg key={t} active={settings.theme === t} onClick={() => update({ theme: t })}>
                    {t.charAt(0).toUpperCase() + t.slice(1)}
                  </Seg>
                ))}
              </div>
            </Group>

            <Group label="Language">
              <div className="space-y-1">
                {LANG_ORDER.map((c) => {
                  const m = getLang(c).meta;
                  return (
                    <Link
                      key={c}
                      to="/$lang"
                      params={{ lang: c }}
                      onClick={() => onOpenChange(false)}
                      className={`flex min-h-11 items-center justify-between rounded-xl px-3 ${
                        c === current ? "bg-secondary font-semibold" : ""
                      }`}
                    >
                      <span>{m.native_name}</span>
                      <StatusBadge status={m.status} />
                    </Link>
                  );
                })}
              </div>
            </Group>

            <Group label="Colours">
              <Legend />
            </Group>
            <div className="h-6" />
          </div>
        </Drawer.Content>
      </Drawer.Portal>
    </Drawer.Root>
  );
}

function Group({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div className="mt-5">
      <p className="mb-2 text-xs font-bold uppercase tracking-widest text-gold">{label}</p>
      {children}
    </div>
  );
}

function Seg({ active, onClick, children }: { active: boolean; onClick: () => void; children: React.ReactNode }) {
  return (
    <button
      type="button"
      aria-pressed={active}
      onClick={onClick}
      className={`min-h-11 rounded-full text-sm font-semibold ${active ? "bg-card text-foreground shadow-sm" : "text-muted-foreground"}`}
    >
      {children}
    </button>
  );
}

function Toggle({ label, on, onChange }: { label: string; on: boolean; onChange: (v: boolean) => void }) {
  return (
    <button
      type="button"
      role="switch"
      aria-checked={on}
      onClick={() => onChange(!on)}
      className="flex min-h-11 w-full items-center justify-between"
    >
      <span>{label}</span>
      <span className={`relative h-7 w-12 rounded-full transition-colors ${on ? "bg-primary" : "bg-muted"}`}>
        <span
          className={`absolute top-1 size-5 rounded-full bg-card shadow transition-all ${on ? "left-6" : "left-1"}`}
        />
      </span>
    </button>
  );
}
