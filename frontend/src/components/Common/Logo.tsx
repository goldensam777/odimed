import { Link } from "@tanstack/react-router"
import { HeartPulse } from "lucide-react"

import { cn } from "@/lib/utils"

interface LogoProps {
  variant?: "full" | "icon" | "responsive"
  className?: string
  asLink?: boolean
}

export function Logo({
  variant = "full",
  className,
  asLink = true,
}: LogoProps) {
  const content =
    variant === "responsive" ? (
      <>
        <div
          className={cn(
            "flex items-center gap-2 group-data-[collapsible=icon]:hidden",
            className,
          )}
        >
          <div className="relative flex items-center justify-center bg-primary/10 p-1.5 rounded-lg">
            <HeartPulse className="h-6 w-6 text-primary animate-[pulse_2s_ease-in-out_infinite]" />
            <div className="absolute inset-0 bg-primary/20 rounded-lg blur-md -z-10 animate-pulse" />
          </div>
          <span className="font-extrabold text-2xl tracking-tighter bg-gradient-to-br from-primary to-emerald-500 bg-clip-text text-transparent">
            Odimed
          </span>
        </div>
        <div
          className={cn(
            "hidden group-data-[collapsible=icon]:flex items-center justify-center bg-primary/10 p-1.5 rounded-lg",
            className,
          )}
        >
          <HeartPulse className="h-5 w-5 text-primary animate-[pulse_2s_ease-in-out_infinite]" />
        </div>
      </>
    ) : (
      <div className={cn("flex items-center gap-2", className)}>
        <div className="relative flex items-center justify-center bg-primary/10 p-1.5 rounded-lg">
          <HeartPulse
            className={cn(
              variant === "full" ? "h-6 w-6" : "h-5 w-5",
              "text-primary animate-[pulse_2s_ease-in-out_infinite]",
            )}
          />
          <div className="absolute inset-0 bg-primary/20 rounded-lg blur-md -z-10 animate-pulse" />
        </div>
        {variant === "full" && (
          <span className="font-extrabold text-2xl tracking-tighter bg-gradient-to-br from-primary to-emerald-500 bg-clip-text text-transparent">
            Odimed
          </span>
        )}
      </div>
    )

  if (!asLink) {
    return content
  }

  return <Link to="/">{content}</Link>
}
