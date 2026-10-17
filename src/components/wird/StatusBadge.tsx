import type { LangMeta } from "@/lib/wird";

const LABEL: Record<LangMeta["status"], string> = {
  draft: "Draft · not yet proofread",
  reviewed: "Reviewed",
  verified: "Verified",
};

export function StatusBadge({ status, short = true }: { status: LangMeta["status"]; short?: boolean }) {
  const cls =
    status === "verified"
      ? "bg-nabi/15 text-nabi"
      : status === "reviewed"
        ? "bg-moon text-moon-foreground"
        : "bg-sun text-sun-foreground";
  return (
    <span className={`inline-flex items-center rounded-full px-2 py-0.5 text-[0.68rem] font-semibold ${cls}`}>
      {short ? status[0].toUpperCase() + status.slice(1) : LABEL[status]}
    </span>
  );
}
