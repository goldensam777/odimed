import { createFileRoute } from "@tanstack/react-router"
import { FileSignature } from "lucide-react"

export const Route = createFileRoute("/_layout/modeles")({
  component: Modeles,
  head: () => ({
    meta: [{ title: "Modèles - Odimed" }],
  }),
})

function Modeles() {
  return (
    <div className="flex flex-col gap-6 p-4 md:p-8 w-full max-w-6xl mx-auto">
      <div>
        <h1 className="text-3xl font-bold tracking-tight text-foreground">
          Modèles & Assets
        </h1>
        <p className="text-muted-foreground mt-1">
          Gérez vos templates Word, signatures et cachets.
        </p>
      </div>
      <div className="flex flex-1 flex-col items-center justify-center p-12 border border-dashed rounded-xl gap-4">
        <FileSignature className="h-12 w-12 text-muted-foreground opacity-50" />
        <p className="text-muted-foreground">
          Uploadez vos fichiers .docx et configurez votre cachet auto-détouré
          bientôt.
        </p>
      </div>
    </div>
  )
}
