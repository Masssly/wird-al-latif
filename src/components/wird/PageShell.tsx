import { Link } from "@tanstack/react-router";
import { ChevronLeft } from "lucide-react";
import type { ReactNode } from "react";

export function PageShell({ title, children }: { title: string; children: ReactNode }) {
  return (
    <div className="min-h-dvh bg-background">
      <header className="sticky top-0 z-10 border-b border-border bg-background/90 pt-safe backdrop-blur">
        <div className="mx-auto flex h-14 max-w-2xl items-center gap-2 px-3">
          <Link to="/" className="-ml-1 flex size-11 items-center justify-center rounded-full" aria-label="Home">
            <ChevronLeft className="size-5" />
          </Link>
          <h1 className="font-serif text-xl font-bold">{title}</h1>
        </div>
      </header>
      <main className="prose-wird mx-auto max-w-2xl space-y-4 px-5 py-6 pb-safe text-[0.95rem] leading-relaxed">
        {children}
      </main>
    </div>
  );
}

export function H2({ children }: { children: ReactNode }) {
  return <h2 className="pt-4 text-xs font-bold uppercase tracking-widest text-gold">{children}</h2>;
}

export function A({ href, children }: { href: string; children: ReactNode }) {
  return (
    <a href={href} className="break-words text-primary underline underline-offset-2" rel="noreferrer" target="_blank">
      {children}
    </a>
  );
}
