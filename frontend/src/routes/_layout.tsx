import { createFileRoute, Outlet, redirect, useLocation } from "@tanstack/react-router"

import { Footer } from "@/components/Common/Footer"
import AppSidebar from "@/components/Sidebar/AppSidebar"
import {
  SidebarInset,
  SidebarProvider,
  SidebarTrigger,
} from "@/components/ui/sidebar"
import { isLoggedIn } from "@/hooks/useAuth"

import { UsersService } from "@/client"

export const Route = createFileRoute("/_layout")({
  component: Layout,
  beforeLoad: async () => {
    if (!isLoggedIn()) {
      throw redirect({
        to: "/login",
      })
    }
    try {
      // Validate the token by trying to fetch the current user
      await UsersService.readUserMe()
    } catch (error) {
      // If it fails (e.g., 401 Unauthorized, expired token, or token from another localhost app)
      localStorage.removeItem("access_token")
      throw redirect({
        to: "/login",
      })
    }
  },
})

function Layout() {
  const location = useLocation()
  const path = location.pathname
  
  const isEditor = path.includes("ordonnances")
  
  let pageName = "Espace de travail"
  if (isEditor) pageName = "Éditeur d'Ordonnances"
  else if (path.includes("referentiel")) pageName = "Référentiel Thérapeutique"
  else if (path.includes("admin")) pageName = "Administration"
  else if (path.includes("settings")) pageName = "Paramètres"
  else if (path === "/") pageName = "Tableau de bord"

  return (
    <SidebarProvider>
      <AppSidebar />
      <SidebarInset className="overflow-hidden h-screen flex flex-col">
        <header className="shrink-0 sticky top-0 z-50 flex h-14 items-center justify-between border-b bg-background/80 backdrop-blur-md px-4 shadow-sm">
          <div className="flex items-center gap-4">
            <SidebarTrigger className="-ml-1 text-muted-foreground hover:text-foreground transition-colors" />
            <div className="h-4 w-px bg-border hidden sm:block"></div>
            <h2 className="text-sm font-semibold tracking-wide text-foreground/80 hidden sm:block">Odimed <span className="font-normal text-muted-foreground">/ {pageName}</span></h2>
          </div>
          <div className="flex items-center gap-4">
             {/* Empty right side as requested */}
          </div>
        </header>
        <main className={`flex-1 overflow-y-auto ${isEditor ? '' : 'p-6 md:p-8'}`}>
          <div className={`mx-auto ${isEditor ? 'h-full w-full max-w-none' : 'max-w-7xl'}`}>
            <Outlet />
          </div>
        </main>
        {!isEditor && <Footer />}
      </SidebarInset>
    </SidebarProvider>
  )
}
