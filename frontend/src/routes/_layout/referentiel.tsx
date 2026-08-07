import { createFileRoute } from "@tanstack/react-router"
import { DatabaseManager } from "@/components/Admin/DatabaseManager"
import useAuth from "@/hooks/useAuth"

export const Route = createFileRoute("/_layout/referentiel")({
  component: Referentiel,
  head: () => ({
    meta: [{ title: "Référentiel - Odimed" }],
  }),
})

function Referentiel() {
  const { user } = useAuth()
  
  return (
    <div className="flex flex-col gap-6 p-4 md:p-8 w-full max-w-6xl mx-auto">
      <div>
        <h1 className="text-3xl font-bold tracking-tight text-foreground">Référentiel Thérapeutique</h1>
        <p className="text-muted-foreground mt-1">Recherche et consultation des spécialités pharmaceutiques et diagnostics (CIM-10).</p>
      </div>
      
      {/* We pass isAdmin to conditionally show/hide the 'Add' buttons if the user is a superuser */}
      <DatabaseManager isAdmin={user?.is_superuser} />
    </div>
  )
}
