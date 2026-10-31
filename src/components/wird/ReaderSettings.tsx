import { Link } from "@tanstack/react-router";
import { Printer } from "lucide-react";
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
  const otherLangs = LANG_ORDER.filter((c) => c !== current);
  return (
    <Drawer.Root open={open} onOpenChange={onOpenChange}>
      <Drawer.Portal>
        <Drawer.Overlay className="fixed inset-0 z-40 bg-foreground/30" />
        <Drawer.Content className="fixed inset-x-0 bottom-0 z-50 flex max-h-[88dvh] flex-col rounded-t-3xl bg-card outline-none">
          <div className="mx-auto mt-3 h-1.5 w-12 shrink-0 rounded-full bg-border" />
          <div className="mx-auto w-full max-w-md overflow-y-auto px-5 pt-4 pb-safe">
            <Drawer.Title className="font-serif text-xl font-bold">Reading settings</Drawer.Title>
            <Drawer.Description className="sr-only">
              Text size, theme, language and colour legend
            </Drawer.Description>

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
              <Toggle
                label="Transliteration"
                on={settings.translit}
                onChange={(v) => update({ translit: v })}
              />
              <Toggle
                label="Meaning"
                on={settings.meaning}
                onChange={(v) => update({ meaning: v })}
              />
              {settings.meaning && otherLangs.length > 0 && (
                <div className="mt-2 border-t border-border pt-2">
                  <p className="mb-1 text-xs text-muted-foreground">
                    Mix in another language's meaning, alongside {getLang(current).meta.native_name}
                    . A language with no meaning for a line is simply left out, not replaced by
                    another.
                  </p>
                  {otherLangs.map((c) => (
                    <Toggle
                      key={c}
                      label={getLang(c).meta.native_name}
                      on={settings.meaningLangs.includes(c)}
                      onChange={(v) =>
                        update({
                          meaningLangs: v
                            ? [...settings.meaningLangs, c]
                            : settings.meaningLangs.filter((x) => x !== c),
                        })
                      }
                    />
                  ))}
                </div>
              )}
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

            <Group label="Print or save as PDF">
              <p className="mb-2 text-xs text-muted-foreground">
                Uses exactly what's shown above: text size, transliteration, and whichever
                languages' meanings are on. There's no separate print version to keep in sync.
              </p>
              <button
                type="button"
                onClick={() => {
                  onOpenChange(false);
                  // Let the sheet finish closing so it isn't what gets printed.
                  setTimeout(() => window.print(), 300);
                }}
                className="flex min-h-11 w-full items-center justify-center gap-2 rounded-full bg-primary text-sm font-semibold text-primary-foreground"
              >
                <Printer className="size-4" /> Print this {getLang(current).meta.native_name}{" "}
                reading
              </button>
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

function Seg({
  active,
  onClick,
  children,
}: {
  active: boolean;
  onClick: () => void;
  children: React.ReactNode;
}) {
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

function Toggle({
  label,
  on,
  onChange,
}: {
  label: string;
  on: boolean;
  onChange: (v: boolean) => void;
}) {
  return (
    <button
      type="button"
      role="switch"
      aria-checked={on}
      onClick={() => onChange(!on)}
      className="flex min-h-11 w-full items-center justify-between"
    >
      <span>{label}</span>
      <span
        className={`relative h-7 w-12 rounded-full transition-colors ${on ? "bg-primary" : "bg-muted"}`}
      >
        <span
          className={`absolute top-1 size-5 rounded-full bg-card shadow transition-all ${on ? "left-6" : "left-1"}`}
        />
      </span>
    </button>
  );
}
