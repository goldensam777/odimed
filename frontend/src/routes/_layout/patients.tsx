import { createFileRoute } from "@tanstack/react-router"
import { Users } from "lucide-react"

export const Route = createFileRoute("/_layout/patients")({
  component: Patients,
  head: () => ({
    meta: [{ title: "Patients - Odimed" }],
  }),
})

function Patients() {
  return (
    <div className="flex flex-col gap-6 p-4 md:p-8 w-full max-w-6xl mx-auto">
      <div>
        <h1 className="text-3xl font-bold tracking-tight text-foreground">
          Patients
        </h1>
        <p className="text-muted-foreground mt-1">
          Dossiers et historiques de vos patients.
        </p>
      </div>
      <div className="flex flex-1 flex-col items-center justify-center p-12 border border-dashed rounded-xl gap-4">
        <Users className="h-12 w-12 text-muted-foreground opacity-50" />
        <p className="text-muted-foreground">
          La gestion des dossiers patients sera implémentée ici.
        </p>
      </div>
    </div>
  )
}
