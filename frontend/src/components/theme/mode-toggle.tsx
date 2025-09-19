"use client";

import * as React from "react";
import { Sun, Moon } from "lucide-react";
import { useTheme } from "next-themes";
import { Button } from "@/components/ui/button";

export function ModeToggle() {
  const { theme, setTheme } = useTheme();
  const [mounted, setMounted] = React.useState(false);

  React.useEffect(() => setMounted(true), []);

  if (!mounted) {
    return <div className="h-8 w-16 animate-pulse rounded-full bg-gray-200" />;
  }

  const isDark = theme === "dark";

  return (
    <Button
      variant="ghost"
      size="sm"
      className="group relative h-8 w-16 rounded-full border-0 bg-gradient-to-r from-orange-100 to-blue-100 p-0 transition-all duration-300 ease-in-out hover:from-orange-200 hover:to-blue-200 focus:ring-2 focus:ring-blue-500/20 focus:outline-none dark:from-gray-800 dark:to-gray-900 dark:hover:from-gray-700 dark:hover:to-gray-800"
      onClick={() => setTheme(isDark ? "light" : "dark")}
      aria-label={`Switch to ${isDark ? "light" : "dark"} mode`}
    >
      {/* Background glow effect */}
      <div className="absolute inset-0 rounded-full bg-gradient-to-r from-orange-400/20 to-blue-400/20 opacity-0 transition-opacity duration-300 group-hover:opacity-100 dark:from-blue-400/20 dark:to-purple-400/20" />

      {/* Sliding circle with enhanced styling */}
      <div
        className={`absolute top-1 ${
          isDark ? "left-9" : "left-1"
        } h-6 w-6 transform rounded-full border border-gray-200/50 bg-white shadow-lg transition-all duration-300 ease-out dark:border-gray-300/20 dark:bg-gray-100`}
        style={{
          boxShadow: isDark
            ? "0 4px 12px rgba(59, 130, 246, 0.3), 0 2px 4px rgba(0, 0, 0, 0.1)"
            : "0 4px 12px rgba(251, 146, 60, 0.3), 0 2px 4px rgba(0, 0, 0, 0.1)",
        }}
      >
        {/* Inner glow */}
        <div
          className={`absolute inset-0 rounded-full transition-all duration-300 ${
            isDark
              ? "bg-gradient-to-br from-blue-400/30 to-purple-400/30"
              : "bg-gradient-to-br from-orange-400/30 to-yellow-400/30"
          }`}
        />
      </div>

      {/* Sun icon with enhanced styling */}
      <Sun
        className={`absolute top-2 left-2 h-4 w-4 transition-all duration-300 ${
          isDark
            ? "scale-75 rotate-90 text-orange-300 opacity-0"
            : "scale-100 rotate-0 text-orange-500 opacity-100"
        }`}
        style={{
          filter: isDark
            ? "none"
            : "drop-shadow(0 0 4px rgba(251, 146, 60, 0.4))",
        }}
      />

      {/* Moon icon with enhanced styling */}
      <Moon
        className={`absolute top-2 right-2 h-4 w-4 transition-all duration-300 ${
          isDark
            ? "scale-100 rotate-0 text-blue-400 opacity-100"
            : "scale-75 -rotate-90 text-blue-300 opacity-0"
        }`}
        style={{
          filter: isDark
            ? "drop-shadow(0 0 4px rgba(59, 130, 246, 0.4))"
            : "none",
        }}
      />

      {/* Subtle animation particles */}
      <div
        className={`absolute inset-0 overflow-hidden rounded-full transition-opacity duration-500 ${
          isDark ? "opacity-100" : "opacity-0"
        }`}
      >
        <div className="absolute top-1 right-3 h-0.5 w-0.5 animate-pulse rounded-full bg-blue-300" />
        <div className="absolute top-3 right-2 h-0.5 w-0.5 animate-pulse rounded-full bg-purple-300 delay-75" />
        <div className="absolute top-5 right-4 h-0.5 w-0.5 animate-pulse rounded-full bg-blue-300 delay-150" />
      </div>

      <div
        className={`absolute inset-0 overflow-hidden rounded-full transition-opacity duration-500 ${
          isDark ? "opacity-0" : "opacity-100"
        }`}
      >
        <div className="absolute top-2 left-3 h-0.5 w-0.5 animate-pulse rounded-full bg-orange-300" />
        <div className="absolute top-4 left-2 h-0.5 w-0.5 animate-pulse rounded-full bg-yellow-300 delay-100" />
      </div>
    </Button>
  );
}
