import { createFileRoute } from "@tanstack/react-router"
import { Printer, Save, FileSignature, LayoutTemplate, File, Search, Settings2 } from "lucide-react"
import { useState } from "react"

import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"
import { PaperEditor } from "@/components/Editor/PaperEditor"
import useAuth from "@/hooks/useAuth"

export const Route = createFileRoute("/_layout/ordonnances")({
  component: NouvelleOrdonnance,
  head: () => ({
    meta: [{ title: "Création Ordonnance - Odimed" }],
  }),
})

function NouvelleOrdonnance() {
  const { user } = useAuth()
  const [paperSize, setPaperSize] = useState<'A4' | 'A5'>('A4')
  
  return (
    <div className="flex flex-col md:flex-row h-full overflow-hidden relative">
      
      {/* Editor Workspace Area (The Desk) */}
      <div className="flex-1 bg-zinc-950/50 dark:bg-black/20 overflow-y-auto no-scrollbar p-0 md:p-8 lg:p-12">
        <PaperEditor paperSize={paperSize} />
      </div>

      {/* Right Side Panel for Actions (The 'deuxième barre' moved to the side) */}
      <div className="w-full md:w-72 bg-card border-l flex flex-col shadow-2xl z-10 shrink-0 h-auto md:h-full">
         <div className="p-4 border-b font-semibold flex items-center gap-2 text-foreground/90">
            <Settings2 className="h-4 w-4 text-primary" />
            Propriétés du document
         </div>
         
         <div className="p-5 flex flex-col gap-8 flex-1 overflow-y-auto no-scrollbar">
            
            {/* Format Selector */}
            <div className="space-y-3">
              <Label className="text-xs text-muted-foreground uppercase tracking-wider font-semibold">Format du papier</Label>
              <div className="bg-muted p-1 rounded-xl flex items-center w-full shadow-inner border border-border/50">
                <button 
                  onClick={() => setPaperSize('A4')}
                  className={`flex-1 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${paperSize === 'A4' ? 'bg-background shadow-md text-foreground ring-1 ring-border' : 'text-muted-foreground hover:text-foreground'}`}
                >
                  <File className="h-4 w-4 inline-block mr-1 text-primary/70" /> A4
                </button>
                <button 
                  onClick={() => setPaperSize('A5')}
                  className={`flex-1 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${paperSize === 'A5' ? 'bg-background shadow-md text-foreground ring-1 ring-border' : 'text-muted-foreground hover:text-foreground'}`}
                >
                  <File className="h-4 w-4 inline-block mr-1 scale-75 text-primary/70" /> A5
                </button>
              </div>
            </div>

            {/* Template Selector */}
            <div className="space-y-3">
               <Label className="text-xs text-muted-foreground uppercase tracking-wider font-semibold">Modèle</Label>
               <Button variant="outline" className="w-full justify-start gap-3 h-10 rounded-xl border-dashed hover:border-primary/50 hover:bg-primary/5 transition-colors">
                 <LayoutTemplate className="h-4 w-4 text-primary/70" /> Changer de modèle
               </Button>
            </div>
         </div>
         
         {/* Action Buttons (Sticky at bottom) */}
         <div className="p-5 border-t bg-muted/10 flex flex-col gap-3">
            <Button variant="outline" className="w-full gap-2 h-11 rounded-xl hover:bg-muted/50 transition-colors">
              <Save className="h-4 w-4 text-muted-foreground" /> Sauvegarder brouillon
            </Button>
            <Button className="w-full gap-2 bg-primary hover:bg-emerald-600 h-11 rounded-xl shadow-[0_4px_14px_0_rgba(16,185,129,0.39)] hover:shadow-[0_6px_20px_rgba(16,185,129,0.23)] transition-all">
              <FileSignature className="h-4 w-4" /> Signer & PDF
            </Button>
         </div>
      </div>

    </div>
  )
}
