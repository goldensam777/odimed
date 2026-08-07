import { createFileRoute } from "@tanstack/react-router"
import { Plus } from "lucide-react"

import useAuth from "@/hooks/useAuth"
import { Button } from "@/components/ui/button"

export const Route = createFileRoute("/_layout/")({
  component: Dashboard,
  head: () => ({
    meta: [
      {
        title: "Dashboard - Odimed",
      },
    ],
  }),
})

function Dashboard() {
  const { user: currentUser } = useAuth()

  // Mocks based on the UI design for now
  const recentPrescriptions = [
    { patient: "Sarah Johnson", date: "Oct 26, 2026", status: "Active" },
    { patient: "John Doe", date: "Oct 25, 2026", status: "Pending" },
    { patient: "Maria Garcia", date: "Oct 25, 2026", status: "Completed" },
    { patient: "Michael Chen", date: "Oct 25, 2026", status: "Completed" },
  ]

  return (
    <div className="flex flex-col gap-8 p-4 md:p-8 w-full max-w-6xl mx-auto mt-2 md:mt-0">
      {/* Header Section */}
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-6">
        <div>
          <h1 className="text-3xl md:text-4xl font-bold tracking-tight text-foreground">
            {currentUser?.full_name ? `Dr. ${currentUser.full_name.split(' ').pop()}` : "Espace Praticien"}
          </h1>
          <p className="text-muted-foreground mt-2 text-base md:text-lg">
            Synthèse de votre activité de prescription.
          </p>
        </div>
        
        <Button className="w-full md:w-auto gap-2 bg-primary hover:bg-emerald-600 text-white font-medium px-6 py-6 md:py-4 rounded-xl shadow-lg shadow-emerald-500/20 transition-all hover:scale-[1.02]">
          <Plus className="h-5 w-5" />
          Nouvelle Ordonnance
        </Button>
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 md:gap-8 mt-2">
        
        {/* Recent Prescriptions Table */}
        <div className="lg:col-span-2 bg-card rounded-3xl border shadow-sm p-6 md:p-8 flex flex-col">
          <div className="flex items-center justify-between mb-8">
            <h2 className="text-xl font-semibold">Dernières ordonnances</h2>
            <Button variant="outline" size="sm" className="rounded-xl">Tout afficher</Button>
          </div>
          
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b text-muted-foreground">
                  <th className="pb-3 font-medium">Patient</th>
                  <th className="pb-3 font-medium">Date</th>
                  <th className="pb-3 font-medium">Statut</th>
                </tr>
              </thead>
              <tbody>
                {recentPrescriptions.map((presc, idx) => (
                  <tr key={idx} className="border-b last:border-0 hover:bg-muted/50 transition-colors">
                    <td className="py-4 font-medium">{presc.patient}</td>
                    <td className="py-4 text-muted-foreground">{presc.date}</td>
                    <td className="py-4">
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                        presc.status === "Active" ? "bg-emerald-500/10 text-emerald-500 border border-emerald-500/20" :
                        presc.status === "Pending" ? "bg-amber-500/10 text-amber-500 border border-amber-500/20" :
                        "bg-blue-500/10 text-blue-500 border border-blue-500/20"
                      }`}>
                        {presc.status === "Active" ? "Validée" : presc.status === "Pending" ? "En attente" : "Finalisée"}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Side widgets */}
        <div className="flex flex-col gap-6">
          <div className="bg-card rounded-2xl border shadow-sm p-6">
            <h3 className="font-semibold text-lg mb-4">Actions requises</h3>
            <div className="space-y-4">
              <div className="p-3 bg-amber-500/10 border border-amber-500/20 rounded-xl">
                <p className="text-sm font-medium text-amber-600 dark:text-amber-400">2 signatures en attente</p>
                <p className="text-xs text-muted-foreground mt-1">Ordonnances au statut brouillon</p>
              </div>
              <div className="p-3 bg-muted rounded-xl">
                <p className="text-sm font-medium">Configuration requise</p>
                <p className="text-xs text-muted-foreground mt-1">Veuillez paramétrer vos modèles d'ordonnance</p>
              </div>
            </div>
          </div>
          
          <div className="bg-gradient-to-br from-primary/10 via-primary/5 to-transparent rounded-2xl border border-primary/10 p-6">
            <h3 className="font-semibold text-lg mb-2">Vue d'ensemble</h3>
            <div className="mt-4 flex items-baseline gap-2">
              <span className="text-4xl font-extrabold tracking-tight text-primary">128</span>
              <span className="text-sm text-muted-foreground font-medium">documents générés</span>
            </div>
            <p className="text-xs text-muted-foreground mt-2">Période : mois en cours</p>
          </div>
        </div>

      </div>
    </div>
  )
}
