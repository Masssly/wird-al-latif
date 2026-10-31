import type { LangMeta } from "@/lib/wird";

/** A flag for text that's still a draft. Reviewed and verified text gets no badge at all. */
export function StatusBadge({ status }: { status: LangMeta["status"] }) {
  if (status !== "draft") return null;
  return (
    <span className="inline-flex items-center rounded-full bg-sun px-2 py-0.5 text-[0.68rem] font-semibold text-sun-foreground">
      Draft
    </span>
  );
}
