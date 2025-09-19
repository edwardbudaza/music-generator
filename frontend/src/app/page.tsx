import Link from "next/link";
import { ModeToggle } from "@/components/theme/mode-toggle";

export default function HomePage() {
  return (
    <div>
      This is home
      <ModeToggle />
    </div>
  );
}
