import { useState } from "react"
import { Search, Plus, Filter, Pill, Activity, FlaskConical } from "lucide-react"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"

// Fake data for UI demonstration
const mockMedicaments = [
  { id: 1, nom: "Amoxicilline", forme: "Comprimé pelliculé", dosage: "1g", molecule: "Amoxicilline", diagnostics: ["Infection respiratoire", "Otite"] },
  { id: 2, nom: "Doliprane", forme: "Comprimé", dosage: "1000mg", molecule: "Paracétamol", diagnostics: ["Fièvre", "Douleur légère à modérée"] },
  { id: 3, nom: "Kardegic", forme: "Sachet", dosage: "75mg", molecule: "Acide acétylsalicylique", diagnostics: ["Prévention cardiovasculaire"] },
]

export function DatabaseManager({ isAdmin = false }: { isAdmin?: boolean }) {
  const [activeTab, setActiveTab] = useState<"medicaments" | "molecules" | "diagnostics">("medicaments")
  const [searchQuery, setSearchQuery] = useState("")

  return (
    <div className="flex flex-col gap-6">
      
      {/* Top Bar: Tabs & Search */}
      <div className="flex flex-col lg:flex-row justify-between gap-4">
        <div className="flex flex-col sm:flex-row bg-muted p-1 rounded-xl w-full lg:w-fit overflow-hidden">
          <button 
            onClick={() => setActiveTab("medicaments")}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors ${activeTab === "medicaments" ? "bg-background shadow-sm text-foreground" : "text-muted-foreground hover:text-foreground"}`}
          >
            <Pill className="h-4 w-4" /> Médicaments
          </button>
          <button 
            onClick={() => setActiveTab("molecules")}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors ${activeTab === "molecules" ? "bg-background shadow-sm text-foreground" : "text-muted-foreground hover:text-foreground"}`}
          >
            <FlaskConical className="h-4 w-4" /> Molécules
          </button>
          <button 
            onClick={() => setActiveTab("diagnostics")}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors ${activeTab === "diagnostics" ? "bg-background shadow-sm text-foreground" : "text-muted-foreground hover:text-foreground"}`}
          >
            <Activity className="h-4 w-4" /> Diagnostics (CIM-10)
          </button>
        </div>

        {isAdmin && (
          <Button className="gap-2 shrink-0 bg-primary hover:bg-emerald-600">
            <Plus className="h-4 w-4" /> 
            Ajouter {activeTab === "medicaments" ? "un médicament" : activeTab === "molecules" ? "une molécule" : "un diagnostic"}
          </Button>
        )}
      </div>

      {/* Main Content Area */}
      <div className="bg-card border rounded-2xl p-6 shadow-sm flex flex-col gap-6">
        
        {/* Filters Area */}
        <div className="flex flex-col md:flex-row gap-4 items-center">
          <div className="relative flex-1 w-full">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input 
              placeholder={`Rechercher parmi les ${activeTab}...`} 
              className="pl-9 bg-muted/50 border-muted"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>
          
          {activeTab === "medicaments" && (
            <Button variant="outline" className="gap-2 shrink-0">
              <Filter className="h-4 w-4" />
              Filtrer par Diagnostic
            </Button>
          )}
        </div>

        {/* Table / List */}
        <div className="overflow-x-auto">
          {activeTab === "medicaments" && (
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b text-muted-foreground text-sm">
                  <th className="pb-3 font-medium">Nom officiel</th>
                  <th className="pb-3 font-medium">Molécule</th>
                  <th className="pb-3 font-medium">Forme & Dosage</th>
                  <th className="pb-3 font-medium">Diagnostics associés</th>
                  {isAdmin && <th className="pb-3 font-medium text-right">Actions</th>}
                </tr>
              </thead>
              <tbody>
                {mockMedicaments.map((med) => (
                  <tr key={med.id} className="border-b last:border-0 hover:bg-muted/30 transition-colors group">
                    <td className="py-4 font-semibold">{med.nom}</td>
                    <td className="py-4 text-muted-foreground text-sm">{med.molecule}</td>
                    <td className="py-4 text-sm">
                      <span className="block">{med.forme}</span>
                      <span className="text-muted-foreground">{med.dosage}</span>
                    </td>
                    <td className="py-4">
                      <div className="flex flex-wrap gap-1">
                        {med.diagnostics.map((diag, i) => (
                          <Badge key={i} variant="secondary" className="bg-emerald-500/10 text-emerald-600 hover:bg-emerald-500/20 border-0 font-normal">
                            {diag}
                          </Badge>
                        ))}
                      </div>
                    </td>
                    {isAdmin && (
                      <td className="py-4 text-right">
                        <Button variant="ghost" size="sm" className="opacity-0 group-hover:opacity-100 transition-opacity">Modifier</Button>
                      </td>
                    )}
                  </tr>
                ))}
              </tbody>
            </table>
          )}
          
          {activeTab !== "medicaments" && (
            <div className="flex flex-col items-center justify-center p-12 text-muted-foreground">
              La vue pour {activeTab} utilise la même logique et sera implémentée de manière similaire.
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
